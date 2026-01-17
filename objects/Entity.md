---
layout: default
title: Entity
---

# Entity

Game objects that exist on grids.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

An `Entity` is a game object that exists at a position on a Grid. Entities represent players, enemies, items, and other interactive objects. They render on top of tiles and can be animated.

## Quick Reference

```python
# Create an entity
player = mcrfpy.Entity(pos=(10, 10), texture=texture, sprite_index=84)

# Add to grid
grid.entities.append(player)

# Move
player.x = 11
player.y = 10

# Animate movement
player.animate("x", 12, duration=0.2, easing="easeOutQuad")

# Change sprite
player.sprite_index = 85
```

## Constructor

```python
mcrfpy.Entity(pos: tuple, texture: Texture, sprite_index: int = 0)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Grid position |
| `pos` | tuple | Position as (x, y) |
| `texture` | Texture | Sprite sheet |
| `sprite_index` | int | Current sprite |
| `scale` | float | Scale factor |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |

## Methods

| Method | Description |
|--------|-------------|
| `animate(prop, target, ...)` | Animate a property |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="Texture" class="object-link">Texture</a>
<a href="../systems/grid" class="object-link">Grid System</a>
<a href="../systems/animation" class="object-link">Animation System</a>
</div>
</div>
