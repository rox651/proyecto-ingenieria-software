"""Pipeline composition — centralizes stub vs live component wiring."""

from __future__ import annotations

import os
from typing import Literal

from voiceloop.config import settings
from voiceloop.pipeline import VoicePipeline
from voiceloop.protocols import (
    AudioCapture,
    AudioPlayback,
    LanguageModel,
    SpeechToText,
    TextToSpeech,
)
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
            use_vad=False,
        )

    return _create_live_pipeline()


def _try_import(name: str, factory):
    try:
        return factory()
    except ImportError:
        return None


def _create_live_pipeline() -> VoicePipeline:
    llm: LanguageModel = StubLanguageModel()
    if settings.openai_api_key:
        from voiceloop.llm.openai_client import OpenAILanguageModel

        llm = OpenAILanguageModel()

    capture: AudioCapture = StubAudioCapture()
    sd_capture = _try_import("sounddevice", lambda: __import__(
        "voiceloop.audio.capture", fromlist=["SoundDeviceCapture"]
    ).SoundDeviceCapture())
    if sd_capture is not None:
        capture = sd_capture

    stt: SpeechToText = StubSpeechToText()
    whisper = _try_import("faster_whisper", lambda: __import__(
        "voiceloop.stt.whisper", fromlist=["WhisperSTT"]
    ).WhisperSTT())
    if whisper is not None:
        stt = whisper

    tts: TextToSpeech = StubTextToSpeech()
    edge = _try_import("edge_tts", lambda: __import__(
        "voiceloop.tts.edge", fromlist=["EdgeTTS"]
    ).EdgeTTS())
    if edge is not None:
        tts = edge

    playback: AudioPlayback = StubAudioPlayback()
    sd_playback = _try_import("sounddevice", lambda: __import__(
        "voiceloop.audio.playback", fromlist=["SoundDevicePlayback"]
    ).SoundDevicePlayback())
    if sd_playback is not None:
        playback = sd_playback

    return VoicePipeline(
        capture=capture,
        stt=stt,
        llm=llm,
        tts=tts,
        playback=playback,
        use_vad=True,
    )
