import pygame
from .ui_component import UIComponent
from .button import Button
from src.utils.logger import Logger
import time  # Add this import for time.sleep

class VolumeSlider(UIComponent):
    """A slider for controlling volume."""
    
    def __init__(self, x, y, width, height, min_value=0.0, max_value=1.0, initial_value=1.0, on_change=None):
        super().__init__("slider", "slider", (x, y), (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.on_change = on_change
        self.dragging = False
        self.slider_width = 20
        self.slider_x = self._value_to_position(initial_value)
        
        # Add this line to initialize the rect attribute properly
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def _value_to_position(self, value):
        """Convert a value to a slider position."""
        value_range = self.max_value - self.min_value
        position_range = self.width - self.slider_width
        relative_value = (value - self.min_value) / value_range
        return self.x + relative_value * position_range
        
    def _position_to_value(self, position):
        """Convert a slider position to a value."""
        position_range = self.width - self.slider_width
        relative_position = max(0, min(position - self.x, position_range)) / position_range
        return self.min_value + relative_position * (self.max_value - self.min_value)
        
    def handle_event(self, event):
        """Handle mouse events for the slider."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.slider_x = max(self.x, min(event.pos[0] - self.slider_width / 2, self.x + self.width - self.slider_width))
                self.value = self._position_to_value(self.slider_x)
                if self.on_change:
                    self.on_change(self.value)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.slider_x = max(self.x, min(event.pos[0] - self.slider_width / 2, self.x + self.width - self.slider_width))
            self.value = self._position_to_value(self.slider_x)
            if self.on_change:
                self.on_change(self.value)
                
    def draw(self, surface):
        """Draw the slider."""
        # Draw track
        pygame.draw.rect(surface, (100, 100, 100), (self.x, self.y + self.height // 2 - 2, self.width, 4))
        # Draw slider
        pygame.draw.rect(surface, (200, 200, 200), (self.slider_x, self.y, self.slider_width, self.height))
    
    def render(self, surface):
        """Render the slider on the given surface."""
        # Implement the same functionality as the current draw method
        self.draw(surface)


class OptionsMenuScreen:
    """Options menu screen with volume controls."""
    

    def __init__(self, screen, sound_manager, back_callback):
        self.screen = screen
        self.sound_manager = sound_manager
        self.back_callback = back_callback
        
        screen_width, screen_height = screen.get_size()
        
        # Create UI components
        title_font = pygame.font.Font(None, 48)
        self.title = title_font.render("Options", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(screen_width // 2, 50))
        
        # Volume sliders
        label_font = pygame.font.Font(None, 24)
        self.master_label = label_font.render("Master Volume", True, (255, 255, 255))
        self.music_label = label_font.render("Music Volume", True, (255, 255, 255))
        self.sound_label = label_font.render("Sound Effects Volume", True, (255, 255, 255))
        
        slider_width = 300
        slider_height = 30
        slider_x = (screen_width - slider_width) // 2
        
        self.master_slider = VolumeSlider(
            slider_x, 120, slider_width, slider_height,
            initial_value=sound_manager.master_volume,
            on_change=self.on_master_volume_change
        )
        
        self.music_slider = VolumeSlider(
            slider_x, 200, slider_width, slider_height,
            initial_value=sound_manager.music_volume,
            on_change=self.on_music_volume_change
        )
        
        self.sound_slider = VolumeSlider(
            slider_x, 280, slider_width, slider_height,
            initial_value=sound_manager.sound_volume,
            on_change=self.on_sound_volume_change
        )
        
        # Toggle buttons for enabling/disabling sound and music
        button_width, button_height = 140, 40
        button_spacing = 20
        
        # Fixed button creation with proper parameters
        self.music_toggle_btn = Button(
            "music_toggle_btn",  # id
            "Music: ON" if sound_manager.music_enabled else "Music: OFF",  # text
            (screen_width // 2 - button_width - button_spacing // 2, 360),  # position as tuple
            (button_width, button_height)  # size as tuple
        )
        self.music_toggle_btn.set_action(self.toggle_music)
        
        self.sound_toggle_btn = Button(
            "sound_toggle_btn",  # id
            "Sound: ON" if sound_manager.sound_enabled else "Sound: OFF",  # text
            (screen_width // 2 + button_spacing // 2, 360),  # position as tuple
            (button_width, button_height)  # size as tuple
        )
        self.sound_toggle_btn.set_action(self.toggle_sound)
        
        # Back button
        self.back_button = Button(
            "back_button",  # id
            "Back",  # text
            ((screen_width - button_width) // 2, screen_height - 100),  # position as tuple
            (button_width, button_height)  # size as tuple
        )
        self.back_button.set_action(self.on_back_clicked)
    
    def toggle_music(self):
        """Toggle music on/off."""
        # Replace the direct implementation with the safe version
        handled = self.toggle_music_safely()
        if handled:
            # Only update button text if operation was successful
            new_state = self.sound_manager.music_enabled
            self.music_toggle_btn.set_text("Music: ON" if new_state else "Music: OFF")
           
    def toggle_sound(self):
        """Toggle sound effects on/off."""
        new_state = not self.sound_manager.sound_enabled
        self.sound_manager.enable_sound(new_state)
        # Use set_text instead of directly modifying text
        self.sound_toggle_btn.set_text("Sound: ON" if new_state else "Sound: OFF")

    def on_master_volume_change(self, value):
        """Handle master volume slider change."""
        self.sound_manager.set_master_volume(value)
        return True  # Operation was successful
    

    def on_music_volume_change(self, value):
        """Handle music volume slider change."""
        self.sound_manager.set_music_volume(value)
        return True  # Operation was successful
    

    def on_sound_volume_change(self, value):
        """Handle sound effects volume slider change."""
        self.sound_manager.set_sound_volume(value)
        return True  # Operation was successful
    

    def on_back_clicked(self):
        """Handle back button click."""
        logger = Logger()
        logger.info("Back button clicked in options menu")
        # Call back_callback to return to previous screen
        self.back_callback()
    

    def handle_event(self, event):
        """Handle UI events."""
        handled = False
        
        # Volume sliders have their own handle_event method
        handled = self.master_slider.handle_event(event)
        handled = self.music_slider.handle_event(event)
        handled = self.sound_slider.handle_event(event)
    
        # Handle button events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not handled:
            pos = event.pos
            # Use handle_click for consistent behavior
            if self.music_toggle_btn.handle_click(pos):
                handled = True
            elif self.sound_toggle_btn.handle_click(pos):
                handled = True
            elif self.back_button.handle_click(pos):
                handled = True
        
        # Return True if we handled the event to prevent further processing
        return handled
    
    def update(self):
        """Update the options menu screen."""
        pass
        

    def draw(self):
        """Draw the options menu screen."""
        # Draw background
        self.screen.fill((30, 30, 50))
        
        # Draw title
        self.screen.blit(self.title, self.title_rect)
        
        # Draw slider labels
        self.screen.blit(self.master_label, (self.master_slider.x, self.master_slider.y - 30))
        self.screen.blit(self.music_label, (self.music_slider.x, self.music_slider.y - 30))
        self.screen.blit(self.sound_label, (self.sound_slider.x, self.sound_slider.y - 30))
        
        # Draw sliders
        self.master_slider.draw(self.screen)
        self.music_slider.draw(self.screen)
        self.sound_slider.draw(self.screen)
        
        # Draw toggle buttons - changed from draw to render
        self.music_toggle_btn.render(self.screen)
        self.sound_toggle_btn.render(self.screen)
        
        # Draw back button - changed from draw to render
        self.back_button.render(self.screen)

    def toggle_music_safely(self, enable=None):
        """
        Safely toggle music on/off with error handling
        
        Args:
            enable: Boolean to force music on (True) or off (False), or None to toggle
            
        Returns:
            Boolean: True if operation was successful, False otherwise
        """
        logger = Logger()
        logger.info(f"Music toggle requested with enable={enable}")

        if not hasattr(self.sound_manager, "music_enabled"):
            logger.error("Sound manager has no music_enabled attribute")
            return False
            
        current_state = self.sound_manager.music_enabled
        
        # If enable is specified, use that value, otherwise toggle current state
        new_state = not current_state if enable is None else enable
        
        logger.info(f"Music state changing from {current_state} to {new_state}")
        
        # First pause any currently playing music if turning off
        if not new_state and current_state:
            self.sound_manager.stop_music(fadeout=1000)
            
        # Now set the new state - use enable_music method if available
        if hasattr(self.sound_manager, "enable_music") and callable(getattr(self.sound_manager, "enable_music")):
            self.sound_manager.enable_music(new_state)
        else:
            self.sound_manager.music_enabled = new_state
        
        # Update config
        from src.utils.config_manager import config_manager
        config_manager.set_value("AUDIO", "music_enabled", new_state)
        
        # If turning on, restart music with careful error handling
        if new_state and not current_state:
            # Find appropriate music to play based on context
            if hasattr(self, 'back_callback') and self.back_callback:
                # We're in options menu, use menu music if available
                try:
                    if hasattr(self.sound_manager, "play_music") and callable(getattr(self.sound_manager, "play_music")):
                        self.sound_manager.play_music("menu", fadein=1000)
                except Exception as e:
                    logger.error(f"Failed to start menu music: {str(e)}")
                    # Try a fallback if available
                    try:
                        if hasattr(self.sound_manager, "play_default_music"):
                            self.sound_manager.play_default_music()
                    except:
                        # Last resort - ignore if this fails
                        pass
            
        return True  # Operation was successful
