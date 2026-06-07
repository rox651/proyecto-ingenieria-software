
from voiceloop.vad.energy import EnergyVAD


def test_vad_detects_speech():
    vad = EnergyVAD(threshold=50.0)
    loud = (b"\x7f\xff" * 800)[:1600]
    assert vad.is_speech(loud) is True


def test_vad_silence():
    vad = EnergyVAD(threshold=50.0)
    assert vad.is_speech(b"\x00" * 1600) is False
