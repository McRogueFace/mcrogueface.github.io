---
title: TileMapFile
layout: default
mcrf:
  objects:
    - TileMapFile
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# TileMapFile

{% raw %}TileMapFile(path: str)

Load a Tiled map file (.tmx or .tmj).

Parses the map and its referenced tilesets, providing access to tile layers,
object layers, and GID resolution.

Args:
    path: Path to the .tmx or .tmj map file.

Properties:
    width (int, read-only): Map width in tiles.
    height (int, read-only): Map height in tiles.
    tile_width (int, read-only): Tile width in pixels.
    tile_height (int, read-only): Tile height in pixels.
    orientation (str, read-only): Map orientation (e.g. 'orthogonal').
    properties (dict, read-only): Custom map properties.
    tileset_count (int, read-only): Number of referenced tilesets.
    tile_layer_names (list, read-only): Names of tile layers.
    object_layer_names (list, read-only): Names of object layers.

Example:
    tm = mcrfpy.TileMapFile('map.tmx')
    data = tm.tile_layer_data('Ground')
    tm.apply_to_tile_layer(my_tile_layer, 'Ground')
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `height` | {% raw %}Map height in tiles (int, read-only).{% endraw %} |
| `object_layer_names` | {% raw %}List of object layer names (read-only).{% endraw %} |
| `orientation` | {% raw %}Map orientation, e.g. 'orthogonal' (str, read-only).{% endraw %} |
| `properties` | {% raw %}Custom map properties as a dict (read-only).{% endraw %} |
| `tile_height` | {% raw %}Tile height in pixels (int, read-only).{% endraw %} |
| `tile_layer_names` | {% raw %}List of tile layer names (read-only).{% endraw %} |
| `tile_width` | {% raw %}Tile width in pixels (int, read-only).{% endraw %} |
| `tileset_count` | {% raw %}Number of referenced tilesets (int, read-only).{% endraw %} |
| `width` | {% raw %}Map width in tiles (int, read-only).{% endraw %} |

## Methods

### `apply_to_tile_layer(tile_layer: TileLayer, layer_name: str, tileset_index: int = 0) -> None`

{% raw %}apply_to_tile_layer(tile_layer: TileLayer, layer_name: str, tileset_index: int = 0) -> None

Resolve GIDs and write sprite indices into a TileLayer.

Args:
    tile_layer: Target TileLayer to write into
    layer_name: Name of the tile layer in this map
    tileset_index: Which tileset to resolve GIDs against (default 0)
{% endraw %}

### `object_layer(name: str) -> list[dict]`

{% raw %}object_layer(name: str) -> list[dict]

Get objects from an object layer as Python dicts.

Args:
    name: Name of the object layer

Returns:
    List of dicts with object properties (id, name, x, y, width, height, etc.).

Raises:
    KeyError: If no object layer with that name exists
{% endraw %}

### `resolve_gid(gid: int) -> tuple[int, int]`

{% raw %}resolve_gid(gid: int) -> tuple[int, int]

Resolve a global tile ID to tileset index and local tile ID.

Args:
    gid: Global tile ID from tile_layer_data()

Returns:
    Tuple of (tileset_index, local_tile_id). (-1, -1) for empty/invalid.
{% endraw %}

### `tile_layer_data(name: str) -> list[int]`

{% raw %}tile_layer_data(name: str) -> list[int]

Get raw global GID data for a tile layer.

Args:
    name: Name of the tile layer

Returns:
    Flat list of global GIDs (0 = empty tile).

Raises:
    KeyError: If no tile layer with that name exists
{% endraw %}

### `tileset(index: int) -> tuple[int, TileSetFile]`

{% raw %}tileset(index: int) -> tuple[int, TileSetFile]

Get a referenced tileset by index.

Args:
    index: Tileset index (0-based)

Returns:
    Tuple of (firstgid, TileSetFile).
{% endraw %}
