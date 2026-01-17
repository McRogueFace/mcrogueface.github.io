---
layout: default
title: Grid
---

# Grid

Tile-based game world container.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `Grid` is a 2D array of tiles that represents your game world. It handles tile rendering, camera control, entity management, and integrates with libtcod for FOV and pathfinding.

## Quick Reference

```python
# Create a grid
grid = mcrfpy.Grid(grid_size=(80, 45), texture=texture)

# Position and zoom
grid.pos = (100, 50)
grid.zoom = 2.0

# Access tiles
cell = grid.at(x, y)
cell.tilesprite = 0
cell.walkable = True

# Add entities
player = mcrfpy.Entity(pos=(10, 10), texture=texture, sprite_index=84)
grid.entities.append(player)

# FOV
grid.compute_fov(player.x, player.y, radius=8)

# Pathfinding
path = grid.compute_astar_path(start_x, start_y, end_x, end_y)
```

## Constructor

```python
mcrfpy.Grid(grid_size: tuple, texture: Texture, pos: tuple = (0, 0), size: tuple = None)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Position |
| `w`, `h` | float | Size |
| `grid_size` | tuple | Tile dimensions (width, height) |
| `texture` | Texture | Sprite sheet for tiles |
| `zoom` | float | Camera zoom level |
| `entities` | EntityCollection | Entities on this grid |
| `perspective` | Entity | FOV perspective entity |

## Methods

| Method | Description |
|--------|-------------|
| `at(x, y)` | Get GridPoint at coordinates |
| `compute_fov(x, y, radius)` | Calculate field of view |
| `compute_astar_path(x1, y1, x2, y2)` | A* pathfinding |
| `compute_dijkstra(x, y)` | Dijkstra distance map |
| `get_dijkstra_distance(x, y)` | Distance to point |

## Related

<div class="related-objects">
<div class="object-links">
<a href="GridPoint" class="object-link">GridPoint</a>
<a href="Entity" class="object-link">Entity</a>
<a href="Texture" class="object-link">Texture</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
