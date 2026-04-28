import os
from dotenv import load_dotenv

load_dotenv()


def generate_explanation(user_prefs: dict, song: dict, score: float, score_reasons: str) -> str:
    """
    Call Gemini to produce a 2-sentence conversational explanation for why
    a song was recommended. Falls back to the rule-based reason string if
    the API key is missing or the call fails.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return f"Recommended because: {score_reasons}."

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        system_prompt = (
            "You are a music recommendation assistant. "
            "Write brief, specific, conversational explanations for why songs were recommended. "
            "Never mention scoring numbers."
        )

        user_prompt = (
            f"User preferences: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
            f"energy={user_prefs['energy']}, likes_acoustic={user_prefs.get('likes_acoustic', False)}\n"
            f"Song: \"{song['title']}\" by {song['artist']} "
            f"(genre={song['genre']}, mood={song['mood']}, energy={song['energy']})\n"
            f"Score: {score:.2f}/5.0\n"
            f"Match reasons: {score_reasons}\n\n"
            "In exactly 1 sentence, explain conversationally why this song fits the user."
        )

        merged_prompt = f"{system_prompt}\n\n{user_prompt}".strip()

        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=merged_prompt,
        )

        return response.text.strip() if response.text else f"Recommended because: {score_reasons}."

    except Exception:
        return f"Recommended because: {score_reasons}."
