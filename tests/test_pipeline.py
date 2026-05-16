import asyncio

import pytest

from voiceloop.pipeline import PipelineState, VoicePipeline
from voiceloop.stubs import StubLanguageModel, StubSpeechToText


@pytest.mark.asyncio
async def test_run_turn_returns_conversation():
    pipeline = VoicePipeline(
        stt=StubSpeechToText(),
        llm=StubLanguageModel(),
    )
    result = await pipeline.run_turn()
    assert result is not None
    assert "hola" in result.user_text.lower()
    assert result.assistant_text
    assert len(pipeline.history) == 2


@pytest.mark.asyncio
async def test_run_respects_max_turns():
    pipeline = VoicePipeline()
    results = await pipeline.run(max_turns=2)
    assert len(results) <= 2
    assert pipeline.state == PipelineState.STOPPED


@pytest.mark.asyncio
async def test_request_stop():
    pipeline = VoicePipeline()

    async def run_and_stop():
        await asyncio.sleep(0.01)
        pipeline.request_stop()

    stopper = asyncio.create_task(run_and_stop())
    results = await pipeline.run(max_turns=100)
    await stopper
    assert pipeline.state == PipelineState.STOPPED
    assert isinstance(results, list)
