---
layout: default
title: Caption
---

# Caption

Text rendering with font and color.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `Caption` renders text at a position. Configure font, size, and color for styled text display.

## Quick Reference

```python
# Create a caption
caption = mcrfpy.Caption(pos=(100, 50), text="Hello, World!")

# Style it
caption.font = mcrfpy.Font("assets/DejaVuSans.ttf")
caption.size = 24
caption.color = mcrfpy.Color(255, 255, 255)

# Add to scene
scene.children.append(caption)

# Update text dynamically
caption.text = f"Score: {score}"
```

## Constructor

```python
mcrfpy.Caption(pos: tuple, text: str = "")
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Position |
| `pos` | tuple | Position as (x, y) |
| `text` | str | Text content |
| `font` | Font | Font to use |
| `size` | int | Font size in pixels |
| `color` | Color | Text color |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Font" class="object-link">Font</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/scene#text" class="object-link">Text Subsystem</a>
</div>
</div>
