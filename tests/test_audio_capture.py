from unittest.mock import patch

import pytest

from voiceloop.audio.capture import SoundDeviceCapture
from voiceloop.config import Settings


@pytest.mark.asyncio
async def test_read_chunk_uses_executor_and_returns_bytes():
    cfg = Settings(sample_rate=16000, channels=1)
    capture = SoundDeviceCapture(cfg=cfg, chunk_duration_ms=100)

    fake_pcm = b"\x01\x00" * 1600

    with patch.object(capture, "_read_blocking", return_value=fake_pcm):
        chunk = await capture.read_chunk()

    assert chunk == fake_pcm


@pytest.mark.asyncio
async def test_capture_propagates_device_error():
    cfg = Settings()
    capture = SoundDeviceCapture(cfg=cfg)

    err = RuntimeError("No se pudo abrir el micrófono.")
    with patch.object(capture, "_read_blocking", side_effect=err):
        with pytest.raises(RuntimeError, match="micrófono"):
            await capture.read_chunk()


def test_frames_per_chunk_calculation():
    cfg = Settings(sample_rate=16000, channels=1)
    capture = SoundDeviceCapture(cfg=cfg, chunk_duration_ms=100)
    assert capture._frames_per_chunk == 1600
