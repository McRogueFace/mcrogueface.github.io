---
layout: default
title: Entity
---

# Entity

Game entity that exists on a grid with sprite rendering.

## Overview

An `Entity` is a game object that exists at a position on a Grid. Entities represent players, enemies, items, and other interactive objects. They render on top of tiles, support smooth animated movement, and integrate with the pathfinding and field-of-view systems.

## Quick Reference

```python
# Create an entity
player = mcrfpy.Entity(grid_pos=(10, 10), texture=texture, sprite_index=84)

# Add to a grid
grid.entities.append(player)

# Move to a new grid position
player.pos = (11, 10)  # Instant move
player.grid_pos = (11, 10)  # Same as above

# Animated movement
player.animate("x", 12.0, 0.2, "easeOutQuad")

# Pathfinding
if player.path_to(15, 10):
    print("Moving to target!")

# Field of view
visible = player.visible_entities(radius=8)
for enemy in visible:
    print(f"Can see: {enemy.name}")
```

## Constructor

```python
mcrfpy.Entity(grid_pos=None, texture=None, sprite_index=0, **kwargs)
```

**Arguments:**
- `grid_pos` (tuple, optional): Grid position as (x, y). Default: (0, 0)
- `texture` (Texture, optional): Texture object for sprite. Default: default texture
- `sprite_index` (int, optional): Index into texture atlas. Default: 0

**Keyword Arguments:**
- `grid` (Grid): Grid to attach entity to
- `visible` (bool): Visibility state. Default: True
- `opacity` (float): Opacity (0.0-1.0). Default: 1.0
- `name` (str): Element name for finding

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `pos` | tuple | Grid position as (x, y) integers |
| `x`, `y` | float | Grid position coordinates |
| `grid_pos` | tuple | Alias for pos |
| `grid_x`, `grid_y` | float | Alias for x, y |
| `draw_pos` | tuple | Pixel position for rendering (fractional tiles) |
| `sprite_index` | int | Current sprite index in texture |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |
| `name` | str | Element name for finding |
| `grid` | Grid | Parent grid or None |
| `gridstate` | GridPointState | Entity's visibility state tracking |

## Methods

| Method | Description |
|--------|-------------|
| `animate(property, target, duration, ...)` | Animate a property over time |
| `move(dx, dy)` | Move by relative offset |
| `resize(width, height)` | Resize to new dimensions |
| `get_bounds()` | Get bounding rectangle (x, y, w, h) |
| `at(x, y)` | Get grid point at position |
| `die()` | Remove this entity from its grid |
| `index()` | Return index in grid's entity collection |
| `path_to(x, y)` | Find and follow A* path to target |
| `update_visibility()` | Recompute FOV from current position |
| `visible_entities(fov, radius)` | Get list of entities in field of view |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="Texture" class="object-link">Texture</a>
<a href="EntityCollection" class="object-link">EntityCollection</a>
<a href="../systems/grid" class="object-link">Grid System</a>
<a href="../systems/animation" class="object-link">Animation System</a>
</div>
</div>
