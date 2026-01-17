---
layout: default
title: Texture
---

# Texture

SFML Texture object for sprite atlases and tile sheets.

## Overview

A `Texture` loads an image file and divides it into a grid of sprites based on the specified tile dimensions. Textures are shared across Sprites, Grids, Entities, and TileLayers. McRogueFace caches textures internally, so loading the same image with the same tile size returns the same texture object.

## Quick Reference

```python
import mcrfpy

# Load a 16x16 tile sprite sheet
texture = mcrfpy.Texture("assets/sprites/dungeon.png", 16, 16)

# Check texture properties
print(f"Sprite size: {texture.sprite_width}x{texture.sprite_height}")
print(f"Sheet size: {texture.sheet_width}x{texture.sheet_height}")
print(f"Total sprites: {texture.sprite_count}")

# Use with Sprite
sprite = mcrfpy.Sprite(pos=(100, 100), texture=texture, sprite_index=0)

# Use with Grid
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture)

# Use with Entity
player = mcrfpy.Entity(pos=(5, 5), texture=texture, sprite_index=84)
```

## Constructor

```python
mcrfpy.Texture(filename: str, sprite_width: int, sprite_height: int)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `filename` | str | Path to image file (PNG, JPG, etc.) |
| `sprite_width` | int | Width of each sprite in pixels |
| `sprite_height` | int | Height of each sprite in pixels |

Raises `IOError` if the image file cannot be loaded.

## Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `source` | str | read-only | Path to the loaded image file |
| `sprite_width` | int | read-only | Width of each sprite in pixels |
| `sprite_height` | int | read-only | Height of each sprite in pixels |
| `sheet_width` | int | read-only | Total width of texture in pixels |
| `sheet_height` | int | read-only | Total height of texture in pixels |
| `sprite_count` | int | read-only | Total number of sprites in the sheet |

## Sprite Index Calculation

Sprites are indexed left-to-right, top-to-bottom, starting from 0:

```
+----+----+----+----+
|  0 |  1 |  2 |  3 |
+----+----+----+----+
|  4 |  5 |  6 |  7 |
+----+----+----+----+
|  8 |  9 | 10 | 11 |
+----+----+----+----+
```

To calculate the index for a sprite at row `r`, column `c`:
```python
columns = texture.sheet_width // texture.sprite_width
index = r * columns + c
```

## Examples

### Basic Texture Loading

```python
import mcrfpy

# Load a sprite sheet
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create sprites using different indices
floor = mcrfpy.Sprite(pos=(0, 0), texture=texture, sprite_index=0)
wall = mcrfpy.Sprite(pos=(16, 0), texture=texture, sprite_index=1)
player = mcrfpy.Sprite(pos=(32, 0), texture=texture, sprite_index=84)
```

### Texture for Grid and Entities

```python
# Load texture
texture = mcrfpy.Texture("assets/tiles.png", 16, 16)

# Create grid using texture
grid = mcrfpy.Grid(
    grid_size=(40, 30),
    texture=texture,
    pos=(0, 0),
    size=(640, 480)
)

# Set tile sprites
for x in range(40):
    for y in range(30):
        cell = grid.at(x, y)
        cell.sprite_index = 0  # Floor tile

# Add entity with same texture
player = mcrfpy.Entity(
    pos=(5, 5),
    texture=texture,
    sprite_index=84  # Player sprite
)
grid.entities.append(player)
```

### Texture Manager

```python
class TextureManager:
    _textures = {}

    @classmethod
    def get(cls, name):
        """Get a preloaded texture by name."""
        return cls._textures.get(name)

    @classmethod
    def load(cls, name, path, tile_w, tile_h):
        """Load and register a texture."""
        cls._textures[name] = mcrfpy.Texture(path, tile_w, tile_h)
        return cls._textures[name]

    @classmethod
    def preload_all(cls):
        """Load all game textures."""
        cls.load("dungeon", "assets/dungeon.png", 16, 16)
        cls.load("characters", "assets/chars.png", 16, 16)
        cls.load("ui", "assets/ui.png", 8, 8)
        cls.load("effects", "assets/effects.png", 32, 32)

# Usage
TextureManager.preload_all()
dungeon_tex = TextureManager.get("dungeon")
```

### Sprite Sheet Information

```python
def print_texture_info(texture):
    """Display texture properties."""
    cols = texture.sheet_width // texture.sprite_width
    rows = texture.sheet_height // texture.sprite_height

    print(f"Source: {texture.source}")
    print(f"Sheet size: {texture.sheet_width}x{texture.sheet_height} pixels")
    print(f"Sprite size: {texture.sprite_width}x{texture.sprite_height} pixels")
    print(f"Grid: {cols} columns x {rows} rows")
    print(f"Total sprites: {texture.sprite_count}")

texture = mcrfpy.Texture("assets/sprites.png", 16, 16)
print_texture_info(texture)
```

### Animated Sprite Frames

```python
class AnimatedSprite:
    def __init__(self, sprite, start_index, frame_count):
        self.sprite = sprite
        self.start_index = start_index
        self.frame_count = frame_count
        self.current_frame = 0
        self.frame_time = 0.1  # seconds per frame
        self.elapsed = 0

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.frame_time:
            self.elapsed -= self.frame_time
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.sprite.sprite_index = self.start_index + self.current_frame

# Usage: Character walk animation (frames 0-3)
texture = mcrfpy.Texture("assets/character.png", 16, 16)
sprite = mcrfpy.Sprite(pos=(100, 100), texture=texture, sprite_index=0)
anim = AnimatedSprite(sprite, start_index=0, frame_count=4)
```

### Different Tile Sizes

```python
# Standard dungeon tiles
tiles_16 = mcrfpy.Texture("assets/tiles_16x16.png", 16, 16)

# Larger character sprites
chars_32 = mcrfpy.Texture("assets/characters_32x32.png", 32, 32)

# Small UI icons
icons_8 = mcrfpy.Texture("assets/icons_8x8.png", 8, 8)

# Non-square tiles (isometric)
iso_tiles = mcrfpy.Texture("assets/isometric.png", 64, 32)
```

## Notes

- Supported formats: PNG (recommended), JPG, BMP, TGA
- PNG with transparency is recommended for sprites
- Textures are cached internally - same file + tile size returns same object
- Large textures may impact memory and performance
- Sprite indices are 0-based and wrap left-to-right, top-to-bottom

## Related

<div class="related-objects">
<div class="object-links">
<a href="Sprite" class="object-link">Sprite</a>
<a href="Entity" class="object-link">Entity</a>
<a href="Grid" class="object-link">Grid</a>
<a href="TileLayer" class="object-link">TileLayer</a>
<a href="Font" class="object-link">Font</a>
</div>
</div>
