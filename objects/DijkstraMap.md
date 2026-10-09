---
layout: default
title: DijkstraMap
mcrf:
  objects: [DijkstraMap, AStarPath, Grid]
  diataxis: reference
  disposition: current
  verified: "0.3.0-dev"
  verified_commit: 73acab0
---

# DijkstraMap

Dijkstra distance map from a fixed root position.

## Overview

A `DijkstraMap` represents precomputed distances from a root position to all reachable cells in a Grid. It is created by `Grid.get_dijkstra_map()` and cannot be instantiated directly. Dijkstra maps are useful for AI pathfinding, influence maps, and flow-field navigation where multiple entities need to path toward the same goal.

## Quick Reference

```python
# Create Dijkstra map from goal position
dijkstra = grid.get_dijkstra_map((goal_x, goal_y))

# Get distance from an entity (or any (x, y) tile position) to the goal
dist = dijkstra.distance(enemy)

# Get full path from position to root (an AStarPath)
path = dijkstra.path_from(enemy)

# Get single step toward goal (for AI)
next_pos = dijkstra.step_from(enemy)
if next_pos:
    enemy.grid_pos = next_pos

# Convert to heightmap for visualization
heightmap = dijkstra.to_heightmap()
```

## Constructor

`DijkstraMap` cannot be instantiated directly. Use `Grid.get_dijkstra_map()` to create maps.

```python
# Correct way to create a Dijkstra map
dijkstra = grid.get_dijkstra_map((goal_x, goal_y))
```

Dijkstra maps are cached by the Grid. Calling `get_dijkstra_map()` with the same root position returns the cached map. Use `grid.clear_dijkstra_maps()` to invalidate the cache when the grid's walkability changes.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `root` | Vector | Goal position, read-only |

## Methods

| Method | Description |
|--------|-------------|
| `distance(pos)` | Get distance from pos (Vector, Entity, or (x, y) tuple) to root, or `None` if unreachable |
| `path_from(pos)` | Get complete path from pos to root as an `AStarPath`, ordered from `pos` toward the root (`origin` is `pos`, `destination` is the root) |
| `step_from(pos)` | Get next step toward root as a Vector (always a cell adjacent to `pos`), or `None` if at root/unreachable |
| `descent_step(pos)` | Get the adjacent cell with the lowest distance (steepest single-hop descent) |
| `invert()` | Return a new `DijkstraMap` with distances inverted (a "flee" field), root unchanged |
| `to_heightmap(size=None, unreachable=-1.0)` | Convert distances to a `HeightMap` for visualization |

## Usage Patterns

### AI Movement Toward Goal

```python
# Create map toward player
player_dijkstra = grid.get_dijkstra_map(player.grid_pos)

# Move all enemies toward player
for enemy in grid.entities:
    if enemy != player:
        next_step = player_dijkstra.step_from(enemy)
        if next_step:
            enemy.grid_pos = next_step
```

### Flee Behavior

```python
# To flee, move to neighbor with highest distance
danger_map = grid.get_dijkstra_map(threat.grid_pos)

def flee_step(entity):
    best_pos = None
    best_dist = danger_map.distance(entity)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = entity.grid_x + dx, entity.grid_y + dy
        if 0 <= nx < grid.grid_size.x and 0 <= ny < grid.grid_size.y and grid.at(nx, ny).walkable:
            dist = danger_map.distance((nx, ny))
            if dist is not None and (best_dist is None or dist > best_dist):
                best_dist = dist
                best_pos = (nx, ny)

    if best_pos:
        entity.grid_pos = best_pos
```

### Distance-Based Decisions

```python
goal_map = grid.get_dijkstra_map(treasure.grid_pos)

for entity in grid.entities:
    dist = goal_map.distance(entity)
    if dist is None:
        print(f"{entity} cannot reach treasure")
    elif dist < 5:
        print(f"{entity} is very close!")
    elif dist < 15:
        print(f"{entity} is {dist} steps away")
```

### Visualization with HeightMap

```python
dijkstra = grid.get_dijkstra_map((goal_x, goal_y))
heightmap = dijkstra.to_heightmap()

# Apply to a color layer for visualization
color_layer = mcrfpy.ColorLayer(z_index=1, name="distance_gradient")
grid.add_layer(color_layer)
color_layer.apply_gradient(
    heightmap,
    (0, 20),                    # value range: 0 (root) to 20 tiles away
    mcrfpy.Color(0, 255, 0),    # Close = green
    mcrfpy.Color(255, 0, 0)     # Far = red
)
```

### Cache Management

```python
# Dijkstra maps are cached automatically
map1 = grid.get_dijkstra_map((10, 10))
map2 = grid.get_dijkstra_map((10, 10))  # Returns cached map

# Clear cache when grid changes
grid.at(5, 5).walkable = False
grid.clear_dijkstra_maps()  # Invalidate all cached maps

# New maps will reflect updated walkability
map3 = grid.get_dijkstra_map((10, 10))  # Recomputed
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="Entity" class="object-link">Entity</a>
<a href="AStarPath" class="object-link">AStarPath</a>
<a href="GridPoint" class="object-link">GridPoint</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
