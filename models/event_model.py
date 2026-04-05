from pymongo import MongoClient
from config import Config
from bson import ObjectId

_client = None


def _collection():
    global _client
    if _client is None:
        _client = MongoClient(Config.MONGO_URI)
    return _client["event_db"]["events"]


def create_event(event_data):
    event = {
        "title": event_data.get("title"),
        "description": event_data.get("description"),
        "date": event_data.get("date"),
        "location": event_data.get("location"),
        "category": event_data.get("category")
    }

    result = _collection().insert_one(event)
    event["_id"] = str(result.inserted_id)

    return event


def get_all_events():
    events = list(_collection().find())

    for event in events:
        event["_id"] = str(event["_id"])

    return events


def get_event_by_id(event_id):
    event = _collection().find_one({"_id": ObjectId(event_id)})

    if event:
        event["_id"] = str(event["_id"])

    return event


def update_event(event_id, updated_data):
    _collection().update_one(
        {"_id": ObjectId(event_id)},
        {"$set": updated_data}
    )

    return get_event_by_id(event_id)


def delete_event(event_id):
    result = _collection().delete_one({"_id": ObjectId(event_id)})

    return result.deleted_count > 0


def get_events_by_category(category):
    events = list(_collection().find({"category": category}))

    for event in events:
        event["_id"] = str(event["_id"])

    return events
