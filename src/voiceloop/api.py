"""FastAPI backend — session control and status for the voice agent."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from voiceloop.factory import create_pipeline, resolve_mode
from voiceloop.pipeline import PipelineState, TurnResult, VoicePipeline

_pipeline: VoicePipeline | None = None
_run_task: asyncio.Task[list[TurnResult]] | None = None


class SessionStatus(BaseModel):
    state: str
    turns_completed: int
    history_length: int


class TurnResponse(BaseModel):
    user_text: str
    assistant_text: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _pipeline
    _pipeline = create_pipeline(resolve_mode())
    yield
    if _pipeline:
        _pipeline.request_stop()
    global _run_task
    if _run_task and not _run_task.done():
        _run_task.cancel()


app = FastAPI(
    title="VoiceLoop API",
    description="REST control plane for the asyncio voice agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "voiceloop"}


@app.get("/status", response_model=SessionStatus)
async def status() -> SessionStatus:
    p = _require_pipeline()
    return SessionStatus(
        state=p.state.value,
        turns_completed=sum(1 for m in p.history if m["role"] == "assistant"),
        history_length=len(p.history),
    )


@app.get("/history")
async def history() -> list[dict[str, str]]:
    p = _require_pipeline()
    return list(p.history)


@app.post("/turn", response_model=TurnResponse)
async def single_turn() -> TurnResponse:
    p = _require_pipeline()
    result = await p.run_turn()
    if result is None:
        return TurnResponse(user_text="", assistant_text="(no speech detected)")
    return TurnResponse(user_text=result.user_text, assistant_text=result.assistant_text)


@app.post("/session/start")
async def start_session(max_turns: int = 3) -> dict[str, Any]:
    global _run_task
    p = _require_pipeline()
    if _run_task and not _run_task.done():
        return {"message": "session already running"}
    p._stop.clear()
    p.state = PipelineState.IDLE
    _run_task = asyncio.create_task(p.run(max_turns=max_turns))
    return {"message": "session started", "max_turns": max_turns}


@app.post("/session/stop")
async def stop_session() -> dict[str, str]:
    p = _require_pipeline()
    p.request_stop()
    return {"message": "stop requested"}


def _require_pipeline() -> VoicePipeline:
    if _pipeline is None:
        raise RuntimeError("Pipeline not initialized")
    return _pipeline


def create_app() -> FastAPI:
    return app
