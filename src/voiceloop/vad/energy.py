"""Energy-based voice activity detection."""

from __future__ import annotations


class EnergyVAD:
    """Detect speech from PCM int16 mono chunks via mean absolute amplitude."""

    def __init__(self, threshold: float = 50.0) -> None:
        self.threshold = threshold

    def is_speech(self, pcm: bytes) -> bool:
        if not pcm:
            return False
        try:
            import numpy as np

            samples = np.frombuffer(pcm, dtype=np.int16)
            if samples.size == 0:
                return False
            return float(np.abs(samples).mean()) > self.threshold
        except ImportError:
            return any(pcm)
