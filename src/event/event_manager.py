class EventManager:
    def __init__(self):
        self.event_queue = []  # List of Event objects

    def add_event(self, event):
        self.event_queue.append(event)

    def process_events(self):
        while self.event_queue:
            event = self.event_queue.pop(0)
            self.handle_event(event)

    def handle_event(self, event):
        # Dispatch the event to the appropriate handler based on type
        if event.event_type == "unit_move":
            # Handle unit movement event
            pass
        elif event.event_type == "combat":
            # Handle combat resolution
            pass
        # Add additional event types as needed