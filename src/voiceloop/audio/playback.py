"""Speaker playback via sounddevice."""

from __future__ import annotations

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="voiceloop-playback")


class SoundDevicePlayback:
    """Play MP3 or PCM audio through the system speaker."""

    async def play(self, audio: bytes) -> None:
        if not audio:
            return
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(_executor, self._play_blocking, audio)

    def _play_blocking(self, audio: bytes) -> None:
        if audio[:3] == b"ID3" or audio[:2] in (b"\xff\xfb", b"\xff\xf3"):
            self._play_mp3(audio)
        else:
            self._play_pcm(audio)

    def _play_mp3(self, audio: bytes) -> None:
        try:
            import miniaudio

            decoded = miniaudio.decode(audio)
            import sounddevice as sd

            sd.play(decoded.samples, decoded.sample_rate)
            sd.wait()
        except ImportError:
            time.sleep(min(len(audio) / 32000, 2.0))

    def _play_pcm(self, audio: bytes) -> None:
        try:
            import numpy as np
            import sounddevice as sd

            samples = np.frombuffer(audio, dtype=np.int16)
            sd.play(samples, samplerate=16000)
            sd.wait()
        except ImportError:
            time.sleep(0.1)
