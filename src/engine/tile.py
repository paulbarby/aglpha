class Tile:
    def __init__(self, tile_type, position):
        self.tile_type = tile_type  # e.g., 'grassland', 'forest', 'desert', etc.
        self.position = position    # (x, y) tuple
        self.explored_by = []       # list of players who have explored this tile