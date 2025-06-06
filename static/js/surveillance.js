// surveillance.js — Handles fetching and rendering Ghost Surveillance Logs with clarity and precision

// Initialize on page load
window.addEventListener("DOMContentLoaded", () => {
  fetchSurveillanceLogs();
});

// Fetch logs from the backend /surveillance route
async function fetchSurveillanceLogs() {
  const container = document.getElementById("surveillanceLogs");

  // Safety check: warn if element is missing
  if (!container) {
    console.warn("🕵️‍♂️ surveillanceLogs container not found in DOM.");
    return;
  }

  container.innerHTML = "<p>🔍 Fetching Ghost Surveillance Logs...</p>";

  try {
    const response = await fetch("/surveillance");
    const logs = await response.json();

    if (!logs || logs.length === 0) {
      container.innerHTML = "<p>⚠️ No surveillance logs available at this time.</p>";
      return;
    }

    const formattedLogs = logs.map(formatLogEntry).join("");
    container.innerHTML = `<div class="logs-list">${formattedLogs}</div>`;

  } catch (error) {
    console.error("❌ Error fetching surveillance logs:", error);
    container.innerHTML = `
      <p style="color: red;">🚨 Failed to retrieve surveillance logs.</p>
      <pre style="color:#777; font-size: 0.9rem;">${error.message}</pre>
    `;
  }
}

// Format a single log entry block with color and clarity
function formatLogEntry(log) {
  const { timestamp, event_type, source, details } = log;

  const time = timestamp
    ? new Date(timestamp).toLocaleString()
    : "Unknown time";

  const colorMap = {
    tamper: "#ff6b6b",
    drift: "#f0ad4e",
    info: "#8bc34a",
    alert: "#d984e0",
    system: "#64b5f6",
  };

  async function loadSurveillanceLogs() {
  const container = document.getElementById("surveillanceLogs");
  container.innerHTML = "<p>Loading surveillance logs...</p>";

  try {
    const res = await fetch("/surveillance/raw");
    const data = await res.json();

    if (!res.ok || !data.status || !data.timeline) {
      container.innerHTML = "<p style='color: red;'>Failed to load logs.</p>";
      return;
    }

    container.innerHTML = "";

    const allEchoes = [
      ...data.top_anomalies,
      ...data.cue_mismatches,
      ...data.tampered_entries
    ];

    const unique = new Map();
    allEchoes.forEach(e => unique.set(e.uid, e)); // deduplicate by UID
    const entries = Array.from(unique.values()).slice(-50).reverse(); // latest 50

    if (entries.length === 0) {
      container.innerHTML = "<p>No suspicious echo entries found.</p>";
      return;
    }

    for (const echo of entries) {
      const entryDiv = document.createElement("div");
      entryDiv.className = "log-entry";

      entryDiv.innerHTML = `
        <div class="meta">🕒 ${echo.timestamp || "unknown"} | UID: <code>${echo.uid}</code></div>
        <div class="event-type">🚨 ${
          echo.is_tampered ? "Tampered" : echo.drift_score > 0.7 ? "Anomaly" : echo.cue_mismatch ? "Cue Mismatch" : "Signal"
        }</div>
        <div class="details">
          Drift Score: ${echo.drift_score?.toFixed(3) || "0.000"}<br/>
          Cue Mismatch: ${echo.cue_mismatch ? "Yes" : "No"}<br/>
          Tampered: ${echo.is_tampered ? "Yes" : "No"}<br/>
          Diff: <code>${JSON.stringify(echo.diff || {}, null, 2)}</code>
        </div>
      `;

      container.appendChild(entryDiv);
    }
  } catch (err) {
    container.innerHTML = `<p style="color: red;">Error fetching surveillance data: ${err}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", loadSurveillanceLogs);

  const tone = event_type?.toLowerCase() || "info";
  const eventColor = colorMap[tone] || "#999";

  return `
    <div class="log-entry" style="
      border-left: 4px solid ${eventColor};
      padding-left: 1rem;
      margin-bottom: 1.5rem;
      background: rgba(255, 255, 255, 0.03);
      border-radius: 4px;
    ">
      <div style="color: #ccc; font-size: 0.9rem;">
        <strong>📅 ${time}</strong> | <span style="color: ${eventColor}; font-weight: bold;">${tone.toUpperCase()}</span>
        <span style="opacity: 0.8;">from</span> <code style="font-size: 0.85rem;">${source || "unknown"}</code>
      </div>
      <div style="margin-top: 0.5rem; color: #e0e0e0; font-style: italic;">
        ${details || "<span style='opacity: 0.6;'>No details provided.</span>"}
      </div>
    </div>
  `;
}