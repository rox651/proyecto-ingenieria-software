const API_BASE = "http://127.0.0.1:8000";
const WS_BASE = API_BASE.replace(/^http/, "ws");

let ws = null;
let pollingFallback = false;

async function fetchJson(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function appendHistory(role, content) {
  const ul = document.getElementById("history");
  if (ul.querySelector(".muted")) ul.innerHTML = "";
  const li = document.createElement("li");
  const label = role === "user" ? "Usuario" : "Asistente";
  const cls = role === "user" ? "role-user" : "role-assistant";
  li.innerHTML = `<span class="${cls}">${label}:</span> ${escapeHtml(content)}`;
  ul.appendChild(li);
}

function handleEvent(data) {
  if (data.event === "state_change") {
    document.getElementById("state").textContent = data.state;
  }
  if (data.event === "transcript") {
    appendHistory("user", data.content);
  }
  if (data.event === "response") {
    appendHistory("assistant", data.content);
    const turns = document.getElementById("turns");
    turns.textContent = String(Number(turns.textContent || 0) + 1);
  }
}

function connectWebSocket() {
  if (ws && ws.readyState <= WebSocket.OPEN) return;

  ws = new WebSocket(`${WS_BASE}/ws/session`);

  ws.onopen = () => {
    pollingFallback = false;
    document.getElementById("conn").textContent = "WebSocket";
  };

  ws.onmessage = (msg) => {
    try {
      handleEvent(JSON.parse(msg.data));
    } catch (_) {
      /* ignore */
    }
  };

  ws.onclose = () => {
    document.getElementById("conn").textContent = "polling";
    pollingFallback = true;
    setTimeout(connectWebSocket, 3000);
  };

  ws.onerror = () => {
    ws.close();
  };
}

async function refreshStatus() {
  const status = await fetchJson("/status");
  document.getElementById("state").textContent = status.state;
  document.getElementById("turns").textContent = String(status.turns_completed);
}

async function refreshHistory() {
  const history = await fetchJson("/history");
  const ul = document.getElementById("history");
  ul.innerHTML = "";
  if (!history.length) {
    ul.innerHTML = "<li class='muted'>Sin mensajes aún</li>";
    return;
  }
  for (const msg of history) {
    appendHistory(msg.role, msg.content);
  }
}

async function runTurn() {
  const btn = document.getElementById("btn-turn");
  btn.disabled = true;
  try {
    await fetchJson("/turn", { method: "POST" });
    if (pollingFallback) {
      await refreshStatus();
      await refreshHistory();
    }
  } catch (e) {
    alert("No se pudo conectar con la API. ¿Está corriendo uvicorn?");
  } finally {
    btn.disabled = false;
  }
}

document.getElementById("btn-turn").addEventListener("click", runTurn);
document.getElementById("btn-refresh").addEventListener("click", async () => {
  await refreshStatus();
  await refreshHistory();
});

connectWebSocket();
refreshStatus().catch(() => {
  document.getElementById("state").textContent = "offline";
});
