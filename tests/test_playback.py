from unittest.mock import patch

import pytest

from voiceloop.audio.playback import SoundDevicePlayback


@pytest.mark.asyncio
async def test_playback_invokes_blocking_play():
    playback = SoundDevicePlayback()
    with patch.object(playback, "_play_blocking") as mock_play:
        await playback.play(b"fake-audio")
        mock_play.assert_called_once_with(b"fake-audio")
