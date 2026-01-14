---
layout: default
title: Fog of War
parent: Cookbook
nav_order: 1
---

# Basic Fog of War

![Fog of War Recipe](/images/cookbook/grid_fog_of_war.png)

Create classic roguelike visibility with visible, discovered, and unknown areas using the Grid's FOV system.

---

## Overview

Fog of war provides three visibility states:
- **Visible**: Currently in player's line of sight (fully lit)
- **Discovered**: Previously seen but not currently visible (dimmed)
- **Unknown**: Never seen (completely black)

---

## Quick Start

```python
import mcrfpy

# Create scene and grid
scene = mcrfpy.Scene("game")
texture = mcrfpy.Texture("assets/dungeon.png", 16, 16)
grid = mcrfpy.Grid(50, 50, texture, 0, 0, 800, 600)

# Add player entity
player = mcrfpy.Entity((25, 25), texture, 0)
grid.entities.append(player)

# Set player as the perspective for FOV
grid.perspective = 0  # Index of player entity
```

---

## Computing Field of View

Use the built-in shadowcasting algorithm:

```python
def update_fov():
    """Recompute FOV from player's position."""
    px, py = player.pos

    # Compute FOV with radius 10, using shadowcasting algorithm
    grid.compute_fov(px, py, radius=10, algorithm=mcrfpy.FOV.SHADOW)

# Call after every player move
def move_player(dx, dy):
    px, py = player.pos
    new_x, new_y = px + dx, py + dy

    # Check if destination is walkable
    if grid.at(new_x, new_y).walkable:
        player.pos = (new_x, new_y)
        update_fov()
```

---

## Rendering with ColorLayer

The ColorLayer applies visibility shading automatically:

```python
# Add a color layer for FOV shading (behind tiles)
color_layer = grid.add_layer("color", z_index=-1)

# Apply perspective-based coloring
color_layer.apply_perspective(
    entity=player,
    visible=mcrfpy.Color(0, 0, 0, 0),       # Transparent - fully visible
    discovered=mcrfpy.Color(40, 40, 60, 180), # Dim blue-gray overlay
    unknown=mcrfpy.Color(0, 0, 0, 255)       # Solid black
)
```

---

## Complete Example

```python
import mcrfpy

# Scene setup
scene = mcrfpy.Scene("dungeon")

# Load tileset
texture = mcrfpy.Texture("assets/dungeon.png", 16, 16)

# Create grid
grid = mcrfpy.Grid(50, 50, texture, 0, 0, 800, 600)
scene.children.append(grid)

# Initialize dungeon - walls block sight and movement
for x in range(50):
    for y in range(50):
        point = grid.at(x, y)
        if x == 0 or y == 0 or x == 49 or y == 49:
            # Outer walls
            point.tilesprite = 1  # Wall tile
            point.walkable = False
            point.transparent = False
        else:
            # Floor tiles
            point.tilesprite = 0  # Floor tile
            point.walkable = True
            point.transparent = True

# Add some pillars to test LOS blocking
pillars = [(10, 10), (20, 15), (30, 25), (15, 35)]
for px, py in pillars:
    point = grid.at(px, py)
    point.tilesprite = 2  # Pillar tile
    point.walkable = False
    point.transparent = False

# Create player
player = mcrfpy.Entity((25, 25), texture, 64)  # Player sprite
grid.entities.append(player)

# Set perspective to player
grid.perspective = 0

# Add fog of war layer
fog_layer = grid.add_layer("color", z_index=-1)

def update_visibility():
    """Update FOV and fog colors."""
    px, py = player.pos

    # Compute new FOV
    grid.compute_fov(px, py, radius=8, algorithm=mcrfpy.FOV.SHADOW)

    # Update fog layer colors
    fog_layer.apply_perspective(
        entity=player,
        visible=mcrfpy.Color(0, 0, 0, 0),
        discovered=mcrfpy.Color(20, 20, 40, 160),
        unknown=mcrfpy.Color(0, 0, 0, 255)
    )

def handle_input(key, state):
    if state != "start":
        return

    px, py = player.pos
    dx, dy = 0, 0

    if key in ("w", "Up"):
        dy = -1
    elif key in ("s", "Down"):
        dy = 1
    elif key in ("a", "Left"):
        dx = -1
    elif key in ("d", "Right"):
        dx = 1

    if dx != 0 or dy != 0:
        new_x, new_y = px + dx, py + dy
        if grid.at(new_x, new_y).walkable:
            player.pos = (new_x, new_y)
            update_visibility()

scene.on_key = handle_input

# Initial FOV calculation
update_visibility()

# Center camera on player
grid.center = player.pos

scene.activate()
```

---

## Checking Visibility in Code

Query visibility state for game logic:

```python
def is_tile_visible(x, y):
    """Check if a tile is currently visible to the player."""
    return grid.is_in_fov(x, y)

def is_tile_discovered(x, y):
    """Check if a tile has ever been seen."""
    state = player.at(x, y)  # Get GridPointState
    return state.discovered

def get_visible_enemies():
    """Return list of enemies the player can see."""
    visible = []
    for entity in grid.entities:
        if entity != player:
            ex, ey = entity.pos
            if grid.is_in_fov(ex, ey):
                visible.append(entity)
    return visible
```

---

## FOV Algorithms

McRogueFace supports multiple FOV algorithms:

```python
# Shadowcasting (default) - fast and produces nice results
grid.compute_fov(x, y, 10, mcrfpy.FOV.SHADOW)

# Recursive shadowcasting - slightly different corner behavior
grid.compute_fov(x, y, 10, mcrfpy.FOV.RECURSIVE_SHADOW)

# Diamond - simple but produces diamond-shaped FOV
grid.compute_fov(x, y, 10, mcrfpy.FOV.DIAMOND)

# Permissive - sees more tiles, good for tactical games
grid.compute_fov(x, y, 10, mcrfpy.FOV.PERMISSIVE)
```

---

## Tips

1. **Call update after movement**: Always recompute FOV after the player moves
2. **Transparent vs Walkable**: A tile can be see-through but not walkable (glass, water)
3. **Layer z-index**: Use negative z-index so fog renders behind entities
4. **Memory**: GridPointState tracks discovered tiles per-entity
5. **Performance**: compute_fov is optimized - safe to call every frame if needed

---

## Related Recipes

- [Dungeon Generator](grid_dungeon_generator.md) - Generate maps with walls
- [Dijkstra Maps](grid_dijkstra.md) - Pathfinding that respects visibility
- [Cell Highlighting](grid_cell_highlighting.md) - Highlight visible targets
