---
title: Drawable
layout: default
mcrf:
  objects:
    - Drawable
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Drawable

{% raw %}Base class for all drawable UI elements{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `on_click` | {% raw %}Callable executed when object is clicked. Function receives (pos: Vector, button: MouseButton, action: InputState).{% endraw %} |
| `opacity` | {% raw %}Opacity level (0.0 = transparent, 1.0 = opaque). Automatically clamped to valid range [0.0, 1.0].{% endraw %} |
| `visible` | {% raw %}Whether the object is visible (bool). Invisible objects are not rendered or clickable.{% endraw %} |
| `z_index` | {% raw %}Z-order for rendering (lower values rendered first). Automatically triggers scene resort when changed.{% endraw %} |

## Methods

### `move(dx, dy) or (delta) -> None`

{% raw %}move(dx, dy) or (delta) -> None

Move the element by a relative offset.

Args:
    dx: Horizontal offset in pixels (or use delta)
    dy: Vertical offset in pixels (or use delta)
    delta: Offset as tuple, list, or Vector: (dx, dy)

Note:
    This modifies the x and y position properties by the given amounts. Accepts move(dx, dy), move((dx, dy)), move(Vector), or move(pos=(dx, dy)).
{% endraw %}

### `resize(width, height) or (size) -> None`

{% raw %}resize(width, height) or (size) -> None

Resize the element to new dimensions.

Args:
    width: New width in pixels (or use size)
    height: New height in pixels (or use size)
    size: Size as tuple, list, or Vector: (width, height)

Note:
    For Caption and Sprite, this may not change actual size if determined by content. Accepts resize(w, h), resize((w, h)), resize(Vector), or resize(pos=(w, h)).
{% endraw %}
