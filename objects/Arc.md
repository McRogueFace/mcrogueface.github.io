---
layout: default
title: Arc
---

# Arc

Draws a curved arc segment between two angles.

## Overview

An `Arc` draws a portion of a circle's outline between a start and end angle. Use arcs for pie charts, radial progress indicators, curved UI elements, and decorative shapes. The arc is drawn clockwise from the start angle to the end angle.

## Quick Reference

```python
# Create a simple arc
arc = mcrfpy.Arc(center=(200, 200), radius=50, start_angle=0, end_angle=180)

# Style it
arc.color = mcrfpy.Color(255, 0, 0)
arc.thickness = 3

# Add to scene
scene.children.append(arc)

# Create a progress indicator (quarter circle)
progress = mcrfpy.Arc(
    center=(100, 100),
    radius=40,
    start_angle=270,
    end_angle=360,
    color=mcrfpy.Color(0, 255, 0),
    thickness=5
)
```

## Constructor

```python
mcrfpy.Arc(center=None, radius=0, start_angle=0, end_angle=90, color=None, thickness=1, **kwargs)
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `center` | tuple | None | Center point as (x, y) |
| `radius` | float | 0 | Radius of the arc |
| `start_angle` | float | 0 | Starting angle in degrees |
| `end_angle` | float | 90 | Ending angle in degrees |
| `color` | Color | None | Arc stroke color |
| `thickness` | float | 1 | Line thickness |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `center` | tuple | Center point as (x, y) |
| `pos` | tuple | Alias for center |
| `radius` | float | Radius of the arc |
| `start_angle` | float | Starting angle in degrees |
| `end_angle` | float | Ending angle in degrees |
| `color` | Color | Arc stroke color |
| `thickness` | float | Line thickness |
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
# Animated loading spinner
arc = mcrfpy.Arc(
    center=(150, 150),
    radius=30,
    start_angle=0,
    end_angle=270,
    color=mcrfpy.Color(100, 150, 255),
    thickness=4
)
scene.children.append(arc)

# Animate the arc rotating
arc.animate("start_angle", 360, 1.0, mcrfpy.Easing.LINEAR)
arc.animate("end_angle", 630, 1.0, mcrfpy.Easing.LINEAR)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Circle" class="object-link">Circle</a>
<a href="Line" class="object-link">Line</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Scene" class="object-link">Scene</a>
</div>
</div>
