# Game Engine Class Specifications Summary

This document summarizes the core classes and managers designed for the Civilization-inspired strategy game. Each section outlines responsibilities, key properties, and methods.

---

## Enumerations

- **GameState**

  - **Purpose:** Tracks the overall game flow.
  - **Values:** `MAIN_MENU`, `IN_GAME`, `PAUSED`, `GAME_OVER`.

- **UnitState**

  - **Purpose:** Represents the various states of a unit during gameplay.
  - **Values:** `IDLE`, `MOVING`, `ATTACKING`, `DEFENDING`, `SELECTED`, `DESTROYED`.

- **CityStatus**

  - **Purpose:** Indicates the current condition or status of a city.
  - **Values:** `PEACEFUL`, `UNDER_ATTACK`, `DEVELOPING`, `AT_WAR`.

- **AIState**

  - **Purpose:** Defines the behavioral state for AI players.
  - **Values:** `IDLE`, `EXPANDING`, `ATTACKING`, `DEFENSIVE`, `DIPLOMATIC`.

- **AnimationState**

  - **Purpose:** Represents the current animation phase for game objects.
  - **Values:** `IDLE`, `WALKING`, `ATTACKING`, `DYING`, `SPAWNING`.

- **GameAudioState**
  - **Purpose:** Defines different audio contexts throughout the game.
  - **Values:** `MAIN_MENU`, `GAMEPLAY`, `COMBAT`, `VICTORY`, `DEFEAT`, `OPTIONS_MENU`.

---

## Core Engine Components

### GameEngine

- **Responsibilities:**  
  Coordinates the overall game flow, turn management, and integrates various managers.

- **Key Properties:**

  - `game_state`: Current state of the game (from **GameState**).
  - `turn`: Current turn counter.
  - `players`: List of players (human and AI).
  - `map`: Instance of the **Map** class representing the game world.
  - Managers for units, cities, AI, events, UI, animations, and sound.

- **Key Methods:**
  - `update()`: Calls updates on all managers to progress game logic.
  - `handle_event(event)`: Processes both pygame events and game-specific events.
  - `_load_default_audio()`: Initializes the audio system with sounds and music.

---

### Map & Tile

#### Map

- **Responsibilities:**  
  Holds the game world grid and supports procedural generation (e.g., using Perlin noise).

- **Key Properties:**
  - `width`, `height`: Dimensions of the map.
  - `tiles`: 2D list of **Tile** objects.

#### Tile

- **Responsibilities:**  
  Represents an individual map cell with a terrain type.

- **Key Properties:**
  - `tile_type`: Type of terrain (e.g., grassland, forest).
  - `position`: Coordinates (x, y).
  - `explored_by`: List of players that have explored this tile.

---

## Domain-Specific Components

### Unit & UnitManager

#### Unit

- **Responsibilities:**  
  Represents a game unit with its behavior and combat capabilities.

- **Key Properties:**
  - `id`: Unique identifier.
  - `unit_type`: E.g., "Spearmen", "Cavalry".
  - `position`: (x, y) coordinate.
  - `state`: Current **UnitState**.
  - `health`, `attack_power`, `defense`, `move_range`.
  - `current_animation`: Reference to an active **Animation** (if any).

#### UnitManager

- **Responsibilities:**  
  Manages all game units and updates their behaviors.

- **Key Properties:**

  - `units`: Dictionary mapping unit IDs to **Unit** objects.

- **Key Methods:**
  - `add_unit(unit)`: Adds a new unit.
  - `update_units()`: Processes unit behavior per game tick or turn.

---

### City & CityManager

#### City

- **Responsibilities:**  
  Represents a city with aspects of growth, resource management, and production.

- **Key Properties:**
  - `id`, `name`, `position`.
  - `status`: Current **CityStatus**.
  - `population`.
  - `resources`: Dictionary of resources (food, wood, stone, gold).
  - `buildings`: List of constructed buildings (e.g., Granaries, Workshops).
  - `production_queue`: Items (units/buildings) in production.

#### CityManager

- **Responsibilities:**  
  Oversees city management, resource updates, and production.

- **Key Properties:**

  - `cities`: Dictionary mapping city IDs to **City** objects.

- **Key Methods:**
  - `add_city(city)`: Registers a new city.
  - `update_cities()`: Updates each city's growth and resource status.

---

### AI Components

#### AIPlayer

- **Responsibilities:**  
  Represents an AI-controlled player with strategic decision-making.

- **Key Properties:**

  - `id`, `name`.
  - `state`: Current **AIState**.
  - `controlled_units`: List of unit IDs under AI control.
  - `controlled_cities`: List of city IDs under AI control.
  - `strategy`: Tactical approach (e.g., "balanced", "aggressive").

- **Key Method:**
  - `make_decision()`: Implements AI decision logic.

#### AIManager

- **Responsibilities:**  
  Manages AI players and triggers their decision-making processes.

- **Key Properties:**

  - `ai_players`: Dictionary mapping AI IDs to **AIPlayer** objects.

- **Key Methods:**
  - `add_ai_player(ai_player)`: Adds a new AI player.
  - `update_ai()`: Updates the state and decisions of all AI players.

---

### Event & EventManager

#### Event

- **Responsibilities:**  
  Represents game events (e.g., unit movement, combat, city updates).

- **Key Properties:**
  - `id`: Unique identifier for the event.
  - `event_type`: Type of event (e.g., "unit_move", "combat").
  - `data`: Dictionary holding event-specific details.
  - `timestamp`: Time when the event occurred.

#### EventManager

- **Responsibilities:**  
  Processes and dispatches events to the appropriate handlers.

- **Key Properties:**

  - `event_queue`: List of pending **Event** objects.

- **Key Methods:**
  - `add_event(event)`: Queues a new event.
  - `process_events()`: Iterates over and processes events.
  - `handle_event(event)`: Dispatches event based on its type.

---

### Audio Components

#### SoundManager

- **Responsibilities:**  
  Handles loading, playback, and volume control of all game audio.

- **Key Properties:**

  - `sound_effects`: Dictionary of loaded sound effect objects.
  - `music_tracks`: Dictionary of music track file paths.
  - `playlists`: Dictionary of playlist configurations.
  - `sound_volume`, `music_volume`, `master_volume`: Volume levels.
  - `sound_enabled`, `music_enabled`: Toggle flags for audio categories.

- **Key Methods:**
  - `load_sound(name, file_path)`: Registers a sound effect.
  - `load_music(name, file_path)`: Registers a music track.
  - `play_sound(name)`: Plays a sound effect.
  - `play_music(name, fadeout, loops)`: Plays a music track.
  - `play_playlist(playlist_name)`: Plays tracks from a configured playlist.
  - `set_master_volume(volume)`: Controls overall volume.

#### AudioStateManager

- **Responsibilities:**  
  Manages audio transitions between different game states.

- **Key Properties:**

  - `current_state`: Current GameAudioState value.
  - `state_music_map`: Maps game states to music tracks.
  - `state_transition_sounds`: Maps state changes to sound effects.

- **Key Methods:**
  - `change_state(new_state)`: Updates audio state and plays appropriate music/sounds.
  - `play_event_sound(sound_name)`: Plays a specific sound regardless of state.

#### SoundAssetsIndex

- **Responsibilities:**  
  Indexes and provides access to all audio files in the game directory.

- **Key Properties:**

  - `music_files`: Dictionary mapping IDs to music file paths.
  - `sound_files`: Dictionary mapping IDs to sound effect file paths.
  - `playlists`: Dictionary of configured playlist data.

- **Key Methods:**
  - `get_sound_path(sound_id)`: Retrieves path for a specific sound effect.
  - `get_music_path(music_id)`: Retrieves path for a specific music track.
  - `get_all_sound_paths()`: Returns all indexed sound effect paths.
  - `get_all_music_paths()`: Returns all indexed music track paths.

---

### UI Components

#### UIManager

- **Responsibilities:**  
  Manages all user interface elements and their interactions.

- **Key Properties:**

  - `ui_elements`: Dictionary of UI elements.
  - `active_screen`: Currently active UI screen.

- **Key Methods:**
  - `is_options_button_clicked(pos)`: Checks if the options button was clicked.
  - `update_ui()`: Updates UI elements based on game state.
  - `render(screen)`: Draws all visible UI elements.

#### OptionsMenuScreen

- **Responsibilities:**  
  Provides interface for adjusting game settings, particularly audio.

- **Key Properties:**

  - `sound_manager`: Reference to the game's SoundManager.
  - Various UI elements: sliders, buttons, etc.

- **Key Methods:**
  - `handle_event(event)`: Processes UI interactions.
  - `toggle_music()`, `toggle_sound()`: Toggle audio categories.
  - `on_master_volume_change()`, `on_music_volume_change()`, `on_sound_volume_change()`: Handle slider adjustments.

---

This structured specification provides a modular and extensible foundation for the game engine, ensuring that core systems such as state management, AI, events, animations, audio, and UI are clearly defined and easily maintainable.
