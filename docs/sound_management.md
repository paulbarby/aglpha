# Sound Management System

## Overview

The game's sound management system handles both music and sound effects, providing a complete audio experience. The system consists of several integrated components that work together to provide audio feedback, background music, and state-based audio transitions.

## Architecture

### Core Components

1. **SoundManager** (`src.ui.sound_manager`)

   - Handles direct playback of sounds and music
   - Manages volume levels for different audio types
   - Tracks enabled/disabled state for sound categories
   - Supports playlist-based music playback

2. **AudioStateManager** (`src.engine.audio_state_manager`)

   - Maps game states to appropriate music and sounds
   - Handles state transitions with appropriate audio cues
   - Defines the GameAudioState enum (MAIN_MENU, GAMEPLAY, COMBAT, etc.)

3. **SoundAssetsIndex** (`src.utils.sound_assets_index`)

   - Scans asset directories to locate sound and music files
   - Provides lookup methods to find audio files by ID
   - Loads playlist configurations from JSON

4. **Configuration Management** (`src.utils.config_manager`)
   - Stores and retrieves user audio preferences
   - Maintains volume levels and enabled states

## Sound Implementation

### Audio File Organization

The system automatically scans and indexes audio files from these directories:

- `assets/sounds/` - For sound effects (WAV, OGG)
- `assets/music/` - For music tracks (MP3, OGG)

Audio files are automatically registered with an ID based on their filename:

```
assets/sounds/unit_move.wav → "unit_move"
assets/music/main_theme.mp3 → "main_theme"
```

### Adding New Sound Effects

1. **Add the sound file to the assets directory**:

   - Place your WAV or OGG file in `assets/sounds/` or a subdirectory
   - The file will be automatically indexed on game startup

2. **Play the sound in your code**:

```python
# The sound ID is derived from the filename (without extension)
self.sound_manager.play_sound("unit_move")
```

### Adding Background Music

1. **Add the music file to the assets directory**:

   - Place your MP3 or OGG file in `assets/music/`
   - The file will be automatically indexed on game startup

2. **Play individual music tracks**:

```python
# Simple playback
self.sound_manager.play_music("main_theme")

# With fade-in effect (1000ms)
self.sound_manager.play_music("main_theme", fadeout=1000)
```

### Using Music Playlists

The game supports playlist-based music playback through the `music_config.json` file:

1. **Define playlists in the config file**:

```json
{
  "playlists": {
    "combat_music": {
      "files": [
        "assets/music/combat_music_1.mp3",
        "assets/music/combat_music_2.mp3",
        "assets/music/combat_music_3.mp3"
      ],
      "play_mode": "random",
      "repeat": true
    }
  }
}
```

2. **Play the playlist**:

```python
self.sound_manager.play_playlist("combat_music")
```

## Audio State Management

The AudioStateManager handles the relationship between game states and audio:

```python
class GameAudioState(Enum):
    """Enum for various game audio states."""
    MAIN_MENU = auto()
    GAMEPLAY = auto()
    COMBAT = auto()
    VICTORY = auto()
    DEFEAT = auto()
    OPTIONS_MENU = auto()
```

Each state is mapped to appropriate music:

```python
self.state_music_map = {
    GameAudioState.MAIN_MENU: "main_menu_music",
    GameAudioState.GAMEPLAY: "gameplay_music",
    GameAudioState.COMBAT: "combat_music",
    # ...
}
```

And state transitions can trigger sound effects:

```python
self.state_transition_sounds = {
    GameAudioState.COMBAT: "battle_start",
    GameAudioState.VICTORY: "victory_cheer",
    GameAudioState.DEFEAT: "defeat_sound"
}
```

### Using Audio States

To change the game's audio state:

```python
# Change to combat music and play battle start sound
self.audio_state_manager.change_state(GameAudioState.COMBAT)
```

## UI Integration

### Options Menu Sound Controls

The game's options menu (`src.ui.options_menu.OptionsMenuScreen`) provides:

1. **Volume sliders** for:

   - Master volume
   - Music volume
   - Sound effects volume

2. **Toggle buttons** for:
   - Enable/disable music
   - Enable/disable sound effects

### Implementation Example

The OptionsMenuScreen includes handlers for these controls:

```python
def on_master_volume_change(self, value):
    """Handle master volume slider change."""
    self.sound_manager.set_master_volume(value)
    return True  # Operation was successful

def on_music_volume_change(self, value):
    """Handle music volume slider change."""
    self.sound_manager.set_music_volume(value)
    return True  # Operation was successful

def toggle_music(self):
    """Toggle music on/off."""
    handled = self.toggle_music_safely()
    if handled:
        new_state = self.sound_manager.music_enabled
        self.music_toggle_btn.set_text("Music: ON" if new_state else "Music: OFF")
```

### Adding Sound to UI Elements

Sound effects can be added to UI interactions:

```python
def handle_click(self, pos):
    if self.active and self.rect.collidepoint(pos):
        # Play UI sound
        self.game_engine.sound_manager.play_sound("button_click")

        # Execute action
        if self.action:
            self.action()
        return True
    return False
```

## System Initialization

The GameEngine initializes the sound system during startup:

```python
def _load_default_audio(self):
    """Load the default game audio files."""
    # Get indexed music files and load them
    music_files = sound_assets.get_all_music_paths()
    for name, path in music_files.items():
        self.sound_manager.load_music(name, path)

    # Get indexed sound effect files and load them
    sound_files = sound_assets.get_all_sound_paths()
    for name, path in sound_files.items():
        self.sound_manager.load_sound(name, path)

    # Load playlist configurations
    self.sound_manager.load_playlists("config/music_config.json")

    # Set initial audio state
    self.audio_state_manager.change_state(GameAudioState.MAIN_MENU)
```

## Error Handling and Fallbacks

The system includes robust error handling:

1. **Missing audio files** are logged but don't crash the game
2. **Fallback tracks** are used when specified audio is missing
3. **Playlist validation** ensures playlists have valid files

```python
def _ensure_essential_audio_mappings(self):
    """Ensure all required audio for the state manager exists in some form."""
    # Map essential audio states to playlists or tracks
    # If primary options aren't available, use fallbacks
    # ...
```

## Best Practices for Adding Sounds

1. **Naming Convention**: Use descriptive, lowercase names with underscores

   - `unit_move.wav` rather than `UnitMove.wav`

2. **File Organization**: Use subdirectories for categories

   - `assets/sounds/ui/` for interface sounds
   - `assets/sounds/units/` for unit-related sounds

3. **Audio Formats**:

   - Sound effects: WAV or OGG (44.1kHz, 16-bit)
   - Music: MP3 or OGG (quality level appropriate for file size constraints)

4. **Volume Consistency**:

   - Normalize volume levels across similar sound types
   - Test sound effects at different master volume settings

5. **Context-Appropriate Audio**:

   - Use terrain-specific sounds:

   ```python
   if terrain == TerrainType.WATER:
       self.sound_manager.play_sound("unit_move_water")
   elif terrain == TerrainType.FOREST:
       self.sound_manager.play_sound("unit_move_forest")
   ```

6. **Audio Cooldowns**:

   - Implement cooldown for repetitive sounds:

   ```python
   current_time = pygame.time.get_ticks()
   if current_time - self.last_sound_time > 500:  # 500ms cooldown
       self.sound_manager.play_sound("click")
       self.last_sound_time = current_time
   ```

7. **Save User Preferences**:
   - Always save audio settings changes:
   ```python
   config_manager.set_value("Audio", "music_volume", new_volume)
   ```

## Playlist Configuration

The `music_config.json` file defines playlists with these properties:

```json
{
  "playlists": {
    "main_menu_playlist": {
      "files": ["assets/music/track1.mp3", "assets/music/track2.mp3"],
      "play_mode": "sequential", // or "random"
      "repeat": true
    }
  }
}
```

- `play_mode`: "sequential" or "random"
- `repeat`: Whether to repeat the playlist when finished
