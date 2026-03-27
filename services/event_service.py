from pymongo import MongoClient
from bson import ObjectId
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client["event_db"]
events_collection = db["events"] 


def create_event(event_data):
    return event_model.create_event(event_data)


def get_all_events():
    return event_model.get_all_events()


def get_event_by_id(event_id):
    return event_model.get_event_by_id(event_id)


def update_event(event_id, data):
    return event_model.update_event(event_id, data)


def delete_event(event_id):
    result = events_collection.delete_one({"_id": ObjectId(event_id)})
    return result.deleted_count > 0


def get_events_by_category(category):
    return event_model.get_events_by_category(category)
