import google.generativeai as genai
from config import Config


genai.configure(api_key=Config.GEMINI_API_KEY)


def generate_event_description(title, category, location):
    """Use Gemini to generate a description for an event."""
    pass


def recommend_events(user_interests, all_events):
    """Use Gemini to recommend events based on user interests."""
    pass
