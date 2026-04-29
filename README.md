# VibeMatch 2.0 — Music Recommender Simulation

## Video Walkthrough

**Demo video:** [CodepathFinalProject.mp4](CodepathFinalProject.mp4)

---

## Base Project

This project extends **Project 3: Music Recommender Simulation** (Module 3 of AI110). The original project was a rule-based content-based filtering system. It scored songs against a user's stated genre, mood, energy, and acoustic preferences and returned the top matches with a plain-language score breakdown. It ran entirely on weighted math with no external AI model. VibeMatch 2.0 builds on that by adding a Claude API explanation layer, input guardrails, and a cleaner file structure with dedicated modules.

---

## Project Summary

VibeMatch 2.0 is a music recommendation system that pairs a simple scoring engine with a Claude-powered explanation layer. Given a user's preferences, it scores all 18 songs in the catalog, ranks them, and asks Claude Haiku to write a short explanation for each result. Guardrails check all inputs before scoring starts. If the Claude API is unavailable, the system falls back to the rule-based reason string automatically.

---

## How The System Works

Real platforms like Spotify use collaborative filtering (based on what similar users listened to) and content-based filtering (based on song attributes). This simulation uses content-based filtering only.

**Scoring algorithm:**
| Signal | Points |
|---|---|
| Genre match | +2.0 |
| Mood match | +1.5 |
| Energy similarity | up to +1.0 |
| Acoustic bonus (if applicable) | up to +0.5 |
| **Max possible** | **5.0** |

**AI Explanation layer:**
After scoring, each recommendation is sent to Gemini (`gemma-3-27b-it`) via the Gemini API. It writes a 2-sentence conversational explanation for why the song fits. If no API key is set or the call fails, the system keeps running and shows the rule-based reason instead.

**Guardrails:**
Before scoring runs, `src/guardrails.py` checks all user inputs. Energy must be between 0.0 and 1.0, genre and mood must be non-empty strings, and `likes_acoustic` must be a boolean. If anything is invalid, a `ValueError` is raised with a clear message.

**Potential biases:** Genre carries the most weight (+2.0), so a same-genre song with the wrong mood can outscore a better mood match from a different genre. This creates a filter bubble. The AI explanation layer describes whatever the scorer decided. It cannot fix a bad recommendation.

---

## Getting Started

### Setup

1. Clone the repository and create a virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Gemini API key:

   ```bash
   cp .env.example .env
   ```

   Open `.env` and replace `your-api-key-here` with your actual key:

   ```
   GEMINI_API_KEY=your-key-here
   ```

   > If you skip this step, the system will still run. AI explanations will fall back to rule-based reasons automatically.

4. Run the recommender:

   ```bash
   python3 src/main.py
   ```

### Running Tests

```bash
pytest
```

---

## Sample Interactions

Below are three example profile runs showing the system end-to-end. The `AI` lines are Claude-generated when an API key is set.

**Example 1 — Chill Lofi**
```
Input: genre=lofi, mood=chill, energy=0.35, likes_acoustic=True

#1  Library Rain by Paper Lanterns
    Score : 4.93 / 5.0
    Why   : genre match (+2.0), mood match (+1.5), energy similarity (+1.00), acoustic bonus (+0.43)
    AI    : Library Rain is a near-perfect match for your preferences. It shares
            your lofi genre and chill mood, and the slow acoustic texture makes it
            great for quiet focus sessions.

#2  Midnight Coding by LoRoom
    Score : 4.79 / 5.0
    Why   : genre match (+2.0), mood match (+1.5), energy similarity (+0.93), acoustic bonus (+0.35)
    AI    : This track fits your lofi and chill preferences closely. The soft
            acoustic warmth works well for late-night listening at low volume.
```

**Example 2 — High-Energy Pop**
```
Input: genre=pop, mood=happy, energy=0.9, likes_acoustic=False

#1  Sunrise City by Neon Echo
    Score : 4.42 / 5.0
    Why   : genre match (+2.0), mood match (+1.5), energy similarity (+0.92)
    AI    : Sunrise City matches your pop and happy preferences well. It is
            upbeat and high-energy, which lines up with what you are looking for.
```

**Example 3 — Guardrail triggered**
```
Input: genre="", mood=happy, energy=0.9, likes_acoustic=False

ValueError: User preference 'genre' must be a non-empty string.
```

---

## System Architecture

See [assets/architecture.md](assets/architecture.md) for the full Mermaid.js diagram.

```
User Input -> Guardrails -> Recommender (score_song) -> Claude AI Explainer -> CLI Output
                                                                 |
                                                       Human Review / Testing
```

| File | Role |
|---|---|
| `src/main.py` | CLI entry point |
| `src/recommender.py` | Rule-based scoring engine |
| `src/guardrails.py` | Input validation and safety checks |
| `src/ai_explainer.py` | Gemini API integration for explanations |
| `data/songs.csv` | 18-song catalog |

---

## Design Decisions

**Why Gemini Flash for explanations?**
Gemini 2.0 Flash is fast and cheap. That matters here because the system makes one API call per recommendation, which adds up to 25 calls across five profiles. Writing 2 sentences about a song match does not need a large model. Speed and cost were the main reasons.

**Why rule-based scoring instead of an LLM?**
The scoring engine is transparent and testable. You can verify exactly why a song ranked where it did. An LLM making ranking decisions would be harder to debug and harder to trust. The design keeps AI in the explanation layer where fluency matters, and keeps the scoring logic deterministic where correctness matters.

**Why guardrails before scoring, not after?**
Checking inputs at the start prevents the scoring function from ever receiving nonsensical values like `energy=-5` and quietly producing wrong results. It is easier to catch a bad input early than to diagnose a weird score later.

**Trade-off: no catalog expansion**
The catalog stays at 18 songs to keep the project self-contained. A larger catalog would reduce the filter-bubble problem, but curating more data was out of scope for this project.

---

## Testing Summary

The existing pytest suite (2 tests) was kept and passes cleanly. Tests check that `recommend()` returns songs sorted by score and that `explain_recommendation()` returns a non-empty string.

Guardrail testing was done manually against these failure cases:
- Empty genre string → `ValueError` raised correctly
- Energy of `1.5` → `ValueError` raised correctly
- `likes_acoustic="yes"` (string instead of bool) → `ValueError` raised correctly
- Empty song catalog → `ValueError` raised correctly

The AI explanation fallback was tested by running without an `ANTHROPIC_API_KEY`. The system continued and displayed rule-based reasons on every line with no crash.

One unexpected finding: the guardrail for `likes_acoustic` would have missed `None` values if the key was just absent from the dict. This was fixed by checking `if likes_acoustic is None` before the type check.

---

## Limitations and Risks

- Genre carries the most weight, which can push irrelevant songs to the top if only one song in that genre exists.
- The system never recommends outside the user's stated genre, creating a filter bubble.
- With only 18 songs, niche-genre users run out of real matches quickly and get filler results.
- No context signals like time of day, activity, or listening history are considered.
- The AI explanation layer describes the algorithm's output. It cannot correct a bad recommendation.

See [model_card.md](model_card.md) for a full breakdown.

---

## Reflection

Recommenders turn data into predictions by reducing taste to numbers and comparing them against a catalog. The tricky part is deciding which numbers matter most. Changing a single weight shifted the entire output, which shows how much human judgment goes into something that feels automatic. Adding the Claude explanation layer made it clear that an LLM can sound confident about a recommendation the underlying model got wrong. The explanation is only as good as the score it is describing. The biggest lesson from this project is that AI components can make a system feel smarter without actually making it more accurate.
