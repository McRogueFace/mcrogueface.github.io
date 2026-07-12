---
title: DijkstraMap
layout: default
mcrf:
  objects:
    - DijkstraMap
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# DijkstraMap

{% raw %}A Dijkstra distance map from a fixed root position.

Created by Grid.get_dijkstra_map(). Cannot be instantiated directly.

Grid caches these maps - multiple requests for the same root return
the same map. Call Grid.clear_dijkstra_maps() after changing grid
walkability to invalidate the cache.

Properties:
    root (Vector): Root position (read-only)

Methods:
    distance(pos) -> float | None: Get distance to root
    path_from(pos) -> AStarPath: Get full path to root
    step_from(pos) -> Vector | None: Get single step toward root

Example:
    dijkstra = grid.get_dijkstra_map(player.pos)
    for enemy in enemies:
        dist = dijkstra.distance(enemy.pos)
        if dist and dist < 10:
            step = dijkstra.step_from(enemy.pos)
            if step:
                enemy.pos = step{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `root` | {% raw %}Root position that distances are measured from (Vector, read-only).{% endraw %} |

## Methods

### `descent_step(pos: Vector | tuple) -> Vector | None`

{% raw %}descent_step(pos: Vector | tuple) -> Vector | None

Get the adjacent cell with the lowest distance (steepest descent). Unlike step_from, this always returns the best neighbor in a single hop without following a precomputed path.

Args:
    pos: Current position as Vector, Entity, or (x, y) tuple

Returns:
    Next position as Vector, or None if pos is a local minimum or off-grid
{% endraw %}

### `distance(pos: Vector | tuple) -> float | None`

{% raw %}distance(pos: Vector | tuple) -> float | None

Get distance from position to root.

Args:
    pos: Position as Vector, Entity, or (x, y) tuple

Returns:
    Float distance, or None if position is unreachable
{% endraw %}

### `invert() -> DijkstraMap`

{% raw %}invert() -> DijkstraMap

Return a new DijkstraMap whose distance field is inverted (safety field). Cells near a root become high values; descend to flee from original roots. The original DijkstraMap is unchanged.


Returns:
    New DijkstraMap with inverted distances
{% endraw %}

### `path_from(pos: Vector | tuple) -> AStarPath`

{% raw %}path_from(pos: Vector | tuple) -> AStarPath

Get full path from position to root.

Args:
    pos: Starting position as Vector, Entity, or (x, y) tuple

Returns:
    AStarPath from pos toward root
{% endraw %}

### `step_from(pos: Vector | tuple) -> Vector | None`

{% raw %}step_from(pos: Vector | tuple) -> Vector | None

Get single step from position toward root.

Args:
    pos: Current position as Vector, Entity, or (x, y) tuple

Returns:
    Next position as Vector, or None if at root or unreachable
{% endraw %}

### `to_heightmap(size=None, unreachable=-1.0) -> HeightMap`

{% raw %}to_heightmap(size=None, unreachable=-1.0) -> HeightMap

Convert distance field to a HeightMap. Each cell's height equals its pathfinding distance from the root, useful for visualization, procedural terrain, or influence mapping.

Args:
    size: Optional (width, height) tuple. Defaults to dijkstra dimensions
    unreachable: Value for cells that cannot reach root (default -1.0)

Returns:
    HeightMap with distance values as heights
{% endraw %}
