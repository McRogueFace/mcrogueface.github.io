---
layout: default
title: Texture
---

# Texture

Sprite sheet loading and management.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `Texture` loads an image file as a sprite sheet with a specified tile size. Textures are shared across Sprites, Grids, and Entities.

## Quick Reference

```python
# Load a 16x16 tile sprite sheet
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Use with sprite
sprite = mcrfpy.Sprite(pos=(0, 0), texture=texture, sprite_index=0)

# Use with grid
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture)

# Use with entity
entity = mcrfpy.Entity(pos=(5, 5), texture=texture, sprite_index=84)
```

## Constructor

```python
mcrfpy.Texture(filename: str, tile_width: int, tile_height: int)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `tile_width` | int | Width of each tile |
| `tile_height` | int | Height of each tile |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Sprite" class="object-link">Sprite</a>
<a href="Grid" class="object-link">Grid</a>
<a href="Entity" class="object-link">Entity</a>
<a href="../systems/scene#image" class="object-link">Image Subsystem</a>
</div>
</div>
