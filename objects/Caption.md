---
layout: default
title: Caption
---

# Caption

Text display UI element with customizable font and styling.

## Overview

A `Caption` renders text at a position with configurable font, size, and colors. Use captions for labels, titles, scores, dialog text, and any other text display. The width and height are automatically computed based on the text content and font size.

## Quick Reference

```python
# Create a caption
title = mcrfpy.Caption(text="Hello, World!", pos=(100, 50))

# Style it
title.font = mcrfpy.Font("assets/DejaVuSans.ttf")
title.font_size = 24
title.fill_color = mcrfpy.Color(255, 255, 255)
title.outline_color = mcrfpy.Color(0, 0, 0)
title.outline = 1

# Add to scene
scene.children.append(title)

# Update text dynamically
title.text = f"Score: {score}"

# Animate properties
title.animate("opacity", 0.0, 2.0, "easeOut")  # Fade out
```

## Constructor

```python
mcrfpy.Caption(pos=None, font=None, text='', **kwargs)
```

**Arguments:**
- `pos` (tuple, optional): Position as (x, y). Default: (0, 0)
- `font` (Font, optional): Font object for text rendering. Default: engine default
- `text` (str, optional): Text content to display. Default: ''

**Keyword Arguments:**
- `fill_color` (Color): Text fill color. Default: (255, 255, 255, 255)
- `outline_color` (Color): Text outline color. Default: (0, 0, 0, 255)
- `outline` (float): Text outline thickness. Default: 0
- `font_size` (float): Font size in points. Default: 16
- `click` (callable): Click event handler
- `visible` (bool): Visibility state. Default: True
- `opacity` (float): Opacity (0.0-1.0). Default: 1.0
- `z_index` (int): Rendering order. Default: 0
- `name` (str): Element name for finding

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | str | Text content |
| `x`, `y` | float | Position coordinates |
| `pos` | Vector | Position as a Vector |
| `font` | Font | Font used for rendering |
| `font_size` | int | Font size in points |
| `fill_color` | Color | Text fill color |
| `outline_color` | Color | Text outline color |
| `outline` | float | Outline thickness |
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
<a href="Font" class="object-link">Font</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/scene" class="object-link">Scene System</a>
</div>
</div>
