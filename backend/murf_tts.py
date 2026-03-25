import requests
import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def generate_audio(text: str, voice_id: str = "en-US-natalie", speed: int = -10) -> str | None:
    """Call Murf AI API to convert text to speech and return base64-encoded audio.

    Args:
        text: The plain-language text to convert to audio.
        voice_id: Murf voice identifier.
        speed: Playback speed adjustment (-50 to 50).

    Returns:
        Base64-encoded MP3 string, or None if the request fails.
    """
    load_dotenv(_ENV_PATH, override=True)
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {
        "Content-Type": "application/json",
        "api-key": os.getenv("MURF_API_KEY"),
    }
    payload = {
        "voiceId": voice_id,
        "text": text,
        "format": "MP3",
        "sampleRate": 24000,
        "speed": speed,
        "pitch": 0,
        "encodeAsBase64": True,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("encodedAudio")
        print(f"Murf API error {response.status_code}: {response.text}")
        return None
    except Exception as e:
        print(f"Murf request failed: {e}")
        return None


def build_tts_text(report_dict: dict) -> str:
    """Convert a structured simplify_report dict into a single readable TTS string.

    Args:
        report_dict: The dict returned by ai_simplifier.simplify_report.

    Returns:
        A single plain-text string suitable for text-to-speech.
    """
    parts = [report_dict.get("summary", "")]

    for section in report_dict.get("sections", []):
        parts.append(section["title"] + ". " + section["plain_text"])

    action_items = report_dict.get("action_items", [])
    if action_items:
        parts.append("Here is what you should do next. " + ". ".join(action_items))

    if report_dict.get("reassurance"):
        parts.append(report_dict["reassurance"])

    return ". ".join(parts)


def get_voices() -> list:
    """Return the list of supported Murf voice options.

    Returns:
        List of dicts with 'id' and 'name' keys.
    """
    return [
        {"id": "en-US-natalie", "name": "Natalie — US English, Female"},
        {"id": "en-US-ken", "name": "Ken — US English, Male"},
        {"id": "en-IN-aarav", "name": "Aarav — Indian English, Male"},
        {"id": "en-IN-priya", "name": "Priya — Indian English, Female"},
    ]
