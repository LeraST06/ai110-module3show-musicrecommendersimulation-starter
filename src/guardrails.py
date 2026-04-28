from typing import Dict, List


def validate_user_prefs(prefs: Dict) -> None:
    """Raise ValueError if a user preference dictionary is invalid."""
    genre = prefs.get("genre", "")
    if not isinstance(genre, str) or not genre.strip():
        raise ValueError("User preference 'genre' must be a non-empty string.")

    mood = prefs.get("mood", "")
    if not isinstance(mood, str) or not mood.strip():
        raise ValueError("User preference 'mood' must be a non-empty string.")

    energy = prefs.get("energy")
    if energy is None:
        raise ValueError("User preference 'energy' is required.")
    if not isinstance(energy, (int, float)) or not (0.0 <= float(energy) <= 1.0):
        raise ValueError(
            f"User preference 'energy' must be a float between 0.0 and 1.0, got {energy!r}."
        )

    likes_acoustic = prefs.get("likes_acoustic")
    if likes_acoustic is None:
        raise ValueError("User preference 'likes_acoustic' is required.")
    if not isinstance(likes_acoustic, bool):
        raise ValueError(
            f"User preference 'likes_acoustic' must be a bool, got {likes_acoustic!r}."
        )


def validate_songs(songs: List) -> None:
    """Raise ValueError if the song catalog is empty."""
    if not songs:
        raise ValueError(
            "Song catalog is empty. Make sure data/songs.csv exists and contains songs."
        )


def validate_k(k: int) -> None:
    """Raise ValueError if k is not a positive integer."""
    if not isinstance(k, int) or k < 1:
        raise ValueError(f"k must be a positive integer, got {k!r}.")
