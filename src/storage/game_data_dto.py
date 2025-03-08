import json
from datetime import datetime
from src.player.player_serializer import PlayerSerializer

class GameDataDTO:
    """
    Data Transfer Object for game data serialization and deserialization.
    Contains all data needed to save and restore a game state.
    """
    def __init__(self, game_name=None, created_at=None, last_saved_at=None):
        self.game_name = game_name
        self.created_at = created_at or datetime.now().isoformat()
        self.last_saved_at = last_saved_at or self.created_at
        
        # Game state data
        self.turn = 0
        self.players = []
        
        # Map data
        self.map_data = {
            'width': 0,
            'height': 0,
            'tiles': []
        }
        
        # Units data
        self.units = []
        
        # Cities data
        self.cities = []
    
    def to_dict(self):
        """Convert DTO to a dictionary for JSON serialization"""
        return {
            'game_name': self.game_name,
            'created_at': self.created_at,
            'last_saved_at': datetime.now().isoformat(),
            'turn': self.turn,
            'players': self.players,
            'map_data': self.map_data,
            'units': self.units,
            'cities': self.cities
        }
    
    @staticmethod
    def from_dict(data_dict):
        """Create a DTO from a dictionary (deserialization)"""
        dto = GameDataDTO(
            game_name=data_dict.get('game_name'),
            created_at=data_dict.get('created_at'),
            last_saved_at=data_dict.get('last_saved_at')
        )
        
        dto.turn = data_dict.get('turn', 0)
        dto.players = data_dict.get('players', [])
        dto.map_data = data_dict.get('map_data', {'width': 0, 'height': 0, 'tiles': []})
        dto.units = data_dict.get('units', [])
        dto.cities = data_dict.get('cities', [])
        
        return dto
    
    def serialize_game_engine(self, game_engine):
        """Extract data from game engine and populate the DTO"""
        # Basic game state
        self.turn = game_engine.turn
        
        # Extract player data using PlayerManager's serialize method
        self.players = game_engine.player_manager.serialize()
        
        # Extract map data using Map's serialize method
        self.map_data = game_engine.map.serialize()
        
        # Extract unit data using UnitManager's serialize method
        self.units = game_engine.unit_manager.serialize()
        
        # Extract city data using CityManager's serialize method
        self.cities = game_engine.city_manager.serialize()
        
        return self
