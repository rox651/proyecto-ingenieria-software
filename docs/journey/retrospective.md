# Sección 3: Veredicto Retrospectivo de los Sub-Agentes

Recuperamos el [Punto de Control Arquitectónico](https://github.com/rox651/proyecto-ingenieria-software/blob/main/architecture-checkpoint.md) de la Tarea 2 y lo evaluamos **en retrospectiva** tras completar los issues `#002–#009`.

---

## Recordatorio: tres sub-agentes paralelos

La skill `/improve-codebase-architecture` simuló tres propuestas para el módulo de composición:

| Agente | Propuesta | Idea central |
|--------|-----------|--------------|
| **A** | Factory minimalista | `create_pipeline(mode)` |
| **B** | Builder | `PipelineBuilder().with_stt(...).build()` |
| **C** | Registry/DI | Contenedor de providers nombrados |

**Híbrido elegido:** Factory (A) + resolución por entorno + fallbacks en `_create_live_pipeline()`.

---

## Impacto en la segunda mitad del proyecto

### Velocidad de desarrollo

| Métrica | Sin factory (proyectado) | Con factory (real) |
|---------|--------------------------|---------------------|
| Archivos tocados por issue | 3–4 (`api`, `cli`, `pipeline`, nuevo módulo) | 1–2 (`factory`, nuevo módulo) |
| Regresiones en `/turn` | Alta probabilidad | 0 en 23 tests |
| Tiempo Ralph por issue | Re-wiring manual | Registrar en `_create_live_pipeline` |

Issues `#004` TTS, `#005` playback, `#002` STT se integraron **solo en factory** — confirmando la predicción del checkpoint.

### Debate que aceleró el equipo

El sub-agente **B (Builder)** habría sido más explícito para tests parciales, pero el agente Ralph lo sobre-usaría (interfaces amplias = **shallow modules**). El sub-agente **C (Registry)** habría introducido indirección difícil de depurar en HITL.

La factory ganó por **profundidad adecuada**: una función, mucho comportamiento oculto — alineado con Ousterhout.

---

## Elasticidad vs Change Amplification

Ousterhout (cap. 1) describe **change amplification**: un cambio pequeño obliga a tocar muchos módulos.

### Prueba de elasticidad: issue `#006` (colas asyncio)

Refactorizamos `run_turn()` a workers + `asyncio.Queue` **sin cambiar**:

- Firma pública `run_turn() -> TurnResult | None`
- Endpoints REST
- Eventos WebSocket (`state_change`, `transcript`, `response`)
- CLI `voiceloop --turns N`

**Veredicto:** la interfaz de `VoicePipeline` absorbió el cambio interno — **baja amplificación del cambio**.

### Prueba de estrés: issue `#007` WebSocket

Se añadió `EventBus` + `/ws/session` sin modificar `create_pipeline()` — solo suscripción en `lifespan`:

```python
_pipeline.events.subscribe(_broadcast_event)
```

La factory no cambió — **buen gusto arquitectónico**: observabilidad como capa orthogonal.

### Punto débil detectado

`_create_live_pipeline()` creció con `if importable` por componente. Si el proyecto superara ~10 providers, aparecería **change amplification** en ese único archivo — señal para migrar al Builder (Agente B) en una futura iteración, no ahora.

---

## Comparativa con módulos superficiales remanentes

Aún coexisten re-exports superficiales en `stt/__init__.py`, `tts/__init__.py`. Decisión consciente: satisfacer estructura de paquetes Python sin extraer más capas hasta que haya lógica compartida (p. ej. métricas de latencia STT).

---

## Veredicto final

| Criterio | Evaluación |
|----------|------------|
| ¿La factory fue elástica? | **Sí** — 6 issues post-checkpoint sin editar `api.py` wiring |
| ¿Change amplification? | **Baja** en pipeline/API; **moderada** en factory (monolito de registro) |
| ¿Information hiding? | **Sí** — frontend aislado de proveedores |
| ¿Velocidad Ralph 2ª mitad? | **Mayor** — seam único documentado en `ralph/prompt.md` |

### Recomendación futura

Si VoiceLoop evoluciona a plugins dinámicos, promover **Agente B (Builder)** manteniendo `create_pipeline("stub")` como atajo. Evitar Registry hasta demostrar necesidad.

---

## Cierre del Software Journey

```
Exploración (grill-me) → Tracer stub → LLM (#003) → Checkpoint (factory)
    → Features paralelos (#002–#009) → E2E → Este sitio
```

**Repositorio:** https://github.com/rox651/proyecto-ingenieria-software  
**Commits:** historial con mensajes `feat(#NNN)` trazables a issues  
**Tests:** 23/23 passing en CI

← [Volver al inicio](/)
