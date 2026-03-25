from pymongo import MongoClient
from config import Config


client = MongoClient(Config.MONGO_URI)
db = client["event_db"]
events_collection = db["events"]


def create_event(event_data):
    event = {
        "title": event_data.get("title"),
        "description": event_data.get("description"),
        "date": event_data.get("date"),
        "location": event_data.get("location"),
        "category": event_data.get("category")
    }
    
    result = events_collection.insert_one(event)
    event["_id"] = str(result.inserted_id)
    
    return event


def get_all_events():
    events = list(events_collection.find())
    
    for event in events:
        event["_id"] = str(event["_id"])
    
    return events


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
