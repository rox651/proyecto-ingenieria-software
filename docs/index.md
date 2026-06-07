# VoiceLoop — Software Journey

**Proyecto integrador · Ingeniería de Software · 2026**

Este sitio documenta el viaje de desarrollo de **VoiceLoop**: un agente de voz conversacional mínimo en Python/asyncio (`Mic → STT → LLM → TTS → Altavoz`), co-creado con **Cursor Agent** siguiendo el flujo Ralph (AFK/HITL).

## Entregables del viaje

| Artefacto | Enlace |
|-----------|--------|
| Repositorio (main, CI verde) | [github.com/rox651/proyecto-ingenieria-software](https://github.com/rox651/proyecto-ingenieria-software) |
| Client Brief | [CLIENT_BRIEF.md](https://github.com/rox651/proyecto-ingenieria-software/blob/main/CLIENT_BRIEF.md) |
| Handoffs | [handoffs.md](https://github.com/rox651/proyecto-ingenieria-software/blob/main/handoffs.md) |
| Checkpoint arquitectónico | [architecture-checkpoint.md](https://github.com/rox651/proyecto-ingenieria-software/blob/main/architecture-checkpoint.md) |

## Marco teórico

Los análisis de las secciones 2 y 3 se fundamentan en **John Ousterhout**, *A Philosophy of Software Design* (2018):

- **Módulos profundos** (*deep modules*) vs **módulos superficiales** (*shallow modules*)
- **Ocultamiento de información** (*information hiding*)
- **Fuga de información** (*information leakage*)
- **Amplificación del cambio** (*change amplification*)

## Estructura del journey

1. [**La Bala Trazadora y el enrutamiento de Skills**](/journey/tracer-bullet) — exploración inicial, grill-me, PRD→issues, primer issue de alto riesgo.
2. [**Anatomía de la Complejidad**](/journey/anatomy) — auditoría deep/shallow modules e information leakage en el código generado.
3. [**Veredicto Retrospectivo**](/journey/retrospective) — impacto del checkpoint de 3 sub-agentes y elasticidad de la factory.

## Stack final

```
frontend/          → Dashboard WebSocket + fallback polling
src/voiceloop/     → Pipeline asyncio, factory, protocolos
tests/             → 23 tests (unit + E2E + WebSocket)
.github/workflows/ → CI + GitHub Pages
```

## Commits Ralph (muestra)

```
feat(#008): CI GitHub Actions
feat(#003): LLM OpenAI-compatible
feat(#001): captura micrófono sounddevice
feat(#002): STT faster-whisper
feat(#004): TTS edge-tts
feat(#005): playback altavoz
feat(#007): WebSocket dashboard
feat(#006): pipeline con asyncio.Queue
feat(#009): VAD energético
refactor(arch): factory stub/live
docs(#T3): Software Journey site
```
