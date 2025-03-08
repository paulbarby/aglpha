import pygame
from src.ui.ui_component import UIComponent
from src.utils.logger import Logger

class Button(UIComponent):
    def __init__(self, id, text, position, size, font_size=32, 
                 text_color=(100, 100, 100), hover_color=(0, 0, 0)):
        super().__init__(id, "button", position, size)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.default_text_color = text_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = None
        self.rendered_text = None
        self.action = None
        
        # New properties for button styling
        self.bg_color = (255, 255, 255)  # White background
        self.border_color = (0, 0, 0)    # Black border
        self.border_width = 2            # 2px border width
        self.border_radius = 10          # Rounded corners
        
    def initialize(self):
        self.font = pygame.font.SysFont(None, self.font_size)
        self.rendered_text = self.font.render(self.text, True, self.text_color)
    
    def set_text(self, new_text):
        """Set new button text and update the rendered text."""
        self.text = new_text
        if self.font is None:
            self.initialize()
        # Make sure to regenerate the rendered text with current text_color
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        
    def set_action(self, action):
        # debug
        Logger().debug(f"Setting action for button {self.id}")
        self.action = action
        
    def contains_point(self, point):
        x, y = point
        return (self.position[0] <= x <= self.position[0] + self.size[0] and
                self.position[1] <= y <= self.position[1] + self.size[1])
    
    def handle_mouse_move(self, pos):
        was_hovered = self.is_hovered
        self.is_hovered = self.contains_point(pos)
        
        if self.is_hovered != was_hovered:
            if self.is_hovered:
                self.text_color = self.hover_color
            else:
                self.text_color = self.default_text_color
            if self.font is None:
                self.initialize()
            self.rendered_text = self.font.render(self.text, True, self.text_color)
            return True
        return False
    
    def handle_click(self, pos):
        # debug
        Logger().debug(f"Handling click for button {self.id}")
        if self.contains_point(pos) and self.action:
            self.action()
            return True
        return False
    
    def render(self, screen):
        if not self.visible:
            return
            
        if self.rendered_text is None:
            self.initialize()
        
        # Draw button background with rounded corners
        rect = pygame.Rect(self.position, self.size)
        pygame.draw.rect(screen, self.bg_color, rect, 0, self.border_radius)
        
        # Draw button border with rounded corners
        pygame.draw.rect(screen, self.border_color, rect, self.border_width, self.border_radius)
            
        # Center text in button
        text_x = self.position[0] + (self.size[0] - self.rendered_text.get_width()) // 2
        text_y = self.position[1] + (self.size[1] - self.rendered_text.get_height()) // 2
        
        screen.blit(self.rendered_text, (text_x, text_y))
        
    def is_clicked(self, mouse_pos):
        """Check if the button is clicked without triggering the action."""
        if not hasattr(self, 'rect'):
            return False
            
        # Simply check if mouse position is within button rect
        return self.rect.collidepoint(mouse_pos)
