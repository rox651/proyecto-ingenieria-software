# Reporte de Control Arquitectónico Intermedio

**Fecha:** 2026-05-16  
**Trigger:** Completados 3 issues Ralph (#008, #003, #001)  
**Skill:** `.cursor/skills/improve-codebase-architecture/SKILL.md`

---

## 1. Diagnóstico inicial

| # | Oportunidad | Riesgo |
|---|-------------|--------|
| 1 | `VoicePipeline` instanciaba stubs directamente en defaults y `api.py` | Cada issue nuevo acoplaría imports en el orquestador |
| 2 | Sin capa de composición | `api.py` vs `cli.py` divergirían en wiring |
| 3 | `pipeline.py` mezcla orquestación + defaults de infra | Dificulta testing aislado por etapa |
| 4 | Paquetes `llm/` y `audio/` recién creados, sin punto único de ensamblaje | Issues #004–#005 repetirían patrón ad-hoc |
| 5 | `PipelineState(str, Enum)` — smell menor | Ruff UP042; corregido a `StrEnum` |

**Elegido para profundización:** #1 + #2 — **módulo de composición del pipeline** (`factory.py`).

---

## 2. Tres propuestas de interfaz (sub-agentes simulados)

### Agente A — Factory minimalista

```python
def create_pipeline(mode: Literal["stub", "live"] = "stub") -> VoicePipeline: ...
```

| Pros | Contras |
|------|---------|
| Mínimo, fácil de testear | Crece un `if/elif` por cada componente live |
| Alineado con `VOICELOOP_MODE` | Menos flexible para tests parciales |

### Agente B — Builder explícito

```python
PipelineBuilder().with_stt(WhisperSTT()).with_llm(OpenAI()).build()
```

| Pros | Contras |
|------|---------|
| Máxima flexibilidad en tests | Verboso para un proyecto semestral pequeño |
| Descubre dependencias al compilar | Overhead para agentes Ralph (más superficie de error) |

### Agente C — Registry / DI container

```python
container.register("llm", OpenAILanguageModel)
pipeline = container.resolve("pipeline")
```

| Pros | Contras |
|------|---------|
| Escalable a muchos providers | Complejidad prematura para VoiceLoop |
| Estilo “framework” | Curva de aprendizaje alta para el curso |

---

## 3. Recomendación híbrida (implementada)

**Factory (A) + resolución por entorno + overrides implícitos en modo `live`:**

- `create_pipeline(mode)` y `resolve_mode()` en `src/voiceloop/factory.py`
- Modo `stub`: siempre stubs (CI, demos sin hardware)
- Modo `live`: `OpenAILanguageModel` si hay API key; `SoundDeviceCapture` si `sounddevice` importable; fallback a stubs
- `api.py` y `cli.py` consumen la factory — **un solo seam** para QA humano

### Justificación técnica

1. **Próximos issues (#004 TTS, #005 playback)** solo registran componentes en `_create_live_pipeline()` sin tocar API ni CLI.
2. **Ralph loops** tienen un archivo obvio que editar; menos riesgo de commits que rompen `api.py`.
3. Builder/Registry se reservan si el proyecto supera ~8 providers configurables.

---

## 4. Cambios aplicados

- Nuevo `src/voiceloop/factory.py`
- `api.py` → `create_pipeline(resolve_mode())`
- `cli.py` → `--mode stub|live`
- Tests: `tests/test_factory.py`
- `PipelineState` migrado a `StrEnum`

**Verificación:** `pytest -v` (14 passed), `ruff check src tests` (clean).

---

## 5. Estado final (Tarea 3)

Todos los issues `#001–#009` completados. Pipeline con colas, WebSocket, VAD, factory live.

**Verificación final:** `pytest -v` (23 passed), Software Journey desplegado en GitHub Pages.

---

## 6. Próximo ciclo Ralph

Proyecto cerrado para el semestre. Mantener factory como seam único si se añaden providers.
