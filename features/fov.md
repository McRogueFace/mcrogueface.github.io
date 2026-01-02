# Field of View

McRogueFace provides a complete field of view (FOV) system for implementing visibility, fog of war, and line-of-sight mechanics in your roguelike games.

## Basic FOV Computation

The simplest FOV workflow: compute visibility from a position, then check which tiles are visible.

```python
import mcrfpy

# Assuming you have a grid set up
grid = mcrfpy.Grid(grid_size=(50, 50), texture=mcrfpy.default_texture)

# Compute FOV from player position
player_x, player_y = 25, 25
radius = 10

grid.compute_fov(player_x, player_y, radius)

# Check if a specific tile is visible
if grid.is_in_fov(30, 28):
    print("Tile (30, 28) is visible")
```

## FOV Algorithms

McRogueFace supports multiple FOV algorithms through the `mcrfpy.FOV` enum:

```python
# Available algorithms
mcrfpy.FOV.BASIC     # Simple raycasting
mcrfpy.FOV.SHADOW    # Shadow casting (recommended)

# Specify algorithm when computing FOV
grid.compute_fov(x, y, radius, algorithm=mcrfpy.FOV.SHADOW)
```

### Algorithm Comparison

| Algorithm | Description | Use Case |
|-----------|-------------|----------|
| `FOV.BASIC` | Simple line-based raycasting | Fast, less accurate |
| `FOV.SHADOW` | Recursive shadowcasting | More natural shadows, preferred for roguelikes |

## Wall Transparency

FOV respects the `transparent` property of each GridPoint:

```python
# Walls block vision
wall = grid.at(20, 20)
wall.walkable = False
wall.transparent = False  # Blocks line of sight

# Glass/bars - can see through but not walk through
bars = grid.at(21, 20)
bars.walkable = False
bars.transparent = True   # Vision passes through

# Water - can walk through (maybe slowly) and see through
water = grid.at(22, 20)
water.walkable = True
water.transparent = True
```

## ColorLayer for FOV Visualization

Use a `ColorLayer` to visually distinguish visible, explored, and unknown areas.

### Basic FOV Shading

```python
# Add a color layer below entities (z_index=-1)
fov_layer = grid.add_layer("color", z_index=-1)

def update_fov_display(player_x, player_y, radius):
    # Compute FOV
    grid.compute_fov(player_x, player_y, radius, mcrfpy.FOV.SHADOW)

    # Update each tile's color based on visibility
    for y in range(50):
        for x in range(50):
            if grid.is_in_fov(x, y):
                # Visible - bright/clear
                fov_layer.set(x, y, mcrfpy.Color(0, 0, 0, 0))
            else:
                # Not visible - dark overlay
                fov_layer.set(x, y, mcrfpy.Color(0, 0, 0, 200))

# Call whenever player moves
update_fov_display(25, 25, 10)
```

### Three-State Visibility (Explored Memory)

For classic roguelike fog of war with memory of explored areas:

```python
# Track which tiles have been seen
explored = [[False for _ in range(50)] for _ in range(50)]

def update_fov_with_memory(player_x, player_y, radius):
    grid.compute_fov(player_x, player_y, radius, mcrfpy.FOV.SHADOW)

    for y in range(50):
        for x in range(50):
            if grid.is_in_fov(x, y):
                # Currently visible
                explored[y][x] = True
                fov_layer.set(x, y, mcrfpy.Color(0, 0, 0, 0))  # Clear
            elif explored[y][x]:
                # Previously seen but not currently visible
                fov_layer.set(x, y, mcrfpy.Color(40, 40, 60, 180))  # Dim
            else:
                # Never seen
                fov_layer.set(x, y, mcrfpy.Color(0, 0, 0, 255))  # Black
```

### Using draw_fov() Helper

The `ColorLayer` provides a built-in method for FOV-based coloring:

```python
fov_layer.draw_fov(
    source=(player_x, player_y),
    radius=10,
    fov=mcrfpy.FOV.SHADOW,
    visible=mcrfpy.Color(255, 255, 200, 64),     # Yellow tint for visible
    discovered=mcrfpy.Color(100, 100, 100, 128), # Gray for explored
    unknown=mcrfpy.Color(0, 0, 0, 255)           # Black for unknown
)
```

## Per-Entity Visibility

Each entity can maintain its own visibility state, useful for:
- Enemy AI that only "knows" what it has seen
- Multiple characters with independent vision
- Replay/review of what entities saw

### GridPointState

Every entity has a `gridstate` property - a collection of `GridPointState` objects tracking what that entity can see:

```python
player = mcrfpy.Entity(grid_pos=(25, 25), texture=texture, sprite_index=64)
grid.entities.append(player)

# Update this entity's personal visibility
player.update_visibility()

# Check visibility from this entity's perspective
for state in player.gridstate:
    if state.visible:
        # This cell is currently visible to the entity
        pass
    if state.discovered:
        # This cell has been seen before by this entity
        pass
```

### GridPointState Properties

| Property | Type | Description |
|----------|------|-------------|
| `visible` | bool | Currently visible to this entity |
| `discovered` | bool | Has ever been seen by this entity |

### Entity Visibility Methods

```python
# Update an entity's FOV (call after movement)
entity.update_visibility()

# Access per-cell state
state = entity.at(10, 15)
if state.visible:
    print("Entity can see (10, 15)")
```

## Perspective Rendering

The grid can render from a specific entity's perspective, showing only what that entity can see:

```python
# Render from first entity's perspective
grid.perspective = 0

# Render from second entity's perspective
grid.perspective = 1

# Omniscient view - show everything
grid.perspective = -1
```

### apply_perspective() for Entity-Based FOV

```python
# Create a color layer for FOV overlay
fov_layer = grid.add_layer("color", z_index=-1)

# Apply perspective from a specific entity
fov_layer.apply_perspective(
    entity=player,
    visible=mcrfpy.Color(0, 0, 0, 0),          # Clear - show tile normally
    discovered=mcrfpy.Color(40, 40, 60, 180),   # Dim overlay for memory
    unknown=mcrfpy.Color(0, 0, 0, 255)          # Black - hide completely
)
```

## Complete FOV Example

```python
import mcrfpy

# Setup
mcrfpy.createScene("game")
mcrfpy.setScene("game")

# Create grid
grid = mcrfpy.Grid(
    grid_size=(40, 30),
    texture=mcrfpy.default_texture,
    pos=(0, 0),
    size=(800, 600)
)
mcrfpy.sceneUI("game").append(grid)

# Initialize map with walls and floors
for y in range(30):
    for x in range(40):
        point = grid.at(x, y)
        # Border walls
        if x == 0 or x == 39 or y == 0 or y == 29:
            point.tilesprite = 1
            point.walkable = False
            point.transparent = False
        # Some interior walls
        elif x == 15 and 5 <= y <= 20:
            point.tilesprite = 1
            point.walkable = False
            point.transparent = False
        elif y == 15 and 20 <= x <= 30:
            point.tilesprite = 1
            point.walkable = False
            point.transparent = False
        else:
            point.tilesprite = 0
            point.walkable = True
            point.transparent = True

# Add FOV color layer
fov_layer = grid.add_layer("color", z_index=-1)

# Track explored tiles
explored = [[False for _ in range(40)] for _ in range(30)]

# Create player
player = mcrfpy.Entity(
    grid_pos=(5, 5),
    texture=mcrfpy.default_texture,
    sprite_index=64
)
grid.entities.append(player)

# FOV update function
def update_fov():
    px, py = int(player.x), int(player.y)
    radius = 8

    # Compute FOV
    grid.compute_fov(px, py, radius, mcrfpy.FOV.SHADOW)

    # Update visibility display
    for y in range(30):
        for x in range(40):
            if grid.is_in_fov(x, y):
                explored[y][x] = True
                fov_layer.set(x, y, mcrfpy.Color(0, 0, 0, 0))
            elif explored[y][x]:
                fov_layer.set(x, y, mcrfpy.Color(30, 30, 50, 180))
            else:
                fov_layer.set(x, y, mcrfpy.Color(0, 0, 0, 255))

# Initial FOV calculation
update_fov()
grid.center = player.pos

# Movement with FOV update
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

    if 0 <= new_x < 40 and 0 <= new_y < 30:
        if grid.at(new_x, new_y).walkable:
            player.pos = (new_x, new_y)
            grid.center = player.pos
            update_fov()

mcrfpy.keypressScene(on_key)
```

## Enemy Visibility

Check if enemies are visible before rendering or taking actions:

```python
def get_visible_enemies():
    """Return list of enemies the player can see."""
    visible = []
    for entity in grid.entities:
        if entity == player:
            continue
        ex, ey = int(entity.x), int(entity.y)
        if grid.is_in_fov(ex, ey):
            visible.append(entity)
    return visible

# Only show enemies in FOV
def update_entity_visibility():
    for entity in grid.entities:
        if entity == player:
            entity.visible = True
            continue
        ex, ey = int(entity.x), int(entity.y)
        entity.visible = grid.is_in_fov(ex, ey)
```

## Performance Considerations

- FOV computation is fast but should still be done only when needed (on player move, not every frame)
- `ColorLayer` updates are efficient - updating individual cells is O(1)
- For very large grids (100x100+), consider computing FOV less frequently
- The `SHADOW` algorithm is slightly slower but produces better results than `BASIC`

## Notes and Caveats

- FOV must be recomputed after the viewer moves
- `transparent` on GridPoint must be set correctly for FOV to work
- FOV radius is in tiles, not pixels
- Entity visibility state is independent of grid FOV state
- `grid.is_in_fov()` checks the most recent `compute_fov()` result

## Related Topics

- [Grid System](grid_system.md) - Grid creation and tile properties
- [Pathfinding](pathfinding.md) - A* and Dijkstra algorithms
- [Scene Management](scenes.md) - Organizing game scenes
