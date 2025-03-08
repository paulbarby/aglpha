import os
import json
from typing import Dict, List, Tuple

# Extensions typically used for different audio types
MUSIC_EXTENSIONS = ['.mp3', '.ogg']
SOUND_EXTENSIONS = ['.wav', '.ogg']  # .ogg can be used for both

class SoundAssetsIndex:
    """
    Indexes all audio files in the assets/sounds directory.
    Provides easy access to file paths and categorizes them as music or sound effects.
    """
    
    def __init__(self):
        self.base_dir = self._get_base_dir()
        self.sound_dir = os.path.join(self.base_dir, "assets", "sounds")
        self.music_dir = os.path.join(self.base_dir, "assets", "music")
        
        # Music and sound effect dictionaries
        self.music_files: Dict[str, str] = {}
        self.sound_files: Dict[str, str] = {}
        
        # Playlists from config
        self.playlists: Dict[str, List[str]] = {}
        
        # Scan the directories to populate the dictionaries
        self._scan_sound_directory()
        self._scan_music_directory()
        self._load_music_config()
    
    def _get_base_dir(self) -> str:
        """Get the base directory of the game."""
        # Start from this file's directory and go up to the project root
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return current_dir
    
    def _load_music_config(self):
        """Load music playlists from config file."""
        config_path = os.path.join(self.base_dir, "config", "music_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                if "playlists" in config:
                    for playlist_name, playlist_data in config["playlists"].items():
                        if "files" in playlist_data:
                            self.playlists[playlist_name] = [
                                os.path.join(self.music_dir, file) if not os.path.isabs(file) else file
                                for file in playlist_data["files"]
                            ]
            except Exception as e:
                print(f"Error loading music config: {e}")
    
    def _scan_sound_directory(self):
        """Scan the sounds directory and categorize files."""
        if not os.path.exists(self.sound_dir):
            os.makedirs(self.sound_dir)
            print(f"Created missing sound directory: {self.sound_dir}")
            return
        
        # Scan the main sounds directory
        self._scan_directory(self.sound_dir)
        
        # Scan any subdirectories for organization
        for item in os.listdir(self.sound_dir):
            subdir_path = os.path.join(self.sound_dir, item)
            if os.path.isdir(subdir_path):
                self._scan_directory(subdir_path)
    
    def _scan_music_directory(self):
        """Scan the music directory for audio files."""
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)
            print(f"Created missing music directory: {self.music_dir}")
            return
        
        for filename in os.listdir(self.music_dir):
            file_path = os.path.join(self.music_dir, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Get file extension and base name
            _, extension = os.path.splitext(filename)
            base_name = os.path.splitext(filename)[0]
            
            # Create a music ID from the file name
            music_id = base_name.replace(" ", "_").lower()
            
            # Categorize by extension
            if extension.lower() in MUSIC_EXTENSIONS:
                self.music_files[music_id] = file_path
    
    def _scan_directory(self, directory: str):
        """Scan a specific directory for audio files."""
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Get file extension and base name
            _, extension = os.path.splitext(filename)
            base_name = os.path.splitext(filename)[0]
            
            # Create a sound ID from the file name
            sound_id = base_name.replace(" ", "_").lower()
            
            # Categorize by extension
            if extension.lower() in MUSIC_EXTENSIONS:
                self.music_files[sound_id] = file_path
            elif extension.lower() in SOUND_EXTENSIONS:
                self.sound_files[sound_id] = file_path
    
    def get_all_sound_paths(self) -> Dict[str, str]:
        """Get all sound effect file paths."""
        return self.sound_files
    
    def get_all_music_paths(self) -> Dict[str, str]:
        """Get all music file paths."""
        return self.music_files
    
    def get_sound_path(self, sound_id: str) -> str:
        """Get the path for a specific sound effect."""
        return self.sound_files.get(sound_id)
    
    def get_music_path(self, music_id: str) -> str:
        """Get the path for a specific music track."""
        return self.music_files.get(music_id)
    
    def get_playlist(self, playlist_name: str) -> List[str]:
        """Get all music file paths for a specific playlist."""
        return self.playlists.get(playlist_name, [])
    
    def print_asset_index(self):
        """Print all indexed assets for debugging."""
        print("\n=== Music Files ===")
        for name, path in self.music_files.items():
            print(f"{name}: {path}")
        
        print("\n=== Sound Effect Files ===")
        for name, path in self.sound_files.items():
            print(f"{name}: {path}")
        
        print("\n=== Playlists ===")
        for name, files in self.playlists.items():
            print(f"{name}: {len(files)} tracks")
            for file in files:
                print(f"  - {os.path.basename(file)}")


# Create a singleton instance
sound_assets = SoundAssetsIndex()
