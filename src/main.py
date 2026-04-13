"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a labeled recommendation block for a given user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print("\n" + "=" * 44)
    print(f"  {label}")
    prefs_summary = " | ".join(f"{k}: {v}" for k, v in user_prefs.items())
    print(f"  {prefs_summary}")
    print("=" * 44)
    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 5.0")
        print(f"    Why   : {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

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

    for label, user_prefs in profiles:
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()
