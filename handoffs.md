# Bitácora de Transferencia (Handoffs)

Resúmenes compactos generados entre sesiones de agente para mitigar ruido de tokens.
Usar la skill `.cursor/skills/handoff/SKILL.md` antes de abrir un chat nuevo.

---

## Handoff — 2026-05-16 (post issues #008, #003, #001)

### Built
- `#008` CI: `.github/workflows/ci.yml` (pytest + ruff en push/PR)
- `#003` LLM: `src/voiceloop/llm/openai_client.py` + tests con `httpx.MockTransport`
- `#001` Audio: `src/voiceloop/audio/capture.py` (`SoundDeviceCapture`, executor async)
- Checkpoint: `src/voiceloop/factory.py` — composición `stub` / `live`

### Architecture decisions
- Protocolos en `protocols.py`; implementaciones por paquete (`llm/`, `audio/`)
- `VOICELOOP_MODE` / `--mode` selecciona stub vs live
- Live LLM solo si `OPENAI_API_KEY` está definida; mic requiere `sounddevice` opcional

### Tests / CI
- 14 tests locales en verde; CI en GitHub Actions (Python 3.11)

### Pending (exact)
| ID | Estado | blocked_by |
|----|--------|------------|
| 002 | open | — |
| 004 | open | — |
| 005 | open | 004 |
| 006 | open | 001–005 (001 ✅ → parcialmente desbloqueado) |
| 007 | open | 003 ✅ **UNBLOCKED** |
| 009 | open | 001 ✅ **UNBLOCKED** |

### Next Ralph target
```bash
./ralph/once.sh 007
```
WebSocket dashboard — `#003` cerrado, dependencia satisfecha.
