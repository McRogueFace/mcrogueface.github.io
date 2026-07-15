---
layout: default
title: ColorLayer
mcrf:
  objects: [ColorLayer, Color, Grid]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# ColorLayer

Grid layer storing RGBA colors per cell.

## Overview

A `ColorLayer` stores color data for each cell in a Grid. Use color layers for lighting effects, fog of war visualization, terrain tinting, or any per-cell color overlay. Color layers can be stacked with tile layers using z-index ordering.

## Quick Reference

```python
# Create standalone, then attach to a Grid
color_layer = mcrfpy.ColorLayer(z_index=1, name="tint")
grid.add_layer(color_layer)

# Set individual cell colors
color_layer.set((5, 5), mcrfpy.Color(255, 0, 0, 128))  # Semi-transparent red

# Fill entire layer
color_layer.fill(mcrfpy.Color(0, 0, 0, 200))  # Dark overlay

# Fill rectangular region
color_layer.fill_rect((10, 10), (20, 20), mcrfpy.Color(50, 50, 100))

# Get cell color
cell_color = color_layer.at((5, 5))

# FOV visualization
color_layer.draw_fov((player_x, player_y), radius=8)  # Paint FOV-based visibility colors
```

## Constructor

`ColorLayer` is created directly, then attached to a `Grid` with `Grid.add_layer()`
(or passed via the Grid constructor's `layers=` list). A layer created with
`grid_size=None` (or `(0, 0)`) auto-resizes to match the Grid when attached.

```python
color_layer = mcrfpy.ColorLayer(z_index=1, name="tint")
grid.add_layer(color_layer)

# Or supply it at construction time
grid = mcrfpy.Grid(grid_size=(80, 45), layers=[color_layer])
```

Full signature:

```python
mcrfpy.ColorLayer(z_index=-1, name=None, grid_size=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `z_index` | int | -1 | Rendering order relative to entities (negative = background, positive = overlay) |
| `name` | str | None | Layer name for `Grid.layer(name)` lookup |
| `grid_size` | tuple | None | Size (w, h); auto-resizes to match the Grid if None or (0, 0) |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `z_index` | int | Rendering order relative to entities |
| `name` | str | Layer name for lookup, read-only |
| `visible` | bool | Visibility toggle |
| `grid_size` | tuple | Layer dimensions (w, h), read-only |
| `grid` | Grid \| None | Parent Grid; setting it manages layer association |

## Methods

| Method | Description |
|--------|-------------|
| `at(pos)` | Get Color at cell position |
| `set(pos, color)` | Set Color at cell position |
| `fill(color)` | Fill entire layer with color |
| `fill_rect(pos, size, color)` | Fill rectangular region |
| `draw_fov(source, radius=None, fov=None, visible=None, discovered=None, unknown=None)` | Paint cells by FOV visibility from `source` (an (x, y) cell) |
| `apply_perspective(entity, visible=None, discovered=None, unknown=None)` | Bind layer to an entity for automatic FOV-based coloring |
| `update_perspective()` | Redraw FOV colors after the bound entity moves |
| `clear_perspective()` | Remove the perspective binding |
| `apply_threshold(source, range, color) -> ColorLayer` | Set a fixed color for cells whose heightmap value falls in `range` |
| `apply_gradient(source, range, color_low, color_high) -> ColorLayer` | Interpolate color across a heightmap value range |
| `apply_ranges(source, ranges) -> ColorLayer` | Apply multiple threshold/gradient ranges in one pass |
| `edit()` | Context manager exposing a zero-copy writable numpy view, shape (h, w, 4), dtype uint8 |

## Usage Patterns

### Fog of War

```python
# Create darkness layer
fog = mcrfpy.ColorLayer(z_index=10, name="fog")
grid.add_layer(fog)
fog.fill(mcrfpy.Color(0, 0, 0, 255))  # Start fully dark

# Update when the player moves: paint FOV-based visibility colors
def update_fov(player):
    fog.draw_fov((player.cell_pos.x, player.cell_pos.y), radius=8,
                 visible=mcrfpy.Color(0, 0, 0, 0),        # fully lit
                 discovered=mcrfpy.Color(0, 0, 0, 160),   # dimmed memory
                 unknown=mcrfpy.Color(0, 0, 0, 255))      # fully dark
```

For fog that updates automatically whenever a specific entity moves, bind the
layer to it instead of calling `draw_fov()` manually:

```python
fog.apply_perspective(player, visible=mcrfpy.Color(0, 0, 0, 0),
                       discovered=mcrfpy.Color(0, 0, 0, 160),
                       unknown=mcrfpy.Color(0, 0, 0, 255))
# ... after the player moves:
fog.update_perspective()
```

### Lighting Effects

```python
light_layer = mcrfpy.ColorLayer(z_index=5, name="lights")
grid.add_layer(light_layer)

def add_light(x, y, color, radius):
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            dist = (dx*dx + dy*dy) ** 0.5
            if dist <= radius:
                alpha = int(255 * (1 - dist / radius))
                light_layer.set((x + dx, y + dy),
                    mcrfpy.Color(color.r, color.g, color.b, alpha))
```

### Heightmap Visualization

```python
color_layer = mcrfpy.ColorLayer(z_index=0, name="terrain")
grid.add_layer(color_layer)

# Color by height threshold (one call per range)
color_layer.apply_threshold(heightmap, range=(0.0, 0.5), color=mcrfpy.Color(0, 0, 100))   # Water (blue)
color_layer.apply_threshold(heightmap, range=(0.5, 1.0), color=mcrfpy.Color(0, 100, 0))   # Land (green)

# Or use a smooth gradient across the whole range
color_layer.apply_gradient(
    heightmap,
    range=(0.0, 1.0),
    color_low=mcrfpy.Color(0, 0, 150),     # Low = deep water
    color_high=mcrfpy.Color(200, 200, 200) # High = mountain
)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="TileLayer" class="object-link">TileLayer</a>
<a href="Color" class="object-link">Color</a>
<a href="FOV" class="object-link">FOV</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
