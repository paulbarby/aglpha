from enum import Enum, auto
from src.utils.logger import Logger
class GameAudioState(Enum):
    """Enum for various game audio states."""
    MAIN_MENU = auto()
    GAMEPLAY = auto()
    COMBAT = auto()
    VICTORY = auto()
    DEFEAT = auto()
    OPTIONS_MENU = auto()

class AudioStateManager:
    """Manages audio states and transitions between them."""
    
    def __init__(self, sound_manager):
        self.logger = Logger()
        self.sound_manager = sound_manager
        self.current_state = None
        self.state_music_map = {
            GameAudioState.MAIN_MENU: "main_menu_music",
            GameAudioState.GAMEPLAY: "gameplay_music",
            GameAudioState.COMBAT: "combat_music",
            GameAudioState.VICTORY: "victory_music",
            GameAudioState.DEFEAT: "defeat_music",
            GameAudioState.OPTIONS_MENU: "main_menu_music"  # Reuse main menu music for options
        }
        
        # Sound effects that play at state transitions
        self.state_transition_sounds = {
            GameAudioState.COMBAT: "battle_start",
            GameAudioState.VICTORY: "victory_cheer",
            GameAudioState.DEFEAT: "defeat_sound"
        }
        
        self.logger.info("Audio state manager initialized")
    

    def change_state(self, new_state):
        """Change the audio state and play appropriate music/sounds."""
        if new_state == self.current_state:
            return
            
        self.logger.info(f"Changing audio state from {self.current_state} to {new_state}")
            
        # Play transition sound if applicable
        if new_state in self.state_transition_sounds:
            sound_name = self.state_transition_sounds[new_state]
            self.sound_manager.play_sound(sound_name)
        
        # Change music based on new state
        if new_state in self.state_music_map:
            music_name = self.state_music_map[new_state]
            
            # Try to play as a playlist first, fall back to single track if needed
            if hasattr(self.sound_manager, 'playlists') and music_name in self.sound_manager.playlists:
                self.sound_manager.play_playlist(music_name)
                self.logger.debug(f"Playing {music_name} playlist for state {new_state}")
            else:
                self.sound_manager.play_music(music_name)
                self.logger.debug(f"Playing {music_name} music track for state {new_state}")
                
        self.current_state = new_state
    

    def play_event_sound(self, sound_name):
        """Play a specific sound effect regardless of state."""
        self.logger.debug(f"Playing event sound: {sound_name}")
        self.sound_manager.play_sound(sound_name)
