from models import event_model


def create_event(event_data):
    return event_model.create_event(event_data)


def get_all_events():
    return event_model.get_all_events()


def get_event_by_id(event_id):
    """Retrieve and return a single event by ID."""
    pass


def update_event(event_id, updated_data):
    """Validate and update an existing event."""
    pass


def delete_event(event_id):
    """Delete an event by ID."""
    pass


def get_events_by_category(category):
    """Retrieve and return events filtered by category."""
    pass
