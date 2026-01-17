---
layout: default
title: Grid
---

# Grid

Tile-based game world container with pathfinding and FOV support.

## Overview

A `Grid` is a 2D array of tiles that represents your game world. It handles tile rendering with multi-layer support, camera control with zoom and perspective, entity management, and integrates with libtcod for field-of-view calculations and A*/Dijkstra pathfinding.

## Quick Reference

```python
# Create a grid
grid = mcrfpy.Grid(grid_size=(80, 45), texture=texture, pos=(0, 0), size=(800, 600))

# Position and zoom
grid.pos = (100, 50)
grid.zoom = 2.0
grid.center_camera((40, 22))  # Center on tile coordinates

# Work with layers
tile_layer = grid.add_layer('tile', z_index=0, texture=texture)
color_layer = grid.add_layer('color', z_index=1)
tile_layer.set((5, 5), 42)  # Set tile sprite index

# Add entities
player = mcrfpy.Entity(pos=(10, 10), texture=texture, sprite_index=84)
grid.entities.append(player)

# Field of view
grid.fov_radius = 8
grid.compute_fov(player.x, player.y, radius=8)
if grid.is_in_fov(15, 10):
    print("Visible!")

# Pathfinding
path = grid.find_path(player.pos, (20, 15))
next_step = path.walk()

# Dijkstra maps
dijkstra = grid.get_dijkstra_map((goal_x, goal_y))
distance = dijkstra.distance((x, y))
```

## Constructor

```python
mcrfpy.Grid(pos=None, size=None, grid_size=None, texture=None, **kwargs)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pos` | tuple | (0, 0) | Screen position (x, y) |
| `size` | tuple | None | Display size (w, h) |
| `grid_size` | tuple | None | Tile dimensions (columns, rows) |
| `texture` | Texture | None | Default sprite sheet for tiles |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Screen position |
| `w`, `h` | float | Display size |
| `pos` | tuple | Position as (x, y) |
| `size` | tuple | Size as (w, h) |
| `center` | tuple | Camera center in pixel coordinates |
| `center_x`, `center_y` | float | Camera center components |
| `zoom` | float | Camera zoom level (1.0 = normal) |
| `grid_size` | tuple | Tile dimensions (width, height), read-only |
| `grid_w`, `grid_h` | int | Grid dimensions, read-only |
| `texture` | Texture | Default sprite sheet for tiles |
| `fill_color` | Color | Background fill color |
| `entities` | EntityCollection | Entities on this grid |
| `layers` | list | All tile and color layers |
| `perspective` | Entity | Entity used for FOV perspective |
| `perspective_enabled` | bool | Whether perspective rendering is active |
| `fov` | FOV | FOV algorithm to use |
| `fov_radius` | int | Default FOV radius |
| `children` | UICollection | Child UI elements |
| `hovered_cell` | tuple | Currently hovered cell (x, y), read-only |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |
| `z_index` | int | Rendering order |
| `name` | str | Object identifier |
| `align` | str | Alignment mode |
| `on_cell_click` | callable | Cell click callback |
| `on_cell_enter` | callable | Cell hover enter callback |
| `on_cell_exit` | callable | Cell hover exit callback |

## Methods

| Method | Description |
|--------|-------------|
| `at(x, y)` | Get GridPoint at tile coordinates |
| `add_layer(type, **kwargs)` | Add a TileLayer ('tile') or ColorLayer ('color') |
| `remove_layer(layer)` | Remove a layer from the grid |
| `layer(z_index)` | Get layer by z-index |
| `center_camera(pos)` | Center camera on tile coordinates |
| `compute_fov(x, y, radius=None)` | Calculate field of view from position |
| `is_in_fov(x, y)` | Check if tile is visible in current FOV |
| `find_path(start, end)` | Compute A* path, returns AStarPath |
| `get_dijkstra_map(root)` | Get/create Dijkstra map from position |
| `clear_dijkstra_maps()` | Clear cached Dijkstra maps |
| `entities_in_radius(pos, radius)` | Get entities within radius |
| `apply_threshold(heightmap, ...)` | Apply heightmap threshold to grid |
| `apply_ranges(heightmap, ...)` | Apply heightmap ranges to grid |
| `animate(prop, target, ...)` | Animate a property |
| `move(dx, dy)` | Move by offset |
| `resize(w, h)` | Change display size |
| `realign()` | Recompute alignment |

## Cell Callbacks

Grid supports three cell interaction callbacks:

```python
def on_click(grid, cell_pos, button):
    x, y = cell_pos
    print(f"Clicked cell ({x}, {y}) with button {button}")

def on_enter(grid, cell_pos):
    x, y = cell_pos
    print(f"Mouse entered cell ({x}, {y})")

def on_exit(grid, cell_pos):
    x, y = cell_pos
    print(f"Mouse exited cell ({x}, {y})")

grid.on_cell_click = on_click
grid.on_cell_enter = on_enter
grid.on_cell_exit = on_exit
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="GridPoint" class="object-link">GridPoint</a>
<a href="Entity" class="object-link">Entity</a>
<a href="Texture" class="object-link">Texture</a>
<a href="ColorLayer" class="object-link">ColorLayer</a>
<a href="TileLayer" class="object-link">TileLayer</a>
<a href="AStarPath" class="object-link">AStarPath</a>
<a href="DijkstraMap" class="object-link">DijkstraMap</a>
<a href="FOV" class="object-link">FOV</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
