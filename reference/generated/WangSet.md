---
title: WangSet
layout: default
mcrf:
  objects:
    - WangSet
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# WangSet

{% raw %}WangSet - Wang terrain auto-tile set from a Tiled tileset.

WangSets are obtained from TileSetFile.wang_sets or TileSetFile.wang_set().
They map abstract terrain types to concrete sprite indices using Tiled's
Wang tile algorithm.

Properties:
    name (str, read-only): Wang set name.
    type (str, read-only): 'corner', 'edge', or 'mixed'.
    color_count (int, read-only): Number of terrain colors.
    colors (list, read-only): List of color dicts.

Example:
    ws = tileset.wang_set('overworld')
    Terrain = ws.terrain_enum()
    tiles = ws.resolve(discrete_map)
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `color_count` | {% raw %}Number of terrain colors (int, read-only).{% endraw %} |
| `colors` | {% raw %}List of color dicts with name, index, tile_id, probability (read-only).{% endraw %} |
| `name` | {% raw %}Wang set name (str, read-only).{% endraw %} |
| `type` | {% raw %}Wang set type: 'corner', 'edge', or 'mixed' (str, read-only).{% endraw %} |

## Methods

### `apply(discrete_map: DiscreteMap, tile_layer: TileLayer) -> None`

{% raw %}apply(discrete_map: DiscreteMap, tile_layer: TileLayer) -> None

Resolve terrain and write tile indices directly into a TileLayer.

Args:
    discrete_map: A DiscreteMap with terrain IDs
    tile_layer: Target TileLayer to write resolved tiles into
{% endraw %}

### `resolve(discrete_map: DiscreteMap) -> list[int]`

{% raw %}resolve(discrete_map: DiscreteMap) -> list[int]

Resolve terrain data to tile indices using Wang tile rules.

Args:
    discrete_map: A DiscreteMap with terrain IDs matching this WangSet's colors

Returns:
    List of tile IDs (one per cell). -1 means no matching Wang tile.
{% endraw %}

### `terrain_enum() -> IntEnum`

{% raw %}terrain_enum() -> IntEnum

Generate a Python IntEnum from this WangSet's terrain colors.


Returns:
    IntEnum class with NONE=0 and one member per color (UPPER_SNAKE_CASE).
{% endraw %}
