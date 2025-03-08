import os
import sqlite3
import json
from datetime import datetime
from src.storage.game_data_dto import GameDataDTO
from src.player.player_serializer import PlayerSerializer
from src.engine.map_serializer import MapSerializer
from src.unit.unit_serializer import UnitSerializer
from src.city.city_serializer import CitySerializer

class GameStorageManager:
    """
    Handles all game storage operations including saving, loading, and deleting games.
    Uses SQLite3 for persistent storage.
    """
    def __init__(self, db_filename="save/game_saves.db"):
        self.db_path = db_filename
        self._ensure_save_directory_exists()
        self._initialize_database()
    
    def _ensure_save_directory_exists(self):
        """Make sure the save directory exists"""
        save_dir = os.path.dirname(self.db_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def _initialize_database(self):
        """Set up the database schema if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create game_saves table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_saves (
            game_name TEXT PRIMARY KEY,
            created_at TEXT,
            last_saved_at TEXT,
            game_data TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def check_game_name_exists(self, game_name):
        """Check if a game with the given name already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM game_saves WHERE game_name = ?", (game_name,))
        result = cursor.fetchone() is not None
        
        conn.close()
        return result
    
    def get_all_game_names(self):
        """Retrieve a list of all saved game names with their creation and last saved dates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT game_name, created_at, last_saved_at FROM game_saves ORDER BY last_saved_at DESC")
        results = cursor.fetchall()
        
        game_list = [
            {
                'name': row[0],
                'created_at': row[1],
                'last_saved_at': row[2]
            }
            for row in results
        ]
        
        conn.close()
        return game_list
    
    def save_game(self, game_data_dto, force_override=False):
        """
        Save the game data to the database
        
        Args:
            game_data_dto (GameDataDTO): The game data to save
            force_override (bool): If True, will override existing save with the same name
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        # Validate that we have a game name
        if not game_data_dto.game_name:
            raise ValueError("Game name cannot be empty")
        
        # Check for duplicate game name
        if self.check_game_name_exists(game_data_dto.game_name) and not force_override:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update last saved timestamp
        game_data_dto.last_saved_at = datetime.now().isoformat()
        
        # Serialize the game data to JSON
        game_data_json = json.dumps(game_data_dto.to_dict())
        
        # Insert or replace the game save
        cursor.execute('''
        INSERT OR REPLACE INTO game_saves (game_name, created_at, last_saved_at, game_data)
        VALUES (?, ?, ?, ?)
        ''', (
            game_data_dto.game_name,
            game_data_dto.created_at,
            game_data_dto.last_saved_at,
            game_data_json
        ))
        
        conn.commit()
        conn.close()
        return True
    
    def update_game(self, game_data_dto):
        """
        Update an existing game save
        
        Args:
            game_data_dto (GameDataDTO): The updated game data
            
        Returns:
            bool: True if update was successful, False if game doesn't exist
        """
        if not self.check_game_name_exists(game_data_dto.game_name):
            return False
        
        return self.save_game(game_data_dto, force_override=True)
    
    def load_game(self, game_name):
        """
        Load game data from the database
        
        Args:
            game_name (str): The name of the game to load
            
        Returns:
            GameDataDTO: The loaded game data or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT game_data FROM game_saves WHERE game_name = ?", (game_name,))
        result = cursor.fetchone()
        
        conn.close()
        
        if not result:
            return None
        
        game_data_dict = json.loads(result[0])
        return GameDataDTO.from_dict(game_data_dict)
    
    def delete_game(self, game_name):
        """
        Delete a game save from the database
        
        Args:
            game_name (str): The name of the game to delete
            
        Returns:
            bool: True if deletion was successful, False if game doesn't exist
        """
        if not self.check_game_name_exists(game_name):
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM game_saves WHERE game_name = ?", (game_name,))
        
        conn.commit()
        conn.close()
        return True
    
    def apply_game_data_to_engine(self, game_data_dto, game_engine):
        """
        Apply loaded game data to the game engine
        
        Args:
            game_data_dto (GameDataDTO): The loaded game data
            game_engine (GameEngine): The game engine to update
            
        Returns:
            bool: True if successful
        """
        # Set basic game state
        game_engine.turn = game_data_dto.turn
        game_engine.game_name = game_data_dto.game_name
        
        # Deserialize map data
        if game_engine.map:
            MapSerializer.deserialize_map(game_data_dto.map_data, game_engine.map)
        
        # Deserialize player data using PlayerManager
        game_engine.player_manager.deserialize(game_data_dto.players)
        
        # Deserialize unit data
        game_engine.unit_manager.deserialize(game_data_dto.units)
        
        # Deserialize city data
        game_engine.city_manager.deserialize(game_data_dto.cities)
        
        return True
