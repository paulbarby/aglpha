import pygame
import os
from src.ui.ui_component import UIComponent
from src.ui.button import Button
from src.engine.core_states import GameState

class NewGameScreen(UIComponent):
    def __init__(self, game_engine):
        super().__init__("new_game_screen", "menu", (0, 0), (0, 0))  # Size will be set to screen size
        self.game_engine = game_engine
        self.background = None
        self.buttons = []
        self.game_name = ""
        self.active_input = False
        self.font = None
        self.title_font = None
        self.title_text = None
        self.input_rect = None
        self.text_surface = None
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def initialize(self, screen_size):
        self.size = screen_size
        
        # Load background
        try:
            bg_path = os.path.join("assets", "images", "main_menu_backdrop.jpg")
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, screen_size)
        except pygame.error as e:
            print(f"Error loading menu assets: {e}")
            # Fallback color if images can't be loaded
            self.background = pygame.Surface(screen_size)
            self.background.fill((0, 0, 80))  # Darker blue for new game screen
        
        # Initialize fonts
        self.font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 48)
        self.title_text = self.title_font.render("Create New Game", True, (255, 255, 255))
        
        # Create input rectangle
        input_width = 300
        input_height = 40
        self.input_rect = pygame.Rect(
            (screen_size[0] - input_width) // 2,
            screen_size[1] // 2 - 30,
            input_width, 
            input_height
        )
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_margin = 20
        
        # Center buttons horizontally, position below input field
        start_x = (screen_size[0] - button_width) // 2
        start_y = self.input_rect.bottom + 50
        
        # Create Start Game button
        start_game_btn = Button(
            "start_game_btn", 
            "Start Game", 
            (start_x, start_y),
            (button_width, button_height)
        )
        start_game_btn.set_action(self.start_game)
        self.buttons.append(start_game_btn)
        
        # Back button
        back_btn = Button(
            "back_btn", 
            "Back", 
            (start_x, start_y + button_height + button_margin),
            (button_width, button_height)
        )
        back_btn.set_action(self.go_back)
        self.buttons.append(back_btn)
        
    def start_game(self):
        if self.game_name.strip():  # Check if game name is not just whitespace
            print(f"Starting new game: {self.game_name}")
            # Here you would store the game name for later use
            self.game_engine.game_name = self.game_name
            self.game_engine.game_state = GameState.IN_GAME
        
    def go_back(self):
        self.game_engine.game_state = GameState.MAIN_MENU
        
    def handle_mouse_move(self, pos):
        for button in self.buttons:
            button.handle_mouse_move(pos)
            
    def handle_click(self, pos):
        # Check if user clicked on input box
        if self.input_rect.collidepoint(pos):
            self.active_input = True
        else:
            self.active_input = False
            
        # Check if user clicked on buttons
        for button in self.buttons:
            if button.handle_click(pos):
                return True
        return False
    
    def handle_key_event(self, event):
        if not self.active_input:
            return False
            
        if event.key == pygame.K_BACKSPACE:
            self.game_name = self.game_name[:-1]
        elif event.key == pygame.K_RETURN:
            self.start_game()
        elif event.key == pygame.K_ESCAPE:
            self.active_input = False
        else:
            # Limit name length to fit in box
            if len(self.game_name) < 20:
                self.game_name += event.unicode
        
        return True
        
    def update(self, delta_time):
        # Cursor blinking
        self.cursor_timer += delta_time
        if self.cursor_timer > 0.5:  # Toggle every 0.5 seconds
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
    def render(self, screen):
        if not self.visible:
            return
        
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
            
        # Draw title
        title_x = (self.size[0] - self.title_text.get_width()) // 2
        title_y = self.size[1] // 4
        screen.blit(self.title_text, (title_x, title_y))
        
        # Draw name entry prompt
        prompt_text = self.font.render("Enter a name for your new game:", True, (255, 255, 255))
        prompt_x = (self.size[0] - prompt_text.get_width()) // 2
        prompt_y = self.input_rect.top - 40
        screen.blit(prompt_text, (prompt_x, prompt_y))
            
        # Draw input box with white background
        pygame.draw.rect(screen, (255, 255, 255), self.input_rect)  # Fill with white
        box_color = (100, 100, 200) if self.active_input else (70, 70, 70)
        pygame.draw.rect(screen, box_color, self.input_rect, 2)  # Draw outline
        
        # Render current text with black color
        text_surface = self.font.render(self.game_name, True, (0, 0, 0))  # Black text
        
        # Ensure text fits in the input box
        text_width = text_surface.get_width()
        
        # Draw text in input box
        screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        
        # Draw cursor when input is active (make cursor black to match text)
        if self.active_input and self.cursor_visible:
            cursor_x = self.input_rect.x + 5 + text_width
            cursor_y = self.input_rect.y + 5
            pygame.draw.line(
                screen, 
                (0, 0, 0),  # Black cursor
                (cursor_x, cursor_y), 
                (cursor_x, cursor_y + self.font.get_height()), 
                2
            )
            
        # Draw buttons
        for button in self.buttons:
            button.render(screen)
