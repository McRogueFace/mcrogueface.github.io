---
layout: default
title: ColorLayer
---

# ColorLayer

Grid layer storing RGBA colors per cell.

## Overview

A `ColorLayer` stores color data for each cell in a Grid. Use color layers for lighting effects, fog of war visualization, terrain tinting, or any per-cell color overlay. Color layers can be stacked with tile layers using z-index ordering.

## Quick Reference

```python
# Create via Grid.add_layer()
color_layer = grid.add_layer('color', z_index=1)

# Set individual cell colors
color_layer.set((5, 5), mcrfpy.Color(255, 0, 0, 128))  # Semi-transparent red

# Fill entire layer
color_layer.fill(mcrfpy.Color(0, 0, 0, 200))  # Dark overlay

# Fill rectangular region
color_layer.fill_rect((10, 10), (20, 20), mcrfpy.Color(50, 50, 100))

# Get cell color
cell_color = color_layer.at((5, 5))

# FOV visualization
color_layer.draw_fov(grid)  # Darken non-visible cells
```

## Constructor

`ColorLayer` is typically created via `Grid.add_layer()`:

```python
color_layer = grid.add_layer('color', z_index=1, grid_size=(80, 45))
```

Direct instantiation:

```python
mcrfpy.ColorLayer(z_index=-1, grid_size=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `z_index` | int | -1 | Rendering order (higher = on top) |
| `grid_size` | tuple | None | Size (w, h), inherits from Grid if None |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `z_index` | int | Rendering order |
| `visible` | bool | Visibility toggle |
| `grid_size` | tuple | Layer dimensions (w, h), read-only |

## Methods

| Method | Description |
|--------|-------------|
| `at(pos)` | Get Color at cell position |
| `set(pos, color)` | Set Color at cell position |
| `fill(color)` | Fill entire layer with color |
| `fill_rect(pos, size, color)` | Fill rectangular region |
| `draw_fov(grid)` | Apply FOV-based darkening |
| `apply_perspective(entity)` | Apply perspective darkening from entity |
| `update_perspective(entity)` | Update existing perspective effect |
| `clear_perspective()` | Remove perspective effect |
| `apply_threshold(heightmap, threshold, below, above)` | Color by heightmap threshold |
| `apply_gradient(heightmap, color1, color2)` | Gradient based on heightmap |
| `apply_ranges(heightmap, ranges)` | Color by heightmap value ranges |

## Usage Patterns

### Fog of War

```python
# Create darkness layer
fog = grid.add_layer('color', z_index=10)
fog.fill(mcrfpy.Color(0, 0, 0, 255))  # Start fully dark

# Update when FOV changes
def update_fov():
    grid.compute_fov(player.x, player.y, radius=8)
    fog.draw_fov(grid)  # Lightens visible cells
```

### Lighting Effects

```python
light_layer = grid.add_layer('color', z_index=5)

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
color_layer = grid.add_layer('color', z_index=0)

# Color by height threshold
color_layer.apply_threshold(
    heightmap,
    threshold=0.5,
    below=mcrfpy.Color(0, 0, 100),   # Water (blue)
    above=mcrfpy.Color(0, 100, 0)    # Land (green)
)

# Or use gradient
color_layer.apply_gradient(
    heightmap,
    mcrfpy.Color(0, 0, 150),   # Low = deep water
    mcrfpy.Color(200, 200, 200) # High = mountain
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
