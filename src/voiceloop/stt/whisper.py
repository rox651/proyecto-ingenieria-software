"""Local STT via faster-whisper."""

from __future__ import annotations

import asyncio
import tempfile
import wave
from concurrent.futures import ThreadPoolExecutor

from voiceloop.config import Settings, settings

_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="voiceloop-stt")
_model_cache: dict[str, object] = {}


class WhisperSTT:
    """SpeechToText using faster-whisper with lazy model loading."""

    def __init__(self, cfg: Settings | None = None) -> None:
        self._cfg = cfg or settings

    def _get_model(self):
        key = self._cfg.whisper_model
        if key not in _model_cache:
            from faster_whisper import WhisperModel

            _model_cache[key] = WhisperModel(key, device="cpu", compute_type="int8")
        return _model_cache[key]

    def _pcm_to_wav(self, pcm: bytes) -> str:
        path = tempfile.mktemp(suffix=".wav")
        with wave.open(path, "wb") as wf:
            wf.setnchannels(self._cfg.channels)
            wf.setsampwidth(2)
            wf.setframerate(self._cfg.sample_rate)
            wf.writeframes(pcm)
        return path

    def _transcribe_sync(self, pcm: bytes) -> str:
        if not pcm or not any(pcm):
            return ""
        wav_path = self._pcm_to_wav(pcm)
        try:
            segments, _info = self._get_model().transcribe(wav_path, beam_size=1)
            return " ".join(seg.text.strip() for seg in segments).strip()
        finally:
            import os

            if os.path.exists(wav_path):
                os.remove(wav_path)

    async def transcribe(self, audio_chunk: bytes) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(_executor, self._transcribe_sync, audio_chunk)
