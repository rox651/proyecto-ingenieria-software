from typing import Protocol, runtime_checkable


@runtime_checkable
class SpeechToText(Protocol):
    async def transcribe(self, audio_chunk: bytes) -> str:
        """Transcribe a chunk of PCM audio to text."""
        ...


@runtime_checkable
class LanguageModel(Protocol):
    async def respond(self, user_text: str, history: list[dict[str, str]]) -> str:
        """Generate assistant reply given user text and conversation history."""
        ...


@runtime_checkable
class TextToSpeech(Protocol):
    async def synthesize(self, text: str) -> bytes:
        """Synthesize speech audio from text."""
        ...


@runtime_checkable
class AudioCapture(Protocol):
    async def read_chunk(self) -> bytes:
        """Read the next audio chunk from the microphone."""
        ...


@runtime_checkable
class AudioPlayback(Protocol):
    async def play(self, audio: bytes) -> None:
        """Play synthesized audio through the speaker."""
        ...
