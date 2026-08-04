# Model Card — Music Recommender + Reliability Layer

## 1. Base Project
This extends my Module 3 Music Recommender Simulation, a content-based recommender
that scores songs by genre, mood, and energy closeness against a user taste profile.

## 2. Intended Use
Suggest songs from a fixed dataset based on a user's stated genre, mood, and energy
preferences, and communicate how confident the system is in each suggestion. It is a
simulation for learning, not a production recommender.

## 3. How the System Works
A user profile (genre, mood, energy) is validated by guardrails, scored against every
song, ranked, and each result is assigned a 0–1 confidence value and a high/medium/low
label. Low-confidence results are flagged. Every run is logged, and a reliability
harness plus a pytest suite verify behavior.

## 4. AI Collaboration
I used an AI assistant to design the reliability layer, scaffold the confidence,
guardrail, and logging modules, and draft the test suite and this model card. The most
useful prompts were specific and named the exact behavior I wanted (e.g. "normalize the
score to 0–1 and flag anything below a threshold as low confidence").

**One helpful AI suggestion:** Normalizing the raw score by the maximum possible score
(4.0) to produce confidence. This was simple, transparent, and easy to test — it made
the "flag weak matches" behavior possible without any complex modeling.

**One flawed AI suggestion I rejected/modified:** An early version treated any unknown
genre as a hard error that stopped the program. I changed this to a *warning* that still
returns results using mood and energy, because crashing on an out-of-catalog genre is
worse for the user than degrading gracefully. I verified the fix with a guardrail test.

## 5. Data
`data/songs.csv`, 16 songs with genre, mood, energy, tempo, valence, danceability, and
acousticness. It is small, hand-made, and not representative of real music catalogs.

## 6. Biases and Limitations
- **Filter-bubble bias:** the +2.0 genre weight strongly favors the user's stated genre,
  reinforcing existing taste and rarely surfacing new genres.
- **Popularity/coverage bias:** genres with more songs in the dataset have more chances
  to appear; sparse genres are under-recommended.
- **Confidence ≠ quality:** confidence measures match strength to the stated profile, not
  whether the song is actually a good recommendation. A weak profile can still yield
  medium confidence from energy closeness alone.
- **Tiny dataset:** 16 songs cannot generalize; results are illustrative only.

## 7. Testing and Reliability Results
11/11 automated tests pass (recommender, confidence, guardrails). The reliability harness
passes 4/4 profiles including an adversarial mismatch and an unknown-genre guardrail, with
an average top-result confidence of 0.77. See `assets/reliability_report.txt`.

## 8. Future Improvements
Add collaborative-filtering signals, calibrate confidence against human ratings, diversify
recommendations to counter filter bubbles, and expand the dataset substantially.

## 9. Responsible Use
This is an educational simulation. Its recommendations and confidence scores should not be
treated as authoritative, and its known biases (genre reinforcement, small data) should be
disclosed wherever results are shown.