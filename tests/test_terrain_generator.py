import unittest
import numpy as np
import sys
import os

# Add the src directory to the path so we can import from there
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.terrain_generator import TerrainGenerator, TerrainType, terrain_type_to_string
from src.utils.logger import Logger
from src.utils.config_manager import config_manager

class MockMap:
    """Mock Map object for testing terrain transitions."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[None for _ in range(width)] for _ in range(height)]
    
    def get_tile(self, x, y):
        return self.tiles[y][x] if 0 <= x < self.width and 0 <= y < self.height else None
    
    def set_tile(self, x, y, tile):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile

class MockTile:
    """Mock Tile object for testing terrain transitions."""
    def __init__(self, tile_type, position):
        self.tile_type = tile_type
        self.position = position
        self.transition_bitmask = 0

class TestTerrainGenerator(unittest.TestCase):
    def setUp(self):
        """Set up the test environment before each test method."""
        self.terrain_generator = TerrainGenerator()
        # Use a fixed seed for reproducible tests
        self.fixed_seed = 12345
        
    def test_initialization(self):
        """Test that the TerrainGenerator initializes correctly."""
        # Check that the configuration is loaded
        self.assertIsNotNone(self.terrain_generator.config)
        self.assertIsInstance(self.terrain_generator.config, dict)
        
        # Check that the logger is initialized
        self.assertIsNotNone(self.terrain_generator.logger)
        self.assertIsInstance(self.terrain_generator.logger, Logger)
        
    def test_height_map_generation(self):
        """Test that height maps are generated correctly."""
        width, height = 50, 40
        height_map = self.terrain_generator._generate_height_map(width, height)
        
        # Check dimensions
        self.assertEqual(height_map.shape, (height, width))
        
        # Check range (should be normalized to 0-1)
        self.assertGreaterEqual(np.min(height_map), 0.0)
        self.assertLessEqual(np.max(height_map), 1.0)
        
        # Check that using the same seed produces the same map
        self.terrain_generator.seed = self.fixed_seed
        map1 = self.terrain_generator._generate_height_map(width, height)
        self.terrain_generator.seed = self.fixed_seed
        map2 = self.terrain_generator._generate_height_map(width, height)
        np.testing.assert_array_equal(map1, map2)
        
        # Check that different seeds produce different maps
        self.terrain_generator.seed = self.fixed_seed + 1
        map3 = self.terrain_generator._generate_height_map(width, height)
        self.assertFalse(np.array_equal(map1, map3))
        
    def test_moisture_map_generation(self):
        """Test that moisture maps are generated correctly."""
        width, height = 50, 40
        # We need a height map for moisture calculation
        self.terrain_generator.height_map = self.terrain_generator._generate_height_map(width, height)
        moisture_map = self.terrain_generator._generate_moisture_map(width, height)
        
        # Check dimensions
        self.assertEqual(moisture_map.shape, (height, width))
        
        # Check range (should be normalized to 0-1)
        self.assertGreaterEqual(np.min(moisture_map), 0.0)
        self.assertLessEqual(np.max(moisture_map), 1.0)
        
    def test_terrain_type_determination(self):
        """Test that terrain types are determined correctly based on height and moisture."""
        test_cases = [
            # height, expected terrain type
            (0.1, TerrainType.WATER_DEEP),
            (0.2, TerrainType.WATER_SHALLOW),
            (0.32, TerrainType.SAND),
            (0.4, TerrainType.GRASS),
            (0.65, TerrainType.HILLS),
            (0.75, TerrainType.ROCK),
            (0.9, TerrainType.MOUNTAIN)
        ]
        
        for height, expected_type in test_cases:
            terrain_type = self.terrain_generator._determine_terrain_type(height, 0.5)
            self.assertEqual(terrain_type, expected_type, 
                             f"For height {height}, expected {expected_type}, got {terrain_type}")
    
    def test_terrain_map_generation(self):
        """Test that complete terrain maps are generated correctly."""
        width, height = 30, 25
        self.terrain_generator.seed = self.fixed_seed
        terrain_map = self.terrain_generator.generate_terrain_map(width, height)
        
        # Check dimensions
        self.assertEqual(terrain_map.shape, (height, width))
        
        # Check that all cells have a valid terrain type
        for y in range(height):
            for x in range(width):
                self.assertIsInstance(terrain_map[y, x], TerrainType)
        
        # Check distribution - there should be a mix of terrain types
        terrain_counts = {}
        for y in range(height):
            for x in range(width):
                terrain_type = terrain_map[y, x]
                if terrain_type in terrain_counts:
                    terrain_counts[terrain_type] += 1
                else:
                    terrain_counts[terrain_type] = 1
        
        # We should have at least 4 different terrain types in a reasonably sized map
        self.assertGreaterEqual(len(terrain_counts), 4, 
                              "Expected at least 4 different terrain types in the map")
    
    def test_terrain_smoothing(self):
        """Test terrain smoothing to create better transitions."""
        height, width = 10, 10
        # Create a test terrain map with abrupt transitions
        terrain_map = np.zeros((height, width), dtype=object)
        
        # Fill with grass
        for y in range(height):
            for x in range(width):
                terrain_map[y, x] = TerrainType.GRASS
        
        # Add a mountain range that would require smoothing
        for x in range(3, 7):
            terrain_map[5, x] = TerrainType.MOUNTAIN
        
        # Smooth the terrain
        smoothed_map = self.terrain_generator._smooth_terrain(terrain_map)
        
        # Check that transitions are smoother - should have intermediate terrain types around mountains
        for x in range(3, 7):
            # Check above and below mountains - should be smoother transitions
            self.assertNotEqual(smoothed_map[4, x], TerrainType.GRASS, 
                              "Expected smoother transition above mountains")
            self.assertNotEqual(smoothed_map[6, x], TerrainType.GRASS, 
                              "Expected smoother transition below mountains")
            
        # The mountains themselves should remain
        for x in range(3, 7):
            self.assertEqual(smoothed_map[5, x], TerrainType.MOUNTAIN, 
                          "Mountains should not be altered by smoothing")
    
    def test_terrain_transitions_bitmask(self):
        """Test that terrain transition bitmasks are calculated correctly."""
        # Create a mock map with different terrain types
        mock_map = MockMap(5, 5)
        
        # Create a pattern: grass in center surrounded by sand
        center_tile = MockTile("grass", (2, 2))
        mock_map.set_tile(2, 2, center_tile)
        
        # Surround with sand
        for y in range(5):
            for x in range(5):
                if not (x == 2 and y == 2):  # Skip center
                    mock_map.set_tile(x, y, MockTile("sand", (x, y)))
        
        # Calculate bitmasks
        self.terrain_generator.create_terrain_transitions(mock_map)
        
        # Center tile should have bitmask 0 (no matching neighbors)
        self.assertEqual(center_tile.transition_bitmask, 0)
        
        # Create a different pattern with some matching neighbors
        mock_map2 = MockMap(3, 3)
        
        # Make all tiles grass
        for y in range(3):
            for x in range(3):
                mock_map2.set_tile(x, y, MockTile("grass", (x, y)))
        
        # Except the center
        center_tile2 = MockTile("sand", (1, 1))
        mock_map2.set_tile(1, 1, center_tile2)
        
        # Calculate bitmasks
        self.terrain_generator.create_terrain_transitions(mock_map2)
        
        # Center sand tile should have bitmask 0 (no matching neighbors)
        self.assertEqual(center_tile2.transition_bitmask, 0)
        
        # The grass tiles should have a specific pattern of bitmasks
        # Top-left corner should match right and bottom
        self.assertEqual(mock_map2.get_tile(0, 0).transition_bitmask, 0b00010100)

    def test_terrain_type_to_string(self):
        """Test that terrain types are correctly converted to strings."""
        test_cases = [
            (TerrainType.WATER_DEEP, "water_deep"),
            (TerrainType.WATER_SHALLOW, "water_shallow"),
            (TerrainType.SAND, "sand"),
            (TerrainType.GRASS, "grass"),
            (TerrainType.HILLS, "hills"),
            (TerrainType.ROCK, "rock"),
            (TerrainType.MOUNTAIN, "mountain")
        ]
        
        for terrain_type, expected_string in test_cases:
            result = terrain_type_to_string(terrain_type)
            self.assertEqual(result, expected_string)
        
        # Test with an invalid terrain type
        class FakeTerrainType:
            pass
            
        result = terrain_type_to_string(FakeTerrainType())
        self.assertEqual(result, "unknown")

if __name__ == '__main__':
    unittest.main()
