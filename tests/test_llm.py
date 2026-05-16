import json

import httpx
import pytest

from voiceloop.config import Settings
from voiceloop.llm.openai_client import SYSTEM_PROMPT, OpenAILanguageModel


def _mock_handler(request: httpx.Request) -> httpx.Response:
    assert request.url.path.endswith("/chat/completions")
    body = json.loads(request.content)
    assert body["messages"][0]["role"] == "system"
    assert body["messages"][0]["content"] == SYSTEM_PROMPT
    assert body["messages"][-1]["content"] == "hola"
    return httpx.Response(
        200,
        json={
            "choices": [
                {"message": {"role": "assistant", "content": "¡Hola! ¿En qué te ayudo?"}}
            ]
        },
    )


@pytest.mark.asyncio
async def test_openai_llm_respond():
    settings = Settings(
        openai_api_key="test-key",
        openai_base_url="https://api.example.com/v1",
        openai_model="gpt-test",
    )
    transport = httpx.MockTransport(_mock_handler)
    async with httpx.AsyncClient(transport=transport, base_url=settings.openai_base_url) as client:
        llm = OpenAILanguageModel(client=client, cfg=settings)
        reply = await llm.respond("hola", [{"role": "user", "content": "hola"}])
        assert "Hola" in reply
