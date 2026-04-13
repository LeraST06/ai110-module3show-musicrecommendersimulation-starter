# Model Card: Music Recommender Simulation

## 1. Model Name

VibeMatch 1.0

---

## 2. Intended Use

Suggests songs from a small catalog based on a user's stated genre, mood, energy, and acoustic preference. Built for classroom exploration only, not real-world use.

---

## 3. How the Model Works

Each song is scored by checking how well it matches the user's profile. Genre and mood matches give fixed point bonuses. Energy closeness is a sliding scale. If the user likes acoustic music, songs with higher acousticness get a small bonus. All songs are ranked by score and the top results are returned.

---

## 4. Data

18 songs across 11 genres (pop, lofi, rock, jazz, classical, metal, hip-hop, r&b, folk, reggae, electronic) and moods ranging from happy to sad. 8 songs were added to the original 10 to improve variety. The catalog is still small and does not include lyrics, language, or listening context.

---

## 5. Strengths

Works well when the user's preferences are consistent and the catalog has multiple songs in their genre. The Chill Lofi profile was the best example, returning highly relevant results across all four scoring features.

---

## 6. Limitations and Bias

Genre carries the most weight, which can backfire. A user who wanted high-energy classical music got a slow, quiet piano piece as the top result simply because it was the only classical song available. The system also never recommends outside the user's stated genre, creating a filter bubble. Most genres have only one song, so niche users run out of real matches quickly.

---

## 7. Evaluation

Five profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases. Chill Lofi worked best. The biggest surprise was Gym Hero appearing in the pop/happy list despite having an "intense" mood, because its genre and energy score were high enough to compensate. The classical edge case showed the genre weight can completely override the rest of the profile.

---

## 8. Future Work

- Expand the catalog so every genre has at least 3 songs.
- Add a diversity rule so the same genre cannot dominate the top 5.
- Let users set a minimum energy threshold to filter out songs that are too far off.

---

## 9. Personal Reflection

The biggest moment was seeing how changing one weight flipped the entire ranking. I did not expect such a small number to matter that much. AI tools helped speed things up, but I had to check the scoring logic myself because the suggestions did not always match what I actually wanted. The strangest part was that the results felt like real recommendations even though the system is literally just adding four numbers together. Next I would add a rule to prevent the same genre from showing up more than twice in a row, because right now it can just stack the same type of song and call it variety.
