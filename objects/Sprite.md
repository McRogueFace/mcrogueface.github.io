---
layout: default
title: Sprite
---

# Sprite

Single image/sprite rendering.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `Sprite` displays a single image from a texture/sprite sheet. Use sprites for UI icons, decorations, and standalone images.

## Quick Reference

```python
# Load texture
texture = mcrfpy.Texture("assets/sprites.png", 16, 16)

# Create sprite
sprite = mcrfpy.Sprite(pos=(100, 100), texture=texture, sprite_index=42)

# Scale it
sprite.scale = 2.0

# Add to scene
scene.children.append(sprite)

# Change displayed sprite
sprite.sprite_index = 43
```

## Constructor

```python
mcrfpy.Sprite(pos: tuple, texture: Texture, sprite_index: int = 0)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Position |
| `pos` | tuple | Position as (x, y) |
| `texture` | Texture | Source sprite sheet |
| `sprite_index` | int | Index into sprite sheet |
| `scale` | float | Scale factor |
| `visible` | bool | Visibility toggle |
| `opacity` | float | Transparency (0.0-1.0) |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Texture" class="object-link">Texture</a>
<a href="Entity" class="object-link">Entity</a>
<a href="../systems/scene#image" class="object-link">Image Subsystem</a>
</div>
</div>
