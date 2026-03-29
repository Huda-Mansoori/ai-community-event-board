from flask import Blueprint, request, jsonify
from services import event_service, ai_service


event_bp = Blueprint("events", __name__, url_prefix="/events")


@event_bp.route("/", methods=["GET"])
def get_all_events():
    events = event_service.get_all_events()
    
    return jsonify({
        "team": "AI Community Event Board - Huda 60304645",
        "events": events
    })


@event_bp.route("/<event_id>", methods=["GET"])
def get_event(event_id):
    event = event_service.get_event_by_id(event_id)
    
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    return jsonify(event)


@event_bp.route("/", methods=["POST"])
def create_event():
    data = request.json
    event = event_service.create_event(data)
    
    return jsonify({
        "message": "Event created successfully",
        "event": event
    }), 201


@event_bp.route("/<event_id>", methods=["PUT"])
def update_event(event_id):
    data = request.json
    event = event_service.update_event(event_id, data)
    
    return jsonify({
        "message": "Event updated",
        "event": event
    })


@event_bp.route("/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    success = event_service.delete_event(event_id)

    if success:
        return jsonify({"message": "Event deleted"})
    else:
        return jsonify({"message": "Event not found"}), 404


@event_bp.route("/category/<category>", methods=["GET"])
def get_events_by_category(category):
    events = event_service.get_events_by_category(category)
    
    return jsonify({
        "events": events
    })


@event_bp.route("/generate-description", methods=["POST"])
def generate_description():
    """Generate an AI-powered event description via Gemini."""
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    category = (data.get("category") or "").strip()
    location = (data.get("location") or "").strip()

    if not title:
        return jsonify({"error": "title is required"}), 400

    try:
        description = ai_service.generate_event_description(title, category, location)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 502

    return jsonify({"description": description})


@event_bp.route("/recommend", methods=["POST"])
def recommend_events():
    """Return AI-powered event recommendations based on user interests."""
    data = request.get_json(silent=True) or {}
    interests = data.get("interests") or []
    events = event_service.get_all_events()
    recommendations = ai_service.recommend_events(interests, events)

    return jsonify({"recommendations": recommendations})
