---
layout: default
title: Alignment
mcrf:
  objects: [Alignment]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Alignment

Alignment enum for positioning UI elements within their parent.

## Overview

The `Alignment` IntEnum controls how UI elements are positioned relative to their parent container. Any drawable's single `align` property takes one of the nine `Alignment` values (or `None` to disable and fall back to manual `pos` positioning); the `margin`, `horiz_margin`, and `vert_margin` properties control the offset from the parent's edges.

## Quick Reference

```python
import mcrfpy

scene = mcrfpy.Scene("alignment_demo")
mcrfpy.current_scene = scene

container = mcrfpy.Frame(pos=(50, 50), size=(400, 300), fill_color=mcrfpy.Color(40, 40, 60))
scene.children.append(container)

# Center a caption in its parent frame
caption = mcrfpy.Caption(text="Centered", pos=(0, 0))
caption.align = mcrfpy.Alignment.CENTER
container.children.append(caption)

# Position a sprite in the top-right corner with margin
sprite = mcrfpy.Sprite(texture=mcrfpy.default_texture, pos=(0, 0))
sprite.align = mcrfpy.Alignment.TOP_RIGHT
sprite.horiz_margin = 10
sprite.vert_margin = 10
container.children.append(sprite)
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

## Usage with `align`

Unlike CSS-style layout systems, McRogueFace does not expose separate horizontal and vertical alignment properties. A single `align` property takes one of the nine combined `Alignment` values, which together describe both axes at once:

```python
# One property covers both axes
element.align = mcrfpy.Alignment.TOP_LEFT     # start of both axes
element.align = mcrfpy.Alignment.CENTER       # middle of both axes
element.align = mcrfpy.Alignment.BOTTOM_RIGHT # end of both axes

# The first word (TOP/CENTER/BOTTOM) controls the vertical axis;
# the second word (LEFT/CENTER/RIGHT) controls the horizontal axis.
```

Setting `align = None` disables automatic alignment and reverts to manual `pos`-based positioning. Call `element.realign()` to recompute position after the parent is resized.

## Related

<div class="related-objects">
<div class="object-links">
<a href="Frame" class="object-link">Frame</a>
<a href="Caption" class="object-link">Caption</a>
<a href="Sprite" class="object-link">Sprite</a>
<a href="Drawable" class="object-link">Drawable</a>
</div>
</div>
