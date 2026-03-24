from pymongo import MongoClient
from config import Config


client = MongoClient(Config.MONGO_URI)
db = client["event_db"]
events_collection = db["events"]


def create_event(event_data):
    """Insert a new event into the database."""
    pass


def get_all_events():
    """Retrieve all events from the database."""
    pass


def get_event_by_id(event_id):
    """Retrieve a single event by its ID."""
    pass


def update_event(event_id, updated_data):
    """Update an existing event by its ID."""
    pass


def delete_event(event_id):
    """Delete an event by its ID."""
    pass


def get_events_by_category(category):
    """Retrieve events filtered by category."""
    pass
