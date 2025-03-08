import uuid
from src.player.player import Player
from src.player.player_serializer import PlayerSerializer

class PlayerManager:
    def __init__(self):
        self.players = []  # List of Player objects
    
    def create_player(self, name, color=(255, 255, 255), is_ai=False):
        """Create a new player and add to the manager"""
        player_id = str(uuid.uuid4())  # Generate a unique ID
        player = Player(player_id, name, color, is_ai)
        self.add_player(player)
        return player
    
    def add_player(self, player):
        """Add an existing player object to the manager"""
        self.players.append(player)
    
    def get_player_by_id(self, player_id):
        """Find and return a player by ID"""
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def remove_player(self, player_id):
        """Remove a player from the manager"""
        self.players = [p for p in self.players if p.id != player_id]
    
    def get_human_players(self):
        """Return all human players"""
        return [p for p in self.players if not p.is_ai]
    
    def get_ai_players(self):
        """Return all AI players"""
        return [p for p in self.players if p.is_ai]
    
    def update_players(self):
        """Update player state, resources, etc."""
        for player in self.players:
            # Update player resources, research, etc.
            pass
    
    def serialize(self):
        """Serialize all players using the PlayerSerializer"""
        return PlayerSerializer.serialize_players(self.players)
    
    def deserialize(self, player_data):
        """Deserialize and rebuild players from saved data"""
        # Clear existing players
        self.players = []
        
        # This would rebuild all players from saved data
        for player_dict in player_data:
            # Create a new player instance based on serialized data
            player_id = player_dict.get('id', str(uuid.uuid4()))
            name = player_dict.get('name', 'Unnamed')
            is_ai = player_dict.get('is_ai', False)
            color = player_dict.get('color', (255, 255, 255))
            
            player = Player(player_id, name, color, is_ai)
            # Set other properties as needed
            
            self.add_player(player)
        
        return True
