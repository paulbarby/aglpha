import pygame

class Viewport:
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        
        # Viewport properties
        self.x = 0  # World x coordinate of top-left corner
        self.y = 0  # World y coordinate of top-left corner
        self.zoom = 1.0
        
        # Dragging state
        self.is_dragging = False
        self.drag_start = (0, 0)
        self.drag_current = (0, 0)

    def screen_to_world(self, screen_pos):
        """Convert screen coordinates to world coordinates"""
        world_x = self.x + screen_pos[0] / self.zoom
        world_y = self.y + screen_pos[1] / self.zoom
        return world_x, world_y
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = (world_x - self.x) * self.zoom
        screen_y = (world_y - self.y) * self.zoom
        return screen_x, screen_y
    
    def start_drag(self, screen_pos):
        """Start dragging the viewport"""
        self.is_dragging = True
        self.drag_start = screen_pos
        self.drag_current = screen_pos
    
    def handle_drag(self, screen_pos):
        """Update viewport position while dragging"""
        if self.is_dragging:
            self.drag_current = screen_pos
            delta_x = self.drag_current[0] - self.drag_start[0]
            delta_y = self.drag_current[1] - self.drag_start[1]
            
            self.x -= delta_x / self.zoom
            self.y -= delta_y / self.zoom
            
            self.drag_start = self.drag_current
            self.clamp_to_map_bounds()
    
    def end_drag(self):
        """End dragging operation"""
        self.is_dragging = False
    
    def handle_zoom(self, zoom_direction, mouse_pos):
        """Zoom in or out, keeping the point under the mouse stable"""
        # Store pre-zoom mouse world position
        world_x, world_y = self.screen_to_world(mouse_pos)
        
        # Adjust zoom factor (limit between 0.25x and 4x)
        old_zoom = self.zoom
        self.zoom += zoom_direction
        self.zoom = max(0.25, min(4.0, self.zoom))
        
        # Ensure the point under the mouse remains stable
        self.x = world_x - mouse_pos[0] / self.zoom
        self.y = world_y - mouse_pos[1] / self.zoom
        
        self.clamp_to_map_bounds()
    
    def center_on_position(self, world_x, world_y):
        """Center the viewport on a specific world position"""
        self.x = world_x - (self.screen_width / self.zoom / 2)
        self.y = world_y - (self.screen_height / self.zoom / 2)
        self.clamp_to_map_bounds()
    
    def clamp_to_map_bounds(self):
        """Ensure viewport stays within map bounds"""
        # Calculate maximum allowed position to keep viewport within map
        max_x = self.map_width * 256 - (self.screen_width / self.zoom)
        max_y = self.map_height * 256 - (self.screen_height / self.zoom)
        
        # Clamp viewport position (don't allow negative coordinates)
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))
    
    def update_visible_tiles(self, game_map):
        """
        Update visibility information for all players
        This method is called from the TileEngine to update which tiles
        are currently visible to each player based on their units and cities
        """
        # This method would normally update player vision based on unit positions
        # For now, it's a stub that would be called by the main game loop
        pass
    
    def get_visible_tiles(self):
        """Get list of tile coordinates visible in the current viewport"""
        visible_tiles = []
        
        # Calculate tile range that could be visible
        start_tile_x = max(0, int(self.x / 256))
        start_tile_y = max(0, int(self.y / 256))
        
        # Calculate how many tiles fit in the viewport based on zoom
        tiles_wide = int(self.screen_width / (256 * self.zoom)) + 2
        tiles_high = int(self.screen_height / (256 * self.zoom)) + 2
        
        end_tile_x = min(start_tile_x + tiles_wide, self.map_width)
        end_tile_y = min(start_tile_y + tiles_high, self.map_height)
        
        # Generate list of visible tile coordinates
        for y in range(start_tile_y, end_tile_y):
            for x in range(start_tile_x, end_tile_x):
                visible_tiles.append((y, x))
                
        return visible_tiles
