# VoiceLoop

![CI](https://github.com/rox651/proyecto-ingenieria-software/actions/workflows/ci.yml/badge.svg)

Agente de voz conversacional mínimo en **Python + asyncio** para entender la arquitectura detrás de frameworks como [Pipecat](https://github.com/pipecat-ai/pipecat) y [LiveKit Agents](https://github.com/livekit/agents).

```
Micrófono → STT → LLM → TTS → Altavoz
```

Incluye **backend** (pipeline asyncio + API FastAPI + WebSocket) y **frontend** (dashboard en tiempo real).

## Software Journey (Tarea 3 — entrega final)

**Sitio de documentación:** https://rox651.github.io/proyecto-ingenieria-software/

Análisis arquitectónico con terminología de John Ousterhout (*A Philosophy of Software Design*):

1. [Bala Trazadora y Skills](./docs/journey/tracer-bullet.md)
2. [Módulos Profundos vs Superficiales](./docs/journey/anatomy.md)
3. [Veredicto Retrospectivo](./docs/journey/retrospective.md)

Desarrollo local del sitio: `npm ci && npm run docs:dev`

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
│   ├── stt/                 # faster-whisper
│   ├── tts/                 # edge-tts
│   ├── vad/                 # detección de voz
│   ├── events.py            # EventBus → WebSocket
│   ├── api.py               # FastAPI — REST + /ws/session
│   └── config.py            # Configuración (pydantic-settings)
├── docs/                    # VitePress — Software Journey
├── frontend/                # Dashboard WebSocket + polling fallback
├── tests/                   # 23 tests (unit + E2E + WebSocket)
├── issues/done/             # Todos los issues completados (#001–#009)
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

## Estado del proyecto (completo)

- [x] Pipeline asyncio con colas (#006) + VAD (#009)
- [x] STT faster-whisper (#002), LLM (#003), TTS edge (#004), playback (#005)
- [x] Captura micrófono (#001), WebSocket dashboard (#007)
- [x] CI (#008), factory arquitectónica, 23 tests passing
- [x] Software Journey desplegado en GitHub Pages

## Licencia

MIT
