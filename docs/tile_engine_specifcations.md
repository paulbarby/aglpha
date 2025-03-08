# Tile Engine Class Specifications Summary

## Tile Engine Components

### TileEngine

- **Responsibilities:**  
  Coordinates the overall game flow, turn management, and integrates various managers.

- **Key Properties:**

  - `game_state`: Current state of the game (from **GameState**).
  - `turn`: Current turn counter.
  - `players`: List of players (human and AI).
  - `map`: Instance of the **Map** class representing the game world.
  - Managers for units, cities, AI, events, UI, and animations.

- **Key Method:**
  - `update()`: Calls updates on all managers to progress game logic.

---

## Tile Rendering System

### **16-bit Bitmasking for Tile Transitions**

#### **How 16-bit Bitmasking Works**

Each tile checks its **8 direct neighbors** (N, NE, E, SE, S, SW, W, NW) and **8 diagonal half-adjacent neighbors** for finer control. The **bit position** corresponds to the neighbor's relative position:

```
  1  2  4
  8  X  16
  32 64 128
```

This results in a **16-bit value** where `0000000000000000` (0) represents an isolated tile, and `1111111111111111` (65535) represents a fully surrounded tile.

### **Tile Variations Needed (Optimized)**

Using **16-bit masking**, the **theoretical max tile count is 256**, but the optimized tile count is **47 unique tiles**:

1. **Core Terrain Tiles (9 Tiles)** - Isolated, fully surrounded, horizontal/vertical edges, crossroads.
2. **Inner Corner Transitions (4 Tiles)** - For wrapping terrain inside another.
3. **Outer Corner Transitions (4 Tiles)** - For outward curving transitions.
4. **Partial Edge Cases (10 Tiles)** - L-shapes, T-junctions, single-side transitions.
5. **Special Cases (10+ Tiles)** - Water-to-land transitions, cliffs, ridges, roads.

### **Tile Selection Algorithm (Python Implementation)**

```python
class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[None for _ in range(width)] for _ in range(height)]

    def get_tile_bitmask(self, x, y, terrain_type):
        bitmask = 0
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

        for i, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.tiles[ny][nx] == terrain_type:
                    bitmask |= (1 << i)

        return bitmask

    def generate_tile_map(self, terrain_data):
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x] = terrain_data[y][x]

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                bitmask = self.get_tile_bitmask(x, y, self.tiles[y][x])
                tile_variant = self.lookup_tile_variant(bitmask)
                self.draw_tile(x, y, tile_variant)

    def lookup_tile_variant(self, bitmask):
        tile_variants = {
            0: "isolated",
            255: "fully_surrounded",
            21844: "vertical_edge_right",
            10922: "vertical_edge_left",
            255: "horizontal_edge_top",
            65280: "horizontal_edge_bottom",
            576: "diagonal_top_left",
            18: "diagonal_bottom_right"
        }
        return tile_variants.get(bitmask, "default")

    def draw_tile(self, x, y, tile_variant):
        print(f"Rendering tile at ({x}, {y}) as {tile_variant}")
```

### **Implementation Details**

1. **`get_tile_bitmask(x, y, terrain_type)`** – Computes the **16-bit** terrain mask for a tile.
2. **`lookup_tile_variant(bitmask)`** – Maps bitmask values to tile transitions.
3. **`render()`** – Iterates over the grid, computes bitmasks, and selects the correct tile.
4. **`draw_tile(x, y, tile_variant)`** – Simulates rendering of tile transitions.

### **Additional Features**

- **Water & Coastline Handling:** Specialized tile blending for natural coastlines.
- **Road & Terrain Transitions:** Roads have separate bitmask logic for seamless integration.
- **Performance Optimization:** Cached results for smooth rendering.

---

## Tile Display System

### **Viewport and Visibility**

- **Visible Tile Calculation**:

  - Visible tiles depend on current window size and zoom factor
  - Only tiles within the viewport rectangle are rendered
  - Formula: `visible_tiles = (window_width / (tile_width * zoom), window_height / (tile_height * zoom))`

- **Tile Properties**:
  - Standard tile size: **256×256 pixels**
  - Arranged in a grid pattern with coordinates (x, y)
  - Each tile represents a discrete game world location

### **Rendering Layers**

The tile engine renders content in distinct layers from bottom to top:

1. **Base Terrain Layer**: The fundamental tile graphics (grass, desert, water)
2. **Resource Layer**: Resources and special features rendered above terrain
   - Natural resources (iron, horses, wheat)
   - Relics and artifacts
   - Abandoned structures
3. **City Layer**: Cities rendered above resources
4. **Unit Layer**: Units positioned on top of all other elements
5. **Fog of War Layer**: Black semi-transparent overlay on unexplored areas
6. **Selection/UI Layer**: Tile selection indicators and UI elements

### **Unit Positioning System**

- Each tile contains an **8×8 grid** of unit slots (64 total positions)
- Units are assigned specific slots within the tile
- Visual positioning is calculated: `unit_x = tile_x + (slot_x * 32)`, `unit_y = tile_y + (slot_y * 32)`
- When multiple units occupy a tile, they are arranged in this grid

```python
def place_unit_on_tile(self, unit, tile):
    # Find first available slot in the tile's 8x8 grid
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
```

### **Fog of War Implementation**

- Unexplored tiles are covered with an opaque black overlay
- Explored but not visible tiles use a semi-transparent dark overlay
- Currently visible tiles have no fog overlay
- Fog status is stored per player in the tile data

```python
def render_fog_of_war(self, tile, player_id):
    if tile not in player.explored_tiles:
        # Draw completely black fog (unexplored)
        draw_rect(tile.x, tile.y, 256, 256, color=(0, 0, 0, 255))
    elif tile not in player.visible_tiles:
        # Draw semi-transparent fog (explored but not visible)
        draw_rect(tile.x, tile.y, 256, 256, color=(0, 0, 0, 128))
```

---

## User Interaction

### **Map Navigation**

- **Panning**: Right-click drag moves the map viewport

  ```python
  def handle_right_drag(self, start_pos, current_pos):
      delta_x = current_pos[0] - start_pos[0]
      delta_y = current_pos[1] - start_pos[1]
      self.viewport_x -= delta_x / self.zoom
      self.viewport_y -= delta_y / self.zoom
      self.update_visible_tiles()
  ```

- **Zooming**: Mouse wheel adjusts the zoom level

  ```python
  def handle_zoom(self, zoom_direction, mouse_pos):
      # Store pre-zoom mouse world position
      world_x = self.viewport_x + mouse_pos[0] / self.zoom
      world_y = self.viewport_y + mouse_pos[1] / self.zoom

      # Adjust zoom factor (limit between 0.25x and 4x)
      old_zoom = self.zoom
      self.zoom += zoom_direction * 0.1
      self.zoom = max(0.25, min(4.0, self.zoom))

      # Ensure the point under the mouse remains stable
      self.viewport_x = world_x - mouse_pos[0] / self.zoom
      self.viewport_y = world_y - mouse_pos[1] / self.zoom

      self.update_visible_tiles()
  ```

- **Tile Selection**: Left-click selects a tile and reveals information
  ```python
  def handle_tile_selection(self, screen_pos):
      # Convert screen coordinates to world coordinates
      world_x = self.viewport_x + screen_pos[0] / self.zoom
      world_y = self.viewport_y + screen_pos[1] / self.zoom

      # Convert to tile coordinates
      tile_x = int(world_x / 256)
      tile_y = int(world_y / 256)

      # Select the tile if valid
      if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
          self.selected_tile = (tile_x, tile_y)
          self.update_info_panel()
  ```

### **Info Panel**

When a tile is selected, the info panel displays:

1. **Terrain information**: Type, movement cost, defense bonus
2. **Resource details**: Type, yield, improvements
3. **Unit list**: All units currently on the tile (up to 64)
4. **City information**: If a city is present on the tile

```python
def update_info_panel(self):
    if self.selected_tile:
        x, y = self.selected_tile
        tile = self.map.tiles[y][x]

        # Update terrain info
        self.info_panel.set_terrain(tile.terrain_type, tile.movement_cost)

        # Update resource info
        if tile.resource:
            self.info_panel.set_resource(tile.resource.type, tile.resource.yield_value)

        # Update unit list (show all units on this tile)
        units = self.get_units_on_tile(x, y)
        self.info_panel.set_unit_list(units)

        # Update city info
        if tile.has_city:
            self.info_panel.set_city(tile.city)
```

---

## Minimap System

### **Minimap Rendering**

- **Minimap Composition**:
  - Scaled-down representation of the full map (typically 1/8 to 1/16 scale)
  - Only shows tiles that the player has explored
  - Uses simplified tile coloring based on terrain type
  - Overlays a viewport rectangle showing the current visible area

```python
def render_minimap(self, screen, player_id):
    # Calculate minimap dimensions
    minimap_width = self.map_width / 8  # 1/8 scale
    minimap_height = self.map_height / 8

    # Draw border
    pygame.draw.rect(screen, (128, 128, 128), (10, 10, minimap_width + 4, minimap_height + 4), 2)

    # Draw minimap terrain
    for y in range(self.map_height):
        for x in range(self.map_width):
            tile = self.map.tiles[y][x]

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
    viewport_x_ratio = self.viewport_x / (self.map_width * 256)
    viewport_y_ratio = self.viewport_y / (self.map_height * 256)
    viewport_width_ratio = (self.screen_width / self.zoom) / (self.map_width * 256)
    viewport_height_ratio = (self.screen_height / self.zoom) / (self.map_height * 256)

    pygame.draw.rect(screen, (255, 255, 255),
        (12 + viewport_x_ratio * minimap_width,
         12 + viewport_y_ratio * minimap_height,
         viewport_width_ratio * minimap_width,
         viewport_height_ratio * minimap_height), 1)
```

### **Minimap Interaction**

- Left-clicking on the minimap immediately repositions the main viewport
- The clicked position becomes the center of the main view

```python
def handle_minimap_click(self, minimap_pos):
    # Convert minimap position to map position ratio
    x_ratio = (minimap_pos[0] - 12) / (self.minimap_width)
    y_ratio = (minimap_pos[1] - 12) / (self.minimap_height)

    # Convert to world coordinates
    target_world_x = x_ratio * (self.map_width * 256)
    target_world_y = y_ratio * (self.map_height * 256)

    # Adjust viewport to center on this position
    self.viewport_x = target_world_x - (self.screen_width / self.zoom / 2)
    self.viewport_y = target_world_y - (self.screen_height / self.zoom / 2)

    # Ensure viewport stays within map bounds
    self.clamp_viewport_to_map()

    # Update visible tiles for new viewport position
    self.update_visible_tiles()
```

---

This **tile engine architecture** provides a comprehensive system for **terrain rendering**, **unit positioning**, **fog of war**, and **user interaction** with a robust minimap for navigation. The system is optimized for performance with selective rendering of visible tiles and efficient handling of complex game elements.
