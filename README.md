Music Recommender + Reliability Layer
Base Project

This project extends my Module 3 Music Recommender Simulation. The original project was a content-based music recommender: it represented songs and a user "taste profile" as data, then used a weighted scoring rule (genre, mood, and energy closeness) to rank and recommend songs, with a short explanation for each pick. This final version keeps that core and adds an integrated reliability layer — confidence scoring, input guardrails, logging, and an automated reliability harness — so the system can tell how trustworthy each recommendation is and fail safely on bad input.

Summary

The system recommends songs from a dataset based on a user's genre, mood, and energy preferences. On top of the original scoring, every recommendation now receives a confidence score (0-1) and label (high/medium/low). Low-confidence matches are flagged rather than presented as strong picks, so a weak recommendation no longer looks like a good one. Bad input is caught by guardrails, and every run is logged for auditing.

Architecture Overview

See diagrams/architecture.mmd for the full diagram. Data flows as:

User profile input (genre, mood, energy)
Guardrails validate the profile (bad input raises a clear error; unknown genres/moods produce warnings instead of crashing)
Recommender scores every song in data/songs.csv and ranks them
Confidence layer normalizes each score to a 0-1 confidence and labels it
Display shows results and flags low-confidence matches

A logger records every run and warning to logs/recommender.log. A reliability harness runs several profiles and writes a pass/fail report to assets/reliability_report.txt, and a pytest suite verifies the recommender, confidence, and guardrail logic.

Setup
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
pip install -r requirements.txt

Run the recommender:

python -m src.main

Run the reliability harness:

python -m src.reliability_harness

Run the tests:

python -m pytest
Sample Interactions
Strong match (Happy Pop profile): Top recommendations: Sunrise City - Score: 3.98 | Confidence: 0.99 (high) Because: ['genre match (+2.0)', 'mood match (+1.0)', 'energy closeness (+0.98)'] Gym Hero - Score: 2.87 | Confidence: 0.72 (high) Because: ['genre match (+2.0)', 'energy closeness (+0.87)'] Night Drive Loop - Score: 0.95 | Confidence: 0.24 (low) [LOW CONFIDENCE - weak match] Because: ['energy closeness (+0.95)']
Guardrail warning (unknown genre "polka"): [!] Input warnings: - genre 'polka' matches no song in the dataset; recommendations will rely on mood and energy only. Top recommendations: ...
Reliability harness output: [PASS] Happy Pop top confidence: 0.99 [PASS] Chill Lofi top confidence: 0.99 [PASS] Adversarial EDM+Sad top confidence: 0.63 [PASS] Unknown genre (guardrail) top confidence: 0.45 RESULT: 4/4 cases passed Average top-result confidence: 0.77
Design Decisions
Confidence as normalized score. Confidence is the raw score divided by the maximum possible score (4.0), clamped to 0-1. This is simple and explainable, though it assumes the max is fixed; a learned calibration would be more accurate but far less transparent.
Warnings vs. errors. Hard problems (missing fields, out-of-range energy) raise errors; soft problems (a genre absent from the dataset) return warnings so the system still produces useful results. This favors graceful degradation over strictness.
Two scoring paths kept. The original dict-based functions and the OOP Recommender class both remain, so existing tests keep passing while the new layer builds on the dict path used by the CLI.
Testing Summary

11 of 11 automated tests pass, covering the recommender, confidence normalization and labeling, and all guardrail cases. The reliability harness passes 4/4 profiles (including an adversarial genre+mood mismatch and an unknown-genre guardrail test) with an average top-result confidence of 0.77. The main limitation surfaced by testing: confidence reflects only how well a song matches the stated profile, not whether the recommendation is genuinely good — a mismatched profile can still yield medium confidence from energy alone.

Reflection

The full responsible-AI reflection — how I collaborated with AI, one helpful and one flawed AI suggestion, and the system's limitations — is in model_card.md.