---
layout: default
title: Alignment
---

# Alignment

Alignment enum for positioning UI elements within their parent.

## Overview

The `Alignment` IntEnum controls how UI elements are positioned relative to their parent container. It affects how `h_align` and `v_align` properties position elements and which margins apply.

## Quick Reference

```python
# Center a caption in its parent frame
caption = mcrfpy.Caption(text="Centered", pos=(0, 0))
caption.h_align = mcrfpy.Alignment.CENTER
caption.v_align = mcrfpy.Alignment.CENTER

# Position in top-right corner with margin
sprite = mcrfpy.Sprite(texture=tex, pos=(0, 0))
sprite.h_align = mcrfpy.Alignment.RIGHT
sprite.v_align = mcrfpy.Alignment.TOP
sprite.horiz_margin = 10
sprite.vert_margin = 10
```

## Values

| Value | Description |
|-------|-------------|
| `TOP_LEFT` | Align to top-left corner |
| `TOP_CENTER` | Align to top center |
| `TOP_RIGHT` | Align to top-right corner |
| `CENTER_LEFT` | Align to center-left |
| `CENTER` | Align to center |
| `CENTER_RIGHT` | Align to center-right |
| `BOTTOM_LEFT` | Align to bottom-left corner |
| `BOTTOM_CENTER` | Align to bottom center |
| `BOTTOM_RIGHT` | Align to bottom-right corner |

## Margin Rules

Different alignments use different margin properties:

| Alignment | Horizontal Margin | Vertical Margin |
|-----------|-------------------|-----------------|
| `CENTER` | Not used | Not used |
| `TOP_CENTER`, `BOTTOM_CENTER` | Not used | Applied |
| `CENTER_LEFT`, `CENTER_RIGHT` | Applied | Not used |
| Corners (`TOP_LEFT`, etc.) | Applied | Applied |

## Usage with h_align and v_align

Elements have separate horizontal and vertical alignment:

```python
# Different h_align and v_align combinations
element.h_align = mcrfpy.Alignment.LEFT   # or CENTER, RIGHT
element.v_align = mcrfpy.Alignment.TOP    # or CENTER, BOTTOM

# The alignment values map to these behaviors:
# LEFT/TOP = start of axis
# CENTER = middle of axis
# RIGHT/BOTTOM = end of axis
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Frame" class="object-link">Frame</a>
<a href="Caption" class="object-link">Caption</a>
<a href="Sprite" class="object-link">Sprite</a>
<a href="Drawable" class="object-link">Drawable</a>
</div>
</div>
