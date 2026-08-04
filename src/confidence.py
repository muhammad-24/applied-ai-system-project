"""Confidence scoring for recommendations.

Converts a raw recommender score into a normalized 0-1 confidence value
and a label. This lets the system flag weak matches instead of presenting
a low-quality recommendation as if it were a strong one.
"""

from typing import Dict, List, Tuple

# Maximum score the dict-based scorer can produce:
#   genre match (2.0) + mood match (1.0) + energy closeness (1.0) = 4.0
MAX_SCORE = 4.0

# Below this confidence, a recommendation is considered unreliable.
LOW_CONFIDENCE_THRESHOLD = 0.35


def score_to_confidence(score: float, max_score: float = MAX_SCORE) -> float:
    """Normalize a raw score to a 0.0-1.0 confidence value."""
    if max_score <= 0:
        return 0.0
    confidence = score / max_score
    # Clamp to [0, 1] so out-of-range scores can't break the label logic.
    return max(0.0, min(1.0, confidence))


def confidence_label(confidence: float) -> str:
    """Map a confidence value to a human-readable label."""
    if confidence >= 0.7:
        return "high"
    if confidence >= LOW_CONFIDENCE_THRESHOLD:
        return "medium"
    return "low"


def annotate_recommendations(
    ranked: List[Tuple[Dict, float, List[str]]]
) -> List[Dict]:
    """Attach confidence value, label, and a reliability flag to each rec.

    Returns a list of dicts so the main app can act on confidence
    (e.g. warn the user) rather than only display the raw score.
    """
    annotated = []
    for song, score, reasons in ranked:
        conf = score_to_confidence(score)
        label = confidence_label(conf)
        annotated.append({
            "song": song,
            "score": score,
            "reasons": reasons,
            "confidence": conf,
            "confidence_label": label,
            "reliable": label != "low",
        })
    return annotated