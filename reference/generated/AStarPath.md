---
title: AStarPath
layout: default
mcrf:
  objects:
    - AStarPath
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# AStarPath

{% raw %}A computed A* path result, consumed step by step.

Created by Grid.find_path(). Cannot be instantiated directly.

Use walk() to get and consume each step, or iterate directly.
Use peek() to see the next step without consuming it.
Use bool(path) or len(path) to check if steps remain.

Properties:
    origin (Vector): Starting position (read-only)
    destination (Vector): Ending position (read-only)
    remaining (int): Steps remaining (read-only)

Example:
    path = grid.find_path(start, end)
    if path:
        while path:
            next_pos = path.walk()
            entity.pos = next_pos{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `destination` | {% raw %}Ending position of the path (Vector, read-only).{% endraw %} |
| `origin` | {% raw %}Starting position of the path (Vector, read-only).{% endraw %} |
| `remaining` | {% raw %}Number of steps remaining in the path (int, read-only).{% endraw %} |

## Methods

### `peek() -> Vector`

{% raw %}peek() -> Vector

See the next step without consuming it.


Returns:
    Next position as Vector

Raises:
    IndexError: If the path is exhausted
{% endraw %}

### `walk() -> Vector`

{% raw %}walk() -> Vector

Get and consume the next step in the path.


Returns:
    Next position as Vector

Raises:
    IndexError: If the path is exhausted
{% endraw %}
