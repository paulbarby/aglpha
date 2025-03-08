# EVENT MANAGEMENT SYSTEM DOCUMENTATION

## Overview

The game utilizes a dual-layer event management system:
1. PyGame events (input, window events)
2. Game-specific events (unit movements, combat, etc.)

## Event Architecture

### PyGame Events
PyGame events are handled through the GameEngine's `handle_event` method, which processes
raw input events like mouse clicks, keyboard actions, or window management.

### Game-Specific Events
Custom game events are managed through the EventManager class, which maintains a queue
of game events and dispatches them to appropriate handlers.

## Event Hierarchy and Priority

Events are processed in the following order:
1. Options menu events (highest priority)
2. Quit events
3. UI events (options button clicks)
4. Game-specific events (only processed when not in options menu)

## Implementing New Events

### Step 1: Define Your Event
Create an Event object with the necessary properties:
```python
from event.event import Event  # Assuming Event class exists

new_event = Event(
    id="unique_id_123",
    event_type="research_complete",
    data={
        "technology": "agriculture",
        "player_id": 1
    },
    timestamp=current_game_time
)
```

### Step 2: Register Event Handler
Add a new condition in the EventManager's handle_event method:

```python
def handle_event(self, event):
    if event.event_type == "unit_move":
        # Handle unit movement
        pass
    elif event.event_type == "combat":
        # Handle combat
        pass
    elif event.event_type == "research_complete":
        # Handle research completion
        self._handle_research_completion(event.data)
        pass
    # Additional event types...
    
def _handle_research_completion(self, data):
    # Implementation of the handler
    technology = data.get("technology")
    player_id = data.get("player_id")
    # Add logic for technology completion
```

### Step 3: Trigger the Event
Add the event to the queue when needed:

```python
def complete_research(self, technology, player_id):
    # Logic for completing research
    # ...
    
    # Create and queue the event
    event = Event(
        id=generate_unique_id(),
        event_type="research_complete",
        data={"technology": technology, "player_id": player_id},
        timestamp=self.game_engine.current_time
    )
    self.event_manager.add_event(event)
```

## Event Flow

1. External input (PyGame events) -> GameEngine.handle_event()
2. Game logic creates custom events -> EventManager.add_event()
3. EventManager.process_events() processes the queue
4. EventManager.handle_event() dispatches events to specific handlers

## Best Practices

1. **Event Data**: Keep event data minimal and relevant. Use dictionaries for flexible data passing.

2. **Event Types**: Use consistent naming conventions for event types (e.g., noun_verb: "unit_move", "research_complete").

3. **Handler Separation**: Implement complex event handlers as separate methods for better organization.

4. **Event Priorities**: Consider implementing priority levels for game events that need immediate processing.

5. **Event Logging**: For debugging, consider logging events:
   ```python
   def add_event(self, event):
       self.event_queue.append(event)
       logging.debug(f"Added event: {event.event_type} with data {event.data}")
   ```

6. **Event Batching**: For performance optimization, consider batching similar events:
   ```python
   def add_movement_events(self, unit_movements):
       # Create multiple unit movement events at once
       for unit_id, path in unit_movements.items():
           self.add_event(Event(
               id=generate_unique_id(),
               event_type="unit_move",
               data={"unit_id": unit_id, "path": path},
               timestamp=self.game_engine.current_time
           ))
   ```

7. **Cancellable Events**: Consider implementing a system for cancellable events:
   ```python
   def handle_event(self, event):
       # Allow systems to cancel events
       if self._pre_event_hooks(event):
           return  # Event canceled
           
       # Regular event handling
       # ...
   ```

## Example: Complete Event Flow

1. Player clicks "Move" button for a unit
2. GameEngine.handle_event processes the mouse click
3. UI detects unit move command and creates a game event
4. EventManager adds the event to the queue
5. During next update, EventManager.process_events() processes the event
6. Unit movement handler executes the movement logic
7. UI updates to reflect the movement
