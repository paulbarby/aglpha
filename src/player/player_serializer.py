class PlayerSerializer:
    """
    Handles serialization and deserialization of Player objects.
    """
    @staticmethod
    def serialize_players(players_list):
        """Convert all players to a serializable format"""
        serialized_players = []
        
        if not players_list:
            return serialized_players
            
        for player in players_list:
            serialized_players.append(PlayerSerializer.serialize_player(player))
            
        return serialized_players
    
    @staticmethod
    def serialize_player(player):
        """Convert a single player to a serializable format"""
        return {
            'id': getattr(player, 'id', ''),
            'name': getattr(player, 'name', ''),
            'is_ai': getattr(player, 'is_ai', False),
            'color': getattr(player, 'color', (255, 255, 255)),
            'resources': getattr(player, 'resources', {}),
            'researched_techs': getattr(player, 'researched_techs', []),
            'current_research': getattr(player, 'current_research', None),
            'research_progress': getattr(player, 'research_progress', 0),
            'controlled_units': getattr(player, 'controlled_units', []),
            'controlled_cities': getattr(player, 'controlled_cities', [])
        }
    
    @staticmethod
    def deserialize_players(player_data, game_engine):
        """Apply serialized player data to the game engine's player manager"""
        return game_engine.player_manager.deserialize(player_data)
