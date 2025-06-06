# Under BACKEND/core/pulse_affinity.py (Final Lightborn Edition)
# Emotional Distance Matrix for Ghost Journal
# Provides tone similarity scores and lookup helpers

PULSE_AFFINITY = {
    "THROBBING": {
        "THROBBING": 1.0, "FRACTURED": 0.85, "PRESSED": 0.8, "ECHOING": 0.75,
        "STILL": 0.4, "UNKNOWN": 0.3, "ABSURD": 0.1
    },
    "FRACTURED": {
        "FRACTURED": 1.0, "THROBBING": 0.85, "PRESSED": 0.7, "ECHOING": 0.65,
        "STILL": 0.4, "UNKNOWN": 0.3, "ABSURD": 0.15
    },
    "PRESSED": {
        "PRESSED": 1.0, "THROBBING": 0.8, "FRACTURED": 0.7, "ECHOING": 0.6,
        "STILL": 0.5, "UNKNOWN": 0.3, "ABSURD": 0.05
    },
    "ECHOING": {
        "ECHOING": 1.0, "FRACTURED": 0.65, "PRESSED": 0.6, "THROBBING": 0.5,
        "STILL": 0.6, "UNKNOWN": 0.5, "ABSURD": 0.2
    },
    "STILL": {
        "STILL": 1.0, "ECHOING": 0.6, "PRESSED": 0.5, "UNKNOWN": 0.4,
        "FRACTURED": 0.4, "THROBBING": 0.4, "ABSURD": 0.1
    },
    "ABSURD": {
        "ABSURD": 1.0, "UNKNOWN": 0.4, "ECHOING": 0.2, "STILL": 0.1,
        "FRACTURED": 0.15, "PRESSED": 0.05, "THROBBING": 0.1
    },
    "UNKNOWN": {
        "UNKNOWN": 1.0, "STILL": 0.4, "ECHOING": 0.5, "FRACTURED": 0.3,
        "THROBBING": 0.3, "PRESSED": 0.3, "ABSURD": 0.4
    }
}

# Check if two pulses are emotionally similar

def emotionally_similar(source: str, target: str, threshold: float = 0.7) -> bool:
    return PULSE_AFFINITY.get(source, {}).get(target, 0.0) >= threshold

# Get closest related tones above threshold

def get_closest_related(pulse: str, threshold: float = 0.6) -> list:
    return [p for p, score in PULSE_AFFINITY.get(pulse, {}).items()
            if score >= threshold and p != pulse]

# Merge multiple pulses into ranked affinity list

def merge_affinities(pulse_list: list, top_n: int = 3) -> list:
    scores = {}
    for pulse in pulse_list:
        for target, val in PULSE_AFFINITY.get(pulse, {}).items():
            if target not in pulse_list:
                scores[target] = scores.get(target, 0) + val
    return sorted(scores.items(), key=lambda x: -x[1])[:top_n]

# 🧪 Local test
if __name__ == "__main__":
    print("Merged Related Pulses:", merge_affinities(["THROBBING", "FRACTURED"]))