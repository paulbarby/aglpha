import pygame
import os
from datetime import datetime
from src.ui.ui_component import UIComponent
from src.ui.button import Button
from src.engine.core_states import GameState
from src.storage.game_storage_manager import GameStorageManager

class LoadGameScreen(UIComponent):
    def __init__(self, game_engine):
        super().__init__("load_game_screen", "menu", (0, 0), (0, 0))  # Size will be set to screen size
        self.game_engine = game_engine
        self.background = None
        self.buttons = []
        self.saved_games = []
        self.selected_game = None
        self.font = None
        self.title_font = None
        self.title_text = None
        self.list_rect = None
        self.storage_manager = GameStorageManager()
        self.scroll_offset = 0
        self.max_visible_games = 6
        
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
            self.background.fill((0, 0, 60))  # Dark blue for load game screen
        
        # Initialize fonts
        self.font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 48)
        self.title_text = self.title_font.render("Load Game", True, (255, 255, 255))
        
        # Create game list rectangle (area where saved games will be displayed)
        list_width = 500
        list_height = 300
        self.list_rect = pygame.Rect(
            (screen_size[0] - list_width) // 2,
            screen_size[1] // 3,
            list_width, 
            list_height
        )
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_margin = 20
        
        # Position buttons below the list
        start_x = (screen_size[0] - button_width) // 2
        start_y = self.list_rect.bottom + 30
        
        # Create Load Game button (initially disabled)
        load_btn = Button(
            "load_btn", 
            "Load Game", 
            (start_x, start_y),
            (button_width, button_height)
        )
        load_btn.set_action(self.load_selected_game)
        self.buttons.append(load_btn)
        
        # Delete Game button (initially disabled)
        delete_btn = Button(
            "delete_btn", 
            "Delete Game", 
            (start_x - button_width - button_margin, start_y),
            (button_width, button_height)
        )
        delete_btn.set_action(self.delete_selected_game)
        self.buttons.append(delete_btn)
        
        # Back button
        back_btn = Button(
            "back_btn", 
            "Back", 
            (start_x + button_width + button_margin, start_y),
            (button_width, button_height)
        )
        back_btn.set_action(self.go_back)
        self.buttons.append(back_btn)
        
        # Scroll buttons
        scroll_up_btn = Button(
            "scroll_up_btn",
            "▲",
            (self.list_rect.right + 10, self.list_rect.top),
            (30, 30)
        )
        scroll_up_btn.set_action(self.scroll_up)
        self.buttons.append(scroll_up_btn)
        
        scroll_down_btn = Button(
            "scroll_down_btn",
            "▼",
            (self.list_rect.right + 10, self.list_rect.bottom - 30),
            (30, 30)
        )
        scroll_down_btn.set_action(self.scroll_down)
        self.buttons.append(scroll_down_btn)
        
    def refresh_saved_games(self):
        """Refresh the list of saved games from the storage manager"""
        self.saved_games = self.storage_manager.get_all_game_names()
        self.selected_game = None
        
    def scroll_up(self):
        """Scroll up in the games list"""
        if self.scroll_offset > 0:
            self.scroll_offset -= 1
            
    def scroll_down(self):
        """Scroll down in the games list"""
        if len(self.saved_games) > self.max_visible_games and self.scroll_offset < len(self.saved_games) - self.max_visible_games:
            self.scroll_offset += 1
            
    def load_selected_game(self):
        """Load the selected game"""
        if self.selected_game:
            game_data = self.storage_manager.load_game(self.selected_game['name'])
            if game_data:
                # Apply the data to the game engine
                self.storage_manager.apply_game_data_to_engine(game_data, self.game_engine)
                self.game_engine.game_state = GameState.IN_GAME
                print(f"Loading game: {self.selected_game['name']}")
        
    def delete_selected_game(self):
        """Delete the selected game"""
        if self.selected_game:
            if self.storage_manager.delete_game(self.selected_game['name']):
                print(f"Deleted game: {self.selected_game['name']}")
                self.refresh_saved_games()
        
    def go_back(self):
        """Return to the main menu"""
        self.game_engine.game_state = GameState.MAIN_MENU
        
    def handle_mouse_move(self, pos):
        for button in self.buttons:
            button.handle_mouse_move(pos)
            
    def handle_click(self, pos):
        # Check if user clicked in the games list
        if self.list_rect.collidepoint(pos):
            self.handle_list_click(pos)
            
        # Check if user clicked on buttons
        for button in self.buttons:
            if button.handle_click(pos):
                return True
        return False
    
    def handle_list_click(self, pos):
        """Handle clicks in the saved games list"""
        if not self.saved_games:
            return
            
        # Calculate which game was clicked
        y_offset = pos[1] - self.list_rect.top
        game_height = 50  # Height for each game entry
        
        clicked_index = self.scroll_offset + (y_offset // game_height)
        
        if 0 <= clicked_index < len(self.saved_games):
            self.selected_game = self.saved_games[clicked_index]
    
    def render(self, screen):
        if not self.visible:
            return
        
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
            
        # Draw title
        title_x = (self.size[0] - self.title_text.get_width()) // 2
        title_y = self.size[1] // 6
        screen.blit(self.title_text, (title_x, title_y))
        
        # Draw games list background
        pygame.draw.rect(screen, (30, 30, 30), self.list_rect)  # Dark gray background
        pygame.draw.rect(screen, (100, 100, 100), self.list_rect, 2)  # Gray border
        
        # Draw saved games
        if not self.saved_games:
            # Show "No saved games" message
            no_games_text = self.font.render("No saved games found", True, (200, 200, 200))
            text_x = self.list_rect.centerx - (no_games_text.get_width() // 2)
            text_y = self.list_rect.centery - (no_games_text.get_height() // 2)
            screen.blit(no_games_text, (text_x, text_y))
        else:
            # Draw visible saved games
            game_height = 50
            visible_games = self.saved_games[self.scroll_offset:self.scroll_offset + self.max_visible_games]
            
            for i, game in enumerate(visible_games):
                game_y = self.list_rect.top + (i * game_height)
                game_rect = pygame.Rect(self.list_rect.left, game_y, self.list_rect.width, game_height)
                
                # Highlight selected game
                if self.selected_game and game['name'] == self.selected_game['name']:
                    pygame.draw.rect(screen, (70, 70, 100), game_rect)  # Highlight color
                
                # Draw game name
                name_text = self.font.render(game['name'], True, (255, 255, 255))
                screen.blit(name_text, (game_rect.left + 10, game_rect.top + 5))
                
                # Draw last saved date
                try:
                    date_str = datetime.fromisoformat(game['last_saved_at']).strftime("%Y-%m-%d %H:%M")
                except:
                    date_str = game['last_saved_at']
                    
                date_text = pygame.font.SysFont(None, 24).render(f"Last saved: {date_str}", True, (200, 200, 200))
                screen.blit(date_text, (game_rect.left + 10, game_rect.top + 30))
                
                # Draw separator line
                if i < len(visible_games) - 1:
                    pygame.draw.line(screen, (100, 100, 100), 
                                    (game_rect.left, game_rect.bottom), 
                                    (game_rect.right, game_rect.bottom), 1)
            
        # Draw buttons
        for button in self.buttons:
            # Enable/disable load and delete buttons based on selection
            if button.id in ["load_btn", "delete_btn"]:
                if self.selected_game:
                    # Enable buttons
                    button.bg_color = (255, 255, 255)  # White background
                    button.text_color = button.default_text_color
                else:
                    # Disable buttons
                    button.bg_color = (150, 150, 150)  # Gray background
                    button.text_color = (100, 100, 100)  # Darker text
                    
            button.render(screen)
