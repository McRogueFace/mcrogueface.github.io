---
title: Mouse
layout: default
mcrf:
  objects:
    - Mouse
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Mouse

{% raw %}Mouse state singleton for reading button/position state and controlling cursor visibility{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `grabbed` | {% raw %}Whether the mouse cursor is confined to the window (default: False).{% endraw %} |
| `left` | {% raw %}True if left mouse button is currently pressed (read-only).{% endraw %} |
| `middle` | {% raw %}True if middle mouse button is currently pressed (read-only).{% endraw %} |
| `pos` | {% raw %}Current mouse position as Vector (read-only).{% endraw %} |
| `right` | {% raw %}True if right mouse button is currently pressed (read-only).{% endraw %} |
| `visible` | {% raw %}Whether the mouse cursor is visible (default: True).{% endraw %} |
| `x` | {% raw %}Current mouse X position in window coordinates (read-only).{% endraw %} |
| `y` | {% raw %}Current mouse Y position in window coordinates (read-only).{% endraw %} |
