class Tile:
    def __init__(self, x, y, terrain_type='grass'):
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.movement_cost = 1  # Default movement cost
        self.defense_bonus = 0  # Default defense bonus
        self.resource = None
        self.improvement = None
        self.unit_grid = [[None for _ in range(8)] for _ in range(8)]  # 8x8 grid for units
        self.has_city = False
        self.city = None
    
    def __repr__(self):
        return f"Tile({self.x}, {self.y}, {self.terrain_type})"

class Resource:
    def __init__(self, resource_type, yield_value):
        self.type = resource_type
        self.yield_value = yield_value

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(x, y) for x in range(width)] for y in range(height)]
        
    def get_tile(self, x, y):
        """Get tile at the specified coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None
    
    def set_terrain(self, x, y, terrain_type):
        """Set the terrain type for a specific tile"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x].terrain_type = terrain_type
            
            # Update movement costs based on terrain
            if terrain_type == 'water':
                self.tiles[y][x].movement_cost = 2
            elif terrain_type == 'mountain':
                self.tiles[y][x].movement_cost = 3
            elif terrain_type == 'forest':
                self.tiles[y][x].movement_cost = 2
            else:
                self.tiles[y][x].movement_cost = 1
            
            # Update defense bonuses based on terrain
            if terrain_type == 'forest':
                self.tiles[y][x].defense_bonus = 25
            elif terrain_type == 'mountain':
                self.tiles[y][x].defense_bonus = 50
            else:
                self.tiles[y][x].defense_bonus = 0
    
    def add_resource(self, x, y, resource_type, yield_value):
        """Add a resource to a specific tile"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x].resource = Resource(resource_type, yield_value)
    
    def place_unit_on_tile(self, unit, tile):
        """Find first available slot in the tile's 8x8 grid"""
        for slot_y in range(8):
            for slot_x in range(8):
                if tile.unit_grid[slot_y][slot_x] is None:
                    # Assign unit to this slot
                    tile.unit_grid[slot_y][slot_x] = unit
                    unit.slot_position = (slot_x, slot_y)
                    unit.pixel_position = (
                        tile.x * 256 + slot_x * 32,
                        tile.y * 256 + slot_y * 32
                    )
                    return True
        return False  # Tile is full (64 units)
    
    def remove_unit_from_tile(self, unit, tile):
        """Remove a unit from its slot in a tile"""
        for slot_y in range(8):
            for slot_x in range(8):
                if tile.unit_grid[slot_y][slot_x] == unit:
                    tile.unit_grid[slot_y][slot_x] = None
                    return True
        return False
    
    def get_tile_bitmask(self, x, y, terrain_type):
        """Calculate the 16-bit bitmask for terrain transitions"""
        bitmask = 0
        directions = [
            (-1, -1), (0, -1), (1, -1),  # NW, N, NE
            (-1, 0),           (1, 0),   # W, E
            (-1, 1),  (0, 1),  (1, 1)    # SW, S, SE
        ]

        for i, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.tiles[ny][nx].terrain_type == terrain_type:
                    bitmask |= (1 << i)

        return bitmask

    def lookup_tile_variant(self, bitmask):
        """
        Map the bitmask to a specific tile variant
        This is a simplified version - a real implementation would have all 47 variants
        """
        # Some of the core variants
        tile_variants = {
            0: "isolated",                  # No neighbors
            255: "fully_surrounded",        # All neighbors
            56: "horizontal_edge_top",      # N, NE, NW
            7: "horizontal_edge_bottom",    # S, SE, SW
            41: "vertical_edge_left",       # W, NW, SW
            148: "vertical_edge_right",     # E, NE, SE
            16: "inner_corner_top_right",   # NE only
            1: "inner_corner_top_left",     # NW only
            4: "inner_corner_bottom_right", # SE only
            64: "inner_corner_bottom_left", # SW only
        }
        return tile_variants.get(bitmask, "default")
    
    def generate_map(self, terrain_data):
        """Generate the map from a 2D array of terrain types"""
        for y in range(min(self.height, len(terrain_data))):
            for x in range(min(self.width, len(terrain_data[0]))):
                self.set_terrain(x, y, terrain_data[y][x])
