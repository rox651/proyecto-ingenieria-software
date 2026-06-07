"""TTS via Microsoft Edge neural voices (edge-tts)."""

from __future__ import annotations

from voiceloop.config import Settings, settings


class EdgeTTS:
    """TextToSpeech producing MP3 bytes."""

    def __init__(self, cfg: Settings | None = None) -> None:
        self._cfg = cfg or settings

    async def synthesize(self, text: str) -> bytes:
        if not text.strip():
            return b""

        import edge_tts

        communicate = edge_tts.Communicate(text, voice=self._cfg.tts_voice)
        audio = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
        return bytes(audio)
