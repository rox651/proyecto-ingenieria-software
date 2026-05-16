const API_BASE = "http://127.0.0.1:8000";

async function fetchJson(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
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
    const li = document.createElement("li");
    const role = msg.role === "user" ? "Usuario" : "Asistente";
    const cls = msg.role === "user" ? "role-user" : "role-assistant";
    li.innerHTML = `<span class="${cls}">${role}:</span> ${escapeHtml(msg.content)}`;
    ul.appendChild(li);
  }
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

async function runTurn() {
  const btn = document.getElementById("btn-turn");
  btn.disabled = true;
  try {
    await fetchJson("/turn", { method: "POST" });
    await refreshStatus();
    await refreshHistory();
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

refreshStatus().catch(() => {
  document.getElementById("state").textContent = "offline";
});
