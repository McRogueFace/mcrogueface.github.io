---
title: Texture
layout: default
mcrf:
  objects:
    - Texture
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Texture

{% raw %}Texture(filename: str, sprite_width: int = 0, sprite_height: int = 0, display_size: tuple = None, display_origin: tuple = None)

A texture atlas for sprites and tiles.

Args:
    filename: Path to an image file (PNG, BMP, etc.).
    sprite_width: Width of each sprite cell in pixels (0 = full image).
    sprite_height: Height of each sprite cell in pixels (0 = full image).
    display_size: Optional (w, h) actual content size within each cell.
    display_origin: Optional (x, y) content offset within each cell.

Properties:
    sprite_width, sprite_height (int, read-only): Cell dimensions.
    sheet_width, sheet_height (int, read-only): Grid dimensions in cells.
    sprite_count (int, read-only): Total number of sprite cells.
    source (str, read-only): File path used to load this texture.
    display_width, display_height (int, read-only): Content size within cells.
    display_offset_x, display_offset_y (int, read-only): Content offset within cells.
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `display_height` | {% raw %}Display height of sprite content within each cell (int, read-only). Defaults to sprite_height.{% endraw %} |
| `display_offset_x` | {% raw %}X offset of sprite content within each cell (int, read-only). Default 0.{% endraw %} |
| `display_offset_y` | {% raw %}Y offset of sprite content within each cell (int, read-only). Default 0.{% endraw %} |
| `display_width` | {% raw %}Display width of sprite content within each cell (int, read-only). Defaults to sprite_width.{% endraw %} |
| `sheet_height` | {% raw %}Number of sprite rows in the texture sheet (int, read-only). Calculated as texture_height / sprite_height.{% endraw %} |
| `sheet_width` | {% raw %}Number of sprite columns in the texture sheet (int, read-only). Calculated as texture_width / sprite_width.{% endraw %} |
| `source` | {% raw %}Source filename path (str, read-only). The path used to load this texture.{% endraw %} |
| `sprite_count` | {% raw %}Total number of sprites in the texture sheet (int, read-only). Equals sheet_width * sheet_height.{% endraw %} |
| `sprite_height` | {% raw %}Height of each sprite in pixels (int, read-only). Specified during texture initialization.{% endraw %} |
| `sprite_width` | {% raw %}Width of each sprite in pixels (int, read-only). Specified during texture initialization.{% endraw %} |

## Methods

### `composite(layers: list[Texture], sprite_width: int, sprite_height: int, name: str = '<composite>') -> Texture`

*classmethod*

{% raw %}composite(layers: list[Texture], sprite_width: int, sprite_height: int, name: str = '<composite>') -> Texture

Alpha-composite multiple texture layers into a single texture.

Args:
    layers: List of Texture objects, composited bottom-to-top
    sprite_width: Width of each sprite cell in the result
    sprite_height: Height of each sprite cell in the result
    name: Optional name for the composite texture

Returns:
    Texture: New texture with all layers composited

Raises:
    ValueError: If layers have different dimensions or list is empty

Note:
    This is a class method. Uses Porter-Duff 'over' alpha compositing.
{% endraw %}

### `from_bytes(data: bytes, width: int, height: int, sprite_width: int, sprite_height: int, name: str = '<generated>') -> Texture`

*classmethod*

{% raw %}from_bytes(data: bytes, width: int, height: int, sprite_width: int, sprite_height: int, name: str = '<generated>') -> Texture

Create a Texture from raw RGBA pixel data.

Args:
    data: Raw RGBA bytes (length must equal width * height * 4)
    width: Image width in pixels
    height: Image height in pixels
    sprite_width: Width of each sprite cell
    sprite_height: Height of each sprite cell
    name: Optional name for the texture (default: '<generated>')

Returns:
    Texture: New texture containing the pixel data

Raises:
    ValueError: If data length does not match width * height * 4

Note:
    This is a class method. Useful for procedurally generated textures.
{% endraw %}

### `hsl_shift(hue_shift: float, sat_shift: float = 0.0, lit_shift: float = 0.0) -> Texture`

{% raw %}hsl_shift(hue_shift: float, sat_shift: float = 0.0, lit_shift: float = 0.0) -> Texture

Create a new texture with HSL color adjustments applied.

Args:
    hue_shift: Hue rotation in degrees [0.0, 360.0)
    sat_shift: Saturation adjustment [-1.0, 1.0] (default 0.0)
    lit_shift: Lightness adjustment [-1.0, 1.0] (default 0.0)

Returns:
    Texture: New texture with color-shifted pixels

Note:
    Preserves alpha channel. Skips fully transparent pixels.
{% endraw %}
