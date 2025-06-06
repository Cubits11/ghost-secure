# 📁 FILE: BACKEND/core/app.py

print("[🟢] Starting Ghost Secure app initialization...")

from flask import Flask, render_template, jsonify, request, g
from flask_cors import CORS
from datetime import datetime
import os, random, json, logging

# --- PATH SETUP ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))
LOG_DIR = os.path.join(PROJECT_ROOT, "LOGS")
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")
DNA_PATH = os.path.join(PROJECT_ROOT, "BACKEND", "content", "dna_bank.json")
LOG_PATH = os.path.join(LOG_DIR, "tone_flow.log")

# --- FLASK APP INIT ---
print("[🟢] Launching Flask server...")
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)
CORS(app)

print("Template folder exists:", os.path.isdir(TEMPLATE_DIR))
print("DNA_PATH =", DNA_PATH)
print("DNA file exists:", os.path.isfile(DNA_PATH))
print("ghost_ui.html exists:", os.path.isfile(os.path.join(TEMPLATE_DIR, "ghost_ui.html")))
# --- LOGGING SETUP ---
os.makedirs(LOG_DIR, exist_ok=True)
logger = logging.getLogger("GhostCore")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_PATH)
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(console_handler)
app.logger = logger

# --- BLUEPRINTS ---
from BACKEND.routes.ghost import ghost_bp
from BACKEND.routes.pulse import pulse_bp
from BACKEND.routes.surveillance import surveillance_bp

app.register_blueprint(ghost_bp, url_prefix="/ghost")
app.register_blueprint(pulse_bp, url_prefix="/pulse")
app.register_blueprint(surveillance_bp, url_prefix="/surveillance")

# --- SECURITY + MEMORY CONTROL ---
from BACKEND.memory.echo_memory import reset_echo_log, export_archive
from BACKEND.core.ghostscript_engine import generate_ghost_response
from BACKEND.security.lockdown_manager import toggle_lockdown, is_locked, get_lock_info

# --- STARTUP TASK ---
reset_echo_log()
logger.info(f"[SYSTEM START] Ghost Journal initialized at {datetime.now().isoformat()}")

# --- LOCKDOWN FILTER ---
@app.before_request
def check_global_lockdown():
    path = request.path
    exempt_paths = ["/", "/status", "/toggle_lockdown", "/get_prompt", "/favicon.ico", "/static", "/echo_archive", "/archive"]
    app.logger.info(f"[DEBUG] Incoming request: {request.method} {path}")

    if any(path == ep or path.startswith(ep + "/") for ep in exempt_paths):
        app.logger.info(f"[LOCKDOWN] Exempt path: {path}")
        return

    if is_locked():
        lock_info = get_lock_info()
        app.logger.warning(f"[LOCKDOWN BLOCKED] Path: {path} | Reason: {lock_info.get('reason')}")
        return jsonify({
            "error": "System is in lockdown mode.",
            "reason": lock_info.get("reason", "Unknown"),
            "timestamp": lock_info.get("timestamp", "Unknown")
        }), 403

# --- ROUTES ---
@app.route("/")
def home():
    try:
        return render_template("ghost_ui.html")
    except Exception as e:
        logger.error(f"[HOME ERROR] {str(e)}")
        return f"<h2>Template Error</h2><pre>{e}</pre>", 500

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.route("/get_prompt")
def get_prompt():
    try:
        with open(DNA_PATH, "r") as f:
            dna = json.load(f)
        questions = [q for q in dna if isinstance(q, dict) and "question" in q]
        chosen = random.choice(questions)
        logger.info(f"[PROMPT] Served: {chosen}")
        return jsonify(prompt=chosen)
    except Exception as e:
        logger.error(f"[PROMPT ERROR] {e}")
        return jsonify(prompt="Ghost is quiet today."), 500

@app.route("/journal", methods=["POST"])
def journal_entry():
    data = request.get_json(force=True)
    entry = data.get("entry", "").strip()
    mode = data.get("mode", "ghost").strip().lower()
    allow_echo = bool(data.get("echo", True))

    if not entry:
        return jsonify({"error": "Journal entry cannot be empty."}), 400

    result = generate_ghost_response(entry, mode, allow_echo)
    return jsonify(result)

@app.route("/pulse", methods=["POST"])
def pulse_entry():
    try:
        print("[DEBUG] /pulse endpoint hit")
        data = request.get_json(force=True)
        entry = data.get("entry", "").strip()
        mode = data.get("mode", "ghost").strip().lower()
        allow_echo = bool(data.get("echo", True))

        if not entry:
            return jsonify({"error": "Journal entry cannot be empty."}), 400

        result = generate_ghost_response(entry, mode, allow_echo)
        return jsonify(result)
    except Exception as e:
        app.logger.exception(f"[PULSE ERROR] {e}")
        return jsonify({"error": "Ghost failed internally.", "details": str(e)}), 500

@app.route("/archive")
def get_archive():
    return jsonify(export_archive())

@app.route("/echo_archive")
def echo_archive():
    return render_template("echo_archive_ui.html")

@app.route("/surveillance_ui")
def surveillance_ui():
    return render_template("surveillance_ui.html")

@app.route("/reset")
def reset_memory():
    reset_echo_log()
    logger.info("[RESET] Echo memory has been reset.")
    return jsonify({"message": "Echo memory reset complete."})

@app.route("/status")
def get_status():
    logger.info("[STATUS] Status check requested.")
    return jsonify({
        "status": "active",
        "lockdown": is_locked(),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route("/toggle_lockdown", methods=["POST"])
def toggle_lockdown_route():
    try:
        new_state = toggle_lockdown()
        logger.warning(f"[LOCKDOWN TOGGLE] Lockdown {'enabled' if new_state else 'disabled'}")
        return jsonify({"enabled": new_state, "message": f"Lockdown {'enabled' if new_state else 'disabled'}"})
    except Exception as e:
        logger.error(f"[LOCKDOWN ERROR] {e}")
        return jsonify({"error": "Failed to toggle lockdown."}), 500

@app.route("/debug/request")
def debug_request():
    return jsonify({
        "method": request.method,
        "path": request.path,
        "endpoint": request.endpoint,
        "blueprint": request.blueprint,
        "args": request.args
    })

@app.after_request
def add_no_cache(response):
    response.headers.update({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    return response

@app.route("/journal_ui")
def journal_ui():
    return render_template("journal_ui.html")

# --- RUN ---
if __name__ == "__main__":
    logger.info("[RUN] Starting Ghost Secure Flask app in debug mode.")
    app.run(
        debug=True,
        port=5050,
        host="127.0.0.1",
        use_reloader=False,  # ✅ Add this line to stop infinite loop
        extra_files=[
            DNA_PATH,
            "BACKEND/security/lockdown_manager.py"
        ]
    )