---
layout: default
title: GridPointState
---

# GridPointState

Tile appearance state.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

`GridPointState` holds the visual appearance of a tile, including foreground and background colors. Used for advanced tile rendering with color overlays.

## Quick Reference

```python
# Get a tile's state
cell = grid.at(5, 5)
state = cell.get_state()

# Modify colors
state.foreground = mcrfpy.Color(255, 255, 255)
state.background = mcrfpy.Color(50, 50, 50)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `foreground` | Color | Foreground/tint color |
| `background` | Color | Background color |

## Related

<div class="related-objects">
<div class="object-links">
<a href="GridPoint" class="object-link">GridPoint</a>
<a href="Grid" class="object-link">Grid</a>
<a href="../systems/grid#layers" class="object-link">Layer Subsystem</a>
</div>
</div>
