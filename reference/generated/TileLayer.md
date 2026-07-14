---
title: TileLayer
layout: default
mcrf:
  objects:
    - TileLayer
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# TileLayer

{% raw %}TileLayer(z_index=-1, name=None, texture=None, grid_size=None)

A grid layer that stores sprite indices per cell for tile-based rendering.

TileLayers can be created standalone and attached to a Grid via add_layer()
or passed to the Grid constructor's layers parameter. Layers with size (0, 0)
automatically resize to match the Grid when attached.

Args:
    z_index (int): Render order relative to entities. Negative values render
        below entities (as backgrounds), positive values render above entities
        (as overlays). Default: -1 (background)
    name (str): Layer name for Grid.layer(name) lookup. Default: None
    texture (Texture): Sprite atlas containing tile images. The texture's
        sprite_size determines individual tile dimensions. Required for
        rendering; can be set after creation. Default: None
    grid_size (tuple): Dimensions as (width, height). If None or (0, 0), the
        layer will auto-resize when attached to a Grid. Default: None

Attributes:
    z_index (int): Layer z-order relative to entities (read/write)
    name (str): Layer name for lookup (read-only)
    visible (bool): Whether layer is rendered (read/write)
    texture (Texture): Sprite atlas for tile images (read/write)
    grid_size (tuple): Layer dimensions as (width, height) (read-only)
    grid (Grid): Parent Grid or None. Setting manages layer association.

Methods:
    at(x, y) -> int: Get the tile index at cell position (x, y)
    set(x, y, index): Set the tile index at cell position (x, y)
    fill(index): Fill the entire layer with a single tile index
    fill_rect(x, y, w, h, index): Fill a rectangular region with a tile index

Tile Index Values:
    -1: No tile (transparent/empty cell)
    0+: Index into the texture's sprite atlas (row-major order)

Example:
    terrain = mcrfpy.TileLayer(z_index=-2, name='terrain', texture=tileset)
    grid = mcrfpy.Grid(grid_size=(20, 15), layers=[terrain])
    terrain.fill(0)  # Fill with tile index 0
    grid.layer('terrain').set(5, 5, 42)  # Place tile 42 at (5, 5){% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `grid` | {% raw %}Parent Grid or None (Grid \| None). Setting manages layer association and handles lazy allocation.{% endraw %} |
| `grid_size` | {% raw %}Layer dimensions as (width, height) tuple (tuple, read-only).{% endraw %} |
| `name` | {% raw %}Layer name (str, read-only). Used for Grid.layer(name) lookup.{% endraw %} |
| `texture` | {% raw %}Texture atlas for tile sprites (Texture \| None).{% endraw %} |
| `visible` | {% raw %}Whether the layer is rendered (bool).{% endraw %} |
| `z_index` | {% raw %}Layer z-order (int). Negative values render below entities.{% endraw %} |

## Methods

### `apply_ranges(source: HeightMap, ranges: list) -> TileLayer`

{% raw %}apply_ranges(source: HeightMap, ranges: list) -> TileLayer

Apply multiple tile assignments from a HeightMap in a single pass. Later ranges override earlier ones if overlapping.

Args:
    source: Source heightmap (must match layer dimensions)
    ranges: List of ((min, max), tile_index) tuples

Returns:
    self for method chaining

Note:
    Cells not matching any range are left unchanged.
{% endraw %}

### `apply_threshold(source: HeightMap, range: tuple, tile: int) -> TileLayer`

{% raw %}apply_threshold(source: HeightMap, range: tuple, tile: int) -> TileLayer

Set a tile index for cells where the HeightMap value falls within a range.

Args:
    source: Source heightmap (must match layer dimensions)
    range: Value range as (min, max) inclusive
    tile: Tile index to set for cells in range

Returns:
    self for method chaining
{% endraw %}

### `at(pos: tuple | Vector) or (x: int, y: int) -> int`

{% raw %}at(pos: tuple | Vector) or (x: int, y: int) -> int

Get the tile index at a cell position. Returns -1 if no tile is set.

Args:
    pos: Position as (x, y) tuple, list, or Vector; or pass x and y separately

Returns:
    Tile index at the specified cell, or -1 if empty

Raises:
    IndexError: If coordinates are out of bounds
{% endraw %}

### `edit() -> context manager`

{% raw %}edit() -> context manager

Context manager yielding a zero-copy, writable view of the layer's tile indices with shape (height, width), dtype int32 (-1 = no tile). Writes to the view alias the layer's storage (no copy). On exit the whole layer is invalidated and re-rendered.


Note:
    Use as `with layer.edit() as view:` -- e.g. np.asarray(view)[...] = ....

See also: Bulk-edit convention (#328) (docs/api-stability.md)
{% endraw %}

### `fill(index: int) -> None`

{% raw %}fill(index: int) -> None

Fill the entire layer with the specified tile index.

Args:
    index: Tile index to fill with (-1 for no tile)
{% endraw %}

### `fill_rect(pos: tuple, size: tuple, index: int) -> None`

{% raw %}fill_rect(pos: tuple, size: tuple, index: int) -> None

Fill a rectangular region with a tile index.

Args:
    pos: Top-left corner as (x, y)
    size: Dimensions as (width, height)
    index: Tile index to fill with (-1 for no tile)
{% endraw %}

### `set(pos, index: int) -> None`

{% raw %}set(pos, index: int) -> None

Set the tile index at a cell position. Use -1 to clear the tile.

Args:
    pos: Position as (x, y) tuple, list, or Vector
    index: Tile index (-1 for no tile)

Raises:
    IndexError: If coordinates are out of bounds
{% endraw %}
