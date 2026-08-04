"""Input validation and guardrails for the recommender.

Catches bad user profiles and empty datasets before they reach the
scoring logic, so the system fails with a clear message instead of
crashing or silently returning nonsense.
"""

from typing import Dict, List


class ValidationError(ValueError):
    """Raised when a user profile or dataset fails validation."""


def validate_songs(songs: List[Dict]) -> None:
    """Ensure the song dataset is present and non-empty."""
    if not songs:
        raise ValidationError("Song dataset is empty - nothing to recommend.")


def validate_user_prefs(user_prefs: Dict, songs: List[Dict]) -> List[str]:
    """Validate a dict-based user profile against the dataset.

    Raises ValidationError on hard failures (missing keys, out-of-range
    energy). Returns a list of soft warnings (e.g. a genre that exists in
    no song) so the caller can log them without crashing.
    """
    warnings: List[str] = []

    required = {"genre", "mood", "energy"}
    missing = required - user_prefs.keys()
    if missing:
        raise ValidationError(f"User profile missing keys: {sorted(missing)}")

    energy = user_prefs["energy"]
    if not isinstance(energy, (int, float)):
        raise ValidationError("energy must be a number.")
    if not 0.0 <= energy <= 1.0:
        raise ValidationError(f"energy must be between 0.0 and 1.0 (got {energy}).")

    known_genres = {s["genre"] for s in songs}
    if user_prefs["genre"] not in known_genres:
        warnings.append(
            f"genre '{user_prefs['genre']}' matches no song in the dataset; "
            f"recommendations will rely on mood and energy only."
        )

    known_moods = {s["mood"] for s in songs}
    if user_prefs["mood"] not in known_moods:
        warnings.append(
            f"mood '{user_prefs['mood']}' matches no song in the dataset."
        )

    return warnings