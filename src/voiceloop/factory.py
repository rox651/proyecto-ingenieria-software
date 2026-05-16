"""Pipeline composition — centralizes stub vs live component wiring."""

from __future__ import annotations

import os
from typing import Literal

from voiceloop.config import settings
from voiceloop.pipeline import VoicePipeline
from voiceloop.stubs import (
    StubAudioCapture,
    StubAudioPlayback,
    StubLanguageModel,
    StubSpeechToText,
    StubTextToSpeech,
)

PipelineMode = Literal["stub", "live"]


def resolve_mode(mode: PipelineMode | None = None) -> PipelineMode:
    if mode is not None:
        return mode
    env = os.getenv("VOICELOOP_MODE", "stub").lower()
    return "live" if env == "live" else "stub"


def create_pipeline(mode: PipelineMode | None = None) -> VoicePipeline:
    """Build a VoicePipeline with components for the given mode."""
    resolved = resolve_mode(mode)

    if resolved == "stub":
        return VoicePipeline(
            capture=StubAudioCapture(),
            stt=StubSpeechToText(),
            llm=StubLanguageModel(),
            tts=StubTextToSpeech(),
            playback=StubAudioPlayback(),
        )

    return _create_live_pipeline()


def _create_live_pipeline() -> VoicePipeline:
    from voiceloop.protocols import AudioCapture, LanguageModel

    llm: LanguageModel = StubLanguageModel()
    if settings.openai_api_key:
        from voiceloop.llm.openai_client import OpenAILanguageModel

        llm = OpenAILanguageModel()

    capture: AudioCapture = StubAudioCapture()
    try:
        from voiceloop.audio.capture import SoundDeviceCapture

        capture = SoundDeviceCapture()
    except ImportError:
        pass

    return VoicePipeline(
        capture=capture,
        stt=StubSpeechToText(),
        llm=llm,
        tts=StubTextToSpeech(),
        playback=StubAudioPlayback(),
    )
