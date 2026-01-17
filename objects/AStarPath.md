---
layout: default
title: AStarPath
---

# AStarPath

Computed A* path result, consumed step by step.

## Overview

An `AStarPath` represents a computed shortest path between two points on a Grid. It is created by `Grid.find_path()` and cannot be instantiated directly. The path is consumed incrementally using `walk()` or inspected using `peek()`.

## Quick Reference

```python
# Create path from grid
path = grid.find_path((player.x, player.y), (target_x, target_y))

if path:
    # Check path length
    print(f"Path has {path.remaining} steps")

    # Peek at next step without consuming
    next_pos = path.peek()

    # Walk the path step by step
    while path.remaining > 0:
        next_step = path.walk()
        if next_step:
            x, y = next_step
            player.x, player.y = x, y
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
| `origin` | tuple | Starting position (x, y), read-only |
| `destination` | tuple | Target position (x, y), read-only |
| `remaining` | int | Number of steps remaining, read-only |

## Methods

| Method | Description |
|--------|-------------|
| `walk()` | Return and consume the next step, or None if exhausted |
| `peek()` | Return the next step without consuming it |

## Usage Patterns

### Basic Movement

```python
path = grid.find_path(entity.pos, goal)
if path:
    next_step = path.walk()
    if next_step:
        entity.x, entity.y = next_step
```

### Animated Movement

```python
path = grid.find_path(player.pos, target)

def move_step(timer):
    if path.remaining > 0:
        x, y = path.walk()
        player.animate("x", x, duration=0.15)
        player.animate("y", y, duration=0.15)
    else:
        timer.cancel()

mcrfpy.Timer("move", move_step, 200)  # Move every 200ms
```

### Path Validation

```python
path = grid.find_path(start, end)

if path is None:
    print("No path exists!")
elif path.remaining == 0:
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
