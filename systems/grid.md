---
layout: default
title: Grid System
---

# Grid System

The Grid System is McRogueFace's tile-based world representation. It provides efficient rendering of large tile maps, manages entities, and integrates with libtcod for field-of-view and pathfinding calculations.

## Overview

```
Grid
  ├── points (GridPointArray)
  │     └── GridPoint (per tile)
  │           └── GridPointState (appearance)
  └── entities (EntityCollection)
        └── Entity (game objects)
```

A [Grid](../objects/Grid) represents a 2D tile-based world. Each tile is a [GridPoint](../objects/GridPoint) with walkability, transparency, and visual state. [Entities](../objects/Entity) are game objects that exist at positions on the grid.

## Objects

| Object | Purpose |
|--------|---------|
| [Grid](../objects/Grid) | Tile-based world container |
| [GridPoint](../objects/GridPoint) | Individual tile properties |
| [GridPointState](../objects/GridPointState) | Tile visual appearance |
| [Entity](../objects/Entity) | Game objects on the grid |

---

## Layer Subsystem {#layers}

Grids support multiple visual layers for rich tile rendering.

### Tile Layers

Each GridPoint has a base tile and can have overlay tiles:

```python
cell = grid.at(5, 5)
cell.tilesprite = 0      # Base floor tile
cell.tile_overlay = 12   # Overlay decoration
```

### Color Layers

GridPointState includes color information:

```python
state = cell.get_state()
state.foreground = mcrfpy.Color(255, 255, 255)
state.background = mcrfpy.Color(50, 50, 50)
```

### Entity Layer

Entities render on top of tiles:

```python
player = mcrfpy.Entity(pos=(10, 10), texture=texture, sprite_index=84)
grid.entities.append(player)
```

---

## FOV Subsystem {#fov}

Field-of-view calculations determine what the player can see, powered by libtcod algorithms.

### Grid Transparency

Tiles have a `transparent` property that affects FOV:

```python
# Walls block sight
wall = grid.at(5, 5)
wall.transparent = False

# Floors allow sight
floor = grid.at(6, 5)
floor.transparent = True
```

### Computing FOV

Compute FOV from a position with a radius:

```python
grid.compute_fov(player.x, player.y, radius=8)
```

### Visibility States

After computing FOV, tiles have visibility states:
- **Visible**: Currently in view
- **Explored**: Previously seen but not currently visible
- **Unexplored**: Never seen

```python
cell = grid.at(x, y)
if cell.visible:
    # Currently in player's sight
elif cell.explored:
    # Previously seen (show dimmed)
else:
    # Never seen (show black)
```

### Perspective Binding

Bind an entity as the FOV perspective:

```python
grid.perspective = player
# FOV automatically updates when player moves
```

---

## Pathfinding Subsystem {#pathfinding}

The Grid System includes A* and Dijkstra pathfinding, powered by libtcod.

### Walkability

Tiles have a `walkable` property for pathfinding:

```python
# Walls block movement
wall = grid.at(5, 5)
wall.walkable = False

# Floors allow movement
floor = grid.at(6, 5)
floor.walkable = True
```

### A* Pathfinding

Find the shortest path between two points:

```python
path = grid.compute_astar_path(
    start_x, start_y,
    end_x, end_y
)

for x, y in path:
    # Move along path
    entity.x, entity.y = x, y
```

### Dijkstra Maps

Compute distance from a point to all reachable tiles:

```python
grid.compute_dijkstra(goal_x, goal_y)

# Get distance to any tile
distance = grid.get_dijkstra_distance(x, y)

# Get direction toward goal
dx, dy = grid.get_dijkstra_step(x, y)
```

### Entity Collision

Check if tiles are occupied:

```python
# Find entities at a position
entities_at_pos = [e for e in grid.entities if e.x == x and e.y == y]
```

---

## Related Objects

<div class="related-objects">
<div class="object-links">
<a href="../objects/Grid" class="object-link">Grid</a>
<a href="../objects/GridPoint" class="object-link">GridPoint</a>
<a href="../objects/GridPointState" class="object-link">GridPointState</a>
<a href="../objects/Entity" class="object-link">Entity</a>
</div>
</div>
