"""Async orchestration: Mic → STT → LLM → TTS → Speaker."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from enum import StrEnum

from voiceloop.config import settings
from voiceloop.events import EventBus
from voiceloop.protocols import (
    AudioCapture,
    AudioPlayback,
    LanguageModel,
    SpeechToText,
    TextToSpeech,
)
from voiceloop.stubs import (
    StubAudioCapture,
    StubAudioPlayback,
    StubLanguageModel,
    StubSpeechToText,
    StubTextToSpeech,
)
from voiceloop.vad.energy import EnergyVAD

logger = logging.getLogger(__name__)


class PipelineState(StrEnum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    STOPPED = "stopped"


@dataclass
class TurnResult:
    user_text: str
    assistant_text: str


@dataclass
class VoicePipeline:
    """Real-time voice loop orchestrator with optional event bus."""

    capture: AudioCapture = field(default_factory=StubAudioCapture)
    stt: SpeechToText = field(default_factory=StubSpeechToText)
    llm: LanguageModel = field(default_factory=StubLanguageModel)
    tts: TextToSpeech = field(default_factory=StubTextToSpeech)
    playback: AudioPlayback = field(default_factory=StubAudioPlayback)
    history: list[dict[str, str]] = field(default_factory=list)
    state: PipelineState = PipelineState.IDLE
    events: EventBus = field(default_factory=EventBus)
    use_vad: bool = False
    _stop: asyncio.Event = field(default_factory=asyncio.Event)

    def request_stop(self) -> None:
        self._stop.set()

    async def _set_state(self, state: PipelineState) -> None:
        self.state = state
        await self.events.emit("state_change", state=state.value)

    async def _capture_with_vad(self) -> bytes:
        """Collect audio until silence endpoint or max duration."""
        if not self.use_vad:
            buffer = bytearray()
            for _ in range(5):
                if self._stop.is_set():
                    break
                buffer.extend(await self.capture.read_chunk())
            return bytes(buffer)

        vad = EnergyVAD(threshold=settings.vad_energy_threshold)
        buffer = bytearray()
        silence_ms = 0
        speech_started = False
        max_ms = 5000
        elapsed_ms = 0
        chunk_ms = settings.chunk_duration_ms

        while elapsed_ms < max_ms and not self._stop.is_set():
            chunk = await self.capture.read_chunk()
            elapsed_ms += chunk_ms

            if vad.is_speech(chunk):
                speech_started = True
                silence_ms = 0
                buffer.extend(chunk)
            elif speech_started:
                silence_ms += chunk_ms
                buffer.extend(chunk)
                if silence_ms >= settings.vad_silence_ms:
                    break

        return bytes(buffer)

    async def run_turn(self) -> TurnResult | None:
        """Execute one turn using asyncio queues between stages."""
        audio_q: asyncio.Queue[bytes | None] = asyncio.Queue(maxsize=1)
        user_q: asyncio.Queue[str | None] = asyncio.Queue(maxsize=1)
        assistant_q: asyncio.Queue[str | None] = asyncio.Queue(maxsize=1)
        tts_q: asyncio.Queue[bytes | None] = asyncio.Queue(maxsize=1)
        result_q: asyncio.Queue[TurnResult | None] = asyncio.Queue(maxsize=1)
        workers: list[asyncio.Task[None]] = []

        async def capture_worker() -> None:
            await self._set_state(PipelineState.LISTENING)
            pcm = await self._capture_with_vad()
            await audio_q.put(pcm)
            await audio_q.put(None)

        async def stt_worker() -> None:
            pcm = await audio_q.get()
            if pcm is None:
                await user_q.put(None)
                return
            text = await self.stt.transcribe(pcm)
            await user_q.put(text)
            await user_q.put(None)

        async def llm_worker() -> None:
            user_text = await user_q.get()
            if user_text is None or not user_text.strip():
                await assistant_q.put(None)
                return
            logger.info("User: %s", user_text)
            self.history.append({"role": "user", "content": user_text})
            await self.events.emit("transcript", role="user", content=user_text)
            await self._set_state(PipelineState.THINKING)
            reply = await self.llm.respond(user_text, self.history)
            await assistant_q.put(reply)
            await assistant_q.put(None)

        async def tts_worker() -> None:
            assistant_text = await assistant_q.get()
            if assistant_text is None or not assistant_text.strip():
                await tts_q.put(None)
                return
            logger.info("Assistant: %s", assistant_text)
            self.history.append({"role": "assistant", "content": assistant_text})
            await self.events.emit("response", role="assistant", content=assistant_text)
            await self._set_state(PipelineState.SPEAKING)
            audio_out = await self.tts.synthesize(assistant_text)
            await tts_q.put(audio_out)
            await tts_q.put(None)

        async def playback_worker() -> None:
            audio_out = await tts_q.get()
            if audio_out is not None:
                await self.playback.play(audio_out)
            user_text = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "user"),
                "",
            )
            assistant_text = next(
                (m["content"] for m in reversed(self.history) if m["role"] == "assistant"),
                "",
            )
            if user_text and assistant_text:
                await result_q.put(TurnResult(user_text=user_text, assistant_text=assistant_text))
            else:
                await result_q.put(None)
            await self._set_state(PipelineState.IDLE)

        workers = [
            asyncio.create_task(capture_worker()),
            asyncio.create_task(stt_worker()),
            asyncio.create_task(llm_worker()),
            asyncio.create_task(tts_worker()),
            asyncio.create_task(playback_worker()),
        ]

        try:
            for task in asyncio.as_completed(workers):
                await task
        except asyncio.CancelledError:
            for w in workers:
                w.cancel()
            raise

        return await result_q.get()

    async def run(self, max_turns: int | None = None) -> list[TurnResult]:
        """Run the pipeline until stopped or max_turns reached."""
        results: list[TurnResult] = []
        turn = 0
        while not self._stop.is_set():
            if max_turns is not None and turn >= max_turns:
                break
            result = await self.run_turn()
            if result is None:
                if self.use_vad:
                    continue
                break
            results.append(result)
            turn += 1
        await self._set_state(PipelineState.STOPPED)
        return results
