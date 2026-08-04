"""Command-line runner for the Music Recommender + Reliability layer.

Flow: validate input (guardrails) -> recommend -> score confidence ->
log the run -> display results, warning on low-confidence matches.
"""

from src.recommender import load_songs, recommend_songs
from src.confidence import annotate_recommendations
from src.guardrails import validate_songs, validate_user_prefs, ValidationError
from src.logging_utils import get_logger

logger = get_logger()


def run(user_prefs, songs, k=5):
    """Run one recommendation request through the full reliability pipeline."""
    validate_songs(songs)
    warnings = validate_user_prefs(user_prefs, songs)
    for w in warnings:
        logger.warning("input warning: %s", w)

    ranked = recommend_songs(user_prefs, songs, k=k)
    annotated = annotate_recommendations(ranked)

    logger.info(
        "request genre=%s mood=%s energy=%s -> %d recs (top confidence=%.2f)",
        user_prefs["genre"], user_prefs["mood"], user_prefs["energy"],
        len(annotated), annotated[0]["confidence"] if annotated else 0.0,
    )
    return annotated, warnings


def display(annotated, warnings):
    """Print recommendations with confidence and low-confidence warnings."""
    if warnings:
        print("\n[!] Input warnings:")
        for w in warnings:
            print(f"    - {w}")

    print("\nTop recommendations:\n")
    for item in annotated:
        song = item["song"]
        flag = "" if item["reliable"] else "  [LOW CONFIDENCE - weak match]"
        print(f"{song['title']} - Score: {item['score']:.2f} "
              f"| Confidence: {item['confidence']:.2f} "
              f"({item['confidence_label']}){flag}")
        print(f"  Because: {item['reasons']}")
        print()


def main():
    songs = load_songs("data/songs.csv")
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    try:
        annotated, warnings = run(user_prefs, songs, k=5)
        display(annotated, warnings)
    except ValidationError as e:
        logger.error("validation failed: %s", e)
        print(f"\n[ERROR] Could not generate recommendations: {e}")


if __name__ == "__main__":
    main()