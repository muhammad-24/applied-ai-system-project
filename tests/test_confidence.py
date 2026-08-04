from src.confidence import (score_to_confidence, confidence_label,
                            annotate_recommendations)


def test_score_to_confidence_normalizes():
    assert score_to_confidence(4.0) == 1.0
    assert score_to_confidence(0.0) == 0.0
    assert score_to_confidence(2.0) == 0.5


def test_score_to_confidence_clamps_out_of_range():
    assert score_to_confidence(10.0) == 1.0
    assert score_to_confidence(-5.0) == 0.0


def test_confidence_labels():
    assert confidence_label(0.9) == "high"
    assert confidence_label(0.5) == "medium"
    assert confidence_label(0.1) == "low"


def test_annotate_flags_low_confidence():
    ranked = [({"title": "Weak"}, 0.5, ["energy closeness (+0.50)"])]
    annotated = annotate_recommendations(ranked)
    assert annotated[0]["reliable"] is False
    assert annotated[0]["confidence_label"] == "low"