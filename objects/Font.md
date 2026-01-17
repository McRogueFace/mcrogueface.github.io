---
layout: default
title: Font
---

# Font

Font loading and text measurement.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `Font` loads a TTF font file for use with Caption elements. Fonts also provide text measurement for layout calculations.

## Quick Reference

```python
# Load a font
font = mcrfpy.Font("assets/fonts/DejaVuSans.ttf")

# Use with caption
caption = mcrfpy.Caption(pos=(0, 0), text="Hello")
caption.font = font
caption.size = 24

# Measure text dimensions
width, height = font.measure("Hello", size=24)
```

## Constructor

```python
mcrfpy.Font(filename: str)
```

## Methods

| Method | Description |
|--------|-------------|
| `measure(text, size)` | Returns (width, height) of text |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Caption" class="object-link">Caption</a>
<a href="../systems/scene#text" class="object-link">Text Subsystem</a>
</div>
</div>
