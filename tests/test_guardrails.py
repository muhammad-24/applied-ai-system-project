import pytest
from src.guardrails import (validate_songs, validate_user_prefs,
                            ValidationError)

SONGS = [
    {"genre": "pop", "mood": "happy", "energy": 0.8},
    {"genre": "lofi", "mood": "chill", "energy": 0.4},
]


def test_empty_dataset_raises():
    with pytest.raises(ValidationError):
        validate_songs([])


def test_missing_key_raises():
    with pytest.raises(ValidationError):
        validate_user_prefs({"genre": "pop"}, SONGS)


def test_out_of_range_energy_raises():
    with pytest.raises(ValidationError):
        validate_user_prefs({"genre": "pop", "mood": "happy", "energy": 5.0}, SONGS)


def test_unknown_genre_returns_warning_not_crash():
    warnings = validate_user_prefs(
        {"genre": "polka", "mood": "happy", "energy": 0.5}, SONGS)
    assert any("polka" in w for w in warnings)


def test_valid_profile_no_warnings():
    warnings = validate_user_prefs(
        {"genre": "pop", "mood": "happy", "energy": 0.8}, SONGS)
    assert warnings == []