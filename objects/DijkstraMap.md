---
layout: default
title: DijkstraMap
---

# DijkstraMap

Dijkstra distance map from a fixed root position.

## Overview

A `DijkstraMap` represents precomputed distances from a root position to all reachable cells in a Grid. It is created by `Grid.get_dijkstra_map()` and cannot be instantiated directly. Dijkstra maps are useful for AI pathfinding, influence maps, and flow-field navigation where multiple entities need to path toward the same goal.

## Quick Reference

```python
# Create Dijkstra map from goal position
dijkstra = grid.get_dijkstra_map((goal_x, goal_y))

# Get distance from any cell to the goal
dist = dijkstra.distance((enemy.x, enemy.y))

# Get full path from position to root
path = dijkstra.path_from((start_x, start_y))

# Get single step toward goal (for AI)
next_pos = dijkstra.step_from((enemy.x, enemy.y))
if next_pos:
    enemy.x, enemy.y = next_pos

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
| `root` | tuple | Goal position (x, y), read-only |

## Methods

| Method | Description |
|--------|-------------|
| `distance(pos)` | Get distance from pos to root, or -1 if unreachable |
| `path_from(pos)` | Get complete path from pos to root as list of tuples |
| `step_from(pos)` | Get next step toward root, or None if at root/unreachable |
| `to_heightmap()` | Convert distances to HeightMap for visualization |

## Usage Patterns

### AI Movement Toward Goal

```python
# Create map toward player
player_dijkstra = grid.get_dijkstra_map((player.x, player.y))

# Move all enemies toward player
for enemy in grid.entities:
    if enemy != player:
        next_step = player_dijkstra.step_from((enemy.x, enemy.y))
        if next_step:
            enemy.x, enemy.y = next_step
```

### Flee Behavior

```python
# To flee, move to neighbor with highest distance
danger_map = grid.get_dijkstra_map((threat.x, threat.y))

def flee_step(entity):
    best_pos = None
    best_dist = danger_map.distance((entity.x, entity.y))

    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = entity.x + dx, entity.y + dy
        if grid.at(nx, ny).walkable:
            dist = danger_map.distance((nx, ny))
            if dist > best_dist:
                best_dist = dist
                best_pos = (nx, ny)

    if best_pos:
        entity.x, entity.y = best_pos
```

### Distance-Based Decisions

```python
goal_map = grid.get_dijkstra_map((treasure.x, treasure.y))

for entity in grid.entities:
    dist = goal_map.distance((entity.x, entity.y))
    if dist < 0:
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

# Apply to color layer for visualization
color_layer = grid.add_layer('color', z_index=1)
color_layer.apply_gradient(
    heightmap,
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
