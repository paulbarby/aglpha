class Player:
    def __init__(self, player_id, name, color):
        self.id = player_id
        self.name = name
        self.color = color
        self.explored_tiles = set()  # Set of tiles this player has seen
        self.visible_tiles = set()   # Set of tiles currently visible
        self.cities = []
        self.units = []
    
    def add_unit(self, unit):
        """Add a unit to this player"""
        self.units.append(unit)
        unit.player = self
        unit.player_id = self.id
        
    def add_city(self, city):
        """Add a city to this player"""
        self.cities.append(city)
        city.player = self
        
    def update_visibility(self, game_map):
        """Update which tiles are visible to this player based on units and cities"""
        # Clear current visible tiles
        self.visible_tiles.clear()
        
        # Add tiles visible from units
        for unit in self.units:
            x, y = unit.tile_position
            visibility_range = unit.visibility_range
            
            for dy in range(-visibility_range, visibility_range + 1):
                for dx in range(-visibility_range, visibility_range + 1):
                    nx, ny = x + dx, y + dy
                    
                    # Check if in map bounds
                    if 0 <= nx < game_map.width and 0 <= ny < game_map.height:
                        tile = game_map.get_tile(nx, ny)
                        
                        # Add to both explored and visible sets
                        self.explored_tiles.add(tile)
                        self.visible_tiles.add(tile)
        
        # Add tiles visible from cities
        for city in self.cities:
            x, y = city.tile_position
            visibility_range = city.visibility_range
            
            for dy in range(-visibility_range, visibility_range + 1):
                for dx in range(-visibility_range, visibility_range + 1):
                    nx, ny = x + dx, y + dy
                    
                    # Check if in map bounds
                    if 0 <= nx < game_map.width and 0 <= ny < game_map.height:
                        tile = game_map.get_tile(nx, ny)
                        
                        # Add to both explored and visible sets
                        self.explored_tiles.add(tile)
                        self.visible_tiles.add(tile)
