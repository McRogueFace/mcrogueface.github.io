---
layout: default
title: Sprite
---

# Sprite

Displays a texture or portion of a texture atlas.

## Overview

A `Sprite` displays a single image from a texture or sprite sheet. Use sprites for UI icons, decorations, character portraits, and standalone images. Sprites support independent horizontal and vertical scaling and can be animated through their sprite_index property.

## Quick Reference

```python
# Load a texture atlas
texture = mcrfpy.Texture("assets/sprites.png", 16, 16)

# Create a sprite from the texture
sprite = mcrfpy.Sprite(pos=(100, 100), texture=texture, sprite_index=42)

# Scale it
sprite.scale = 2.0  # Uniform scaling

# Or scale independently
sprite.scale_x = 2.0
sprite.scale_y = 1.5

# Add to scene
scene.children.append(sprite)

# Animate through sprite frames
sprite.animate("sprite_index", 45, 0.5)  # Animate to frame 45
```

## Constructor

```python
mcrfpy.Sprite(pos=None, texture=None, sprite_index=0, **kwargs)
```

**Arguments:**
- `pos` (tuple, optional): Position as (x, y). Default: (0, 0)
- `texture` (Texture, optional): Texture object to display. Default: default texture
- `sprite_index` (int, optional): Index into texture atlas. Default: 0

**Keyword Arguments:**
- `scale` (float): Uniform scale factor. Default: 1.0
- `scale_x` (float): Horizontal scale factor. Default: 1.0
- `scale_y` (float): Vertical scale factor. Default: 1.0
- `click` (callable): Click event handler
- `visible` (bool): Visibility state. Default: True
- `opacity` (float): Opacity (0.0-1.0). Default: 1.0
- `z_index` (int): Rendering order. Default: 0
- `name` (str): Element name for finding

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Position coordinates |
| `pos` | Vector | Position as a Vector |
| `texture` | Texture | Source texture/sprite sheet |
| `sprite_index` | int | Index into texture atlas |
| `scale` | float | Uniform scale factor |
| `scale_x` | float | Horizontal scale factor |
| `scale_y` | float | Vertical scale factor |
| `w` | float | Computed width (read-only) |
| `h` | float | Computed height (read-only) |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |
| `z_index` | int | Rendering order (lower = first) |
| `name` | str | Element name for finding |
| `parent` | Drawable | Parent element or None |
| `hovered` | bool | Mouse hover state (read-only) |
| `on_click` | callable | Click event handler |
| `on_enter` | callable | Mouse enter handler |
| `on_exit` | callable | Mouse exit handler |
| `on_move` | callable | Mouse move handler |

## Methods

| Method | Description |
|--------|-------------|
| `animate(property, target, duration, ...)` | Animate a property over time |
| `move(dx, dy)` | Move by relative offset |
| `resize(width, height)` | Resize to new dimensions |
| `realign()` | Reapply alignment relative to parent |
| `get_bounds()` | Get bounding rectangle (x, y, w, h) |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Texture" class="object-link">Texture</a>
<a href="Entity" class="object-link">Entity</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Scene" class="object-link">Scene</a>
</div>
</div>
