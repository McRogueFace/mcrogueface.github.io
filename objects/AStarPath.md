---
layout: default
title: AStarPath
mcrf:
  objects: [AStarPath]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# AStarPath

Computed A* path result, consumed step by step.

## Overview

An `AStarPath` represents a computed shortest path between two points on a Grid. It is created by `Grid.find_path()` and cannot be instantiated directly. The path is consumed incrementally using `walk()` or inspected using `peek()`.

## Quick Reference

```python
# Create path from grid
path = grid.find_path(player.cell_pos, (target_x, target_y))

if path:
    # Check path length
    print(f"Path has {path.remaining} steps")

    # Peek at next step without consuming
    next_pos = path.peek()

    # Walk the path step by step
    while path:
        next_step = path.walk()
        x, y = next_step
        player.cell_pos = (x, y)
```

## Constructor

`AStarPath` cannot be instantiated directly. Use `Grid.find_path()` to create paths.

```python
# Correct way to create a path
path = grid.find_path(start_pos, end_pos)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `origin` | Vector | Starting position (x, y), read-only |
| `destination` | Vector | Target position (x, y), read-only |
| `remaining` | int | Number of steps remaining, read-only |

## Methods

| Method | Description |
|--------|-------------|
| `walk()` | Return and consume the next step as a Vector; raises `IndexError` if exhausted |
| `peek()` | Return the next step as a Vector without consuming it; raises `IndexError` if exhausted |

`AStarPath` also supports `len()` and `bool()` — both reflect `remaining`, so `while path:` is a
convenient way to drain it.

## Usage Patterns

### Basic Movement

```python
path = grid.find_path(entity.cell_pos, goal)
if path:
    next_step = path.walk()
    entity.cell_pos = next_step
```

`cell_pos` is the entity's logical grid cell (a Vector); it is distinct from `pos`/`x`/`y`,
which are the entity's *pixel* position on screen.

### Animated Movement

```python
path = grid.find_path(player.cell_pos, target)

def move_step(timer, runtime_ms):
    if path:
        x, y = path.walk()
        player.animate("draw_x", x, 0.15)
        player.animate("draw_y", y, 0.15)
    else:
        timer.stop()

mcrfpy.Timer("move", move_step, 200)  # Move every 200ms
```

`draw_x`/`draw_y` animate the entity's fractional `draw_pos` (smooth tile-to-tile motion),
separate from the logical `cell_pos` used for collision and pathfinding.

### Path Validation

```python
path = grid.find_path(start, end)

if path is None:
    print("No path exists!")
elif len(path) == 0:
    print("Already at destination")
else:
    print(f"Path found: {path.remaining} steps from {path.origin} to {path.destination}")
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="Entity" class="object-link">Entity</a>
<a href="DijkstraMap" class="object-link">DijkstraMap</a>
<a href="GridPoint" class="object-link">GridPoint</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
