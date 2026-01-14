# Grid System

The Grid is the foundation of tile-based games in McRogueFace. It provides efficient rendering, camera controls, and serves as the container for game entities.

## Creating a Grid

```python
import mcrfpy

# Create a scene first
scene = mcrfpy.Scene("game")

# Basic grid creation
grid = mcrfpy.Grid(
    grid_size=(50, 50),      # 50x50 tiles
    texture=mcrfpy.default_texture,  # Built-in tileset
    pos=(0, 0),              # Screen position
    size=(800, 600)          # Display size in pixels
)

# Add to scene
scene.children.append(grid)
```

### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `grid_size` | tuple | Grid dimensions as `(width, height)` in tiles |
| `texture` | Texture | Sprite sheet for tile rendering |
| `pos` | tuple | Screen position `(x, y)` in pixels |
| `size` | tuple | Display size `(width, height)` in pixels |

Alternative keyword arguments:
- `grid_x`, `grid_y` instead of `grid_size`
- `x`, `y` instead of `pos`
- `w`, `h` instead of `size`

## Grid Properties

```python
# Grid dimensions (read-only)
width, height = grid.grid_size
print(f"Grid is {width}x{height} tiles")

# Camera control
grid.center = (25, 25)       # Center camera on tile (25, 25)
grid.center_x = 25           # Individual axis control
grid.center_y = 25
grid.zoom = 2.0              # 2x zoom (closer view)

# Appearance
grid.fill_color = mcrfpy.Color(20, 20, 30)  # Background color
grid.visible = True
grid.opacity = 1.0           # 0.0 to 1.0
```

## GridPoint - Individual Tiles

Each tile in the grid is represented by a `GridPoint` object. Access tiles using the `at()` method:

```python
# Get a specific tile
point = grid.at(10, 15)

# Tile properties
point.walkable = True        # Can entities walk here?
point.transparent = True     # Does light/vision pass through?
point.tilesprite = 0         # Base tile sprite index
point.color = mcrfpy.Color(255, 255, 255)  # Tile tint
```

### GridPoint Properties

| Property | Type | Description |
|----------|------|-------------|
| `walkable` | bool | Whether entities can occupy this tile |
| `transparent` | bool | Whether vision/light passes through |
| `tilesprite` | int | Sprite index from the grid's texture |
| `color` | Color | Tint color applied to the tile |
| `color_overlay` | Color | Additional overlay color (for effects) |
| `tile_overlay` | int | Overlay sprite index (-1 for none) |
| `entities` | list | Entities currently at this position (read-only) |

## Working with Tiles

### Setting Up a Basic Map

```python
# Define tile types
FLOOR = 0
WALL = 1
WATER = 2

# Fill the grid with floors and add walls around the edge
for y in range(50):
    for x in range(50):
        point = grid.at(x, y)

        # Border walls
        if x == 0 or x == 49 or y == 0 or y == 49:
            point.tilesprite = WALL
            point.walkable = False
            point.transparent = False
        else:
            point.tilesprite = FLOOR
            point.walkable = True
            point.transparent = True
```

### Creating Rooms and Corridors

```python
def create_room(grid, x, y, width, height):
    """Carve a rectangular room into the grid."""
    for ry in range(y, y + height):
        for rx in range(x, x + width):
            point = grid.at(rx, ry)
            point.tilesprite = FLOOR
            point.walkable = True
            point.transparent = True

def create_corridor(grid, x1, y1, x2, y2):
    """Create an L-shaped corridor between two points."""
    # Horizontal segment
    for x in range(min(x1, x2), max(x1, x2) + 1):
        point = grid.at(x, y1)
        point.tilesprite = FLOOR
        point.walkable = True
        point.transparent = True

    # Vertical segment
    for y in range(min(y1, y2), max(y1, y2) + 1):
        point = grid.at(x2, y)
        point.tilesprite = FLOOR
        point.walkable = True
        point.transparent = True

# Example usage
create_room(grid, 5, 5, 8, 6)
create_room(grid, 25, 20, 10, 8)
create_corridor(grid, 9, 8, 30, 24)
```

## Entity Placement

Entities are game objects that exist on the grid. They are managed through the `grid.entities` collection.

```python
# Create an entity
player = mcrfpy.Entity(
    grid_pos=(10, 10),       # Position in grid coordinates
    texture=mcrfpy.default_texture,
    sprite_index=64          # '@' character in many tilesets
)

# Add to grid
grid.entities.append(player)

# Entity properties
player.pos = (15, 15)        # Move to new position
player.x = 15                # Individual coordinate access
player.y = 15
player.sprite_number = 64    # Change appearance

# Position can be read as tuple or individual coordinates
x, y = player.pos
print(f"Player at ({player.x}, {player.y})")
```

### Entity Collection Operations

```python
# Access all entities
for entity in grid.entities:
    print(f"Entity at {entity.pos}")

# Get entity count
count = len(grid.entities)

# Remove an entity
grid.entities.remove(entity)

# Find entities at a position
point = grid.at(10, 10)
entities_here = point.entities  # List of entities at this tile
```

### Spawning Multiple Entities

```python
import random

def spawn_enemies(grid, count):
    """Spawn enemies at random walkable positions."""
    enemies = []

    for _ in range(count):
        # Find a walkable position
        while True:
            x = random.randint(1, 48)
            y = random.randint(1, 48)
            point = grid.at(x, y)

            if point.walkable and len(point.entities) == 0:
                break

        # Create enemy entity
        enemy = mcrfpy.Entity(
            grid_pos=(x, y),
            texture=mcrfpy.default_texture,
            sprite_index=111  # 'o' for orc
        )
        grid.entities.append(enemy)
        enemies.append(enemy)

    return enemies

# Spawn 10 enemies
enemies = spawn_enemies(grid, 10)
```

## Camera Control

The grid's camera determines which portion of the grid is visible on screen.

```python
# Center on the player
grid.center = player.pos

# Smooth camera following
def update_camera():
    target_x, target_y = player.pos
    current_x = grid.center_x
    current_y = grid.center_y

    # Lerp toward target (smooth following)
    lerp_speed = 0.1
    grid.center_x = current_x + (target_x - current_x) * lerp_speed
    grid.center_y = current_y + (target_y - current_y) * lerp_speed

# Call every frame
camera_timer = mcrfpy.Timer("camera", lambda t, rt: update_camera(), 0.016)

# Zoom controls
grid.zoom = 1.0   # Default view
grid.zoom = 2.0   # Zoomed in (tiles appear larger)
grid.zoom = 0.5   # Zoomed out (see more tiles)
```

## Grid Layers

Grids support additional layers for visual effects. See [Field of View](fov.md) for details on `ColorLayer`.

```python
# Add a color layer (useful for FOV shading)
color_layer = grid.add_layer("color", z_index=-1)

# Set individual cell colors
color_layer.set(10, 10, mcrfpy.Color(255, 0, 0, 128))  # Red tint

# Fill entire layer
color_layer.fill(mcrfpy.Color(0, 0, 0, 0))  # Clear/transparent
```

## Complete Example

```python
import mcrfpy
import random

# Setup scene
scene = mcrfpy.Scene("game")
scene.activate()

# Create grid
grid = mcrfpy.Grid(
    grid_size=(50, 50),
    texture=mcrfpy.default_texture,
    pos=(0, 0),
    size=(800, 600)
)
scene.children.append(grid)

# Initialize map (all walls)
for y in range(50):
    for x in range(50):
        point = grid.at(x, y)
        point.tilesprite = 1  # Wall
        point.walkable = False
        point.transparent = False

# Carve rooms
rooms = [
    (5, 5, 10, 8),
    (25, 5, 12, 10),
    (8, 25, 15, 12),
    (35, 30, 10, 15)
]

for rx, ry, rw, rh in rooms:
    for y in range(ry, ry + rh):
        for x in range(rx, rx + rw):
            point = grid.at(x, y)
            point.tilesprite = 0  # Floor
            point.walkable = True
            point.transparent = True

# Connect rooms with corridors
for i in range(len(rooms) - 1):
    x1 = rooms[i][0] + rooms[i][2] // 2
    y1 = rooms[i][1] + rooms[i][3] // 2
    x2 = rooms[i+1][0] + rooms[i+1][2] // 2
    y2 = rooms[i+1][1] + rooms[i+1][3] // 2

    # Horizontal then vertical
    for x in range(min(x1, x2), max(x1, x2) + 1):
        point = grid.at(x, y1)
        point.tilesprite = 0
        point.walkable = True
        point.transparent = True

    for y in range(min(y1, y2), max(y1, y2) + 1):
        point = grid.at(x2, y)
        point.tilesprite = 0
        point.walkable = True
        point.transparent = True

# Create player in first room
player = mcrfpy.Entity(
    grid_pos=(10, 9),
    texture=mcrfpy.default_texture,
    sprite_index=64
)
grid.entities.append(player)

# Center camera on player
grid.center = player.pos

# Movement handler
def on_key(key, action):
    if action != "start":
        return

    dx, dy = 0, 0
    key = key.lower()

    if key in ("up", "w"): dy = -1
    elif key in ("down", "s"): dy = 1
    elif key in ("left", "a"): dx = -1
    elif key in ("right", "d"): dx = 1
    else:
        return

    new_x = int(player.x) + dx
    new_y = int(player.y) + dy

    # Check collision
    if grid.at(new_x, new_y).walkable:
        player.pos = (new_x, new_y)
        grid.center = player.pos

scene.on_key = on_key
```

## Notes and Caveats

- Grid coordinates are integers starting at (0, 0)
- The `at()` method returns a reference - changes affect the grid directly
- Entity positions are in grid coordinates, not pixels
- Camera center can be set outside grid bounds (shows empty space)
- Grid rendering is optimized - only visible tiles are drawn
- The `grid_size` property is read-only after creation

## Related Topics

- [Field of View](fov.md) - Visibility and fog of war
- [Pathfinding](pathfinding.md) - A* and Dijkstra algorithms
- [Animation](animation.md) - Smooth entity movement
- [Scene Management](scenes.md) - Organizing game scenes
