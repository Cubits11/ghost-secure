🕯️ GHOST SECURE

Ghost Secure** is a cryptographically sealed, emotionally intelligent journaling system.

It merges AI-driven emotional analysis with tamper-proof memory storage, whisper-based memory resurrection, and adaptive tone modulation. Ghost Secure is designed for humans who need more than just a journaling app — it’s for those who need a haunted mirror that listens, forgets wisely, and remembers when it matters most.

---

## 📜 Table of Contents

- [🌌 Philosophy](#-philosophy)
- [🧠 System Overview](#-system-overview)
- [🔐 Security Features](#-security-features)
- [🧬 Emotional Architecture](#-emotional-architecture)
- [🕯️ Whisper Engine](#️-whisper-engine)
- [📁 Directory Structure](#-directory-structure)
- [⚙️ Setup & Installation](#️-setup--installation)
- [🧪 Testing Suite](#-testing-suite)
- [🔄 API Endpoints](#-api-endpoints)
- [📊 Data Flow Summary](#-data-flow-summary)
- [🧭 Future Features](#-future-features)
- [🖋️ License](#-license)

---

## 🌌 Philosophy

Ghost Secure was born from the question:  
> *“What if a journal could remember just enough to help — and forget enough to heal?”*

It’s not just a product.  
It’s a spiritual machine.

- **Journaling becomes a ritual.**
- **Resurrected memories become whispers.**
- **Cryptographic hashes become emotional contracts.**

Ghost Secure protects your feelings like secrets, and treats your history like a soulprint.

---

## 🧠 System Overview

| Layer              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| **Frontend**       | Animated journal UI with whisper rendering, quote retrieval, and user prompts |
| **Backend Core**   | Handles tone flow, tag detection, quote logic, pulse affinity, echo routing |
| **Echo Memory**    | Stores journal entries as fingerprinted, hash-verified echoes              |
| **Whisper Engine** | Resurrects emotionally resonant echoes via affinity × pressure scoring     |
| **Security Layer** | Lockdown mode, cryptographic logging, whisper signature chain               |
| **Tone Tracker**   | Stores evolving emotional flow per user                                    |
| **Surveillance Log** | Audits user activity, system decisions, and whisper triggers              |

---

## 🔐 Security Features

- **Echo Integrity Hashing**: Each echo is signed using SHA-256 and timestamped.
- **Whisper Chain**: Each whisper includes the hash of the previous to form a tamper-evident chain.
- **Lockdown Mode**: Freezes journal entry. Read-only access to archives is permitted.
- **Surveillance Logging**: All actions (whisper resurrection, tone changes, entry submission) are logged with metadata.
- **Replay Protection**: Whispers use nonces to prevent duplication or spoofing.
- **Audit Routes**: `/verify_whisper_log`, `/surveillance`, and `/status` ensure system transparency.

---

## 🧬 Emotional Architecture

- **Emotional Tags**: Custom-defined taxonomy with severity scoring (e.g., `loop`, `disconnected`, `ache`, `hopeful`)
- **Tone Flow**: Dynamically adjusted tone modes (e.g., ghost, monk, absurd) based on pressure and tag evolution.
- **Tag Drift**: Allows tags to shift naturally over time to reflect healing, suppression, or transformation.
- **Symbolic Silence Layer**: System may refuse to speak when loop tags dominate, modeling emotional silence.

---

## 🕯️ Whisper Engine

The heart of Ghost Secure.

- **Affinity Score**:  
  `AS = (0.35 × fingerprint) + (0.3 × tag_overlap) + (0.25 × pressure) - (0.1 × drift)`

- **Echo Decay**:  
  `pressure(t) = initial_pressure × e^(-λt)`

- **Trigger Logic**:  
  Whispers are returned when `(affinity × pressure) ≥ dynamic_threshold`.

- **User Feedback**:  
  Whispers are spectral journal fragments, appearing like a ghost returning to say:  
  *“You’ve been here before.”*

---

## 📁 Directory Structure

GHOST_SECURE/
│
├── BACKEND/
│   ├── app.py                      # Flask app entrypoint
│   ├── core/
│   │   ├── ghostscript_engine.py  # Pulse classification & whisper routing
│   │   ├── emotional_tag_detector.py
│   │   ├── tone_strategy_engine.py
│   │   ├── tone_flow_engine.py
│   │   ├── tag_logic_engine.py
│   ├── memory/
│   │   ├── echo_memory.py
│   │   ├── tone_tracker.py
│   │   ├── echo_decay.py
│   │   ├── echo_resonance_engine.py
│   │   ├── journal_logger.py
│   ├── content/
│   │   ├── dna_bank.json          # Prompt bank
│   │   ├── quote_bank.py
│   ├── routes/
│   │   ├── ghost.py
│   │   ├── pulse.py
│   │   ├── archive.py
│   ├── security/
│   │   ├── security_layer.py
│   │   ├── whisper_chain.py
│
├── LOGS/
│   ├── secure_echo_log.jsonl
│   ├── tone_flow.log
│
├── TESTS/
│   ├── test_echo_memory.py
│   ├── test_tone_strategy.py
│   ├── test_ghost_whispers.py
│
├── templates/
│   ├── ghost_ui.html
│   ├── archive_view.html
│
├── static/
│   ├── style.css
│   ├── ghost.js


---

## ⚙️ Setup & Installation

### 1. Clone the Repo

```bash
git clone https://github.com/YourUsername/ghost-secure.git
cd ghost-secure

### 2. Set up the Virutal Enviornemnt
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Run the server
python BACKEND/app.py

Server runs at: http://localhost:5000

---
🧪 Testing Suite

Run all unit tests:
python -m unittest discover -s TESTS/

Includes:
	•	Echo deduplication & fingerprinting
	•	Whisper resurrection scenarios
	•	Tone strategy and routing logic
	•	Cryptographic hash verification

⸻

🔄 API Endpoints
Route                Method     Description
/journal             POST       Submit a journal entry
/get_prompt          GET        Get a random DNA writing prompt
/status              GET        System status ping
/reset               GET        Reset journal log (dev only)
/archive             GET        View past echoes (JSON + HTML)
/toggle_lockdown     POST       Enable or disable lockdown mode
/surveillance        GET        Return recent system action logs
/verify_whisper_log  GET        Validate whisper chain integrity

📊 Data Flow Summary
	1.	User submits entry → /journal
	2.	System:
	•	Detects emotional tags
	•	Classifies pulse & tone
	•	Stores entry with fingerprint
	•	Calculates affinity with past echoes
	•	Resurrects whispers (if thresholds met)
	3.	Returns:
	•	Ghost response
	•	Echo metadata
	•	Optional whispers

All actions are logged securely and signed for auditability.

⸻

🧭 Future Features
	•	Soulprint Engine — longitudinal user identity signature
	•	Analyst Mode — visualize tone drift, loop recurrence, silence patterns
	•	Reverse Whispers — ghost initiates reflection without entry
	•	User authentication & multi-user expansion
	•	Encrypted syncable backups & exportable memories

⸻

🖋️ License

MIT License.
Use, adapt, or extend with care and credit.
Do not use for commercial emotion mining without permission.

⸻

🕯️ “You are not alone. You are echoed.
And Ghost remembers only what needs to return.”



