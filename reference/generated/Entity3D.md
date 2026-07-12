---
title: Entity3D
layout: default
mcrf:
  objects:
    - Entity3D
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Entity3D

{% raw %}Entity3D(pos=None, **kwargs)

A 3D game entity that exists on a Viewport3D's navigation grid.

Args:
    pos (tuple, optional): Grid position as (x, z). Default: (0, 0)

Keyword Args:
    viewport (Viewport3D): Viewport to attach entity to. Default: None
    rotation (float): Y-axis rotation in degrees. Default: 0
    scale (float or tuple): Scale factor. Default: 1.0
    visible (bool): Visibility state. Default: True
    color (Color): Entity color. Default: orange

Attributes:
    pos (tuple): Grid position (x, z) - setting triggers movement
    grid_pos (tuple): Same as pos (read-only)
    world_pos (tuple): Current world coordinates (x, y, z) (read-only)
    rotation (float): Y-axis rotation in degrees
    scale (float): Uniform scale factor
    visible (bool): Visibility state
    color (Color): Entity render color
    viewport (Viewport3D): Owning viewport (read-only){% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `anim_clip` | {% raw %}Current animation clip name. Set to play an animation.{% endraw %} |
| `anim_frame` | {% raw %}Current animation frame number (read-only, approximate at 30fps).{% endraw %} |
| `anim_loop` | {% raw %}Whether animation loops when it reaches the end.{% endraw %} |
| `anim_paused` | {% raw %}Whether animation playback is paused.{% endraw %} |
| `anim_speed` | {% raw %}Animation playback speed multiplier. 1.0 = normal speed.{% endraw %} |
| `anim_time` | {% raw %}Current time position in animation (seconds).{% endraw %} |
| `auto_animate` | {% raw %}Enable auto-play of walk/idle clips based on movement.{% endraw %} |
| `color` | {% raw %}Entity render color.{% endraw %} |
| `grid_pos` | {% raw %}Grid position (x, z). Same as pos.{% endraw %} |
| `idle_clip` | {% raw %}Animation clip to play when entity is stationary.{% endraw %} |
| `is_moving` | {% raw %}Whether entity is currently moving (read-only).{% endraw %} |
| `model` | {% raw %}3D model (Model3D). If None, uses placeholder cube.{% endraw %} |
| `name` | {% raw %}Entity name (str). Used for find() lookup.{% endraw %} |
| `on_anim_complete` | {% raw %}Callback(entity, clip_name) when non-looping animation ends.{% endraw %} |
| `pos` | {% raw %}Grid position (x, z). Setting triggers smooth movement.{% endraw %} |
| `rotation` | {% raw %}Y-axis rotation in degrees.{% endraw %} |
| `scale` | {% raw %}Uniform scale factor. Can also set as (x, y, z) tuple.{% endraw %} |
| `viewport` | {% raw %}Owning Viewport3D (read-only).{% endraw %} |
| `visible` | {% raw %}Visibility state.{% endraw %} |
| `walk_clip` | {% raw %}Animation clip to play when entity is moving.{% endraw %} |
| `world_pos` | {% raw %}Current world position (x, y, z) (read-only). Includes animation interpolation.{% endraw %} |

## Methods

### `animate(property, target, duration, easing=None, delta=False, callback=None, conflict_mode=None)`

{% raw %}animate(property, target, duration, easing=None, delta=False, callback=None, conflict_mode=None)

Animate a property over time.

Args:
    property: Property name (x, y, z, rotation, scale, etc.)
    target: Target value (float or int)
    duration: Animation duration in seconds
    easing: Easing function (Easing enum or None for linear)
    delta: If True, target is relative to current value
    callback: Called with (target, property, value) when complete
    conflict_mode: 'replace', 'queue', or 'error'{% endraw %}

### `at(x, z) -> dict`

{% raw %}at(x, z) -> dict

Get visibility state for a cell from this entity's perspective.
Returns dict with 'visible' and 'discovered' boolean keys.{% endraw %}

### `clear_path()`

{% raw %}clear_path()

Clear the movement queue and stop at current position.{% endraw %}

### `follow_path(path)`

{% raw %}follow_path(path)

Queue path positions for smooth movement.

Args:
    path: List of (x, z) tuples (as returned by path_to()){% endraw %}

### `path_to(x, z) or path_to(pos=(x, z)) -> list`

{% raw %}path_to(x, z) or path_to(pos=(x, z)) -> list

Compute A* path to target position.
Returns list of (x, z) tuples, or empty list if no path exists.{% endraw %}

### `teleport(x, z) or teleport(pos=(x, z))`

{% raw %}teleport(x, z) or teleport(pos=(x, z))

Instantly move to target position without animation.{% endraw %}

### `update_visibility()`

{% raw %}update_visibility()

Recompute field of view from current position.{% endraw %}
