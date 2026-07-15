---
mcrf:
  objects: [Grid, ColorLayer, Entity, FOV, Color]
  diataxis: howto
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

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

grid.compute_fov((player_x, player_y), radius=radius)

# Check if a specific tile is visible
if grid.is_in_fov(30, 28):
    print("Tile (30, 28) is visible")
```

`compute_fov()` takes the origin as a single `pos` argument (tuple, list, or `Vector`) followed by keyword arguments — it does not accept `x, y` as two separate positional arguments. `is_in_fov()` accepts either `(x, y)` separately or as a single tuple.

## FOV Algorithms

McRogueFace supports multiple FOV algorithms through the `mcrfpy.FOV` enum:

```python
# Available algorithms (mcrfpy.FOV is an IntEnum)
mcrfpy.FOV.BASIC          # Simple raycasting
mcrfpy.FOV.DIAMOND        # Diamond-shaped raycasting
mcrfpy.FOV.SHADOW         # Recursive shadowcasting (recommended)
mcrfpy.FOV.RESTRICTIVE    # Restrictive precise angle shadowcasting
mcrfpy.FOV.PERMISSIVE_0   # ... through PERMISSIVE_8

# Specify algorithm when computing FOV
grid.compute_fov((x, y), radius=radius, algorithm=mcrfpy.FOV.SHADOW)
```

### Algorithm Comparison

| Algorithm | Description | Use Case |
|-----------|-------------|----------|
| `FOV.BASIC` | Simple line-based raycasting | Fast, less accurate |
| `FOV.DIAMOND` | Diamond-shaped raycasting | Symmetric, moderate cost |
| `FOV.SHADOW` | Recursive shadowcasting | More natural shadows, preferred for roguelikes |
| `FOV.RESTRICTIVE` / `FOV.PERMISSIVE_0`-`8` | Precise angle-based shadowcasting | Tunable strictness for edge-of-vision cells |

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
fov_layer = mcrfpy.ColorLayer(z_index=-1, name="fog")
grid.add_layer(fov_layer)

def update_fov_display(player_x, player_y, radius):
    # Compute FOV
    grid.compute_fov((player_x, player_y), radius=radius, algorithm=mcrfpy.FOV.SHADOW)

    # Update each tile's color based on visibility
    for y in range(50):
        for x in range(50):
            if grid.is_in_fov(x, y):
                # Visible - bright/clear
                fov_layer.set((x, y), mcrfpy.Color(0, 0, 0, 0))
            else:
                # Not visible - dark overlay
                fov_layer.set((x, y), mcrfpy.Color(0, 0, 0, 200))

# Call whenever player moves
update_fov_display(25, 25, 10)
```

`add_layer()` takes a layer *object*, never a string — construct a `mcrfpy.ColorLayer` (or `mcrfpy.TileLayer`) first, then attach it with `grid.add_layer(layer)`, or pass `layers=[...]` to the `Grid` constructor. `ColorLayer.set()` takes the cell position as a single `(x, y)` tuple, not two separate arguments.

### Three-State Visibility (Explored Memory)

For classic roguelike fog of war with memory of explored areas:

```python
# Track which tiles have been seen
explored = [[False for _ in range(50)] for _ in range(50)]

def update_fov_with_memory(player_x, player_y, radius):
    grid.compute_fov((player_x, player_y), radius=radius, algorithm=mcrfpy.FOV.SHADOW)

    for y in range(50):
        for x in range(50):
            if grid.is_in_fov(x, y):
                # Currently visible
                explored[y][x] = True
                fov_layer.set((x, y), mcrfpy.Color(0, 0, 0, 0))  # Clear
            elif explored[y][x]:
                # Previously seen but not currently visible
                fov_layer.set((x, y), mcrfpy.Color(40, 40, 60, 180))  # Dim
            else:
                # Never seen
                fov_layer.set((x, y), mcrfpy.Color(0, 0, 0, 255))  # Black
```

This hand-rolled `explored` grid is exactly what `entity.perspective_map` gives you for free per-entity — see [Per-Entity Visibility](#per-entity-visibility) below — but computing it manually against a single shared grid-level FOV (as above) is a legitimate approach when you only need one shared "explored" state (e.g. a single-player game with no need to track other actors' knowledge separately).

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

### perspective_map

Every entity has a `perspective_map` property — a `DiscreteMap` recording what that entity has seen. It's lazily allocated the first time it's read, once the entity has a grid, and holds one value per cell: `0`/`mcrfpy.Perspective.UNKNOWN` (never seen), `1`/`mcrfpy.Perspective.DISCOVERED` (seen before, not currently visible), `2`/`mcrfpy.Perspective.VISIBLE` (in current FOV).

```python
player = mcrfpy.Entity(grid_pos=(25, 25), texture=mcrfpy.default_texture, sprite_index=64)
grid.entities.append(player)

# Update this entity's personal visibility
player.update_visibility()

# Check visibility from this entity's perspective (grid_w/grid_h live on
# the underlying GridData, reachable via grid.grid_data)
for y in range(grid.grid_data.grid_h):
    for x in range(grid.grid_data.grid_w):
        state = player.perspective_map[x, y]
        if state == mcrfpy.Perspective.VISIBLE:
            # This cell is currently visible to the entity
            pass
        elif state == mcrfpy.Perspective.DISCOVERED:
            # This cell has been seen before by this entity
            pass
```

### perspective_map Values

| Value | Perspective enum | Description |
|-------|-------------------|-------------|
| `0` | `Perspective.UNKNOWN` | Never seen by this entity |
| `1` | `Perspective.DISCOVERED` | Seen before, not currently visible |
| `2` | `Perspective.VISIBLE` | Currently visible to this entity |

### Entity Visibility Methods

```python
# Update an entity's FOV (call after movement)
entity.update_visibility()

# entity.at(x, y) returns the GridPoint only if that cell is currently
# VISIBLE to this entity's perspective_map; otherwise it returns None.
point = entity.at(10, 15)
if point is not None:
    print("Entity can see (10, 15)")
```

## Perspective Rendering

A `Grid` (view) can render from a specific entity's perspective, showing only what that entity has discovered/can see. `grid.perspective` takes an `Entity`, not an index:

```python
# Render from a specific entity's perspective
grid.perspective = player

# Omniscient view - show everything
grid.perspective = None
```

### apply_perspective() for Entity-Based FOV

```python
# Create a color layer for FOV overlay
fov_layer = mcrfpy.ColorLayer(z_index=-1, name="fog")
grid.add_layer(fov_layer)

# Apply perspective from a specific entity
fov_layer.apply_perspective(
    entity=player,
    visible=mcrfpy.Color(0, 0, 0, 0),          # Clear - show tile normally
    discovered=mcrfpy.Color(40, 40, 60, 180),   # Dim overlay for memory
    unknown=mcrfpy.Color(0, 0, 0, 255)          # Black - hide completely
)

# Call after the entity moves to refresh the layer
fov_layer.update_perspective()
```

## Complete FOV Example

```python
import mcrfpy

# Setup
scene = mcrfpy.Scene("game")
mcrfpy.current_scene = scene

# Create grid
grid = mcrfpy.Grid(
    grid_size=(40, 30),
    texture=mcrfpy.default_texture,
    pos=(0, 0),
    size=(800, 600)
)
scene.children.append(grid)

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
fov_layer = mcrfpy.ColorLayer(z_index=-1, name="fog")
grid.add_layer(fov_layer)

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
    px, py = player.grid_x, player.grid_y
    radius = 8

    # Compute FOV
    grid.compute_fov((px, py), radius=radius, algorithm=mcrfpy.FOV.SHADOW)

    # Update visibility display
    for y in range(30):
        for x in range(40):
            if grid.is_in_fov(x, y):
                explored[y][x] = True
                fov_layer.set((x, y), mcrfpy.Color(0, 0, 0, 0))
            elif explored[y][x]:
                fov_layer.set((x, y), mcrfpy.Color(30, 30, 50, 180))
            else:
                fov_layer.set((x, y), mcrfpy.Color(0, 0, 0, 255))

# Initial FOV calculation
update_fov()
grid.center = player.pos

# Movement with FOV update
def on_key(key, action):
    if action != mcrfpy.InputState.PRESSED:
        return

    dx, dy = 0, 0

    if key in (mcrfpy.Key.UP, mcrfpy.Key.W): dy = -1
    elif key in (mcrfpy.Key.DOWN, mcrfpy.Key.S): dy = 1
    elif key in (mcrfpy.Key.LEFT, mcrfpy.Key.A): dx = -1
    elif key in (mcrfpy.Key.RIGHT, mcrfpy.Key.D): dx = 1
    else:
        return

    new_x = player.grid_x + dx
    new_y = player.grid_y + dy

    if 0 <= new_x < 40 and 0 <= new_y < 30:
        if grid.at(new_x, new_y).walkable:
            player.grid_pos = (new_x, new_y)
            grid.center = player.pos
            update_fov()

scene.on_key = on_key
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
        ex, ey = entity.grid_x, entity.grid_y
        if grid.is_in_fov(ex, ey):
            visible.append(entity)
    return visible

# Only show enemies in FOV
def update_entity_visibility():
    for entity in grid.entities:
        if entity == player:
            entity.visible = True
            continue
        ex, ey = entity.grid_x, entity.grid_y
        entity.visible = grid.is_in_fov(ex, ey)
```

`entity.x`/`entity.y` are *pixel* coordinates relative to the grid (requires grid attachment); the logical tile coordinates are `entity.grid_x`/`entity.grid_y` (aliases: `cell_x`/`cell_y`). A simpler alternative for this exact check is `player.visible_entities()`, which returns the list of other entities visible from an entity's own position directly.

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
