"""Pipeline event broadcasting for WebSocket clients."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

EventHandler = Callable[[str, dict[str, Any]], Awaitable[None]]


class EventBus:
    """Simple async pub/sub for pipeline lifecycle events."""

    def __init__(self) -> None:
        self._handlers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        self._handlers.append(handler)

    async def emit(self, event: str, **payload: Any) -> None:
        for handler in list(self._handlers):
            await handler(event, **payload)


def websocket_payload(event: str, **payload: Any) -> dict[str, Any]:
    return {"event": event, **payload}
