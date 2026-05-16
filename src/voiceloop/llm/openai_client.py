"""OpenAI-compatible chat completions client."""

from __future__ import annotations

import httpx

from voiceloop.config import Settings, settings

SYSTEM_PROMPT = (
    "Eres un asistente de voz conversacional en español. "
    "Responde de forma breve (1-3 oraciones), clara y natural para ser leída en voz alta. "
    "No uses markdown ni listas."
)


class OpenAILanguageModel:
    """LanguageModel backed by an OpenAI-compatible chat API."""

    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        cfg: Settings | None = None,
    ) -> None:
        self._cfg = cfg or settings
        self._client = client
        self._owns_client = client is None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            headers = {}
            if self._cfg.openai_api_key:
                headers["Authorization"] = f"Bearer {self._cfg.openai_api_key}"
            self._client = httpx.AsyncClient(
                base_url=self._cfg.openai_base_url.rstrip("/"),
                headers=headers,
                timeout=60.0,
            )
        return self._client

    async def respond(self, user_text: str, history: list[dict[str, str]]) -> str:
        if not user_text.strip():
            return ""

        messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)

        client = await self._get_client()
        response = await client.post(
            "/chat/completions",
            json={
                "model": self._cfg.openai_model,
                "messages": messages,
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    async def aclose(self) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()
            self._client = None
