---
layout: default
title: Line
---

# Line

Draws a straight line between two points.

## Overview

A `Line` draws a straight segment between a start and end point with configurable thickness and color. Use lines for connectors, dividers, graphs, decorative elements, and drawing geometric shapes.

## Quick Reference

```python
# Create a simple line
line = mcrfpy.Line(start=(50, 50), end=(200, 150))
line.color = mcrfpy.Color(255, 255, 0)
line.thickness = 2

# Add to scene
scene.children.append(line)

# Create a divider
divider = mcrfpy.Line(
    start=(0, 100),
    end=(400, 100),
    thickness=1,
    color=mcrfpy.Color(100, 100, 100)
)
```

## Constructor

```python
mcrfpy.Line(start=None, end=None, thickness=1.0, color=None, **kwargs)
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `start` | tuple | None | Starting point as (x, y) |
| `end` | tuple | None | Ending point as (x, y) |
| `thickness` | float | 1.0 | Line thickness |
| `color` | Color | None | Line color |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `start` | tuple | Starting point as (x, y) |
| `end` | tuple | Ending point as (x, y) |
| `pos` | tuple | Midpoint of the line |
| `thickness` | float | Line thickness |
| `color` | Color | Line color |
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
# Draw a triangle using three lines
points = [(100, 50), (50, 150), (150, 150)]
color = mcrfpy.Color(255, 100, 100)

for i in range(3):
    line = mcrfpy.Line(
        start=points[i],
        end=points[(i + 1) % 3],
        thickness=2,
        color=color
    )
    scene.children.append(line)

# Animated growing line
growing_line = mcrfpy.Line(
    start=(200, 100),
    end=(200, 100),  # Start with zero length
    thickness=3,
    color=mcrfpy.Color(0, 255, 255)
)
scene.children.append(growing_line)

# Animate the end point to create a growing effect
growing_line.animate("end", (350, 200), 1.5, mcrfpy.Easing.EASE_OUT)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Arc" class="object-link">Arc</a>
<a href="Circle" class="object-link">Circle</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Scene" class="object-link">Scene</a>
</div>
</div>
