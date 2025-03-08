import numpy as np
from noise import pnoise2, snoise2
import random
from enum import Enum, auto
from src.utils.logger import Logger
from src.utils.config_manager import config_manager

class TerrainType(Enum):
    """Enum for different terrain types."""
    WATER_DEEP = auto()
    WATER_SHALLOW = auto()
    SAND = auto()
    GRASS = auto()
    HILLS = auto()
    ROCK = auto()
    MOUNTAIN = auto()

class TerrainGenerator:
    """
    Terrain generator that creates procedural terrain maps using noise functions.
    Supports multiple terrain types with proper transitions.
    """
    
    def __init__(self):
        self.logger = Logger()
        self.logger.info("Initializing terrain generator")
        
        # Load configuration or use defaults
        self.config = {
            'noise_scale': config_manager.get_value("TERRAIN", "noise_scale", 0.1),
            'octaves': config_manager.get_value("TERRAIN", "octaves", 6),
            'persistence': config_manager.get_value("TERRAIN", "persistence", 0.5),
            'lacunarity': config_manager.get_value("TERRAIN", "lacunarity", 2.0),
            'water_level': config_manager.get_value("TERRAIN", "water_level", 0.3),
            'sand_level': config_manager.get_value("TERRAIN", "sand_level", 0.35),
            'grass_level': config_manager.get_value("TERRAIN", "grass_level", 0.6),
            'hills_level': config_manager.get_value("TERRAIN", "hills_level", 0.7),
            'rock_level': config_manager.get_value("TERRAIN", "rock_level", 0.85),
            'deep_water_level': config_manager.get_value("TERRAIN", "deep_water_level", 0.15)
        }
        
        # Random seed for terrain generation
        self.seed = random.randint(0, 999999)
        self.logger.debug(f"Using terrain seed: {self.seed}")
        
        # Store height and moisture maps
        self.height_map = None
        self.moisture_map = None

    def generate_terrain_map(self, width, height, seed=None):
        """
        Generate a complete terrain map with all terrain types.
        
        Args:
            width (int): Map width in tiles
            height (int): Map height in tiles
            seed (int, optional): Seed for random generation. If None, uses instance seed.
            
        Returns:
            numpy.ndarray: 2D array of TerrainType enums
        """
        if seed is not None:
            self.seed = seed
            
        self.logger.info(f"Generating terrain map {width}x{height} with seed {self.seed}")
        
        # Generate height and moisture maps
        self.height_map = self._generate_height_map(width, height)
        self.moisture_map = self._generate_moisture_map(width, height)
        
        # Combine height and moisture into terrain types
        terrain_map = np.zeros((height, width), dtype=object)
        
        for y in range(height):
            for x in range(width):
                terrain_map[y, x] = self._determine_terrain_type(
                    self.height_map[y, x], 
                    self.moisture_map[y, x]
                )
        
        # Optional: Apply terrain smoothing and transitions
        terrain_map = self._smooth_terrain(terrain_map)
        
        self.logger.info(f"Terrain map generated successfully")
        return terrain_map
        
    def _generate_height_map(self, width, height):
        """Generate a height map using Perlin noise."""
        self.logger.debug("Generating height map")
        
        height_map = np.zeros((height, width))
        
        scale = self.config['noise_scale']
        octaves = self.config['octaves']
        persistence = self.config['persistence']
        lacunarity = self.config['lacunarity']
        
        # Generate base noise
        for y in range(height):
            for x in range(width):
                height_map[y, x] = snoise2(
                    x * scale, 
                    y * scale, 
                    octaves=octaves, 
                    persistence=persistence, 
                    lacunarity=lacunarity, 
                    base=self.seed
                )
        
        # Normalize to 0-1 range
        height_map = (height_map - height_map.min()) / (height_map.max() - height_map.min())
        
        # Apply optional continent shape mask
        height_map = self._apply_continent_mask(height_map, width, height)
        
        return height_map
    
    def _generate_moisture_map(self, width, height):
        """Generate a moisture map using a different seed."""
        self.logger.debug("Generating moisture map")
        
        moisture_map = np.zeros((height, width))
        moisture_seed = self.seed + 1000  # Use a different seed for moisture
        
        scale = self.config['noise_scale'] * 1.5  # Different scale for variety
        octaves = self.config['octaves'] - 1
        persistence = self.config['persistence']
        lacunarity = self.config['lacunarity']
        
        # Generate moisture noise
        for y in range(height):
            for x in range(width):
                moisture_map[y, x] = snoise2(
                    x * scale, 
                    y * scale, 
                    octaves=octaves, 
                    persistence=persistence, 
                    lacunarity=lacunarity, 
                    base=moisture_seed
                )
        
        # Normalize to 0-1 range
        moisture_map = (moisture_map - moisture_map.min()) / (moisture_map.max() - moisture_map.min())
        
        # Moisture is influenced by height - areas near water are more likely to be moist
        for y in range(height):
            for x in range(width):
                if self.height_map[y, x] < self.config['water_level']:
                    # Increase moisture near water
                    radius = 3
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                                if distance <= radius:
                                    factor = (radius - distance) / radius * 0.3
                                    moisture_map[ny, nx] = min(1.0, moisture_map[ny, nx] + factor)
        
        return moisture_map
    
    def _apply_continent_mask(self, height_map, width, height):
        """Apply a mask to create continents rather than random noise."""
        # Create a radial gradient to push land toward the center
        center_x, center_y = width // 2, height // 2
        max_distance = ((width // 2) ** 2 + (height // 2) ** 2) ** 0.5
        
        for y in range(height):
            for x in range(width):
                # Calculate distance from center (0 to 1)
                dx, dy = x - center_x, y - center_y
                distance = ((dx ** 2) + (dy ** 2)) ** 0.5 / max_distance
                
                # Apply edge falloff to create coastlines
                edge_falloff = distance ** 2
                
                # Blend with height map
                height_map[y, x] = height_map[y, x] * (1.0 - edge_falloff) - (edge_falloff * 0.2)
        
        # Re-normalize to 0-1 range after applying the continent mask
        height_map = (height_map - height_map.min()) / (height_map.max() - height_map.min())
        
        return height_map
    
    def _determine_terrain_type(self, height, moisture):
        """Determine terrain type based on height and moisture."""
        if height < self.config['deep_water_level']:
            return TerrainType.WATER_DEEP
        elif height < self.config['water_level']:
            return TerrainType.WATER_SHALLOW
        elif height < self.config['sand_level']:
            return TerrainType.SAND
        elif height < self.config['grass_level']:
            return TerrainType.GRASS
        elif height < self.config['hills_level']:
            return TerrainType.HILLS
        elif height < self.config['rock_level']:
            return TerrainType.ROCK
        else:
            return TerrainType.MOUNTAIN
    
    def _smooth_terrain(self, terrain_map):
        """Apply smoothing to terrain map to create better transitions."""
        height, width = terrain_map.shape
        smoothed_map = np.copy(terrain_map)
        
        # Apply simple smoothing pass for terrain transitions
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # Skip water and mountains for better transitions - mountains should never be altered
                if terrain_map[y, x] in [TerrainType.WATER_DEEP, TerrainType.WATER_SHALLOW, TerrainType.MOUNTAIN]:
                    continue
                    
                # Count surrounding terrain types
                terrain_counts = {}
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        
                        nx, ny = x + dx, y + dy
                        neighbor_type = terrain_map[ny, nx]
                        
                        if neighbor_type in terrain_counts:
                            terrain_counts[neighbor_type] += 1
                        else:
                            terrain_counts[neighbor_type] = 1
                
                # Special case for smoothing around mountains
                if TerrainType.MOUNTAIN in terrain_counts and terrain_map[y, x] == TerrainType.GRASS:
                    # Always create a transition from grass to mountains
                    smoothed_map[y, x] = TerrainType.HILLS
                    continue
                
                # Determine most common neighbor
                if terrain_counts:
                    most_common = max(terrain_counts.items(), key=lambda x: x[1])[0]
                    most_common_count = terrain_counts[most_common]
                    
                    # Adjust terrain if neighbors are very different
                    current_type = terrain_map[y, x]
                    if most_common_count >= 5 and current_type != most_common:
                        # Check if terrain types are vastly different (e.g., mountains next to grass)
                        terrain_diff = abs(current_type.value - most_common.value)
                        if terrain_diff > 1:  # Reduced from 2 to catch more transitions
                            # Set to an intermediate terrain type
                            if current_type.value > most_common.value:
                                smoothed_map[y, x] = TerrainType(most_common.value + 1)
                            else:
                                smoothed_map[y, x] = TerrainType(most_common.value - 1)
        
        return smoothed_map
    
    def create_terrain_transitions(self, map_obj):
        """
        Apply terrain transitions to an existing Map object.
        Calculates bit masks for each tile to determine the appropriate transition tile.
        
        Args:
            map_obj: The Map object with tiles to update
            
        Returns:
            Updated map_obj with transition information
        """
        self.logger.info("Creating terrain transitions")
        
        # For each tile, calculate a bitmask based on surrounding tiles
        for y in range(map_obj.height):
            for x in range(map_obj.width):
                current_tile = map_obj.get_tile(x, y)
                
                # Skip if no tile exists
                if not current_tile:
                    continue
                    
                # Calculate terrain bitmask
                bitmask = self._calculate_terrain_bitmask(map_obj, x, y)
                
                # Store bitmask on the tile for rendering
                current_tile.transition_bitmask = bitmask
        
        return map_obj
    
    def _calculate_terrain_bitmask(self, map_obj, x, y):
        """Calculate a 16-bit bitmask for terrain transitions."""
        current_tile = map_obj.get_tile(x, y)
        current_type = current_tile.tile_type
        
        # 8 directions: N, NE, E, SE, S, SW, W, NW
        directions = [
            (0, -1), (1, -1), (1, 0), (1, 1), 
            (0, 1), (-1, 1), (-1, 0), (-1, -1)
        ]
        
        bitmask = 0
        
        # Check each neighboring tile
        for i, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            
            # Check if neighbor is within map bounds
            if 0 <= nx < map_obj.width and 0 <= ny < map_obj.height:
                neighbor_tile = map_obj.get_tile(nx, ny)
                
                # If neighbor is same type, set corresponding bit
                if neighbor_tile and neighbor_tile.tile_type == current_type:
                    bitmask |= (1 << i)
        
        return bitmask

# Utility function to convert TerrainType to string
def terrain_type_to_string(terrain_type):
    """Convert TerrainType enum to string representation."""
    return {
        TerrainType.WATER_DEEP: "water_deep",
        TerrainType.WATER_SHALLOW: "water_shallow",
        TerrainType.SAND: "sand",
        TerrainType.GRASS: "grass",
        TerrainType.HILLS: "hills",
        TerrainType.ROCK: "rock",
        TerrainType.MOUNTAIN: "mountain"
    }.get(terrain_type, "unknown")
