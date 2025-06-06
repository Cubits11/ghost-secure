// echo_archive.js – Fetch and render echo memory from backend

window.onload = () => {
  loadEchoes();
};

async function loadEchoes() {
  const container = document.getElementById("echoContainer");
  container.innerHTML = "🔍 Loading echo memory...";

  try {
    const res = await fetch("/archive");
    const data = await res.json(); // ✅ This returns { pulseType: [echo, echo] }

    const entries = Object.entries(data)
      .flatMap(([pulse, echoes]) =>
        Array.isArray(echoes)
          ? echoes.map(e => ({ ...e, pulse }))
          : []
      )
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    if (entries.length === 0) {
      container.innerHTML = "⚠️ No echo memory available.";
      return;
    }

    const echoesHTML = entries
      .map(e => renderEchoEntry(e.fingerprint || "—", e))
      .join("<div class='divider'></div>");

    container.innerHTML = echoesHTML;

  } catch (err) {
    console.error("Failed to fetch echo memory:", err);
    container.innerHTML = "❌ Error loading echoes.";
  }
}

function renderEchoEntry(fingerprint, echo) {
  const {
    tone = "unknown",
    pulse = "UNKNOWN",
    response = "—",
    timestamp = null,
    tags = []
  } = echo;

  const toneTag = tone.toUpperCase();
  const tagList = Array.isArray(tags) ? tags.join(", ") : "None";

  const formattedTime = timestamp
    ? new Date(timestamp).toLocaleString()
    : "Unknown time";

  return `
    <div class="echo-entry">
      <div class="echo-meta">
        🧬 <span class="tone-tag">${toneTag}</span> | 🫀 ${pulse} | 🕒 ${formattedTime}<br>
        🏷️ Tags: ${tagList}
      </div>
      <div class="echo-content">${response}</div>
    </div>
  `;
}