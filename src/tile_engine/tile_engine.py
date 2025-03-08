import pygame
from .map import GameMap
from .player import Player
from .viewport import Viewport
from .info_panel import InfoPanel
from .unit_manager import UnitManager
from .city_manager import CityManager

class TileEngine:
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        
        # Core game state
        self.game_state = "PLAYING"  # Can be PLAYING, MENU, GAME_OVER
        self.turn = 0
        self.players = []
        self.current_player_id = 0
        
        # Initialize map and managers
        self.map = GameMap(map_width, map_height)
        self.viewport = Viewport(screen_width, screen_height, map_width, map_height)
        self.info_panel = InfoPanel(screen_width, screen_height)
        self.unit_manager = UnitManager(self.map)
        self.city_manager = CityManager(self.map)
        
        # Selection state
        self.selected_tile = None
        self.selected_unit = None
    
    def add_player(self, name, color):
        player = Player(len(self.players), name, color)
        self.players.append(player)
        return player
    
    def update(self):
        """Main update method called each frame"""
        self.unit_manager.update()
        self.city_manager.update()
        self.update_visible_tiles()
        
    def next_turn(self):
        """Advance to the next turn"""
        self.turn += 1
        self.current_player_id = (self.current_player_id + 1) % len(self.players)
        print(f"Turn {self.turn}: {self.players[self.current_player_id].name}'s turn")
        
    def update_visible_tiles(self):
        """Update which tiles are visible in the current viewport"""
        self.viewport.update_visible_tiles(self.map)
        
    def handle_input(self, event):
        """Process user input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_tile_selection(event.pos)
            elif event.button == 3:  # Right click
                self.viewport.start_drag(event.pos)
            elif event.button == 4:  # Scroll up
                self.viewport.handle_zoom(0.1, event.pos)
            elif event.button == 5:  # Scroll down
                self.viewport.handle_zoom(-0.1, event.pos)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right click release
                self.viewport.end_drag()
                
        elif event.type == pygame.MOUSEMOTION:
            if self.viewport.is_dragging:
                self.viewport.handle_drag(event.pos)
    
    def handle_tile_selection(self, screen_pos):
        """Convert screen position to tile coordinates and select the tile"""
        # Check if click is in the minimap area
        if self.is_point_in_minimap(screen_pos):
            self.handle_minimap_click(screen_pos)
            return
        
        world_x, world_y = self.viewport.screen_to_world(screen_pos)
        tile_x = int(world_x / 256)
        tile_y = int(world_y / 256)
        
        if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
            self.selected_tile = (tile_x, tile_y)
            self.update_info_panel()
            
            # Check for unit selection
            tile = self.map.get_tile(tile_x, tile_y)
            units = self.unit_manager.get_units_on_tile(tile)
            if units and units[0].player_id == self.current_player_id:
                self.selected_unit = units[0]
    
    def update_info_panel(self):
        """Update the info panel with the selected tile's information"""
        if self.selected_tile:
            x, y = self.selected_tile
            tile = self.map.get_tile(x, y)
            
            # Update terrain info
            self.info_panel.set_terrain(tile.terrain_type, tile.movement_cost)
            
            # Update resource info
            if tile.resource:
                self.info_panel.set_resource(tile.resource.type, tile.resource.yield_value)
            
            # Update unit list
            units = self.unit_manager.get_units_on_tile(tile)
            self.info_panel.set_unit_list(units)
            
            # Update city info
            if tile.has_city:
                self.info_panel.set_city(tile.city)
    
    def is_point_in_minimap(self, point):
        """Check if a point is within the minimap area"""
        minimap_width = self.map_width / 8  # 1/8 scale
        minimap_height = self.map_height / 8
        
        return (10 <= point[0] <= 10 + minimap_width + 4 and
                10 <= point[1] <= 10 + minimap_height + 4)
    
    def handle_minimap_click(self, minimap_pos):
        """Handle click on the minimap to reposition viewport"""
        minimap_width = self.map_width / 8
        minimap_height = self.map_height / 8
        
        # Convert minimap position to map position ratio
        x_ratio = (minimap_pos[0] - 12) / minimap_width
        y_ratio = (minimap_pos[1] - 12) / minimap_height
        
        # Convert to world coordinates
        target_world_x = x_ratio * (self.map_width * 256)
        target_world_y = y_ratio * (self.map_height * 256)
        
        # Center viewport on this position
        self.viewport.center_on_position(target_world_x, target_world_y)
        
    def render(self, screen):
        """Render the entire game view"""
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Render visible map tiles
        self.render_map(screen)
        
        # Render minimap
        self.render_minimap(screen)
        
        # Render info panel
        self.info_panel.render(screen)
    
    def render_map(self, screen):
        """Render the visible portion of the map"""
        visible_tiles = self.viewport.get_visible_tiles()
        for tile_y, tile_x in visible_tiles:
            tile = self.map.get_tile(tile_x, tile_y)
            if not tile:
                continue
                
            # Get screen position for this tile
            screen_x, screen_y = self.viewport.world_to_screen(
                tile_x * 256, tile_y * 256
            )
            
            # Only render if on screen
            if (-256 <= screen_x <= self.screen_width and 
                -256 <= screen_y <= self.screen_height):
                
                # Render base terrain
                self.render_tile(screen, tile, screen_x, screen_y)
                
                # Render resources if any
                if tile.resource:
                    self.render_resource(screen, tile.resource, screen_x, screen_y)
                
                # Render city if present
                if tile.has_city:
                    self.render_city(screen, tile.city, screen_x, screen_y)
                
                # Render units
                units = self.unit_manager.get_units_on_tile(tile)
                for unit in units:
                    self.render_unit(screen, unit, screen_x, screen_y)
                
                # Render fog of war
                player = self.players[self.current_player_id]
                self.render_fog_of_war(screen, tile, player, screen_x, screen_y)
                
                # Render selection highlight if selected
                if self.selected_tile == (tile_x, tile_y):
                    pygame.draw.rect(screen, (255, 255, 0), 
                                    (screen_x, screen_y, 256, 256), 2)

    def render_tile(self, screen, tile, screen_x, screen_y):
        """Render a single tile with proper transitions"""
        bitmask = self.map.get_tile_bitmask(tile.x, tile.y, tile.terrain_type)
        tile_variant = self.map.lookup_tile_variant(bitmask)
        
        # In a real implementation, you'd load the appropriate texture based on tile_variant
        # For this example, we'll use colored rectangles
        terrain_colors = {
            'grass': (100, 200, 100),
            'desert': (240, 220, 130),
            'water': (64, 164, 223),
            'mountain': (139, 137, 137),
            'forest': (34, 139, 34),
        }
        color = terrain_colors.get(tile.terrain_type, (128, 128, 128))
        
        # Scale rectangle based on zoom
        zoom_adjusted_size = int(256 * self.viewport.zoom)
        
        # Draw tile
        pygame.draw.rect(screen, color, 
                         (screen_x, screen_y, zoom_adjusted_size, zoom_adjusted_size))
    
    def render_resource(self, screen, resource, screen_x, screen_y):
        """Render a resource on a tile"""
        # In a real implementation, you'd render a resource sprite
        resource_color = (255, 215, 0)  # Gold color for resources
        resource_size = int(32 * self.viewport.zoom)
        pygame.draw.circle(screen, resource_color, 
                         (screen_x + 128, screen_y + 128), resource_size)
    
    def render_city(self, screen, city, screen_x, screen_y):
        """Render a city on a tile"""
        # In a real implementation, you'd render a city sprite
        city_color = (200, 200, 200)
        
        # Draw a simple house shape
        points = [
            (screen_x + 128, screen_y + 80),  # Top
            (screen_x + 188, screen_y + 120),  # Right
            (screen_x + 188, screen_y + 200),  # Bottom right
            (screen_x + 68, screen_y + 200),   # Bottom left
            (screen_x + 68, screen_y + 120),   # Left
        ]
        pygame.draw.polygon(screen, city_color, points)
    
    def render_unit(self, screen, unit, tile_x, tile_y):
        """Render a unit on its slot position within a tile"""
        slot_x, slot_y = unit.slot_position
        unit_x = tile_x + (slot_x * 32) * self.viewport.zoom
        unit_y = tile_y + (slot_y * 32) * self.viewport.zoom
        unit_size = int(24 * self.viewport.zoom)
        
        # Draw unit as a colored circle
        pygame.draw.circle(screen, unit.player.color, 
                        (unit_x + 16, unit_y + 16), unit_size)
    
    def render_fog_of_war(self, screen, tile, player, screen_x, screen_y):
        """Render fog of war for unexplored or non-visible tiles"""
        if tile not in player.explored_tiles:
            # Draw completely black fog (unexplored)
            pygame.draw.rect(screen, (0, 0, 0, 255), 
                            (screen_x, screen_y, 256 * self.viewport.zoom, 256 * self.viewport.zoom))
        elif tile not in player.visible_tiles:
            # Draw semi-transparent fog (explored but not visible)
            fog_surface = pygame.Surface((256, 256), pygame.SRCALPHA)
            pygame.draw.rect(fog_surface, (0, 0, 0, 128), 
                            (0, 0, 256, 256))
            screen.blit(fog_surface, (screen_x, screen_y))
    
    def render_minimap(self, screen, player_id=None):
        """Render the minimap in the corner of the screen"""
        if player_id is None:
            player_id = self.current_player_id
            
        # Calculate minimap dimensions
        minimap_width = self.map_width / 8  # 1/8 scale
        minimap_height = self.map_height / 8

        # Draw border
        pygame.draw.rect(screen, (128, 128, 128), (10, 10, minimap_width + 4, minimap_height + 4), 2)

        # Draw minimap terrain
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile = self.map.get_tile(x, y)

                # Only draw explored tiles
                if tile in self.players[player_id].explored_tiles:
                    # Get color based on terrain
                    color = self.get_terrain_color(tile.terrain_type)

                    # Draw minimap pixel
                    pygame.draw.rect(screen, color,
                        (12 + x * (minimap_width / self.map_width),
                        12 + y * (minimap_height / self.map_height),
                        minimap_width / self.map_width + 1,
                        minimap_height / self.map_height + 1))

        # Draw viewport rectangle
        viewport_x_ratio = self.viewport.x / (self.map_width * 256)
        viewport_y_ratio = self.viewport.y / (self.map_height * 256)
        viewport_width_ratio = (self.screen_width / self.viewport.zoom) / (self.map_width * 256)
        viewport_height_ratio = (self.screen_height / self.viewport.zoom) / (self.map_height * 256)

        pygame.draw.rect(screen, (255, 255, 255),
            (12 + viewport_x_ratio * minimap_width,
            12 + viewport_y_ratio * minimap_height,
            viewport_width_ratio * minimap_width,
            viewport_height_ratio * minimap_height), 1)
    
    def get_terrain_color(self, terrain_type):
        """Get a simplified color for the minimap based on terrain type"""
        colors = {
            'grass': (34, 139, 34),    # Forest Green
            'desert': (238, 214, 175),  # Sand
            'water': (30, 144, 255),    # Dodger Blue
            'mountain': (139, 137, 137),  # Gray
            'forest': (0, 100, 0),      # Dark Green
        }
        return colors.get(terrain_type, (100, 100, 100))
