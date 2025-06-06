import hashlib
import re
import os
from typing import List, Dict, Any, Set

# -----------------------------------------------
# ⚡️ Efficient Fallback Stemmer
# -----------------------------------------------
def basic_stem(word):
    for suffix in ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

# -----------------------------------------------
# 🧠 Smart Stemmer Toggle (NLTK optional)
# -----------------------------------------------
USE_NLTK = os.getenv("USE_NLTK_STEMMER", "0") == "1"

if USE_NLTK:
    try:
        from nltk.stem import PorterStemmer
        stemmer = PorterStemmer()

        def smart_stem(word):
            return stemmer.stem(word)
    except Exception:
        def smart_stem(word):
            return basic_stem(word)
else:
    def smart_stem(word):
        return basic_stem(word)

# -----------------------------------------------
# ❌ Lightweight Stopwords (Emotional clarity)
# -----------------------------------------------
STOPWORDS = {
    "the", "is", "and", "a", "an", "to", "in", "on", "at", "i", "you", "he", "she",
    "they", "it", "of", "for", "with", "this", "that", "was", "were", "are", "am",
    "be", "been", "being", "so", "just", "very", "really", "not", "no", "yes", "do", "does"
}

# -----------------------------------------------
# 🧽 Clean + Stem Entry
# -----------------------------------------------
def clean_and_stem(entry: str) -> List[str]:
    entry = re.sub(r"[^\w\s]", "", entry.lower())
    tokens = entry.split()
    return [smart_stem(word) for word in tokens if word not in STOPWORDS]

# -----------------------------------------------
# 🧠 Symbolic Cue Detection
# -----------------------------------------------
def detect_symbolic_cue(words: List[str]) -> str:
    joined = " ".join(words)

    if any(w in joined for w in ["float", "drift", "vanish", "empty", "fade"]):
        return "DRIFT"
    if any(joined.count(w) > 2 for w in set(words)):
        return "LOOP"
    if any(w in joined for w in ["scream", "explode", "punch", "kill", "snap", "rage", "shatter"]):
        return "SPIKE"
    if any(w in joined for w in ["again", "repeat", "echo", "same", "still"]):
        return "ECHO"
    if any(w in joined for w in ["okay", "fine", "happy", "smile", "normal", "nothing"]):
        return "MASK"
    if any(w in joined for w in ["nothing", "pointless", "meaningless", "empty", "void"]):
        return "VOID"

    return "NONE"

# -----------------------------------------------
# 🧬 Fingerprint Generator
# -----------------------------------------------
def generate_fingerprint(entry_text: str, tone: str, tag: str, user_id="anonymous") -> Dict[str, Any]:
    stemmed_words = clean_and_stem(entry_text)
    symbolic_cue = detect_symbolic_cue(stemmed_words)

    if not stemmed_words:
        stemmed_words = ["blank"]

    joined = "_".join(stemmed_words[:5]) or "EMPTY"
    raw_normalized = " ".join(stemmed_words)
    normalized_hash = hashlib.sha256(raw_normalized.encode("utf-8")).hexdigest()

    fingerprint_id = f"{joined}_TAG:{tag}_TONE:{tone}_CUE:{symbolic_cue}"

    return {
        "fingerprint": fingerprint_id,
        "normalized_hash": normalized_hash,
        "stemmed_words": stemmed_words,
        "tag": tag,
        "tone": tone,
        "symbolic": symbolic_cue,
        "user_id": user_id,
        "word_count": len(stemmed_words),
        "char_count": len(entry_text.strip()),
        "prev_fingerprint": None
    }

# ---------- Jaccard Similarity ----------
def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union else 0.0

# ---------- Fingerprint Diff ----------
def diff_fingerprints(fp1: Dict[str, Any], fp2: Dict[str, Any]) -> Dict[str, Any]:
    stem1 = set(fp1.get("stemmed_words", []))
    stem2 = set(fp2.get("stemmed_words", []))
    sim = jaccard_similarity(stem1, stem2)

    cue_match = fp1.get("symbolic") == fp2.get("symbolic")
    tone_shift = fp1.get("tone") != fp2.get("tone")
    tag_shift = fp1.get("tag") != fp2.get("tag")

    return {
        "similarity": round(sim, 3),
        "cue_match": cue_match,
        "tone_shift": tone_shift,
        "tag_shift": tag_shift,
        "anomaly_score": round((1 - sim) + int(tone_shift) + int(tag_shift), 3)
    }

# ---------- Emotional Drift ----------
def compute_emotional_drift(fp_old: Dict[str, Any], fp_new: Dict[str, Any]) -> Dict[str, Any]:
    drift = {
        "tone_changed": fp_old.get("tone") != fp_new.get("tone"),
        "symbolic_change": fp_old.get("symbolic") != fp_new.get("symbolic"),
        "jaccard_drop": 1 - jaccard_similarity(
            set(fp_old.get("stemmed_words", [])),
            set(fp_new.get("stemmed_words", []))
        )
    }
    drift["score"] = round(drift["jaccard_drop"] + int(drift["tone_changed"]) + int(drift["symbolic_change"]), 3)
    return drift

# ---------- Checksum Generation ----------
def fingerprint_checksum(fp: Dict[str, Any]) -> str:
    content = f"{fp.get('fingerprint')}" \
              f"{''.join(fp.get('stemmed_words', []))}" \
              f"{fp.get('tag')}" \
              f"{fp.get('tone')}" \
              f"{fp.get('symbolic')}"
    return hashlib.sha256(content.encode()).hexdigest()