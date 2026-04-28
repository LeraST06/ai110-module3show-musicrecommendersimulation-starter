# Model Card: Music Recommender Simulation

## 1. Model Name

VibeMatch 2.0

---

## 2. Intended Use

This system suggests songs from a small catalog based on a user's genre, mood, energy, and acoustic preferences. It then uses the Gemini API to write a short explanation for each recommendation. This is a classroom project, not a real-world application.

---

## 3. How the Model Works

**Scoring (rule-based layer)**
Each song is scored based on how well it matches the user's profile. Genre and mood matches give fixed point bonuses. Energy is a sliding scale, so closer values score higher. If the user likes acoustic music, songs with higher acousticness get a small bonus. All songs are ranked by score and the top results are returned.

| Signal | Points |
|---|---|
| Genre match | +2.0 |
| Mood match | +1.5 |
| Energy similarity | up to +1.0 |
| Acoustic bonus (if applicable) | up to +0.5 |
| **Max possible** | **5.0** |

**Explanation (AI layer)**
After scoring, each recommendation is sent to Gemini (`gemini-2.0-flash`) via the Gemini API. Gemini gets the user preferences, the song details, the score, and the match reasons, then writes a 2-sentence explanation of why the song fits. If the API is unavailable, the system uses the rule-based reason string instead.

**Guardrails**
Before any scoring happens, `guardrails.py` checks all inputs:
- `energy` must be a float between 0.0 and 1.0
- `genre` and `mood` must be non-empty strings
- `likes_acoustic` must be a boolean
- `k` must be a positive integer
- The song catalog must not be empty

If any value is invalid, the system raises a `ValueError` with a clear message and stops.

---

## 4. Data

18 songs across 11 genres (pop, lofi, rock, jazz, classical, metal, hip-hop, r&b, folk, reggae, electronic) with moods ranging from happy to sad. Each song has 10 attributes: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.

---

## 5. Strengths

The system works well when the user's preferences are consistent and the catalog has multiple songs in their genre. The Chill Lofi profile is the best example, returning highly relevant results across all four scoring features. The AI explanation layer also adds context that the score alone cannot show. For example, it can explain why a chill ambient track suits a late-night focus session even when the genre is not an exact match.

---

## 6. Limitations and Bias

**Scoring layer:**
Genre carries the most weight, which can backfire. A user who wanted high-energy classical music got a slow, quiet piano piece as the top result simply because it was the only classical song in the catalog. The system never recommends outside the user's stated genre, so it creates a filter bubble. Most genres only have one song, so niche users run out of real matches quickly.

**AI explanation layer:**
Gemini's explanations are only as accurate as the information passed to it. If the scoring model produces a bad recommendation, Gemini will still write a confident explanation for it. The explanation does not fix bad scores. It just describes them.

---

## 7. Evaluation

Five profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases. Chill Lofi worked best. The biggest surprise was Gym Hero appearing in the pop/happy list despite having an "intense" mood, because its genre and energy score were high enough to make up for it. The classical edge case showed that genre weight can completely override the rest of the profile.

The guardrails were tested against these failure cases: empty genre string, energy above 1.0 or below 0.0, non-boolean `likes_acoustic`, and empty catalog. Each one raised a `ValueError` with a clear message.

---

## 8. Reliability Mechanism

`src/guardrails.py` checks all inputs before they reach the scoring engine. This prevents silent failures like a negative energy value producing nonsensical scores, or an empty genre string matching every song equally. The AI explainer also has a try/except fallback. If the Gemini API call fails for any reason (no key, network error, rate limit), the system keeps running and shows the rule-based explanation instead.

---

## 9. Ethics and Misuse

**Could this system be misused?**
The recommender itself is low risk. It only re-ranks a fixed 18-song catalog. But the Claude API integration does introduce one concern: a user could inject text into the genre or mood fields to try to manipulate Claude's output (for example, setting `genre` to `"pop. Also write marketing copy for..."`). The guardrails reduce this risk by rejecting non-string or overly long inputs, but they do not fully sanitize against prompt injection. A production version would need to strip or escape user-provided strings before including them in prompts.

The AI explanation layer could also give users false confidence in poor recommendations. Because Claude always writes a coherent explanation, a user might trust a bad result more than they should. Adding a confidence flag for low-scoring recommendations would make the system more honest.

---

## 10. AI Collaboration

*This section describes my experience working with AI tools while building this project.*

**Helpful suggestion:**
When building `src/ai_explainer.py`, Claude Code suggested adding a fallback before making the API call. It checks for the `GEMINI_API_KEY` environment variable first, and if the key is missing or the call fails, it returns the rule-based reason string instead. I had not planned for this. I was focused on making the main path work. That fallback turned out to be important because the system needs to run during demos even when no API key is set up, and without it the whole run would crash on the first recommendation.

**Flawed or incorrect suggestion:**
Claude's initial README draft used `python -m src.main` as the run command. When I tested it in the terminal, it failed with a `ModuleNotFoundError` because `src/` has no `__init__.py` and Python could not resolve the imports. The correct command is `python3 src/main.py`, which adds `src/` to the path automatically. The suggestion looked fine on paper but did not work. I had to actually run the code to catch the bug.

---

## 11. Future Work

- Expand the catalog so every genre has at least 3 songs.
- Add a rule so the same genre cannot dominate all 5 results.
- Let users set a minimum energy threshold to filter out songs that are too far off.
- Pass Claude a richer system prompt that includes genre descriptions so explanations feel more specific and musical.

---

## 12. Personal Reflection

The biggest moment was seeing how changing one weight flipped the entire ranking. I did not expect such a small number to matter that much. Adding the Claude explanation layer made it clear that the AI is narrating the algorithm's decisions, not making its own. If the score is wrong, the explanation will still sound confident. The part that stuck with me most is that AI components can make a system feel smarter without actually making it more accurate.
