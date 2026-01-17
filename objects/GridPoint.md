---
layout: default
title: GridPoint
---

# GridPoint

Grid cell data for pathfinding, FOV, and layer access.

## Overview

A `GridPoint` represents a single cell in a Grid, providing access to pathfinding properties (walkable, transparent) and any named layers attached to the grid. GridPoints cannot be instantiated directly - they are returned by `Grid.at()`.

## Quick Reference

```python
# Get a grid point
point = grid.at(5, 10)

# Check/set pathfinding properties
if point.walkable and point.transparent:
    print("Cell is passable and see-through")

point.walkable = False  # Block movement
point.transparent = False  # Block line of sight

# Get position
x, y = point.grid_pos
print(f"Cell at ({x}, {y})")

# Get entities at this cell
for entity in point.entities:
    print(f"Entity: {entity.name}")

# Access named layers (if grid has layers)
# point.<layer_name> returns the layer's value at this cell
```

## Obtaining GridPoints

GridPoints are obtained through `Grid.at()`:

```python
# By coordinates
point = grid.at(x, y)

# By tuple/Vector
point = grid.at((x, y))
point = grid.at(some_vector)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `walkable` | bool | Whether entities can move through this cell |
| `transparent` | bool | Whether light/sight passes through this cell |
| `grid_pos` | tuple | Grid coordinates as (x, y) tuple (read-only) |
| `entities` | list | List of Entity objects at this cell (read-only) |

## Dynamic Layer Access

When a Grid has named layers (ColorLayer or TileLayer), you can access layer values through the GridPoint using the layer's name as an attribute:

```python
# Add named layers to grid
grid.add_layer('color', 'terrain_tint', z_index=-1)
grid.add_layer('tile', 'decorations', z_index=1, texture=deco_tex)

# Access through GridPoint
point = grid.at(5, 5)

# Get/set color layer value
point.terrain_tint = mcrfpy.Color(255, 200, 200)
current_color = point.terrain_tint

# Get/set tile layer value
point.decorations = 42  # tile index
current_tile = point.decorations
```

## Usage Patterns

### Terrain Setup

```python
# Create terrain from heightmap
for y in range(grid.grid_h):
    for x in range(grid.grid_w):
        point = grid.at(x, y)
        height = heightmap.get(x, y)

        if height < 0.3:
            # Water - not walkable, transparent
            point.walkable = False
            point.transparent = True
        elif height > 0.8:
            # Mountain - not walkable, blocks sight
            point.walkable = False
            point.transparent = False
        else:
            # Land - passable
            point.walkable = True
            point.transparent = True
```

### Checking Cell Contents

```python
def can_place_entity(grid, x, y):
    """Check if an entity can be placed at this cell."""
    point = grid.at(x, y)

    # Must be walkable
    if not point.walkable:
        return False

    # Must not have other entities
    if point.entities:
        return False

    return True
```

### Door Implementation

```python
class Door:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x
        self.y = y
        self.is_open = False

    def toggle(self):
        point = self.grid.at(self.x, self.y)
        self.is_open = not self.is_open

        # Open doors are passable and transparent
        point.walkable = self.is_open
        point.transparent = self.is_open
```

## Notes

- GridPoint properties directly affect pathfinding algorithms (`Grid.find_path()`, `Grid.get_dijkstra_map()`)
- The `transparent` property affects FOV calculations (`Grid.compute_fov()`, `Grid.is_in_fov()`)
- Changes to `walkable` require calling `Grid.clear_dijkstra_maps()` to invalidate cached pathfinding data
- Entity collision is separate from `walkable` - entities can occupy the same cell unless your game logic prevents it

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="GridPointState" class="object-link">GridPointState</a>
<a href="Entity" class="object-link">Entity</a>
<a href="ColorLayer" class="object-link">ColorLayer</a>
<a href="TileLayer" class="object-link">TileLayer</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
