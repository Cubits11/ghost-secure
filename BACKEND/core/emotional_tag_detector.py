import re
import json
import os
import logging
from collections import Counter

# 🧭 Get path to project root (one level above BACKEND/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_DIR = os.path.join(PROJECT_ROOT, "LOGS")
LOG_PATH = os.path.join(LOG_DIR, "emotional_tagging.log")

# 🛡️ Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# 🧾 Initialize logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("GhostTagEngine")

# 🔹 Precompiled emotional regex patterns
TAG_PATTERNS = {
    "grief": [
        r"\bgrie(?:f|ving)\b", r"\bloss\b", r"\bmis(?:s|sing)\b",
        r"\bempt(?:y|iness)\b", r"\bdeath\b", r"\bfuneral\b"
    ],
    "relapse": [
        r"\brelaps(?:e|ed|ing)\b", r"\bagain\b", r"\bback to (?:zero|start)\b",
        r"\b(?:can'?t|unable) (?:stop|control)\b", r"\b(?:failed|failure) again\b"
    ],
    "disconnection": [
        r"\bdisconnect(?:ed|ion)?\b", r"\bnumb\b", r"\bautopilot\b",
        r"\bfloating\b", r"\bout of body\b", r"\b(?:feel|felt) nothing\b"
    ],
    "shame": [
        r"\basham(?:e|ed)\b", r"\bdisgust(?:ed|ing)?\b", r"\bembarrass(?:ed|ing)\b",
        r"\bhumiliat(?:e|ed|ion)\b", r"\bworthless\b", r"\b(?:hate|despise) myself\b"
    ],
    "collapse": [
        r"\bcollaps(?:e|ed|ing)\b", r"\bbreak(?:ing|down)\b", r"\bgave up\b",
        r"\bcan'?t (?:go on|continue)\b", r"\b(?:final|last) straw\b"
    ],
    "rage": [
        r"\brag(?:e|ing)\b", r"\bfur(?:y|ious)\b", r"\bexplod(?:e|ing)\b",
        r"\b(?:seeing|losing) red\b", r"\b(?:fuming|seething)\b"
    ],
    "healing": [
        r"\bheal(?:ing)?\b", r"\bprogress\b", r"\bbetter today\b",
        r"\bforward\b", r"\bstep by step\b"
    ]
}

# ⚡ Precompile all regex for performance
COMPILED_PATTERNS = {
    tag: [re.compile(pat, re.IGNORECASE) for pat in patterns]
    for tag, patterns in TAG_PATTERNS.items()
}

# 📂 Load emotional lexicon from DNA bank
def load_dna_bank():
    """Load emotional lexicon with fallback to default"""
    DEFAULT_LEX = {
        "grief": ["loss", "gone", "ache", "empty", "funeral", "death"],
        "relapse": ["again", "failed", "weak", "zero", "control", "repeat"],
        "disconnection": ["numb", "void", "autopilot", "floating", "robot", "empty"],
        "shame": ["ashamed", "disgust", "embarrass", "humiliate", "worthless"],
        "collapse": ["broken", "finished", "collapse", "overwhelmed", "drowning"],
        "rage": ["furious", "anger", "explode", "rage", "seething", "fuming"],
        "healing": ["progress", "step", "forward", "growing", "stronger"]
    }

    DNA_PATH = os.path.join(PROJECT_ROOT, "content", "dna_bank.json")
    try:
        if os.path.exists(DNA_PATH):
            with open(DNA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            logger.warning("dna_bank.json not found. Using default lexicon")
            return DEFAULT_LEX
    except Exception as e:
        logger.error(f"DNA bank load failed: {str(e)}")
        return DEFAULT_LEX

EMOTION_LEXICON = load_dna_bank()

# 🔍 Core detection function
def detect_tag(entry: str) -> tuple:
    """Detect primary emotional tag and severity (1-3). Returns: (tag, severity)"""
    if not entry.strip():
        return "empty", 0

    entry = entry.lower()
    tags_detected = []

    # 🧠 Phase 1: Regex pattern matching
    for tag, patterns in COMPILED_PATTERNS.items():
        if any(p.search(entry) for p in patterns):
            tags_detected.append(tag)
            logger.debug(f"Regex match: {tag} | {entry[:30]}...")

    # 📚 Phase 2: Lexical analysis
    words = re.findall(r'\b\w+\b', entry)
    for word in words:
        for tag, keywords in EMOTION_LEXICON.items():
            if word in keywords:
                tags_detected.append(tag)
                logger.debug(f"Lexical match: {tag} | {word}")

    # ⚖️ Phase 3: Determine primary tag & severity
    if tags_detected:
        counter = Counter(tags_detected)
        top_tag, freq = counter.most_common(1)[0]
        severity = min(3, max(1, freq))
        logger.info(f"Detected: {top_tag} (severity {severity})")
        return top_tag, severity

    logger.info("No emotional tags detected")
    return "unknown", 1

# 🧪 Test harness
if __name__ == "__main__":
    test_entries = [
        ("I lost my father yesterday", "grief", 3),
        ("Relapsed again after 3 days clean", "relapse", 2),
        ("Feeling completely numb and disconnected", "disconnection", 3),
        ("I'm so ashamed of my actions", "shame", 2),
        ("Can't control my rage today", "rage", 3),
        ("Making small steps forward", "healing", 1)
    ]

    print("🚀 Running Emotional Tag Detector Tests:")
    for entry, expected_tag, expected_sev in test_entries:
        tag, sev = detect_tag(entry)
        status = "✅" if tag == expected_tag and sev == expected_sev else "❌"
        print(f"{status} {entry[:30]:<35} | Got: {tag}({sev}) | Expected: {expected_tag}({expected_sev})")