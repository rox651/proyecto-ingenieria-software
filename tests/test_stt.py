from unittest.mock import MagicMock, patch

import pytest

from voiceloop.stt.whisper import WhisperSTT


@pytest.mark.asyncio
async def test_whisper_transcribe_empty_on_silence():
    stt = WhisperSTT()
    assert await stt.transcribe(b"\x00" * 100) == ""


@pytest.mark.asyncio
async def test_whisper_transcribe_uses_model():
    stt = WhisperSTT()
    mock_model = MagicMock()
    seg = MagicMock()
    seg.text = " hola mundo "
    mock_model.transcribe.return_value = ([seg], None)

    with patch.object(stt, "_get_model", return_value=mock_model):
        with patch.object(stt, "_pcm_to_wav", return_value="/tmp/x.wav"):
            text = await stt.transcribe(b"\x01" * 320)

    assert text == "hola mundo"
    mock_model.transcribe.assert_called_once()
