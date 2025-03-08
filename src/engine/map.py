from src.engine.tile import Tile  # added import
from src.engine.map_serializer import MapSerializer

class Map:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.tiles = [[Tile("grassland", (x, y)) for x in range(width)] for y in range(height)]
    
    def serialize(self):
        """Serialize map data using the MapSerializer"""
        return MapSerializer.serialize_map(self)
    
    def deserialize(self, map_data):
        """Deserialize and rebuild map from saved data"""
        return MapSerializer.deserialize_map(map_data, self)
