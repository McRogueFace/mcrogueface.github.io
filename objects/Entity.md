---
layout: default
title: Entity
mcrf:
  objects: [Entity, Behavior, Trigger]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Entity

Game entity that exists on a grid with sprite rendering.

## Overview

An `Entity` is a game object that exists at a position on a Grid. Entities represent players, enemies, items, and other interactive objects. They render on top of tiles, support smooth animated movement, and integrate with the pathfinding and field-of-view systems.

## Quick Reference

```python
import mcrfpy

scene = mcrfpy.Scene("entity-demo")
mcrfpy.current_scene = scene

grid = mcrfpy.Grid(
    grid_size=(16, 12),
    texture=mcrfpy.default_texture,
    pos=(0, 0),
    size=(1024, 768),
    zoom=4.0
)
scene.children.append(grid)

for y in range(12):
    for x in range(16):
        grid.at(x, y).tilesprite = 48

# Create an entity
player = mcrfpy.Entity(grid_pos=(10, 10), texture=mcrfpy.default_texture, sprite_index=84)

# Add to a grid
grid.entities.append(player)

# Move to a new grid (tile) position -- instant, integer coordinates
player.grid_pos = (11, 10)

# Animated movement: 'x' is an alias for 'draw_x', the fractional tile
# coordinate used for smooth motion between cells.
player.animate("x", 12.0, 0.2, mcrfpy.Easing.EASE_OUT_QUAD)

# Pathfinding: find_path() returns an AStarPath (or None if unreachable);
# it does not move the entity itself.
path = player.find_path((15, 10))
if path is not None:
    print("Path found!")

# Field of view
visible = player.visible_entities(radius=8)
for enemy in visible:
    print(f"Can see: {enemy.name}")
```

Note: `pos` and `grid_pos` are **not** the same kind of value. `grid_pos` (and
its aliases `cell_pos`, `x`/`y` in grid-cell terms via `grid_x`/`grid_y`) is
the integer logical tile coordinate. `pos` is the entity's **pixel** position
relative to the grid (`draw_pos * tile_size`), and requires the entity to be
attached to a grid. Setting `grid_pos` teleports the entity instantly, and
`draw_pos` catches up immediately unless you are mid-animation.

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
| `pos` | Vector | Pixel position relative to the grid (`draw_pos * tile_size`); requires a grid |
| `x`, `y` | float | Pixel position components (same space as `pos`) |
| `grid_pos` | Vector | Integer logical tile coordinate (the canonical game position) |
| `cell_pos` | Vector | Alias for `grid_pos` |
| `grid_x`, `grid_y` | int | Integer tile coordinate components |
| `cell_x`, `cell_y` | int | Aliases for `grid_x`, `grid_y` |
| `draw_pos` | Vector | Fractional tile position used for smooth animation between cells |
| `sprite_index` | int | Current sprite index in texture |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |
| `name` | str | Element name for finding |
| `grid` | Grid | Parent grid or None |
| `labels` | frozenset[str] | String labels used for collision/targeting; assign any iterable of strings to replace them all |
| `turn_order` | int | Turn order for `grid.step()`; 0 = skip, higher = later |
| `move_speed` | float | Animation duration (seconds) used by behaviors when moving; 0 = instant |
| `sight_radius` | int | FOV radius used by the TARGET trigger. Default 10 |
| `perspective_map` | DiscreteMap | Per-entity FOV memory: 3-state values per cell (0=unknown, 1=discovered, 2=visible). Lazy-allocated on first access once the entity has a grid. |

## Methods

| Method | Description |
|--------|-------------|
| `animate(property, target, duration, ...)` | Animate a property over time. Valid properties: `draw_x`/`draw_y` (aliased as `x`/`y`), `sprite_scale`, `sprite_index`, `sprite_offset_x`, `sprite_offset_y` |
| `move(dx, dy)` | Move by a relative pixel offset |
| `at(x, y)` | Return the `GridPoint` at (x, y) if currently visible to this entity's `perspective_map`, otherwise `None` |
| `die()` | Remove this entity from its grid |
| `index()` | Return this entity's index in its grid's entity collection |
| `find_path(target, diagonal_cost=1.41, collide=None)` | Compute an A* path to `target` (Vector/Entity/tuple); returns an `AStarPath`, or `None` if no path exists. Does not move the entity |
| `path_to(x, y)` | Compute an A* path to (x, y); returns a list of (x, y) tuples. Does not move the entity |
| `set_behavior(type, waypoints=None, turns=0, path=None, pathfinder=None)` | Configure autonomous behavior for `grid.step()` turn management (see `Behavior` enum) |
| `add_label(label)` / `remove_label(label)` / `has_label(label)` | Manage this entity's `labels` set |
| `update_visibility()` | Recompute FOV from the current position and refresh `perspective_map`. Called automatically when the entity moves if the grid has FOV configured |
| `visible_entities(fov=None, radius=None)` | Get a list of other entities visible from this entity's position |

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
