
// =======================
// 📜 Ghost UI – Main Logic
// =======================

// Animate ritual gate elements on window load
window.onload = () => {
  try {
    refreshSystemStatus(); // Lockdown + Tone
    setInterval(refreshSystemStatus, 10000);
  } catch (err) {
    console.error("[Ghost.js Init Error]", err);
  }
};

// 🚪 Enter the journal after ritual gate
function enterJournal() {
  document.getElementById("ritualGate").style.display = "none";
  document.getElementById("journalInterface").style.display = "flex";
}

// 🔁 Fetch and update lockdown + tone status
async function refreshSystemStatus() {
  try {
    const res = await fetch("/status");
    const data = await res.json();
    updateLockdownUI(data.lockdown);
    updateToneUI(data.tone_mode || "ghost");
  } catch (err) {
    console.error("System status fetch failed:", err);
  }
}

// 🔒 Enable/disable journal UI based on lockdown
function updateLockdownUI(isLocked) {
  const entry = document.getElementById("entry");
  const button = document.querySelector(".submit-btn");
  const banner = document.getElementById("lockdownBanner");

  entry.disabled = isLocked;
  button.disabled = isLocked;
  banner.style.display = isLocked ? "block" : "none";
}

// 🧠 Display current tone mode in UI
function updateToneUI(currentTone) {
  const toneStatus = document.getElementById("toneStatus");
  toneStatus.textContent = `🧠 Ghost is currently thinking in: “${currentTone}” tone.`;
}

// 📤 Submit entry to /pulse and render animated response
async function submitEntry() {
  // throw new Error("🔥 FORCE CRASH");
  const entryText = document.getElementById('entry').value.trim();
  const toneMode = document.getElementById('toneMode').value;
  const allowEcho = document.getElementById('echoToggle').checked;
  const responseBox = document.getElementById('response');
  const drawer = document.getElementById('echoDrawer');
  const submitBtn = document.querySelector('.submit-btn');

  if (!entryText) {
    responseBox.innerHTML = '<p style="opacity: 0.6;">Ghost waits for words before speaking.</p>';
    return;
  }

  responseBox.innerHTML = '<span style="opacity: 0.6;">...listening...</span>';
  submitBtn.disabled = true;

  try {
    const res = await fetch('/pulse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ entry: entryText, mode: toneMode, echo: allowEcho })
    });

    const data = await res.json();
    console.log("[DEBUG] Received from /pulse:", data);
    if (!data || !data.ghost_response) {
      responseBox.innerHTML = '<p style="color: red;">Ghost is silent. No words returned.</p>';
      submitBtn.disabled = false;
      return;
    }

    animateResponse(data, responseBox, submitBtn);
    await loadEchoDrawer(); // Load echoed memories

  } catch (err) {
    console.error("Submission error:", err);
    responseBox.innerHTML = '<p style="color: red;">Ghost could not speak. Check your connection.</p>';
    submitBtn.disabled = false;
  }
}

// 🎞️ Typewriter animation for ghost's reply
function animateResponse(data, responseBox, submitBtn) {
  try {
    if (!data || !data.ghost_response) {
      responseBox.innerHTML = `<p style="color: red;">Ghost is silent. Still no words returned.</p>`;
      submitBtn.disabled = false;
      return;
    }

    const responseText = `"${(data.ghost_response || "").trim()}"`;
    const pulse = data.pulse || "—";
    const tone = data.tone_origin || "ghost";
    const strategy = (Array.isArray(data.strategy) ? data.strategy.join(', ') : data.strategy) || "—";
    const labelText = `Pulse: ${pulse} | Tone: ${tone} | Strategy: ${strategy}`;

    responseBox.innerHTML = `<p class="ghost-line ghost-tone-${tone}"></p><div class="label"></div>`;
    const lineElem = document.querySelector('.ghost-line');
    const labelElem = document.querySelector('.label');

    let i = 0;
    const interval = setInterval(() => {
      if (i < responseText.length) {
        lineElem.textContent += responseText.charAt(i++);
      } else {
        clearInterval(interval);
        labelElem.textContent = labelText;
        submitBtn.disabled = false;
      }
    }, 40);
  } catch (err) {
    console.error("[ERROR] animateResponse failed:", err);
    responseBox.innerHTML = `<p style="color: red;">Ghost failed to respond properly.</p>`;
    submitBtn.disabled = false;
  }
}

// 📜 Load last 3 echoed memories
async function loadEchoDrawer() {
  const drawer = document.getElementById("echoDrawer");
  drawer.innerHTML = "";

  try {
    const res = await fetch("/archive");
    const archive = await res.json();

    const allEntries = Object.entries(archive)
      .flatMap(([pulse, entries]) =>
        Array.isArray(entries)
          ? entries.map(e => ({ ...e, pulse }))
          : []
      )
      .filter(e => e.timestamp) // Filter malformed entries
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      .slice(0, 3);

    if (allEntries.length === 0) {
      drawer.innerHTML = "<p style='color: #ffcc00;'>⚠️ No echo memory available.</p>";
      return;
    }

    drawer.innerHTML = "<h3>🗂️ Recently Echoed</h3>";
    allEntries.forEach(entry => {
      const block = document.createElement("div");
      block.className = "echo-block";
      block.innerHTML = `
        <div class="label">${entry.timestamp} | ${entry.pulse}</div>
        <div class="line">“${entry.entry.slice(0, 100)}...”</div>
      `;
      drawer.appendChild(block);
    });

  } catch (err) {
    console.error("Echo drawer failed:", err);
    drawer.innerHTML = "<p style='color: red;'>Echo drawer failed to load echoes.</p>";
  }
}
