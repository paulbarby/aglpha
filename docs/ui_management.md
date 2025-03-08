# UI MANAGEMENT SYSTEM DOCUMENTATION

## Overview

The game's UI management system handles all visual interface elements that players interact with, 
from buttons and menus to information panels and tooltips. It's implemented through a UIManager 
class that integrates with the GameEngine to provide a consistent, event-driven interface.

## UI Architecture

### UIManager

The UIManager class (`src.ui.ui_manager`) serves as the central controller for all UI elements and:
- Creates and positions UI components
- Processes UI-related events
- Updates UI elements based on game state
- Manages visibility and interactivity of elements
- Integrates with the GameEngine's event handling system

### Integration with GameEngine

The UIManager is initialized by and communicates with the GameEngine:
```python
# In GameEngine.__init__
self.ui_manager = UIManager(self)  

# In GameEngine.handle_event
if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    if self.ui_manager.is_options_button_clicked(event.pos):
        self.transition_to_options_menu()
        return True  # Event was handled
```

## Core UI Components

1. **Buttons**: Interactive elements for player actions
2. **Panels**: Container elements for organizing related UI components
3. **Menus and Screens**: Complete UI views (like OptionsMenuScreen)
4. **Sliders**: For adjusting values (volume controls, etc.)
5. **Toggle Buttons**: For binary states (on/off)
6. **Labels/Text**: Display information to the player
7. **Tooltips**: Contextual information displayed on hover

## Event Handling System

UI elements in the game follow a consistent event handling pattern:

```python
def handle_event(self, event):
    """Handle UI events."""
    handled = False
    
    # Let child components handle events first
    for component in self.components:
        if component.handle_event(event):
            handled = True
    
    # Handle click events
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not handled:
        pos = event.pos
        if self.rect.collidepoint(pos):
            # Handle the click
            self.on_click()
            handled = True
    
    return handled  # Return whether event was handled
```

## Implementing UI Elements

### Step 1: Define the UI Element

```python
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.active = True
        
    def draw(self, surface):
        # Drawing logic
        color = (200, 200, 200) if self.hovered else (150, 150, 150)
        pygame.draw.rect(surface, color, self.rect)
        
        # Render text
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def handle_click(self, pos):
        """Handle mouse click at position pos."""
        if self.active and self.rect.collidepoint(pos):
            if self.action:
                self.action()
            return True
        return False
        
    def update(self, mouse_pos):
        """Update hover state based on mouse position."""
        self.hovered = self.rect.collidepoint(mouse_pos)
```

### Step 2: Create Screen/Menu Components

Following the pattern of OptionsMenuScreen:

```python
class GameMenuScreen:
    def __init__(self, screen, game_engine, back_callback):
        self.screen = screen
        self.game_engine = game_engine
        self.back_callback = back_callback
        
        # Initialize UI elements
        self.buttons = []
        self.buttons.append(Button(100, 100, 200, 50, "End Turn", 
                                  self.game_engine.end_turn))
        self.buttons.append(Button(100, 160, 200, 50, "Options", 
                                  self.game_engine.transition_to_options_menu))
        self.buttons.append(Button(100, 220, 200, 50, "Save Game", 
                                  self.game_engine.save_game))
        
    def handle_event(self, event):
        """Handle UI events."""
        handled = False
        
        # Check for button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for button in self.buttons:
                if button.handle_click(pos):
                    handled = True
                    break
        
        return handled
        
    def update(self):
        """Update the menu screen."""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            
    def draw(self):
        """Draw the menu screen."""
        # Background
        self.screen.fill((50, 50, 80))
        
        # Draw all buttons
        for button in self.buttons:
            button.draw(self.screen)
```

### Step 3: Register with UIManager

```python
class UIManager:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.ui_elements = {}
        self.active_screen = None
        self.initialize_ui()
        
    def initialize_ui(self):
        # Create persistent UI elements
        self.ui_elements['options_button'] = Button(
            x=760, y=10, 
            width=100, height=30, 
            text="Options",
            action=self.game_engine.transition_to_options_menu
        )
        
    def set_active_screen(self, screen_name, **kwargs):
        """Set the active UI screen."""
        if screen_name == "options":
            self.active_screen = OptionsMenuScreen(
                self.game_engine.screen,
                self.game_engine.sound_manager,
                lambda: self.set_active_screen(None)
            )
        elif screen_name == "main_menu":
            # Initialize main menu
            pass
        else:
            self.active_screen = None
            
    def handle_event(self, event):
        """Process UI events."""
        # Let active screen handle events first
        if self.active_screen and self.active_screen.handle_event(event):
            return True
            
        # Handle events for persistent UI elements
        # ...
        
        return False
```

## UI Context Management

The game uses an event-driven approach to update UI based on game state:

```python
def update_ui(self):
    # Update active screen if any
    if self.active_screen:
        self.active_screen.update()
    
    # Update UI based on current game state
    game_state = self.game_engine.get_state()
    
    # Show/hide elements based on state
    self.ui_elements['unit_panel'].active = (game_state.selected_unit is not None)
    if game_state.selected_unit:
        self.ui_elements['unit_panel'].update_for_unit(game_state.selected_unit)
    
    # Update cursor position for hover effects
    mouse_pos = pygame.mouse.get_pos()
    for element in self.ui_elements.values():
        if hasattr(element, 'update') and element.active:
            element.update(mouse_pos)
```

## Rendering Structure

UI rendering follows a layered approach:

```python
def render(self, screen):
    # Render game elements first
    # ...
    
    # Render persistent UI elements
    for element in self.ui_elements.values():
        if element.active:
            element.draw(screen)
    
    # Render active screen (modal) on top
    if self.active_screen:
        self.active_screen.draw()
```

## Screen Management

The game uses specialized screen classes (like OptionsMenuScreen) that encapsulate:
- UI components specific to that screen
- Event handling
- Drawing logic
- State management

Each screen typically follows this pattern:
1. Initialize components
2. Handle events and return whether they were handled
3. Update state based on time or input
4. Draw components to the screen

## Best Practices

1. **Consistent Event Handling**: Always return True when an event is handled to prevent further processing

2. **Component Encapsulation**: UI elements should handle their own drawing and event processing

3. **Callback Functions**: Use callbacks for actions to maintain separation of concerns

4. **Use Screen Classes**: Encapsulate related UI elements in specialized screen classes

5. **State-Driven UI**: Update UI visibility and functionality based on game state

6. **Input Validation**: Always check bounds and validate user input

7. **Visual Feedback**: Provide hover effects and visual cues for interactive elements

8. **Modularity**: Design UI components to be reusable

## Example: Complete UI Flow

1. Player clicks on the map
2. GameEngine receives the click event
3. Event is passed to UIManager's handle_event method
4. UIManager determines the click is on a unit
5. The selection is updated in the game state
6. In the next update cycle, UIManager reads the new game state
7. UIManager activates and updates the unit panel with unit information
8. On the next render cycle, the unit panel is drawn with the specific unit's details
