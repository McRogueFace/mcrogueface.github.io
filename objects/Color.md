---
layout: default
title: Color
---

# Color

RGBA color representation.

## Overview

The `Color` class represents colors with red, green, blue, and alpha (transparency) components. Colors are used for fills, outlines, text, and other visual styling throughout McRogueFace.

## Quick Reference

```python
# Create colors
red = mcrfpy.Color(255, 0, 0)
semi_transparent = mcrfpy.Color(100, 100, 255, 128)

# From hex string
blue = mcrfpy.Color.from_hex("#0066CC")
white = mcrfpy.Color.from_hex("FFFFFF")

# Color interpolation
start = mcrfpy.Color(255, 0, 0)
end = mcrfpy.Color(0, 0, 255)
middle = start.lerp(end, 0.5)  # Purple

# Apply to elements
frame.fill_color = mcrfpy.Color(40, 40, 60)
caption.fill_color = mcrfpy.Color(255, 255, 255)
```

## Constructor

```python
mcrfpy.Color(r: int = 0, g: int = 0, b: int = 0, a: int = 255)
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `r` | int | 0 | Red component (0-255) |
| `g` | int | 0 | Green component (0-255) |
| `b` | int | 0 | Blue component (0-255) |
| `a` | int | 255 | Alpha component (0-255, 255=opaque) |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `r` | int | Red component (0-255, auto-clamped) |
| `g` | int | Green component (0-255, auto-clamped) |
| `b` | int | Blue component (0-255, auto-clamped) |
| `a` | int | Alpha component (0-255, auto-clamped) |

## Methods

| Method | Description |
|--------|-------------|
| `from_hex(hex_string)` | Create Color from hex string (class method) |
| `to_hex()` | Convert to hex string (e.g., "#FF0066") |
| `lerp(other, t)` | Linear interpolate to another color (t: 0.0-1.0) |

## Important Note

Colors retrieved from UI elements are **copies**, not references. To modify an element's color, you must reassign the entire color:

```python
# This does NOT work:
frame.fill_color.r = 255  # No effect!

# This works:
color = frame.fill_color
color.r = 255
frame.fill_color = color  # Reassign to apply

# Or create new color:
frame.fill_color = mcrfpy.Color(255, 0, 0)
```

## Hex Format

The `from_hex()` method accepts:
- `"#RRGGBB"` - With hash prefix
- `"RRGGBB"` - Without hash prefix
- `"#RRGGBBAA"` - With alpha
- `"RRGGBBAA"` - With alpha, no hash

## Related

<div class="related-objects">
<div class="object-links">
<a href="Frame" class="object-link">Frame</a>
<a href="Caption" class="object-link">Caption</a>
</div>
</div>
