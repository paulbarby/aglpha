class Event:
    def __init__(self, id, event_type, data, timestamp):
        self.id = id
        self.event_type = event_type  # e.g., "unit_move", "combat", "city_update"
        self.data = data              # Dictionary with event details
        self.timestamp = timestamp