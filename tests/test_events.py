import pytest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch
from app import app

#creating test version of the app 
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client



#checking does the home page load
def test_health_check_status_code(client):
    response = client.get("/health")
    assert response.status_code == 200

# then Does it return "ok"
def test_health_check_returns_ok(client):
    response = client.get("/health")
    data = response.get_json()
    assert data["status"] == "ok"



#checking GET /events/ return 200
@patch("services.event_service.get_all_events")
def test_get_all_events_status_code(mock_get, client):
    mock_get.return_value = []  # pretend database returns empty list
    response = client.get("/events/")
    assert response.status_code == 200

#checking the response contain "events"?
@patch("services.event_service.get_all_events")
def test_get_all_events_has_events_key(mock_get, client):
    mock_get.return_value = []
    response = client.get("/events/")
    data = response.get_json()
    assert "events" in data


# checking creating an event return 201?
@patch("services.event_service.create_event")
def test_create_event_status_code(mock_create, client):
    mock_create.return_value = {"title": "Test Event"}
    response = client.post("/events/", json={
        "title": "Test Event",
        "description": "A test event",
        "date": "2026-04-01",
        "location": "Doha",
        "category": "sports"
    })
    assert response.status_code == 201

#return a success message?
@patch("services.event_service.create_event")
def test_create_event_success_message(mock_create, client):
    mock_create.return_value = {"title": "Test Event"}
    response = client.post("/events/", json={"title": "Test Event"})
    data = response.get_json()
    assert data["message"] == "Event created successfully"


#will a wrong ID return 404?
@patch("services.event_service.get_event_by_id")
def test_get_event_wrong_id_returns_404(mock_get, client):
    mock_get.return_value = None  # pretend event not found
    response = client.get("/events/wrongid123")
    assert response.status_code == 404

# checking if a wrong ID return error message?
@patch("services.event_service.get_event_by_id")
def test_get_event_wrong_id_error_message(mock_get, client):
    mock_get.return_value = None
    response = client.get("/events/wrongid123")
    data = response.get_json()
    assert data["error"] == "Event not found"


# deleting an event return success message?
@patch("services.event_service.delete_event")
def test_delete_event_success(mock_delete, client):
    mock_delete.return_value = True  # pretend delete worked
    response = client.delete("/events/someid123")
    data = response.get_json()
    assert data["message"] == "Event deleted"

# deleting a non existing event return 404?
@patch("services.event_service.delete_event")
def test_delete_event_not_found(mock_delete, client):
    mock_delete.return_value = False  # pretend event doesnt exist
    response = client.delete("/events/fakeid999")
    assert response.status_code == 404



# GET /events/category/sports return 200?
@patch("services.event_service.get_events_by_category")
def test_get_by_category_status_code(mock_get, client):
    mock_get.return_value = []
    response = client.get("/events/category/sports")
    assert response.status_code == 200

# return events list?
@patch("services.event_service.get_events_by_category")
def test_get_by_category_has_events_key(mock_get, client):
    mock_get.return_value = []
    response = client.get("/events/category/sports")
    data = response.get_json()
    assert "events" in data