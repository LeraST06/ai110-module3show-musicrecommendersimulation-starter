# VibeMatch 2.0 — System Architecture

```mermaid
flowchart TD
    A["User Input\ngenre · mood · energy · likes_acoustic"] --> B["Guardrails\nsrc/guardrails.py\nvalidate_user_prefs · validate_songs · validate_k"]

    B -->|invalid input| ERR["ValueError\nwith clear message"]
    B -->|valid input| C["Song Catalog\ndata/songs.csv\n18 songs · 10 attributes"]

    C --> D["Recommender\nsrc/recommender.py\nscore_song · recommend_songs"]
    D --> E["Top-K Songs\nranked by score\nmax 5.0 pts each"]

    E --> F["AI Explainer\nsrc/ai_explainer.py\ngenerate_explanation"]
    F -->|GEMINI_API_KEY set| G["Gemini API\ngemini-1.5-flash"]
    F -->|no API key| H["Rule-Based Fallback\nreturns score_reasons string"]

    G --> I["Natural Language\nExplanation\n2 sentences"]
    H --> I

    E --> J["CLI Output\nsrc/main.py\nScore · Why · AI label"]
    I --> J

    J --> K["Human Review\nUser reads output\nand evaluates relevance"]
    J --> L["Automated Tests\npytest\ntest_recommender.py"]

    K -->|feedback| A
    L -->|pass / fail| M["Test Results\nall 2 tests passed"]
```

## Component Summary

| File | Role |
|---|---|
| `src/main.py` | CLI entry point, loads data, runs profiles, prints output |
| `src/recommender.py` | Core scoring algorithm, `score_song` and `recommend_songs` |
| `src/guardrails.py` | Input validation, rejects malformed preferences before scoring |
| `src/ai_explainer.py` | Claude integration, converts scores into conversational explanations |
| `data/songs.csv` | Static song catalog, 18 songs across 11 genres |
| `.env` | Holds `GEMINI_API_KEY` (not committed to git) |

## Data Flow

1. `main.py` calls `load_songs("data/songs.csv")` and validates the catalog with `validate_songs`.
2. For each user profile, `validate_user_prefs` runs before scoring begins.
3. `recommend_songs` scores every song using `score_song` (genre, mood, energy, acoustic weights) and returns the top-k sorted results.
4. For each result, `generate_explanation` sends a short prompt to Claude Haiku and gets back a 2-sentence explanation. If the API is unavailable, it falls back to the rule-based reason string.
5. `main.py` prints the score, rule-based reasons, and AI explanation side by side.
6. The user reads the output and checks whether the recommendations make sense. This is the human review step.
7. `pytest` runs the automated test suite separately to verify the core scoring logic and explanation output.
