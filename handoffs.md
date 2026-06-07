# Bitácora de Transferencia (Handoffs)

Resúmenes compactos generados entre sesiones de agente para mitigar ruido de tokens.

---

## Handoff — 2026-05-16 (post issues #008, #003, #001)

### Built
- `#008` CI, `#003` LLM, `#001` mic, `factory.py`

### Next Ralph target
`./ralph/once.sh 007`

---

## Handoff — 2026-06-07 (entrega final Tarea 3)

### Built
- `#002` WhisperSTT, `#004` EdgeTTS, `#005` SoundDevicePlayback
- `#006` pipeline con asyncio.Queue (5 workers)
- `#007` WebSocket `/ws/session` + EventBus
- `#009` EnergyVAD en modo live
- E2E: `tests/test_e2e.py`, `tests/test_websocket.py` (23 tests total)
- Docs: VitePress Software Journey en `/docs`

### Architecture decisions
- Eventos de dominio (`transcript`, `response`) — sin leakage OpenAI al frontend
- Factory absorbió todos los providers live

### Pending
- Ningún issue en `issues/` — todos en `issues/done/`

### URLs entrega
- Repo: https://github.com/rox651/proyecto-ingenieria-software
- Journey: https://rox651.github.io/proyecto-ingenieria-software/
