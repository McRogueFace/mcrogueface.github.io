---
layout: default
title: Circle
---

# Circle

Draws a filled or outlined circle.

## Overview

A `Circle` draws a circular shape with optional fill and outline. Use circles for buttons, indicators, decorative elements, and any round UI components. Circles can be filled, outlined, or both.

## Quick Reference

```python
# Create a filled circle
circle = mcrfpy.Circle(radius=30, center=(100, 100))
circle.fill_color = mcrfpy.Color(0, 255, 0)

# Add to scene
scene.children.append(circle)

# Circle with outline only
ring = mcrfpy.Circle(
    radius=50,
    center=(200, 200),
    fill_color=mcrfpy.Color(0, 0, 0, 0),  # Transparent fill
    outline_color=mcrfpy.Color(255, 255, 255),
    outline=3
)
```

## Constructor

```python
mcrfpy.Circle(radius=0, center=None, fill_color=None, outline_color=None, outline=0, **kwargs)
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `radius` | float | 0 | Circle radius |
| `center` | tuple | None | Center point as (x, y) |
| `fill_color` | Color | None | Interior fill color |
| `outline_color` | Color | None | Border color |
| `outline` | float | 0 | Border thickness |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `radius` | float | Circle radius |
| `center` | tuple | Center point as (x, y) |
| `pos` | tuple | Alias for center |
| `fill_color` | Color | Interior fill color |
| `outline_color` | Color | Border color |
| `outline` | float | Border thickness |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |
| `z_index` | int | Draw order |
| `name` | str | Object identifier |
| `hovered` | bool | Mouse hover state (read-only) |

## Methods

| Method | Description |
|--------|-------------|
| `animate(property, target, duration, easing)` | Animate a property over time |
| `move(dx, dy)` | Move by relative offset |
| `resize(dw, dh)` | Resize by relative amount |
| `realign()` | Recalculate position based on alignment |

## Events

| Property | Description |
|----------|-------------|
| `on_click` | Callback when clicked |
| `on_enter` | Callback when mouse enters |
| `on_exit` | Callback when mouse exits |
| `on_move` | Callback when mouse moves over |

## Example

```python
# Interactive button circle
button = mcrfpy.Circle(
    radius=25,
    center=(150, 150),
    fill_color=mcrfpy.Color(50, 50, 200),
    outline_color=mcrfpy.Color(100, 100, 255),
    outline=2
)

def on_hover_enter(x, y):
    button.fill_color = mcrfpy.Color(80, 80, 230)

def on_hover_exit(x, y):
    button.fill_color = mcrfpy.Color(50, 50, 200)

def on_click(x, y):
    print("Button clicked!")

button.on_enter = on_hover_enter
button.on_exit = on_hover_exit
button.on_click = on_click

scene.children.append(button)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Arc" class="object-link">Arc</a>
<a href="Line" class="object-link">Line</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Scene" class="object-link">Scene</a>
</div>
</div>
