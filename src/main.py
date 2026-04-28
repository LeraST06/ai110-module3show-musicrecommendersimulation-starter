"""
Command line runner for the Music Recommender Simulation (VibeMatch 2.0).

Run from the project root:
    python3 src/main.py
"""

from recommender import load_songs, recommend_songs
from guardrails import validate_user_prefs, validate_songs, validate_k
from ai_explainer import generate_explanation


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5, use_ai: bool = False) -> None:
    """Print a labeled recommendation block with an optional AI-generated explanation for the top result."""
    validate_user_prefs(user_prefs)
    validate_k(k)

    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * 50)
    print(f"  {label}")
    prefs_summary = " | ".join(f"{key}: {val}" for key, val in user_prefs.items())
    print(f"  {prefs_summary}")
    print("=" * 50)

    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 5.0")
        print(f"    Why   : {explanation}")
        if i == 1 and use_ai:
            ai_note = generate_explanation(user_prefs, song, score, explanation)
            print(f"    AI    : {ai_note}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    validate_songs(songs)

    profiles = [
        (
            "High-Energy Pop",
            {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
        ),
        (
            "Chill Lofi",
            {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
        ),
        (
            "Deep Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.95, "likes_acoustic": False},
        ),
        (
            "Edge Case: Classical Fan Wanting High Energy",
            {"genre": "classical", "mood": "energetic", "energy": 0.9, "likes_acoustic": True},
        ),
        (
            "Edge Case: Conflicting Sad + High Energy",
            {"genre": "electronic", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
        ),
    ]

    for i, (label, user_prefs) in enumerate(profiles):
        print_recommendations(label, user_prefs, songs, use_ai=(i == 0))


if __name__ == "__main__":
    main()
