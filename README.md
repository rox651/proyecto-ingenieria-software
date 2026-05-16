# VoiceLoop

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
│   ├── api.py               # FastAPI — control de sesiones
│   └── config.py            # Configuración (pydantic-settings)
├── frontend/                # Dashboard HTML/JS
├── tests/                   # pytest + pytest-asyncio
├── issues/                  # Backlog para el agente (markdown)
├── ralph/                   # Prompt e instrucciones del agente AFK
└── .cursor/skills/tdd/      # Skill TDD para Cursor
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
| `ralph/once.sh` | Muestra issues abiertos, últimos commits y el prompt |
| `.cursor/skills/tdd/` | Skill TDD: un test → implementación mínima |

### Cómo ejecutar una iteración (HITL)

1. Asegúrate de tener issues en `issues/` (no en `done/`).
2. Ejecuta:

   ```bash
   bash ralph/once.sh
   ```

3. En **Cursor Agent**, pega el contenido de `ralph/prompt.md` y pide:
   > Pick the highest-priority AFK issue in issues/ and complete one task.

4. Observa: ¿eligió bien la tarea? ¿los tests son útiles? ¿el commit es claro?
5. Al terminar, el agente debe mover el issue a `issues/done/` y hacer commit.

### Modo AFK (futuro)

Para ejecución más autónoma, se puede usar Cursor CLI o Cloud Agents con el mismo `ralph/prompt.md`. En esta entrega el foco es **human-in-the-loop** para calibrar prompts e issues.

## Estado actual (entrega 1)

- [x] Pipeline asyncio con stubs funcionales
- [x] API REST (`/health`, `/status`, `/turn`, `/session/*`)
- [x] Frontend básico conectado a la API
- [x] Tests de pipeline y API
- [ ] Captura real de micrófono (issue 001)
- [ ] STT / LLM / TTS reales (issues 002–005)
- [ ] WebSocket en frontend (issue 007)

## Issues en GitHub

Los archivos en `issues/` deben publicarse también como **GitHub Issues** para la entrega. Ejemplo:

```bash
gh issue create --title "Audio capture with sounddevice" --body-file issues/001-audio-capture-sounddevice.md
```

## Licencia

MIT
