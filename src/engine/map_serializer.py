class MapSerializer:
    """
    Handles serialization and deserialization of Map objects.
    """
    @staticmethod
    def serialize_map(game_map):
        """Convert map to a serializable dictionary format"""
        if not game_map:
            return {
                'width': 0,
                'height': 0,
                'tiles': []
            }
            
        serialized_data = {
            'width': game_map.width,
            'height': game_map.height,
            'tiles': MapSerializer.serialize_tiles(game_map)
        }
        
        return serialized_data
    
    @staticmethod
    def serialize_tiles(game_map):
        """Convert map tiles to a serializable format"""
        serialized_tiles = []
        for y in range(game_map.height):
            for x in range(game_map.width):
                tile = game_map.tiles[y][x]
                serialized_tiles.append({
                    'position': (x, y),
                    'tile_type': tile.tile_type,
                    'explored_by': tile.explored_by.copy() if hasattr(tile, 'explored_by') else []
                })
        return serialized_tiles
    
    @staticmethod
    def deserialize_map(map_data, map_instance):
        """Apply serialized map data to a Map instance"""
        # This would rebuild the map from saved data
        # Implementation depends on how Map is constructed
        pass
