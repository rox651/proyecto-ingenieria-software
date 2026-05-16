"""Stub implementations for development without hardware or API keys."""



class StubAudioCapture:
    """Yields silence chunks; replace with sounddevice implementation."""

    def __init__(self, chunk_size: int = 3200) -> None:
        self._chunk_size = chunk_size
        self._ticks = 0

    async def read_chunk(self) -> bytes:
        import asyncio

        await asyncio.sleep(0.01)
        self._ticks += 1
        # Simulate speech after a few chunks (stub for end-to-end demos)
        if self._ticks > 2:
            return b"\x01" * self._chunk_size
        return b"\x00" * self._chunk_size


class StubSpeechToText:
    async def transcribe(self, audio_chunk: bytes) -> str:
        if not any(audio_chunk):
            return ""
        return "hola, ¿cómo estás?"


class StubLanguageModel:
    async def respond(self, user_text: str, history: list[dict[str, str]]) -> str:
        if not user_text.strip():
            return ""
        return f"Recibí tu mensaje: «{user_text}». (respuesta stub)"


class StubTextToSpeech:
    async def synthesize(self, text: str) -> bytes:
        return text.encode("utf-8")


class StubAudioPlayback:
    async def play(self, audio: bytes) -> None:
        import asyncio

        await asyncio.sleep(0.1)
