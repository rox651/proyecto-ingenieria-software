"""Microphone capture via sounddevice (optional dependency)."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor

from voiceloop.config import Settings, settings

_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="voiceloop-audio")


class SoundDeviceCapture:
    """Read PCM chunks from the system microphone using sounddevice."""

    def __init__(
        self,
        cfg: Settings | None = None,
        chunk_duration_ms: int = 100,
    ) -> None:
        self._cfg = cfg or settings
        self._chunk_duration_ms = chunk_duration_ms
        self._frames_per_chunk = int(
            self._cfg.sample_rate * self._chunk_duration_ms / 1000
        )
        self._stream = None

    def _read_blocking(self) -> bytes:
        import numpy as np
        import sounddevice as sd

        if self._stream is None:
            try:
                self._stream = sd.InputStream(
                    samplerate=self._cfg.sample_rate,
                    channels=self._cfg.channels,
                    dtype="int16",
                    blocksize=self._frames_per_chunk,
                )
                self._stream.start()
            except Exception as exc:
                raise RuntimeError(
                    "No se pudo abrir el micrófono. Verifica permisos y dispositivos."
                ) from exc

        data, _overflowed = self._stream.read(self._frames_per_chunk)
        return np.asarray(data, dtype=np.int16).tobytes()

    async def read_chunk(self) -> bytes:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(_executor, self._read_blocking)

    def close(self) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
