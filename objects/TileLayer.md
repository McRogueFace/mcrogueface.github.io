---
layout: default
title: TileLayer
mcrf:
  objects: [TileLayer, Grid, HeightMap, Texture]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# TileLayer

Grid layer storing sprite indices per cell.

## Overview

A `TileLayer` stores tile sprite indices for each cell in a Grid. Use tile layers for terrain, walls, decorations, or any tile-based graphics. Multiple tile layers can be stacked using z-index ordering to create parallax effects or separate visual concerns.

## Quick Reference

```python
# Create standalone, then attach with Grid.add_layer() (a layer OBJECT, not a string)
floor_layer = mcrfpy.TileLayer(z_index=0, texture=floor_texture)
grid.add_layer(floor_layer)

wall_layer = mcrfpy.TileLayer(z_index=1, texture=wall_texture)
grid.add_layer(wall_layer)

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

`TileLayer` objects are constructed standalone, then attached to a Grid with
`Grid.add_layer()` (or passed in the Grid constructor's `layers=[...]` list).
`add_layer()` takes a layer object -- never a string:

```python
tile_layer = mcrfpy.TileLayer(z_index=0, texture=my_texture, grid_size=(80, 45))
grid.add_layer(tile_layer)
```

Direct instantiation:

```python
mcrfpy.TileLayer(z_index=-1, name=None, texture=None, grid_size=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `z_index` | int | -1 | Rendering order (higher = on top) |
| `name` | str | None | Layer name, used for `Grid.layer(name)` lookup |
| `texture` | Texture | None | Sprite sheet for tiles |
| `grid_size` | tuple | None | Size (w, h); auto-resizes to match the Grid when attached if None or (0, 0) |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `z_index` | int | Rendering order relative to entities |
| `name` | str | Layer name, read-only |
| `visible` | bool | Visibility toggle |
| `texture` | Texture \| None | Sprite sheet for tiles |
| `grid_size` | tuple | Layer dimensions (w, h), read-only |
| `grid` | Grid \| None | Parent Grid; setting manages layer association |

## Methods

| Method | Description |
|--------|-------------|
| `at(pos)` | Get sprite index at cell position |
| `set(pos, sprite_index)` | Set sprite index at cell position |
| `fill(sprite_index)` | Fill entire layer with sprite |
| `fill_rect(pos, size, sprite_index)` | Fill rectangular region |
| `apply_threshold(heightmap, range, tile)` | Set `tile` for cells whose heightmap value falls in `range=(min, max)` |
| `apply_ranges(heightmap, ranges)` | Set tiles by heightmap value ranges; `ranges` is a list of `((min, max), tile_index)` tuples |
| `edit()` | Context manager yielding a zero-copy numpy view (int32, shape `(height, width)`) of the tile indices |

## Usage Patterns

### Multi-Layer Terrain

```python
# Base terrain layer
ground = mcrfpy.TileLayer(z_index=0, texture=terrain_tex)
grid.add_layer(ground)
ground.fill(GRASS_TILE)

# Water layer
water = mcrfpy.TileLayer(z_index=1, texture=terrain_tex)
grid.add_layer(water)
# Only set water tiles where needed, leave rest transparent

# Decoration layer (trees, rocks)
decor = mcrfpy.TileLayer(z_index=2, texture=decor_tex)
grid.add_layer(decor)
```

### Procedural Generation with Heightmap

```python
terrain = mcrfpy.TileLayer(z_index=0, texture=tiles)
grid.add_layer(terrain)

# Use a threshold for simple water/land: (min, max) range -> single tile
terrain.apply_threshold(heightmap, range=(0.0, 0.3), tile=WATER_TILE)
terrain.apply_threshold(heightmap, range=(0.3, 1.0), tile=GRASS_TILE)

# Or use ranges for more variety: list of ((min, max), tile_index)
terrain.apply_ranges(heightmap, [
    ((0.0, 0.2), DEEP_WATER),
    ((0.2, 0.35), SHALLOW_WATER),
    ((0.35, 0.6), GRASS),
    ((0.6, 0.8), HILLS),
    ((0.8, 1.0), MOUNTAIN)
])
```

### Building Structures

```python
walls = mcrfpy.TileLayer(z_index=1, texture=wall_tex)
grid.add_layer(walls)

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
floor_layer = mcrfpy.TileLayer(z_index=0, texture=tex)
grid.add_layer(floor_layer)
roof_layer = mcrfpy.TileLayer(z_index=5, texture=tex)
grid.add_layer(roof_layer)

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
