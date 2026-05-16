"""Async orchestration: Mic → STT → LLM → TTS → Speaker."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from enum import StrEnum

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
    """Real-time voice loop orchestrator."""

    capture: AudioCapture = field(default_factory=StubAudioCapture)
    stt: SpeechToText = field(default_factory=StubSpeechToText)
    llm: LanguageModel = field(default_factory=StubLanguageModel)
    tts: TextToSpeech = field(default_factory=StubTextToSpeech)
    playback: AudioPlayback = field(default_factory=StubAudioPlayback)
    history: list[dict[str, str]] = field(default_factory=list)
    state: PipelineState = PipelineState.IDLE
    _stop: asyncio.Event = field(default_factory=asyncio.Event)

    def request_stop(self) -> None:
        self._stop.set()

    async def run_turn(self) -> TurnResult | None:
        """Execute one conversational turn through the full pipeline."""
        self.state = PipelineState.LISTENING
        audio_buffer = bytearray()

        for _ in range(5):
            if self._stop.is_set():
                self.state = PipelineState.STOPPED
                return None
            chunk = await self.capture.read_chunk()
            audio_buffer.extend(chunk)

        user_text = await self.stt.transcribe(bytes(audio_buffer))
        if not user_text.strip():
            self.state = PipelineState.IDLE
            return None

        logger.info("User: %s", user_text)
        self.history.append({"role": "user", "content": user_text})

        self.state = PipelineState.THINKING
        assistant_text = await self.llm.respond(user_text, self.history)
        if not assistant_text.strip():
            self.state = PipelineState.IDLE
            return None

        logger.info("Assistant: %s", assistant_text)
        self.history.append({"role": "assistant", "content": assistant_text})

        self.state = PipelineState.SPEAKING
        audio_out = await self.tts.synthesize(assistant_text)
        await self.playback.play(audio_out)

        self.state = PipelineState.IDLE
        return TurnResult(user_text=user_text, assistant_text=assistant_text)

    async def run(self, max_turns: int | None = None) -> list[TurnResult]:
        """Run the pipeline until stopped or max_turns reached."""
        results: list[TurnResult] = []
        turn = 0
        while not self._stop.is_set():
            if max_turns is not None and turn >= max_turns:
                break
            result = await self.run_turn()
            if result is None:
                continue
            results.append(result)
            turn += 1
        self.state = PipelineState.STOPPED
        return results
