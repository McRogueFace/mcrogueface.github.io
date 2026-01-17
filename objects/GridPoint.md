---
layout: default
title: GridPoint
---

# GridPoint

Individual tile in a grid.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `GridPoint` represents a single tile in a Grid. It stores the tile's visual appearance and properties like walkability and transparency for FOV/pathfinding.

## Quick Reference

```python
# Access a grid point
cell = grid.at(5, 5)

# Set tile appearance
cell.tilesprite = 0  # Floor tile

# Set properties
cell.walkable = True
cell.transparent = True

# Check visibility (after compute_fov)
if cell.visible:
    # Currently in player's view
elif cell.explored:
    # Previously seen
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `tilesprite` | int | Tile sprite index |
| `walkable` | bool | Can entities walk here? |
| `transparent` | bool | Does light pass through? |
| `visible` | bool | Currently in FOV? (read-only) |
| `explored` | bool | Has been seen? (read-only) |
| `color` | Color | Tile tint color |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="GridPointState" class="object-link">GridPointState</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
