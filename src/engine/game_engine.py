from src.engine.core_states import GameState
from src.engine.map import Map
from src.unit.unit_manager import UnitManager
from src.city.city_manager import CityManager
from src.ai.ai_manager import AIManager
from src.ui.ui_manager import UIManager
from src.event.event_manager import EventManager
from src.ui.animation_manager import AnimationManager
from src.player.player_manager import PlayerManager
from src.ui.sound_manager import SoundManager
from src.engine.audio_state_manager import AudioStateManager, GameAudioState
from src.ui.options_menu import OptionsMenuScreen
from src.utils.logger import Logger
from src.utils.sound_assets_index import sound_assets
from src.utils.config_manager import config_manager
import os
import pygame  # Add this import for pygame event types

class GameEngine:
    def __init__(self):
        # Initialize logger first
        self.logger = Logger()
        self.logger.info("Game engine initializing...")
        
        # Check for audio debug mode in config
        self.audio_debug = config_manager.get_value("DEBUG", "audio_debug", False)
        if self.audio_debug:
            self.logger.info("Audio debug logging is ENABLED")
        
        # Global game state and turn management
        self.game_state = GameState.MAIN_MENU
        self.turn = 0
        self.game_name = ""  # Store new game name
        
        # Replace players list with PlayerManager
        self.player_manager = PlayerManager()
        self.map = Map()   # procedural map using tiles
        
        # Managers for different domains of the game
        self.unit_manager = UnitManager()
        self.city_manager = CityManager()
        self.ai_manager = AIManager()
        self.ui_manager = UIManager()
        self.event_manager = EventManager()
        self.animation_manager = AnimationManager()
        
        # Initialize sound subsystem
        self.sound_manager = SoundManager()
        self.audio_state_manager = AudioStateManager(self.sound_manager)
        
        # Load default sounds and music
        self._load_default_audio()
        
        # Set initial audio state to main menu music
        self.audio_state_manager.change_state(GameAudioState.MAIN_MENU)
        
        self.options_menu = None
        self.screen = None  # Will be set later
        
        self.logger.info("Game engine initialized successfully")

    def set_screen(self, screen):
        """Set the game screen reference."""
        self.screen = screen
        self.logger.info("Game screen reference set")

    def _load_default_audio(self):
        """Load the default game audio files."""
        self.logger.info("Loading audio assets...")
        
        # Add error tracking for audio loading
        audio_load_errors = 0
        
        # Get indexed music files and load them
        music_files = sound_assets.get_all_music_paths()
        if self.audio_debug:
            self.logger.debug(f"Available music tracks: {list(music_files.keys())}")
        
        for name, path in music_files.items():
            if os.path.exists(path):
                try:
                    self.sound_manager.load_music(name, path)
                    if self.audio_debug:
                        self.logger.debug(f"Successfully loaded music: {name} from {path}")
                except Exception as e:
                    audio_load_errors += 1
                    self.logger.error(f"Error loading music '{name}': {str(e)}")
            else:
                audio_load_errors += 1
                error_msg = f"Music file not found: {path}"
                self.logger.warning(error_msg)
                if self.audio_debug:
                    self.logger.debug(f"Failed to load music '{name}'. File does not exist at path: {path}")
                    self.logger.debug(f"Current working directory: {os.getcwd()}")
        
        # Get indexed sound effect files and load them
        sound_files = sound_assets.get_all_sound_paths()
        if self.audio_debug:
            self.logger.debug(f"Available sound effects: {list(sound_files.keys())}")
            
        for name, path in sound_files.items():
            if os.path.exists(path):
                try:
                    self.sound_manager.load_sound(name, path)
                    if self.audio_debug:
                        self.logger.debug(f"Successfully loaded sound: {name} from {path}")
                except Exception as e:
                    audio_load_errors += 1
                    self.logger.error(f"Error loading sound '{name}': {str(e)}")
            else:
                audio_load_errors += 1
                self.logger.warning(f"Sound file not found: {path}")
                if self.audio_debug:
                    self.logger.debug(f"Failed to load sound '{name}'. File does not exist at path: {path}")
        
        if audio_load_errors > 0:
            self.logger.warning(f"Encountered {audio_load_errors} errors while loading audio assets")
        
        # Load playlist configurations from the JSON file
        config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "music_config.json")
        if os.path.exists(config_file):
            try:
                # Try to load and validate the JSON file before passing to sound_manager
                validated_config = self._validate_and_repair_json(config_file)
                if validated_config:
                    # Use the validated JSON directly
                    self.sound_manager.playlists = validated_config.get("playlists", {})
                    self.logger.info(f"Music playlists loaded from {config_file}")
                    if self.audio_debug:
                        self.logger.debug(f"Playlist configuration loaded successfully")
                        self.logger.debug(f"Loaded playlists: {list(validated_config.get('playlists', {}).keys())}")
                else:
                    # Fall back to letting sound_manager try loading
                    self.sound_manager.load_playlists(config_file)
            except Exception as e:
                self.logger.error(f"Error loading playlist config: {str(e)}")
                if self.audio_debug:
                    self._display_json_error_location(config_file, e)
        else:
            self.logger.warning(f"Music config file not found: {config_file}")
            if self.audio_debug:
                self.logger.debug(f"Music config file not found at: {config_file}")
                self.logger.debug(f"Expected full path: {os.path.abspath(config_file)}")
        
        self.logger.info(f"Audio assets loading completed. {len(music_files)} music tracks and {len(sound_files)} sound effects indexed.")
        
        # Ensure essential audio is defined for the audio state manager
        self._ensure_essential_audio_mappings()
    
    def _validate_and_repair_json(self, json_file_path):
        """Validate and attempt to repair common JSON syntax errors."""
        try:
            with open(json_file_path, 'r') as f:
                content = f.read()
                
            # Try to parse as-is first
            try:
                import json
                return json.loads(content)
            except json.JSONDecodeError as e:
                if self.audio_debug:
                    self.logger.debug(f"JSON validation error: {str(e)}")
                    self._display_json_error_location(json_file_path, e)
                
                # Common repairs:
                # 1. Fix property names without quotes
                import re
                # Look for patterns like {key: value, instead of {"key": value,
                fixed_content = re.sub(r'(\{|\,)\s*([a-zA-Z0-9_]+)\s*:', r'\1 "\2":', content)
                
                # 2. Fix trailing commas in objects and arrays
                fixed_content = re.sub(r',(\s*[\}\]])', r'\1', fixed_content)
                
                if fixed_content != content:
                    if self.audio_debug:
                        self.logger.debug("Attempted to repair JSON syntax")
                    
                    # Save the fixed JSON
                    backup_path = json_file_path + ".backup"
                    try:
                        import shutil
                        shutil.copy2(json_file_path, backup_path)
                        self.logger.info(f"Created backup of original config at {backup_path}")
                        
                        with open(json_file_path, 'w') as f:
                            f.write(fixed_content)
                        self.logger.info(f"Saved repaired JSON configuration")
                        
                        # Try to parse the fixed content
                        return json.loads(fixed_content)
                    except Exception as repair_err:
                        self.logger.error(f"Failed to repair JSON: {str(repair_err)}")
                        return None
                else:
                    self.logger.warning("Could not automatically repair JSON syntax")
                    return None
        except Exception as e:
            self.logger.error(f"Error validating JSON file: {str(e)}")
            return None
    
    def _display_json_error_location(self, json_file_path, error):
        """Display the location of a JSON error with context."""
        try:
            if not hasattr(error, 'lineno') or not hasattr(error, 'colno'):
                self.logger.debug(f"Error details not available")
                return
            
            with open(json_file_path, 'r') as f:
                lines = f.readlines()
                
            error_line = error.lineno - 1  # 0-based index
            if error_line < 0 or error_line >= len(lines):
                self.logger.debug(f"Error line {error.lineno} out of range")
                return
                
            # Get the problematic line and position
            line = lines[error_line]
            self.logger.debug(f"Error at line {error.lineno}, column {error.colno}")
            self.logger.debug(f"Problematic line: {line.rstrip()}")
            
            # Show position with a marker
            position_marker = ' ' * (error.colno - 1) + '^'
            self.logger.debug(f"Position:        {position_marker}")
            
            # Show surrounding context (3 lines before and after)
            start = max(0, error_line - 3)
            end = min(len(lines), error_line + 4)
            
            context = []
            for i in range(start, end):
                prefix = "-> " if i == error_line else "   "
                context.append(f"{prefix}{i+1}: {lines[i].rstrip()}")
            
            self.logger.debug("Context:")
            for ctx_line in context:
                self.logger.debug(ctx_line)
                
        except Exception as e:
            self.logger.debug(f"Error displaying JSON error location: {str(e)}")

    def _ensure_essential_audio_mappings(self):
        """Ensure all required audio for the state manager exists in some form."""
        self.logger.info("Ensuring essential audio mappings...")
        
        # Define mappings between game audio states and playlist/track names
        state_to_playlist_mappings = {
            "MAIN_MENU": ["main_menu_playlist", "menu_playlist", "title_playlist"],
            "GAMEPLAY": ["gameplay_playlist", "world_playlist", "main_gameplay_playlist"],
            "COMBAT": ["combat_playlist", "battle_playlist", "war_playlist"],
            "VICTORY": ["victory_playlist", "win_playlist"],
            "DEFEAT": ["defeat_playlist", "game_over_playlist"],
            "OPTIONS_MENU": ["menu_playlist", "ui_playlist"]
        }
        
        # Define fallback individual tracks if playlists aren't available
        required_music = {
            "main_menu_music": ["main_menu", "menu", "title"],
            "gameplay_music": ["gameplay", "game", "world"],
            "combat_music": ["combat", "battle", "fight"],
            "victory_music": ["victory", "win"],
            "defeat_music": ["defeat", "lose", "game_over"]
        }
        
        required_sounds = {
            "button_click": ["click", "button"],
            "battle_start": ["battle_start", "combat_start"],
            "victory_cheer": ["victory_sound", "win_sound"],
            "defeat_sound": ["defeat_sound", "lose_sound"]
        }
        
        # Get available audio resources
        available_playlists = list(self.sound_manager.playlists.keys()) if hasattr(self.sound_manager, "playlists") else []
        available_music = list(sound_assets.get_all_music_paths().keys())
        available_sounds = list(sound_assets.get_all_sound_paths().keys())
        
        if self.audio_debug:
            self.logger.debug(f"Audio mapping - Available playlists: {available_playlists}")
            self.logger.debug(f"Audio mapping - Available music tracks: {available_music}")
            self.logger.debug(f"Audio mapping - Available sound effects: {available_sounds}")
            self.logger.debug(f"Audio mapping - Required music tracks: {list(required_music.keys())}")
            self.logger.debug(f"Audio mapping - Required sound effects: {list(required_sounds.keys())}")
            
            # Check if SoundManager has the expected attributes
            sound_mgr_attrs = [attr for attr in dir(self.sound_manager) if not attr.startswith('__')]
            self.logger.debug(f"SoundManager attributes: {sound_mgr_attrs}")
            
            # Check if AudioStateManager has the expected attributes
            audio_state_attrs = [attr for attr in dir(self.audio_state_manager) if not attr.startswith('__')]
            self.logger.debug(f"AudioStateManager attributes: {audio_state_attrs}")
        
        # First, ensure playlists are mapped to game states if available
        for state, playlist_options in state_to_playlist_mappings.items():
            # Find the first matching playlist
            found_playlist = next((playlist for playlist in playlist_options if playlist in available_playlists), None)
            
            if found_playlist:
                self.logger.info(f"Mapped {state} audio state to playlist '{found_playlist}'")
                # Register this mapping with the audio state manager
                self.audio_state_manager.register_playlist_for_state(state, found_playlist)
                if self.audio_debug:
                    self.logger.debug(f"Successfully mapped state '{state}' to playlist '{found_playlist}'")
                    if hasattr(self.sound_manager, "playlists") and found_playlist in self.sound_manager.playlists:
                        playlist_tracks = self.sound_manager.playlists[found_playlist]
                        self.logger.debug(f"Playlist '{found_playlist}' contains tracks: {playlist_tracks}")
            else:
                self.logger.warning(f"No playlist found for {state} state. Will fall back to individual tracks.")
                if self.audio_debug:
                    self.logger.debug(f"Failed to find playlist for state '{state}'. Searched for: {playlist_options}")
                    self.logger.debug(f"Will use individual tracks instead for state '{state}'")
        
        # Then, ensure individual tracks are available as fallbacks
        for required, alternates in required_music.items():
            all_options = [required] + alternates
            found_track = next((track for track in all_options if track in available_music), None)
            
            if not found_track:
                if available_music:
                    fallback_track = available_music[0]
                    self.logger.warning(f"Required music '{required}' not found. Using '{fallback_track}' instead.")
                    # Re-map the first available music to the required name
                    self.sound_manager.music_tracks[required] = sound_assets.get_music_path(fallback_track)
                    if self.audio_debug:
                        self.logger.debug(f"Required track '{required}' and alternates {alternates} not found.")
                        self.logger.debug(f"Using fallback track '{fallback_track}' for '{required}'")
            elif self.audio_debug and found_track != required:
                self.logger.debug(f"Using alternate track '{found_track}' for required track '{required}'")
        
        # Do the same for sound effects
        for required, alternates in required_sounds.items():
            all_options = [required] + alternates
            found_sound = next((sound for sound in all_options if sound in available_sounds), None)
            
            if not found_sound:
                if available_sounds:
                    fallback_sound = available_sounds[0]
                    self.logger.warning(f"Required sound '{required}' not found. Using '{fallback_sound}' instead.")
                    # Load the first available sound under the required name
                    self.sound_manager.load_sound(required, sound_assets.get_sound_path(fallback_sound))
                    if self.audio_debug:
                        self.logger.debug(f"Required sound '{required}' and alternates {alternates} not found.")
                        self.logger.debug(f"Using fallback sound '{fallback_sound}' for '{required}'")
            elif self.audio_debug and found_sound != required:
                self.logger.debug(f"Using alternate sound '{found_sound}' for required sound '{required}'")
        
        self.logger.info("Audio mappings completed.")
    
    def transition_to_options_menu(self):
        """Transition to the options menu."""
        self.logger.info("Transitioning to options menu")
        if self.screen is None:
            self.logger.error("Cannot show options menu: screen is not set")
            return
            
        self.options_menu = OptionsMenuScreen(self.screen, self.sound_manager, self.return_to_main_menu)
        if self.audio_debug:
            self.logger.debug("Changing audio state to OPTIONS_MENU")
        self.audio_state_manager.change_state(GameAudioState.OPTIONS_MENU)
    
    def return_to_main_menu(self):
        """Return to the main menu from options."""
        self.logger.info("Returning to main menu from options")
        self.options_menu = None
        self.game_state = GameState.MAIN_MENU  # Explicitly set game state to MAIN_MENU
        if self.audio_debug:
            self.logger.debug("Changing audio state to MAIN_MENU")
        self.audio_state_manager.change_state(GameAudioState.MAIN_MENU)
        
        # Ensure settings are saved when returning from options
        self.save_settings()
    
    def save_settings(self):
        """Save all current settings to config file."""
        # Settings are saved automatically when changed via the config_manager
        self.logger.info("Game settings saved")
        
    def shutdown(self):
        """Perform cleanup operations before shutting down the game."""
        self.logger.info("Game shutting down, saving settings...")
        # Save any final settings
        self.save_settings()
        
        # Final cleanup
        self.sound_manager.stop_music(force=True)
        pygame.quit()
        
        self.logger.info("Game shutdown complete")
        
    def handle_event(self, event):
        """Handle game events."""

        # Handle options menu events first if active (PRIORITY)
        if self.options_menu:
            # Let options menu handle the event first
            handled = self.options_menu.handle_event(event)
            
            # If options menu handled it or indicated it needs focus, don't process further
            if handled:
                return True
                
            # Check if this is a click event that might have closed the options menu
            if hasattr(event, 'type') and event.type == pygame.MOUSEBUTTONDOWN and not self.options_menu:
                # Options menu was closed during event handling (back button was clicked)
                # Prevent this same click from being processed by the main menu
                return True

        # Check for quit event first to ensure we save settings
        if hasattr(event, 'type') and event.type == pygame.QUIT:
            self.shutdown()
            return True  # Event was handled
        
        # Only if options menu is not active or didn't handle the event:
        if hasattr(event, 'type'):
            # Check for options button click event
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                # Check if options button was clicked
                if self.ui_manager.is_options_button_clicked(event.pos):
                    self.transition_to_options_menu()
                    return True  # Event was handled
        
        # Only process game events if we're not in options menu
        if not self.options_menu:
            # Handle existing event processing
            self.event_manager.process_events()
            self.animation_manager.update_animations()
            self.player_manager.update_players()
            self.unit_manager.update_units()
            self.city_manager.update_cities()
            self.ai_manager.update_ai()
            self.ui_manager.update_ui()
        
        return False  # Event wasn't specifically handled
    
    def update(self):
        """Update game state."""
        # Only update game components if not in options menu
        if not self.options_menu:
            self.event_manager.process_events()
            self.animation_manager.update_animations()
            self.player_manager.update_players()
            self.unit_manager.update_units()
            self.city_manager.update_cities()
            self.ai_manager.update_ai()
            self.ui_manager.update_ui()
        else:
            # Update only options menu if active
            try:
                self.options_menu.update()
            except Exception as e:
                self.logger.error(f"Error updating options menu: {str(e)}")
                self.return_to_main_menu()
    
    def render(self, screen):
        """Render the current game state."""
        # First check if options menu is active and render it
        if self.options_menu:
            self.options_menu.draw()
            return
            
        # Otherwise, use the UI manager to render the appropriate screen
        self.ui_manager.render(screen)
