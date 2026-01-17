---
layout: default
title: TileLayer
---

# TileLayer

Grid layer storing sprite indices per cell.

## Overview

A `TileLayer` stores tile sprite indices for each cell in a Grid. Use tile layers for terrain, walls, decorations, or any tile-based graphics. Multiple tile layers can be stacked using z-index ordering to create parallax effects or separate visual concerns.

## Quick Reference

```python
# Create via Grid.add_layer()
floor_layer = grid.add_layer('tile', z_index=0, texture=floor_texture)
wall_layer = grid.add_layer('tile', z_index=1, texture=wall_texture)

# Set individual tile sprites
floor_layer.set((5, 5), 42)  # Set sprite index 42 at position (5, 5)

# Fill entire layer with one tile
floor_layer.fill(0)  # Fill with sprite index 0

# Fill rectangular region
wall_layer.fill_rect((0, 0), (80, 1), 16)  # Top wall

# Get tile at position
sprite_idx = floor_layer.at((5, 5))
```

## Constructor

`TileLayer` is typically created via `Grid.add_layer()`:

```python
tile_layer = grid.add_layer('tile', z_index=0, texture=my_texture, grid_size=(80, 45))
```

Direct instantiation:

```python
mcrfpy.TileLayer(z_index=-1, texture=None, grid_size=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `z_index` | int | -1 | Rendering order (higher = on top) |
| `texture` | Texture | None | Sprite sheet for tiles |
| `grid_size` | tuple | None | Size (w, h), inherits from Grid if None |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `z_index` | int | Rendering order |
| `visible` | bool | Visibility toggle |
| `texture` | Texture | Sprite sheet for tiles |
| `grid_size` | tuple | Layer dimensions (w, h), read-only |

## Methods

| Method | Description |
|--------|-------------|
| `at(pos)` | Get sprite index at cell position |
| `set(pos, sprite_index)` | Set sprite index at cell position |
| `fill(sprite_index)` | Fill entire layer with sprite |
| `fill_rect(pos, size, sprite_index)` | Fill rectangular region |
| `apply_threshold(heightmap, threshold, below, above)` | Set tiles by heightmap threshold |
| `apply_ranges(heightmap, ranges)` | Set tiles by heightmap value ranges |

## Usage Patterns

### Multi-Layer Terrain

```python
# Base terrain layer
ground = grid.add_layer('tile', z_index=0, texture=terrain_tex)
ground.fill(GRASS_TILE)

# Water layer
water = grid.add_layer('tile', z_index=1, texture=terrain_tex)
# Only set water tiles where needed, leave rest transparent

# Decoration layer (trees, rocks)
decor = grid.add_layer('tile', z_index=2, texture=decor_tex)
```

### Procedural Generation with Heightmap

```python
terrain = grid.add_layer('tile', z_index=0, texture=tiles)

# Use threshold for simple water/land
terrain.apply_threshold(
    heightmap,
    threshold=0.3,
    below=WATER_TILE,
    above=GRASS_TILE
)

# Or use ranges for more variety
terrain.apply_ranges(heightmap, [
    (0.0, 0.2, DEEP_WATER),
    (0.2, 0.35, SHALLOW_WATER),
    (0.35, 0.6, GRASS),
    (0.6, 0.8, HILLS),
    (0.8, 1.0, MOUNTAIN)
])
```

### Building Structures

```python
walls = grid.add_layer('tile', z_index=1, texture=wall_tex)

def draw_room(x, y, w, h):
    # Top and bottom walls
    walls.fill_rect((x, y), (w, 1), WALL_H)
    walls.fill_rect((x, y + h - 1), (w, 1), WALL_H)

    # Left and right walls
    for row in range(y, y + h):
        walls.set((x, row), WALL_V)
        walls.set((x + w - 1, row), WALL_V)

    # Corners
    walls.set((x, y), CORNER_TL)
    walls.set((x + w - 1, y), CORNER_TR)
    walls.set((x, y + h - 1), CORNER_BL)
    walls.set((x + w - 1, y + h - 1), CORNER_BR)

draw_room(10, 5, 15, 10)
```

### Layer Visibility Toggle

```python
floor_layer = grid.add_layer('tile', z_index=0, texture=tex)
roof_layer = grid.add_layer('tile', z_index=5, texture=tex)

def toggle_roof():
    roof_layer.visible = not roof_layer.visible

# When player enters building, hide roof
roof_layer.visible = False
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="ColorLayer" class="object-link">ColorLayer</a>
<a href="Texture" class="object-link">Texture</a>
<a href="GridPoint" class="object-link">GridPoint</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
