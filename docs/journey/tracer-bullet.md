# Sección 1: La Bala Trazadora y el Enrutamiento de las Skills

## Contexto del proyecto

VoiceLoop nace del [Client Brief](https://github.com/rox651/proyecto-ingenieria-software/blob/main/CLIENT_BRIEF.md): un loop `Mic → STT → LLM → TTS → Altavoz` en Python puro, sin Pipecat/LiveKit, con panel web y API. El desarrollo se ejecutó con **Cursor Agent** en lugar de Claude Code, reutilizando el flujo [Running Your AFK Agent](https://www.aihero.dev/running-your-afk-agent-a9l1u).

---

## grill-me: refinando asunciones antes del código

En el curso se recomienda la skill **grill-me** para tensionar el diseño. En nuestro flujo con Cursor, el equivalente fue una sesión de exploración estructurada **antes del scaffold**:

| Asunción inicial | Pregunta “grill” | Refinamiento |
|------------------|------------------|--------------|
| “Necesito Pipecat desde el día 1” | ¿Qué capa quieres entender realmente? | Python asyncio puro; frameworks como referencia, no dependencia |
| “Un solo script de 500 líneas” | ¿Cómo testeas sin micrófono en CI? | Protocolos + stubs + factory `stub`/`live` |
| “Frontend React inmediato” | ¿Cuál es el tracer mínimo de UI? | HTML/JS + REST; WebSocket en issue posterior |
| “Whisper en GPU” | ¿Qué corre en la laptop del curso? | `faster-whisper` tiny/int8, opcional en extras |

El **árbol de diseño** resultante:

```
VoiceLoop
├── Core asyncio (pipeline)
├── Protocolos intercambiables (STT, LLM, TTS, I/O)
├── Factory de composición
├── API FastAPI (control plane)
└── Dashboard (observabilidad)
```

Este árbol se materializó en `issues/001–009` como **vertical slices** independientes.

---

## La Bala Trazadora (Tracer Bullet)

Ousterhout no usa el término “tracer bullet” (viene de *The Pragmatic Programmer*), pero el curso lo alinea con **reducir riesgo temprano** construyendo un camino end-to-end delgado.

### Primera bala: pipeline stub (Tarea 1)

El primer tracer fue el **loop completo con stubs**:

```python
# Firma pública mínima — oculta 5 etapas
result = await pipeline.run_turn()
# → TurnResult(user_text, assistant_text)
```

Esto validó: asyncio, historial, tests, API `/turn`, dashboard estático.

### Segunda bala: issue de mayor incertidumbre — `#003` LLM

Tras CI (`#008`), atacamos **`#003` OpenAI-compatible LLM** porque:

1. Introduce **I/O de red** asíncrona (httpx) — primer fallo real fuera del proceso.
2. Define el **contrato conversacional** (system prompt, historial) que STT/TTS deben respetar.
3. Desbloquea `#007` WebSocket (eventos `transcript` / `response`).

Ralph ejecutó TDD: test con `MockTransport` → implementación mínima → commit `feat(#003)`.

### Tercera bala: `#006` colas asyncio

El issue más arriesgado arquitectónicamente fue **`#006` streaming con `asyncio.Queue`**: refactor del orquestador sin romper `/turn`. Se validó con 23 tests incluyendo E2E.

---

## Enrutamiento de Skills

| Skill | Cuándo | Efecto |
|-------|--------|--------|
| `/tdd` | Cada issue Ralph | Red-Green-Refactor; tests como contrato |
| `/handoff` | Tras 2–3 issues | `handoffs.md` — purga ruido de contexto |
| `/improve-codebase-architecture` | Mid-sprint | `factory.py` — ver [Sección 3](./retrospective) |
| `ralph/once.sh <ID>` | Siguiente ticket | Respeta `blocked_by` en frontmatter |

### Orden Ralph ejecutado

```
#008 CI → #003 LLM → #001 mic → [checkpoint] → #002 #004 #005 #006 #007 #009
```

Prioridad explícita en `ralph/prompt.md`: bugfix → infra → tracer → feature.

---

## Lección

La bala trazadora no fue “el micrófono” primero, sino **el contrato del loop** (stub) y luego **el LLM** (incertidumbre externa). Eso evitó optimizar audio antes de saber si la conversación funcionaba — coherente con minimizar **change amplification** temprana (Ousterhout, cap. 1).

**Siguiente:** [Anatomía de la Complejidad →](./anatomy)
