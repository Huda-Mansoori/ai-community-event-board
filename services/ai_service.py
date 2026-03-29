import requests
from config import Config


API_BASE = "https://aiplatform.googleapis.com/v1/publishers/google/models"
DEFAULT_MODEL = "gemini-2.5-flash-lite"


def _normalize_gemini_error(error):
    message = str(error)

    if "SERVICE_DISABLED" in message:
        return (
            "Gemini API is disabled for this Google project. "
            "Enable the API in Google Cloud Console and try again."
        )

    if "API_KEY" in message and "INVALID" in message:
        return "Invalid Gemini API key. Check GEMINI_API_KEY in your .env file."

    if "PermissionDenied" in message:
        return "Gemini request was denied. Verify API enablement and key permissions."

    return f"Gemini API request failed: {message}"


def _fallback_description(title, category, location):
    safe_category = category or "community"
    safe_location = location or "our local area"
    return (
        f"Join us for {title}, a {safe_category} event happening at {safe_location}. "
        "Come connect with others, share ideas, and enjoy a welcoming community experience."
    )


def _call_gemini(prompt):
    """Call Gemini via the Vertex AI REST API (same endpoint the API key is authorized for)."""
    if not Config.GEMINI_API_KEY:
        return None

    url = f"{API_BASE}/{DEFAULT_MODEL}:generateContent?key={Config.GEMINI_API_KEY}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        return None

    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        return None

    return parts[0].get("text", "").strip()


def generate_event_description(title, category, location):
    """Use Gemini to generate a description for an event."""
    clean_title = (title or "").strip()
    clean_category = (category or "").strip()
    clean_location = (location or "").strip()

    if not clean_title:
        raise ValueError("Event title is required to generate a description")

    if not Config.GEMINI_API_KEY:
        return _fallback_description(clean_title, clean_category, clean_location)

    prompt = (
        "Write a concise and friendly event description in 2-3 sentences. "
        "Mention who should attend and what they can expect. "
        "Do not use markdown or bullet points.\n\n"
        f"Title: {clean_title}\n"
        f"Category: {clean_category or 'General'}\n"
        f"Location: {clean_location or 'TBA'}"
    )

    try:
        generated_text = _call_gemini(prompt)
        if generated_text:
            return generated_text
        raise RuntimeError("Gemini returned an empty response")
    except Exception as error:
        raise RuntimeError(_normalize_gemini_error(error)) from error


def recommend_events(user_interests, all_events):
    """Use Gemini to recommend events based on user interests."""
    interests = user_interests or []
    events = all_events or []

    if not events:
        return []

    normalized_interests = [str(item).lower() for item in interests if str(item).strip()]

    if not normalized_interests:
        return events[:3]

    scored = []
    for event in events:
        text_blob = " ".join([
            str(event.get("title", "")),
            str(event.get("description", "")),
            str(event.get("category", ""))
        ]).lower()

        score = sum(1 for term in normalized_interests if term in text_blob)
        scored.append((score, event))

    scored.sort(key=lambda item: item[0], reverse=True)
    top_matches = [event for score, event in scored if score > 0][:5]

    return top_matches or events[:3]
