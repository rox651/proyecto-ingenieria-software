# Client Brief — VoiceLoop

## Cliente

**Homero** — desarrollador de software que quiere dominar la arquitectura de agentes de voz conversacionales sin depender de frameworks de alto nivel (Pipecat, LiveKit Agents) hasta entender cada capa.

## Problema

Los frameworks de agentes de voz ocultan la orquestación entre micrófono, STT, LLM y TTS. Eso acelera el prototipado, pero dificulta depurar latencia, manejo de interrupciones y flujos asyncio en producción. Necesito una herramienta mínima pero real que pueda usar en mi día a día para experimentar con pipelines de voz y, a la vez, servir como base educativa del semestre.

## Solución propuesta

**VoiceLoop**: un agente de voz conversacional mínimo en Python puro con `asyncio`, más un panel web y una API REST para monitorear y controlar sesiones.

### Loop en tiempo real

```
Micrófono → Speech-to-Text → LLM → Text-to-Speech → Altavoz
```

### Componentes del sistema

| Capa | Tecnología | Rol |
|------|------------|-----|
| **Core (backend)** | Python 3.11+, asyncio | Pipeline de audio y orquestación del loop |
| **STT** | faster-whisper / API | Transcripción en streaming |
| **LLM** | OpenAI-compatible API | Generación de respuestas conversacionales |
| **TTS** | edge-tts o pyttsx3 | Síntesis de voz |
| **API** | FastAPI | Control de sesiones, health, métricas |
| **Frontend** | HTML + JS (evolución a React) | Dashboard de estado del agente |

## Usuarios objetivo

1. **Yo (desarrollador)** — uso diario para probar prompts, latencia y configuraciones de audio.
2. **Compañeros del curso** — referencia de arquitectura asyncio para el proyecto integrador.

## Alcance del MVP (semestre)

- Captura de audio desde micrófono con buffering asyncio.
- Transcripción incremental (STT).
- Conversación con contexto (LLM).
- Reproducción de respuestas (TTS).
- API REST para iniciar/detener sesiones y consultar estado.
- UI web simple que muestre transcripciones y respuestas en tiempo real.

## Fuera de alcance (por ahora)

- Despliegue en producción multi-tenant.
- Wake word / VAD avanzado (fase posterior).
- Soporte telefónico (SIP/WebRTC completo).

## Criterios de éxito

- El loop completo funciona en local con latencia perceptible < 3 s por turno (objetivo).
- Cada etapa del pipeline es intercambiable (interfaces claras).
- Tests automatizados cubren al menos el orquestador y la API.
- El desarrollo sigue el flujo AFK/HITL con Cursor (ver README).

## Restricciones

- Python puro para el core; sin Pipecat ni LiveKit en la primera fase.
- Código abierto en GitHub con issues trazables.
- Desarrollo asistido por agentes (Cursor), no vibe-coding sin estructura.

## Inspiración técnica

- [Pipecat](https://github.com/pipecat-ai/pipecat) — arquitectura de frames y processors.
- [LiveKit Agents](https://github.com/livekit/agents) — workers y pipelines de voz.
- [Running Your AFK Agent](https://www.aihero.dev/running-your-afk-agent-a9l1u) — flujo de trabajo con agente autónomo.
