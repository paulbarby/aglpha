import pygame
import os
from src.ui.ui_component import UIComponent
from src.ui.button import Button
from src.engine.core_states import GameState

class MainMenu(UIComponent):
    def __init__(self, game_engine):
        super().__init__("main_menu", "menu", (0, 0), (0, 0))  # Size will be set to screen size
        self.game_engine = game_engine
        self.background = None
        self.logo = None
        self.buttons = []
        
    def initialize(self, screen_size):
        self.size = screen_size
        
        # Load background and logo
        try:
            bg_path = os.path.join("assets", "images", "main_menu_backdrop.jpg")
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, screen_size)
            
            logo_path = os.path.join("assets", "images", "logo.png")
            self.logo = pygame.image.load(logo_path)
            # Keep logo aspect ratio while scaling to reasonable size
            logo_width = min(screen_size[0] * 0.7, self.logo.get_width())
            logo_scale = logo_width / self.logo.get_width()
            logo_height = self.logo.get_height() * logo_scale
            self.logo = pygame.transform.scale(self.logo, (int(logo_width), int(logo_height)))
        except pygame.error as e:
            print(f"Error loading menu assets: {e}")
            # Fallback color if images can't be loaded
            self.background = pygame.Surface(screen_size)
            self.background.fill((0, 0, 100))
        
        # Create buttons
        button_width = 300
        button_height = 50
        button_margin = 20
        
        # Center buttons horizontally and vertically on screen
        start_x = (screen_size[0] - button_width) // 2
        
        # Calculate total height of all buttons + margins
        total_button_height = 4 * button_height + 3 * button_margin
        # Center the entire button group vertically
        start_y = (screen_size[1] - total_button_height) // 2
        
        # Create New Game button
        new_game_btn = Button(
            "new_game_btn", 
            "Create New Game", 
            (start_x, start_y),
            (button_width, button_height)
        )
        new_game_btn.set_action(lambda: self.change_game_state(GameState.NEW_GAME))
        self.buttons.append(new_game_btn)
        
        # Load Game button
        load_game_btn = Button(
            "load_game_btn", 
            "Load Existing Game", 
            (start_x, start_y + button_height + button_margin),
            (button_width, button_height)
        )
        load_game_btn.set_action(lambda: self.change_game_state(GameState.LOAD_GAME))
        self.buttons.append(load_game_btn)
        
        # Options button
        options_btn = Button(
            "options_btn", 
            "Options", 
            (start_x, start_y + (button_height + button_margin) * 2),
            (button_width, button_height)
        )
        options_btn.set_action(self.on_options_clicked)
        self.buttons.append(options_btn)
        
        # Exit button
        exit_btn = Button(
            "exit_btn", 
            "Exit", 
            (start_x, start_y + (button_height + button_margin) * 3),
            (button_width, button_height)
        )
        exit_btn.set_action(self.exit_game)
        self.buttons.append(exit_btn)
        
    def change_game_state(self, new_state):
        self.game_engine.game_state = new_state
        
        # If changing to load game screen, refresh the saved games list
        if new_state == GameState.LOAD_GAME and 'load_game_screen' in self.game_engine.ui_manager.components:
            self.game_engine.ui_manager.components['load_game_screen'].refresh_saved_games()
        
    def exit_game(self):
        pygame.quit()
        import sys
        sys.exit()
        
    def handle_mouse_move(self, pos):
        for button in self.buttons:
            button.handle_mouse_move(pos)
            
    def handle_click(self, pos):
        for button in self.buttons:
            if button.handle_click(pos):
                return True
        return False
        
    def render(self, screen):
        if not self.visible:
            return
        
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
            
        # Draw logo centered at top
        if self.logo:
            logo_x = (self.size[0] - self.logo.get_width()) // 2
            logo_y = 50  # Position from top
            screen.blit(self.logo, (logo_x, logo_y))
            
        # Draw buttons
        for button in self.buttons:
            button.render(screen)
    
    def on_options_clicked(self):
        """Handle options button click."""
        from .options_menu import OptionsMenuScreen
        self.game_engine.transition_to_options_menu()
