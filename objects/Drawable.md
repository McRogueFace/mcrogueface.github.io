---
layout: default
title: Drawable
---

# Drawable

Base class for all drawable UI elements.

## Overview

`Drawable` is the abstract base class for all visual UI elements in McRogueFace. You cannot instantiate Drawable directly; instead, use its subclasses like Frame, Caption, Sprite, and Grid. This class defines common properties and methods shared by all drawable elements.

## Quick Reference

```python
# Drawable is abstract - use subclasses
frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
caption = mcrfpy.Caption(text="Hello", pos=(10, 10))
sprite = mcrfpy.Sprite(texture=tex, pos=(50, 50))

# Common Drawable properties
frame.visible = False
frame.opacity = 0.5
frame.z_index = 10

# Common Drawable methods
frame.move(50, 25)
frame.resize(200, 150)

# Click handling
def on_click(x, y, button):
    print(f"Clicked at ({x}, {y})")

frame.on_click = on_click
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `on_click` | callable | Click event handler function |
| `opacity` | float | Transparency (0.0 = invisible, 1.0 = opaque) |
| `visible` | bool | Whether element is rendered |
| `z_index` | int | Draw order (higher = drawn on top) |

## Methods

| Method | Description |
|--------|-------------|
| `move(dx, dy)` | Move element by relative offset |
| `resize(w, h)` | Set element size |

## Click Handler

The `on_click` callback receives:
- `x` - X coordinate of click (relative to element)
- `y` - Y coordinate of click (relative to element)
- `button` - Mouse button ("left", "right", "middle")

```python
def handle_click(x, y, button):
    if button == "left":
        print("Left clicked!")

element.on_click = handle_click
```

## Subclasses

All drawable UI elements inherit from Drawable:

- **Frame** - Rectangular container with fill and outline
- **Caption** - Text display element
- **Sprite** - Textured image element
- **Grid** - Tile-based grid container
- **Arc** - Curved line/wedge shape
- **Circle** - Circular shape
- **Line** - Line segment

## Z-Index Ordering

Elements with higher z_index values are drawn on top of elements with lower values. Elements with the same z_index are drawn in the order they were added to the scene.

```python
background.z_index = 0
game_ui.z_index = 10
popup.z_index = 100  # Always on top
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Frame" class="object-link">Frame</a>
<a href="Caption" class="object-link">Caption</a>
<a href="Sprite" class="object-link">Sprite</a>
<a href="Grid" class="object-link">Grid</a>
</div>
</div>
