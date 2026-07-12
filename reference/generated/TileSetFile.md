---
title: TileSetFile
layout: default
mcrf:
  objects:
    - TileSetFile
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# TileSetFile

{% raw %}TileSetFile(path: str)

Load a Tiled tileset file (.tsx or .tsj).

Parses the tileset and provides access to tile metadata, properties,
Wang sets, and texture creation.

Args:
    path: Path to the .tsx or .tsj tileset file.

Properties:
    name (str, read-only): Tileset name.
    tile_width (int, read-only): Width of each tile in pixels.
    tile_height (int, read-only): Height of each tile in pixels.
    tile_count (int, read-only): Total number of tiles.
    columns (int, read-only): Number of columns in the tileset image.
    image_source (str, read-only): Resolved path to the tileset image.
    properties (dict, read-only): Custom properties from the tileset.
    wang_sets (list, read-only): List of WangSet objects.

Example:
    ts = mcrfpy.TileSetFile('tileset.tsx')
    texture = ts.to_texture()
    print(f'{ts.name}: {ts.tile_count} tiles')
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `columns` | {% raw %}Number of columns in tileset image (int, read-only).{% endraw %} |
| `image_source` | {% raw %}Resolved path to the tileset image file (str, read-only).{% endraw %} |
| `margin` | {% raw %}Margin around tiles in pixels (int, read-only).{% endraw %} |
| `name` | {% raw %}Tileset name (str, read-only).{% endraw %} |
| `properties` | {% raw %}Custom tileset properties as a dict (read-only).{% endraw %} |
| `spacing` | {% raw %}Spacing between tiles in pixels (int, read-only).{% endraw %} |
| `tile_count` | {% raw %}Total number of tiles (int, read-only).{% endraw %} |
| `tile_height` | {% raw %}Height of each tile in pixels (int, read-only).{% endraw %} |
| `tile_width` | {% raw %}Width of each tile in pixels (int, read-only).{% endraw %} |
| `wang_sets` | {% raw %}List of WangSet objects from this tileset (read-only).{% endraw %} |

## Methods

### `tile_info(tile_id: int) -> dict | None`

{% raw %}tile_info(tile_id: int) -> dict | None

Get metadata for a specific tile.

Args:
    tile_id: Local tile ID (0-based)

Returns:
    Dict with 'properties' and 'animation' keys, or None if no metadata.
{% endraw %}

### `to_texture() -> Texture`

{% raw %}to_texture() -> Texture

Create a Texture from the tileset image.


Returns:
    A Texture object for use with TileLayer.
{% endraw %}

### `wang_set(name: str) -> WangSet`

{% raw %}wang_set(name: str) -> WangSet

Look up a WangSet by name.

Args:
    name: Name of the Wang set

Returns:
    The WangSet object.

Raises:
    KeyError: If no WangSet with that name exists
{% endraw %}
