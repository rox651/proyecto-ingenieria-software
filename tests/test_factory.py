import os
from unittest.mock import patch

from voiceloop.factory import create_pipeline, resolve_mode
from voiceloop.stubs import StubLanguageModel


def test_resolve_mode_defaults_to_stub():
    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("VOICELOOP_MODE", None)
        assert resolve_mode() == "stub"


def test_resolve_mode_from_env():
    with patch.dict(os.environ, {"VOICELOOP_MODE": "live"}):
        assert resolve_mode() == "live"


def test_create_pipeline_stub_mode():
    pipeline = create_pipeline("stub")
    assert isinstance(pipeline.llm, StubLanguageModel)


def test_create_live_pipeline_uses_openai_when_key_set():
    from voiceloop.config import settings
    from voiceloop.llm.openai_client import OpenAILanguageModel

    with patch.object(settings, "openai_api_key", "sk-test"):
        pipeline = create_pipeline("live")
        assert isinstance(pipeline.llm, OpenAILanguageModel)
