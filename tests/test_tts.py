import sys
from unittest.mock import MagicMock, patch

import pytest

from voiceloop.config import Settings
from voiceloop.tts.edge import EdgeTTS


async def _fake_stream():
    yield {"type": "audio", "data": b"mp3chunk"}
    yield {"type": "WordBoundary"}


@pytest.mark.asyncio
async def test_edge_tts_synthesize():
    cfg = Settings(tts_voice="es-MX-DaliaNeural")
    tts = EdgeTTS(cfg=cfg)

    mock_comm = MagicMock()
    mock_comm.stream = _fake_stream

    mock_module = MagicMock()
    mock_module.Communicate.return_value = mock_comm

    with patch.dict(sys.modules, {"edge_tts": mock_module}):
        audio = await tts.synthesize("Hola")

    assert audio == b"mp3chunk"
