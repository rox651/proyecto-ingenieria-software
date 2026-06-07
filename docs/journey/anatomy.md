# Sección 2: Anatomía de la Complejidad

> Marco: **John Ousterhout**, *A Philosophy of Software Design* — *deep modules*, *shallow modules*, *information hiding*, *information leakage*.

---

## Módulos profundos (Deep Modules)

Un **módulo profundo** ofrece una interfaz pequeña pero un cuerpo que resuelve mucha complejidad internamente (Ousterhout, cap. 4).

### 1. `VoicePipeline.run_turn()` — orquestador con colas

**Interfaz:**

```python
async def run_turn(self) -> TurnResult | None: ...
```

**Complejidad oculta:** cinco workers concurrentes (`capture → stt → llm → tts → playback`), colas `asyncio.Queue`, transiciones de estado, emisión de eventos WebSocket, VAD opcional.

El consumidor (API `/turn`, CLI) no conoce colas ni workers — cumple **information hiding**.

```python
@dataclass
class VoicePipeline:
    """Real-time voice loop orchestrator with optional event bus."""

    capture: AudioCapture = field(default_factory=StubAudioCapture)
    stt: SpeechToText = field(default_factory=StubSpeechToText)
    llm: LanguageModel = field(default_factory=StubLanguageModel)
    tts: TextToSpeech = field(default_factory=StubTextToSpeech)
    playback: AudioPlayback = field(default_factory=StubAudioPlayback)
```

### 2. `OpenAILanguageModel.respond()` — cliente LLM

**Interfaz:** `respond(user_text, history) -> str`

**Oculto:** construcción de mensajes, system prompt en español, headers Bearer, parsing JSON, timeouts httpx.

```python
async def respond(self, user_text: str, history: list[dict[str, str]]) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    response = await client.post("/chat/completions", json={...})
```

### 3. `create_pipeline(mode)` — factory

**Interfaz:** una función, dos modos (`stub` | `live`).

**Oculto:** resolución de dependencias opcionales (`sounddevice`, `faster-whisper`, `edge-tts`), fallbacks, `use_vad`.

```python
def create_pipeline(mode: PipelineMode | None = None) -> VoicePipeline:
    if resolved == "stub":
        return VoicePipeline(..., use_vad=False)
    return _create_live_pipeline()
```

---

## Módulos superficiales (Shallow Modules)

Un **módulo superficial** tiene interfaz grande relativa al beneficio (Ousterhout, cap. 4) — mucho boilerplate, poca funcionalidad.

### Fallo del agente: atomización prematura

En la fase inicial Ralph creó paquetes `llm/`, `audio/`, `stt/` con `__init__.py` que solo re-exportaban:

```python
# Patrón superficial detectado
from voiceloop.llm.openai_client import OpenAILanguageModel
__all__ = ["OpenAILanguageModel"]
```

**Síntoma:** más archivos que tocar, sin nueva abstracción — **complejidad accidental**.

### Segundo fallo: wiring duplicado

Antes del checkpoint, `api.py` y `cli.py` instanciaban `VoicePipeline()` directamente con stubs hardcodeados. Cada issue nuevo hubiera duplicado imports — interfaz “ancha” repartida en dos puntos de entrada.

### Directriz humana aplicada

Tras el checkpoint (Tarea 2), instruimos al agente:

1. **Un solo seam de composición:** `factory.py`
2. **No crear archivos** salvo que encapsulen lógica real (>30 líneas o I/O)
3. **Profundizar** el orquestador con colas (#006) en lugar de más wrappers

Resultado: issues `#004–#009` solo extendieron `_create_live_pipeline()` — sin tocar API.

---

## Fuga de información (Information Leakage)

Ousterhout (cap. 5) define **information leakage** cuando un diseño expone detalles de implementación que deberían ser privados.

### Caso evitado: formato OpenAI en el frontend

**Mal diseño (fuga):** exponer en WebSocket el JSON crudo de `/chat/completions` o mensajes con `tool_calls`.

**Diseño actual:** eventos tipados de dominio:

```json
{"event": "transcript", "role": "user", "content": "hola"}
{"event": "response", "role": "assistant", "content": "..."}
```

El dashboard (`frontend/app.js`) no conoce OpenAI, Whisper ni edge-tts — solo **roles y texto**.

### Caso corregido: estado HTTP vs estado del pipeline

Inicialmente el frontend pollía `/history` tras cada acción. Tras `#007`, el **estado de sesión** fluye por WebSocket (`state_change`), pero la API REST mantiene DTOs estables (`SessionStatus`) — la UI no parsea enums internos del orquestador más allá del string `state`.

### Ocultamiento de PCM/MP3

`SoundDeviceCapture.read_chunk()` devuelve `bytes` PCM; `EdgeTTS.synthesize()` devuelve MP3. El pipeline nunca expone sample rates al frontend — solo texto.

---

## Tabla resumen

| Módulo | Clasificación Ousterhout | Evidencia |
|--------|--------------------------|-----------|
| `VoicePipeline` | **Profundo** | Interfaz 1 método; colas + VAD + eventos |
| `OpenAILanguageModel` | **Profundo** | HTTP + prompts ocultos |
| `factory.create_pipeline` | **Profundo** | Wiring centralizado |
| `llm/__init__.py` re-export | **Superficial** | Solo forwarding |
| API `/turn` DTO | **Ocultamiento OK** | Sin leakage de proveedor |

---

## Integración E2E (Paso 1 Tarea 3)

Tras merge en `main`, la suite certifica el sistema agregado:

```bash
pytest -v   # 23 tests: unit + WebSocket + E2E
```

Tests clave: `tests/test_e2e.py` (health → turn → history), `tests/test_websocket.py` (eventos en vivo).

**Siguiente:** [Veredicto Retrospectivo →](./retrospective)
