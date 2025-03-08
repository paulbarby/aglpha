import pygame
from src.engine.core_states import GameState
from src.ui.main_menu import MainMenu
from src.ui.new_game_screen import NewGameScreen
from src.ui.load_game_screen import LoadGameScreen  # Add this import

class UIManager:
    def __init__(self, game_engine=None):
        self.ui_state = "main_menu"  # e.g., "in_game", "paused", etc.
        self.components = {}         # {component_id: UIComponent}
        self.game_engine = game_engine
        self.screen_size = (0, 0)
        self.last_update_time = pygame.time.get_ticks()

    def initialize(self, game_engine, screen_size):
        self.game_engine = game_engine
        self.screen_size = screen_size
        
        # Create main menu
        main_menu = MainMenu(self.game_engine)
        main_menu.initialize(screen_size)
        self.add_component(main_menu)
        
        # Create new game screen
        new_game_screen = NewGameScreen(self.game_engine)
        new_game_screen.initialize(screen_size)
        self.add_component(new_game_screen)
        
        # Create load game screen
        load_game_screen = LoadGameScreen(self.game_engine)
        load_game_screen.initialize(screen_size)
        self.add_component(load_game_screen)

    def add_component(self, component):
        self.components[component.id] = component

    def process_input(self, input_event):
        # Process input events to update UI (mouse clicks, key presses, etc.)
        if input_event.type == pygame.MOUSEMOTION:
            self.handle_mouse_move(input_event.pos)
        elif input_event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(input_event.pos)
        elif input_event.type == pygame.KEYDOWN and self.game_engine.game_state == GameState.NEW_GAME:
            if 'new_game_screen' in self.components:
                self.components['new_game_screen'].handle_key_event(input_event)
            
    def handle_mouse_move(self, pos):
        if self.game_engine.game_state == GameState.MAIN_MENU and 'main_menu' in self.components:
            self.components['main_menu'].handle_mouse_move(pos)
        elif self.game_engine.game_state == GameState.NEW_GAME and 'new_game_screen' in self.components:
            self.components['new_game_screen'].handle_mouse_move(pos)
        elif self.game_engine.game_state == GameState.LOAD_GAME and 'load_game_screen' in self.components:
            self.components['load_game_screen'].handle_mouse_move(pos)
            
    def handle_click(self, pos):
        if self.game_engine.game_state == GameState.MAIN_MENU and 'main_menu' in self.components:
            self.components['main_menu'].handle_click(pos)
        elif self.game_engine.game_state == GameState.NEW_GAME and 'new_game_screen' in self.components:
            self.components['new_game_screen'].handle_click(pos)
        elif self.game_engine.game_state == GameState.LOAD_GAME and 'load_game_screen' in self.components:
            self.components['load_game_screen'].handle_click(pos)

    def is_options_button_clicked(self, pos):
        """Check if the options button was clicked."""
        if self.game_engine and self.game_engine.game_state == GameState.MAIN_MENU:
            if 'main_menu' in self.components:
                # Check if any of the main menu's buttons is the options button
                for button in self.components['main_menu'].buttons:
                    if button.id == "options_btn" and button.contains_point(pos):
                        return True
        return False

    def update_ui(self):
        # Calculate delta time for animations
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_update_time) / 1000.0  # Convert to seconds
        self.last_update_time = current_time
        
        # Update components based on game state
        if self.game_engine.game_state == GameState.NEW_GAME and 'new_game_screen' in self.components:
            self.components['new_game_screen'].update(delta_time)
        
    def render(self, screen):
        # Render appropriate UI components based on game state
        if self.game_engine.game_state == GameState.MAIN_MENU and 'main_menu' in self.components:
            self.components['main_menu'].render(screen)
        elif self.game_engine.game_state == GameState.NEW_GAME and 'new_game_screen' in self.components:
            self.components['new_game_screen'].render(screen)
        elif self.game_engine.game_state == GameState.LOAD_GAME and 'load_game_screen' in self.components:
            self.components['load_game_screen'].render(screen)
        # Other UI rendering for different game states will be added here