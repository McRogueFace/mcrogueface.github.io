---
layout: default
title: Frame
---

# Frame

Rectangular container with background and border.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `Frame` is a rectangular UI element that can contain other elements. Use frames for panels, buttons, dialog boxes, and other UI containers.

## Quick Reference

```python
# Create a frame
frame = mcrfpy.Frame(pos=(100, 100), size=(200, 150))

# Style it
frame.fill_color = mcrfpy.Color(40, 40, 40)
frame.outline_color = mcrfpy.Color(100, 100, 100)
frame.outline = 2

# Add to scene
scene.children.append(frame)

# Frames can contain children
frame.children.append(caption)
```

## Constructor

```python
mcrfpy.Frame(pos: tuple, size: tuple)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Position |
| `w`, `h` | float | Size |
| `pos` | tuple | Position as (x, y) |
| `size` | tuple | Size as (w, h) |
| `fill_color` | Color | Background color |
| `outline_color` | Color | Border color |
| `outline` | float | Border thickness |
| `children` | UICollection | Child elements |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Scene" class="object-link">Scene</a>
<a href="Caption" class="object-link">Caption</a>
<a href="../systems/scene" class="object-link">Scene System</a>
</div>
</div>
