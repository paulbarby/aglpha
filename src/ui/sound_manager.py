import pygame
import os
import json
import random
from src.utils.logger import Logger, try_except
from src.utils.config_manager import config_manager

class SoundManager:
    """Manages all game sounds and music."""
    
    def __init__(self):
        self.logger = Logger()
        try:
            pygame.mixer.init()
            self.logger.info("Sound system initialized successfully")
        except pygame.error as e:
            self.logger.error(f"Failed to initialize sound system: {e}", exc_info=True)
            
        self.sound_effects = {}
        self.music_tracks = {}
        
        # New playlist attributes
        self.playlists = {}
        self.current_playlist = None
        self.current_track_index = 0
        self.playlist_playing = False

        # Load settings from config
        self.sound_volume = config_manager.get_value("Audio", "sound_volume", 1.0)
        self.music_volume = config_manager.get_value("Audio", "music_volume", 1.0)
        self.master_volume = config_manager.get_value("Audio", "master_volume", 1.0)
        self.sound_enabled = config_manager.get_value("Audio", "sound_enabled", True)
        self.music_enabled = config_manager.get_value("Audio", "music_enabled", True)
        
        self.logger.info(f"Audio settings loaded: master={self.master_volume}, music={self.music_volume}, sound={self.sound_volume}, music_enabled={self.music_enabled}, sound_enabled={self.sound_enabled}")
    
    @try_except
    def load_sound(self, name, file_path):
        """Load a sound effect."""
        if not self.sound_enabled:
            return
            
        if name in self.sound_effects:
            self.logger.debug(f"Sound '{name}' already loaded")
            return
            
        if not os.path.exists(file_path):
            self.logger.warning(f"Sound file not found: {file_path}")
            return
            
        try:
            sound = pygame.mixer.Sound(file_path)
            self.sound_effects[name] = sound
            self._update_sound_volume(name)
            self.logger.debug(f"Successfully loaded sound: {name} from {file_path}")
        except pygame.error as e:
            self.logger.error(f"Could not load sound {file_path}: {e}")
    
    @try_except
    def load_music(self, name, file_path):
        """Load a music track."""
        if not self.music_enabled:
            return
            
        if name in self.music_tracks:
            self.logger.debug(f"Music '{name}' already loaded")
            return
            
        if not os.path.exists(file_path):
            self.logger.warning(f"Music file not found: {file_path}")
            # Create a placeholder so we don't keep trying to load it
            self.music_tracks[name] = None
            return
            
        self.music_tracks[name] = file_path
        self.logger.debug(f"Successfully registered music: {name} from {file_path}")
    
    @try_except
    def play_sound(self, name):
        """Play a sound effect."""
        if not self.sound_enabled:
            return
            
        if name in self.sound_effects and self.sound_effects[name] is not None:
            try:
                self.sound_effects[name].play()
                self.logger.debug(f"Playing sound: {name}")
            except pygame.error as e:
                self.logger.error(f"Error playing sound {name}: {e}")
        else:
            self.logger.warning(f"Attempted to play non-existent sound: {name}")
    
    @try_except
    def play_music(self, name, loops=-1):
        """Play a music track, looping by default."""
        if not self.music_enabled:
            return
            
        if name in self.music_tracks and self.music_tracks[name] is not None:
            try:
                pygame.mixer.music.load(self.music_tracks[name])
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                pygame.mixer.music.play(loops)
                self.logger.debug(f"Playing music: {name}")
            except pygame.error as e:
                self.logger.error(f"Could not play music {name}: {e}")
        else:
            self.logger.warning(f"Attempted to play non-existent music track: {name}")
    
    @try_except
    def stop_music(self, force=False):
        """Stop currently playing music."""
        if not self.music_enabled and not force:
            return
            
        try:
            pygame.mixer.music.stop()
            # Added: stop any running playlist
            if self.playlist_playing:
                self.playlist_playing = False
            self.logger.debug("Stopped music playback")
        except pygame.error as e:
            self.logger.error(f"Error stopping music: {e}")
    
    @try_except
    def pause_music(self):
        """Pause currently playing music."""
        if not self.music_enabled:
            return
            
        try:
            pygame.mixer.music.pause()
            self.logger.debug("Paused music playback")
        except pygame.error as e:
            self.logger.error(f"Error pausing music: {e}")
    
    @try_except
    def unpause_music(self):
        """Unpause music."""
        if not self.music_enabled:
            return
            
        try:
            pygame.mixer.music.unpause()
            self.logger.debug("Unpaused music playback")
        except pygame.error as e:
            self.logger.error(f"Error unpausing music: {e}")
    
    @try_except
    def set_master_volume(self, volume):
        """Set master volume (0.0 to 1.0)."""
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()
        self.logger.debug(f"Set master volume to {self.master_volume}")
        config_manager.set_value("Audio", "master_volume", self.master_volume)
    
    @try_except
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music_enabled:
            try:
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                self.logger.debug(f"Set music volume to {self.music_volume}")
            except pygame.error as e:
                self.logger.error(f"Error setting music volume: {e}")
        config_manager.set_value("Audio", "music_volume", self.music_volume)
    
    @try_except
    def set_sound_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sound_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()
        self.logger.debug(f"Set sound effects volume to {self.sound_volume}")
        config_manager.set_value("Audio", "sound_volume", self.sound_volume)
    
    @try_except
    def _update_sound_volume(self, sound_name):
        """Update volume for a specific sound effect."""
        if not self.sound_enabled:
            return
            
        if sound_name in self.sound_effects and self.sound_effects[sound_name] is not None:
            try:
                self.sound_effects[sound_name].set_volume(self.sound_volume * self.master_volume)
            except pygame.error as e:
                self.logger.error(f"Error updating sound volume for {sound_name}: {e}")
    
    @try_except
    def _update_all_volumes(self):
        """Update volume for all sounds and music."""
        if self.music_enabled:
            try:
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            except pygame.error as e:
                self.logger.error(f"Error updating music volume: {e}")
        
        if self.sound_enabled:
            for sound_name in self.sound_effects:
                self._update_sound_volume(sound_name)
    
    def enable_sound(self, enabled):
        """Enable or disable sound effects."""
        self.sound_enabled = enabled
        self.logger.info(f"Sound effects {'enabled' if enabled else 'disabled'}")
        config_manager.set_value("Audio", "sound_enabled", enabled)
    
    @try_except
    def enable_music(self, enabled):
        """Safely enable or disable music with improved error handling."""
        previous_state = self.music_enabled
        self.music_enabled = enabled
        
        # Stop current music if we're disabling music
        if previous_state and not enabled:
            self.stop_music(fadeout=500)
        # Start default music if we're enabling music and nothing is playing
        elif not previous_state and enabled and not pygame.mixer.music.get_busy():
            self.play_default_music()
        
        # Save to config
        from src.utils.config_manager import config_manager
        config_manager.set_value("AUDIO", "music_enabled", enabled)

    @try_except
    def load_playlists(self, config_file):
        """Load playlist configurations from a JSON file."""
        if not os.path.exists(config_file):
            self.logger.warning(f"Playlist config file not found: {config_file}")
            return False
            
        try:
            with open(config_file, 'r') as f:
                playlist_data = json.load(f)
                
            if 'playlists' not in playlist_data:
                self.logger.warning("Invalid playlist config format: 'playlists' key not found")
                return False
                
            self.playlists = playlist_data['playlists']
            self.logger.info(f"Successfully loaded {len(self.playlists)} playlists from {config_file}")
            
            # Verify and log each playlist
            for playlist_name, playlist in self.playlists.items():
                if 'files' in playlist:
                    self.logger.debug(f"Processing playlist: {playlist_name} with {len(playlist['files'])} tracks")
                    missing_files = []
                    valid_files = []
                    
                    # Verify each music file exists
                    for i, file_path in enumerate(playlist['files']):
                        # Normalize path separators for the current OS
                        normalized_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), file_path))
                        
                        if os.path.exists(normalized_path):
                            track_name = f"{playlist_name}_{i}"
                            self.load_music(track_name, normalized_path)
                            valid_files.append(file_path)
                        else:
                            missing_files.append(file_path)
                    
                    # Log results for this playlist
                    if missing_files:
                        self.logger.warning(f"Playlist '{playlist_name}': {len(missing_files)} of {len(playlist['files'])} files not found")
                        for missing in missing_files:
                            self.logger.warning(f"  Missing file: {missing}")
                    
                    if valid_files:
                        self.logger.info(f"Playlist '{playlist_name}': {len(valid_files)} valid tracks loaded")
                        for valid in valid_files[:3]:  # Log first 3 files to avoid excessive logging
                            self.logger.debug(f"  Valid file: {valid}")
                        if len(valid_files) > 3:
                            self.logger.debug(f"  ... and {len(valid_files) - 3} more")
                    else:
                        self.logger.error(f"Playlist '{playlist_name}' has no valid files!")
            
            return True
        except Exception as e:
            self.logger.error(f"Error loading playlist config: {e}", exc_info=True)
            return False
    
    @try_except
    def set_playlist(self, playlist_name):
        """Set the current playlist."""
        if not self.music_enabled:
            return False
            
        if playlist_name not in self.playlists:
            self.logger.warning(f"Playlist not found: {playlist_name}")
            return False
            
        self.stop_music()
        self.current_playlist = playlist_name
        self.current_track_index = 0
        self.playlist_playing = False
        self.logger.debug(f"Set current playlist to: {playlist_name}")
        return True
    
    @try_except
    def play_playlist(self, playlist_name=None, restart=False):
        """Start or continue playing the current playlist or a specified one."""
        if not self.music_enabled:
            return
            
        # If a playlist name is provided, set it as the current playlist
        if playlist_name:
            if not self.set_playlist(playlist_name):
                return
        
        # Make sure we have a playlist set
        if not self.current_playlist:
            self.logger.warning("No playlist selected")
            return
            
        # Reset the index if restarting or not playing
        if restart or not self.playlist_playing:
            self.current_track_index = 0
            
        self.playlist_playing = True
        self._play_current_playlist_track()
        
    @try_except
    def _play_current_playlist_track(self):
        """Play the current track from the active playlist."""
        if not self.music_enabled or not self.playlist_playing:
            return
            
        playlist = self.playlists[self.current_playlist]
        files = playlist['files']
        play_mode = playlist.get('play_mode', 'sequential')
        
        if not files:
            self.logger.warning(f"Playlist '{self.current_playlist}' has no files")
            self.playlist_playing = False
            return
            
        # Select the track based on the play mode
        if play_mode == 'random':
            track_index = random.randint(0, len(files) - 1)
        else:  # sequential
            track_index = self.current_track_index
            
        # Get the track file
        file_path = files[track_index]
        track_name = f"{self.current_playlist}_{track_index}"
        
        # Use existing play_music method
        self.play_music(track_name, loops=0)  # Loop=0 means play once
        
        # Register music end event if not already registered
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
    
    @try_except
    def handle_event(self, event):
        """Handle pygame events for music playback."""
        if event.type == pygame.USEREVENT + 1 and self.playlist_playing:
            self._play_next_playlist_track()
    
    @try_except
    def _play_next_playlist_track(self):
        """Play the next track in the current playlist."""
        if not self.current_playlist or not self.playlist_playing:
            return
            
        playlist = self.playlists[self.current_playlist]
        play_mode = playlist.get('play_mode', 'sequential')
        repeat = playlist.get('repeat', True)
        
        if play_mode == 'sequential':
            self.current_track_index += 1
            if self.current_track_index >= len(playlist['files']):
                if repeat:
                    self.current_track_index = 0
                else:
                    self.playlist_playing = False
                    return
                    
        self._play_current_playlist_track()
    
    @try_except
    def stop_playlist(self):
        """Stop the currently playing playlist."""
        self.playlist_playing = False
        self.stop_music()
        self.logger.debug("Stopped playlist playback")

    @try_except
    def play_default_music(self):
        """Play a default music track as fallback."""
        # Find any available music track
        if hasattr(self, "music_tracks") and self.music_tracks:
            track_name = next(iter(self.music_tracks.keys()))
            self.play_music(track_name)