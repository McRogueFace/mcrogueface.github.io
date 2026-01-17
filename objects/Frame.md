---
layout: default
title: Frame
---

# Frame

Rectangular container UI element with background and border.

## Overview

A `Frame` is a rectangular UI element that can contain other drawable elements. Use frames for panels, buttons, dialog boxes, HUDs, and other UI containers. Frames support clipping children to their bounds and caching their subtree for performance optimization.

## Quick Reference

```python
# Create a styled panel
panel = mcrfpy.Frame(pos=(100, 100), size=(200, 150))
panel.fill_color = mcrfpy.Color(40, 40, 40, 200)
panel.outline_color = mcrfpy.Color(100, 100, 100)
panel.outline = 2

# Add to scene
scene.children.append(panel)

# Frames can contain children
label = mcrfpy.Caption(text="Panel Title", pos=(10, 10))
panel.children.append(label)

# Enable clipping for scrollable content
panel.clip_children = True

# Animate properties
panel.animate("opacity", 0.5, 1.0, "easeInOut")
```

## Constructor

```python
mcrfpy.Frame(pos=None, size=None, **kwargs)
```

**Arguments:**
- `pos` (tuple, optional): Position as (x, y). Default: (0, 0)
- `size` (tuple, optional): Size as (width, height). Default: (0, 0)

**Keyword Arguments:**
- `fill_color` (Color): Background fill color. Default: (0, 0, 0, 128)
- `outline_color` (Color): Border outline color. Default: (255, 255, 255, 255)
- `outline` (float): Border thickness. Default: 0
- `click` (callable): Click event handler
- `children` (list): Initial child elements
- `visible` (bool): Visibility state. Default: True
- `opacity` (float): Opacity (0.0-1.0). Default: 1.0
- `z_index` (int): Rendering order. Default: 0
- `name` (str): Element name for finding
- `clip_children` (bool): Clip children to frame bounds. Default: False
- `cache_subtree` (bool): Cache rendering to texture. Default: False

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Position coordinates |
| `w`, `h` | float | Size dimensions |
| `pos` | Vector | Position as a Vector |
| `size` | tuple | Size as (w, h) |
| `fill_color` | Color | Background color |
| `outline_color` | Color | Border color |
| `outline` | float | Border thickness |
| `children` | UICollection | Child elements |
| `clip_children` | bool | Whether to clip children to bounds |
| `cache_subtree` | bool | Cache rendering to texture |
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
<a href="Scene" class="object-link">Scene</a>
<a href="Caption" class="object-link">Caption</a>
<a href="Sprite" class="object-link">Sprite</a>
<a href="UICollection" class="object-link">UICollection</a>
<a href="../systems/scene" class="object-link">Scene System</a>
</div>
</div>
