# VoiceLoop

![CI](https://github.com/rox651/proyecto-ingenieria-software/actions/workflows/ci.yml/badge.svg)

Agente de voz conversacional mínimo en **Python + asyncio** para entender la arquitectura detrás de frameworks como [Pipecat](https://github.com/pipecat-ai/pipecat) y [LiveKit Agents](https://github.com/livekit/agents).

```
Micrófono → STT → LLM → TTS → Altavoz
```

Incluye **backend** (pipeline asyncio + API FastAPI) y **frontend** (dashboard web).

## Client Brief

Ver [CLIENT_BRIEF.md](./CLIENT_BRIEF.md) para problema, usuarios, alcance y criterios de éxito.

## Estructura del proyecto

```
.
├── CLIENT_BRIEF.md          # Brief del cliente
├── src/voiceloop/           # Backend Python
│   ├── pipeline.py          # Orquestador asyncio
│   ├── protocols.py         # Interfaces (STT, LLM, TTS, audio)
│   ├── stubs.py             # Implementaciones stub para desarrollo
│   ├── factory.py           # Composición stub/live (checkpoint arquitectura)
│   ├── llm/                 # Cliente OpenAI-compatible
│   ├── audio/               # Captura de micrófono
│   ├── api.py               # FastAPI — control de sesiones
│   └── config.py            # Configuración (pydantic-settings)
├── frontend/                # Dashboard HTML/JS
├── tests/                   # pytest + pytest-asyncio
├── issues/                  # Backlog para el agente (markdown)
├── handoffs.md              # Bitácora de transferencia entre sesiones
├── architecture-checkpoint.md
├── ralph/                   # Prompt e instrucciones del agente AFK
└── .cursor/skills/          # tdd, handoff, improve-codebase-architecture
```

## Inicio rápido

```bash
# Requiere Python 3.11+
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # opcional: API keys

# CLI — pipeline con stubs (sin mic/API)
voiceloop --turns 1 -v
voiceloop --mode live --turns 1   # requiere OPENAI_API_KEY y opcional sounddevice

# API
uvicorn voiceloop.api:app --reload

# Tests
pytest -v
ruff check src tests
```

### Dashboard

Con la API en `http://127.0.0.1:8000`, abre `frontend/index.html` en el navegador (o sirve la carpeta con cualquier static server).

## Flujo de trabajo con Cursor (AFK / HITL)

Este proyecto sigue el flujo descrito en [Running Your AFK Agent](https://www.aihero.dev/running-your-afk-agent-a9l1u), adaptado de **Claude Code** a **Cursor**:

| Artefacto | Rol |
|-----------|-----|
| `issues/*.md` | Backlog legible por humanos y por el agente |
| `ralph/prompt.md` | Instrucciones del agente (prioridades, TDD, commits) |
| `ralph/once.sh <ID>` | Carga issue por ID y muestra prompt |
| `.cursor/skills/handoff/` | Resumen compacto entre sesiones → `handoffs.md` |
| `.cursor/skills/improve-codebase-architecture/` | Revisión mid-sprint → `architecture-checkpoint.md` |

### Tarea 2 — Ralph Loops (HITL + QA en el Seam)

1. **Ejecutar issue:** `./ralph/once.sh 008` (o el ID desbloqueado)
2. **Cursor Agent:** completar con TDD; commit `feat(#NNN): ...`
3. **QA humano (seam):** `git log`, `pytest`, revisar acoplamientos
4. **Tras 2–3 issues:** invocar skill `improve-codebase-architecture` → ver `architecture-checkpoint.md`
5. **Handoff:** antes de nueva sesión larga, skill `handoff` → actualizar `handoffs.md`
6. **Siguiente ciclo:** revisar `blocked_by`; issues desbloqueados en Kanban

### Cómo ejecutar una iteración (HITL)

```bash
./ralph/once.sh        # listar issues abiertos
./ralph/once.sh 007    # apuntar al issue #007
```

En **Cursor Agent:** completar el issue indicado. Commit: `feat(#007): descripción`.

## Estado actual

- [x] Pipeline asyncio + factory `stub`/`live`
- [x] API REST + frontend básico
- [x] CI GitHub Actions (#008)
- [x] LLM OpenAI-compatible (#003)
- [x] Captura micrófono sounddevice (#001)
- [x] Checkpoint arquitectónico (`factory.py`)
- [ ] STT faster-whisper (#002)
- [ ] TTS edge-tts (#004) → desbloquea #005
- [ ] WebSocket dashboard (#007) — **desbloqueado**

## Issues en GitHub

Los archivos en `issues/` deben publicarse también como **GitHub Issues** para la entrega. Ejemplo:

```bash
gh issue create --title "Audio capture with sounddevice" --body-file issues/001-audio-capture-sounddevice.md
```

## Licencia

MIT
