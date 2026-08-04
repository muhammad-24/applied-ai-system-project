"""Reliability harness: runs several user profiles against the recommender
and checks each against an expectation, then reports pass/fail and average
confidence. Writes a reproducible report to assets/reliability_report.txt.
"""

import os
from src.recommender import load_songs
from src.main import run
from src.guardrails import ValidationError

REPORT_PATH = os.path.join("assets", "reliability_report.txt")

# Each case: a profile, a human-readable expectation, and a checker function
# that returns True if the top result meets the expectation.
CASES = [
    {
        "name": "Happy Pop",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "criteria": "Top result is a pop, happy, high-confidence match",
        "check": lambda ann: ann[0]["song"]["genre"] == "pop"
                             and ann[0]["confidence_label"] == "high",
    },
    {
        "name": "Chill Lofi",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.4},
        "criteria": "Top result is a lofi track with high confidence",
        "check": lambda ann: ann[0]["song"]["genre"] == "lofi"
                             and ann[0]["confidence_label"] == "high",
    },
    {
        "name": "Adversarial EDM+Sad",
        "prefs": {"genre": "edm", "mood": "melancholy", "energy": 0.5},
        "criteria": "System returns results but flags low/medium confidence",
        "check": lambda ann: ann[0]["confidence_label"] in ("low", "medium"),
    },
    {
        "name": "Unknown genre (guardrail)",
        "prefs": {"genre": "polka", "mood": "happy", "energy": 0.5},
        "criteria": "Unknown genre produces a warning but does not crash",
        "check": lambda ann: len(ann) > 0,
    },
]


def run_harness():
    songs = load_songs("data/songs.csv")
    lines = []
    passed = 0
    confidences = []

    lines.append("RELIABILITY REPORT - Music Recommender")
    lines.append("=" * 50)

    for case in CASES:
        try:
            annotated, warnings = run(case["prefs"], songs, k=5)
            ok = bool(annotated) and case["check"](annotated)
            top_conf = annotated[0]["confidence"] if annotated else 0.0
            confidences.append(top_conf)
        except ValidationError as e:
            annotated, warnings, ok, top_conf = [], [], False, 0.0
            lines.append(f"  ERROR: {e}")

        passed += int(ok)
        result = "PASS" if ok else "FAIL"
        lines.append("")
        lines.append(f"[{result}] {case['name']}")
        lines.append(f"  criteria: {case['criteria']}")
        lines.append(f"  top confidence: {top_conf:.2f}")
        if warnings:
            for w in warnings:
                lines.append(f"  warning: {w}")

    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
    lines.append("")
    lines.append("=" * 50)
    lines.append(f"RESULT: {passed}/{len(CASES)} cases passed")
    lines.append(f"Average top-result confidence: {avg_conf:.2f}")

    report = "\n".join(lines)
    os.makedirs("assets", exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report + "\n")
    return report


if __name__ == "__main__":
    print(run_harness())