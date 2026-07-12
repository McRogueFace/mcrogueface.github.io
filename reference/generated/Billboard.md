---
title: Billboard
layout: default
mcrf:
  objects:
    - Billboard
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Billboard

{% raw %}Billboard(texture=None, sprite_index=0, pos=(0,0,0), scale=1.0, facing='camera_y')

A camera-facing 3D sprite for trees, items, particles, etc.

Args:
    texture (Texture, optional): Sprite sheet texture. Default: None
    sprite_index (int): Index into sprite sheet. Default: 0
    pos (tuple): World position (x, y, z). Default: (0, 0, 0)
    scale (float): Uniform scale factor. Default: 1.0
    facing (str): Facing mode - 'camera', 'camera_y', or 'fixed'. Default: 'camera_y'

Properties:
    texture (Texture): Sprite sheet texture
    sprite_index (int): Index into sprite sheet
    pos (tuple): World position (x, y, z)
    scale (float): Uniform scale factor
    facing (str): Facing mode - 'camera', 'camera_y', or 'fixed'
    theta (float): Horizontal rotation for 'fixed' mode (radians)
    phi (float): Vertical tilt for 'fixed' mode (radians)
    opacity (float): Opacity 0.0 (transparent) to 1.0 (opaque)
    visible (bool): Visibility state{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `facing` | {% raw %}Facing mode: 'camera', 'camera_y', or 'fixed' (str){% endraw %} |
| `opacity` | {% raw %}Opacity from 0.0 (transparent) to 1.0 (opaque) (float){% endraw %} |
| `phi` | {% raw %}Vertical tilt for 'fixed' mode in radians (float){% endraw %} |
| `pos` | {% raw %}World position as (x, y, z) tuple{% endraw %} |
| `scale` | {% raw %}Uniform scale factor (float){% endraw %} |
| `sprite_index` | {% raw %}Index into sprite sheet (int){% endraw %} |
| `texture` | {% raw %}Sprite sheet texture (Texture or None){% endraw %} |
| `theta` | {% raw %}Horizontal rotation for 'fixed' mode in radians (float){% endraw %} |
| `visible` | {% raw %}Visibility state (bool){% endraw %} |
