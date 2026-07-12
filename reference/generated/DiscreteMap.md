---
title: DiscreteMap
layout: default
mcrf:
  objects:
    - DiscreteMap
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# DiscreteMap

{% raw %}DiscreteMap(size: tuple[int, int], fill: int = 0, enum: type[IntEnum] = None)

A 2D grid of uint8 values (0-255) for discrete/categorical data.

DiscreteMap provides memory-efficient storage for terrain types, region IDs,
walkability masks, and other categorical data. Uses 4x less memory than HeightMap
for the same dimensions.

Args:
    size: (width, height) dimensions. Immutable after creation.
    fill: Initial value for all cells (0-255). Default 0.
    enum: Optional IntEnum class for value interpretation.

Example:
    from enum import IntEnum
    class Terrain(IntEnum):
        WATER = 0
        GRASS = 1
        MOUNTAIN = 2

    dmap = mcrfpy.DiscreteMap((100, 100), fill=0, enum=Terrain)
    dmap.fill(Terrain.GRASS, pos=(10, 10), size=(20, 20))
    print(dmap[15, 15])  # Terrain.GRASS
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `enum_type` | {% raw %}Optional IntEnum class for value interpretation.{% endraw %} |
| `size` | {% raw %}Dimensions (width, height) of the map. Read-only.{% endraw %} |

## Methods

### `add(other: DiscreteMap | int, *, pos=None, source_pos=None, size=None) -> DiscreteMap`

{% raw %}add(other: DiscreteMap | int, *, pos=None, source_pos=None, size=None) -> DiscreteMap

Add values from another map or a scalar, with saturation to 0-255.

Args:
    other: DiscreteMap to add, or int scalar to add to all cells
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `bitwise_and(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap`

{% raw %}bitwise_and(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap

Bitwise AND with another DiscreteMap.

Args:
    other: DiscreteMap for AND operation
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `bitwise_or(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap`

{% raw %}bitwise_or(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap

Bitwise OR with another DiscreteMap.

Args:
    other: DiscreteMap for OR operation
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `bitwise_xor(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap`

{% raw %}bitwise_xor(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap

Bitwise XOR with another DiscreteMap.

Args:
    other: DiscreteMap for XOR operation
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `bool(condition: int | set | callable) -> DiscreteMap`

{% raw %}bool(condition: int | set | callable) -> DiscreteMap

Create binary mask from condition. Returns NEW DiscreteMap.

Args:
    condition: int: match that value; set: match any in set; callable: predicate

Returns:
    DiscreteMap: new map with 1 where condition true, 0 elsewhere
{% endraw %}

### `clear() -> DiscreteMap`

{% raw %}clear() -> DiscreteMap

Set all cells to 0. Equivalent to fill(0).


Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `copy_from(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap`

{% raw %}copy_from(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap

Copy values from another DiscreteMap into the specified region.

Args:
    other: DiscreteMap to copy from
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `count(value: int) -> int`

{% raw %}count(value: int) -> int

Count cells with the specified value.

Args:
    value: Value to count (0-255)

Returns:
    int: Number of cells with that value
{% endraw %}

### `count_range(min_val: int, max_val: int) -> int`

{% raw %}count_range(min_val: int, max_val: int) -> int

Count cells with values in the specified range (inclusive).

Args:
    min_val: Minimum value (inclusive)
    max_val: Maximum value (inclusive)

Returns:
    int: Number of cells in range
{% endraw %}

### `fill(value: int, *, pos=None, size=None) -> DiscreteMap`

{% raw %}fill(value: int, *, pos=None, size=None) -> DiscreteMap

Set cells in region to the specified value.

Args:
    value: The value to set (0-255, or IntEnum member)
    pos: Region start (x, y) in destination (default: (0, 0))
    size: Region (width, height) to fill (default: remaining space)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `from_bytes(data: bytes, size: tuple[int, int], *, enum: type = None) -> DiscreteMap`

*classmethod*

{% raw %}from_bytes(data: bytes, size: tuple[int, int], *, enum: type = None) -> DiscreteMap

Create a DiscreteMap from raw byte data.

Args:
    data: Raw cell data (one byte per cell, row-major)
    size: (width, height) dimensions
    enum: Optional IntEnum class for value interpretation

Returns:
    DiscreteMap: new map initialized from data

Raises:
    ValueError: Data length does not match width * height
{% endraw %}

### `from_heightmap(hmap: HeightMap, mapping: list[tuple[tuple[float,float], int]], *, enum=None) -> DiscreteMap`

*classmethod*

{% raw %}from_heightmap(hmap: HeightMap, mapping: list[tuple[tuple[float,float], int]], *, enum=None) -> DiscreteMap

Create DiscreteMap from HeightMap using range-to-value mapping.

Args:
    hmap: HeightMap to convert
    mapping: List of ((min, max), value) tuples
    enum: Optional IntEnum class for value interpretation

Returns:
    DiscreteMap: new map with mapped values
{% endraw %}

### `get(x, y) or (pos) -> int | Enum`

{% raw %}get(x, y) or (pos) -> int | Enum

Get the value at integer coordinates.

Args:
    x, y: Position as two ints, tuple, list, or Vector

Returns:
    int or enum member if enum_type is set

Raises:
    IndexError: Position is out of bounds
{% endraw %}

### `histogram() -> dict[int, int]`

{% raw %}histogram() -> dict[int, int]

Get a histogram of value counts.


Returns:
    dict: {value: count} for all values present in the map
{% endraw %}

### `invert() -> DiscreteMap`

{% raw %}invert() -> DiscreteMap

Return NEW DiscreteMap with (255 - value) for each cell.


Returns:
    DiscreteMap: new inverted map (original unchanged)
{% endraw %}

### `mask() -> memoryview`

{% raw %}mask() -> memoryview

Get raw uint8_t data as memoryview for libtcod compatibility.


Returns:
    memoryview: Direct access to internal buffer (read/write)
{% endraw %}

### `max(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap`

{% raw %}max(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap

Set each cell to the maximum of this and another DiscreteMap.

Args:
    other: DiscreteMap to compare with
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `min(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap`

{% raw %}min(other: DiscreteMap, *, pos=None, source_pos=None, size=None) -> DiscreteMap

Set each cell to the minimum of this and another DiscreteMap.

Args:
    other: DiscreteMap to compare with
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `min_max() -> tuple[int, int]`

{% raw %}min_max() -> tuple[int, int]

Get the minimum and maximum values in the map.


Returns:
    tuple[int, int]: (min_value, max_value)
{% endraw %}

### `multiply(factor: float, *, pos=None, size=None) -> DiscreteMap`

{% raw %}multiply(factor: float, *, pos=None, size=None) -> DiscreteMap

Multiply values by a scalar factor, with saturation to 0-255.

Args:
    factor: Multiplier for each cell
    pos: Region start (x, y) (default: (0, 0))
    size: Region (width, height) (default: entire map)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `set(x: int, y: int, value: int) -> None`

{% raw %}set(x: int, y: int, value: int) -> None

Set the value at integer coordinates.

Args:
    x: X coordinate
    y: Y coordinate
    value: Value to set (0-255, or IntEnum member)

Raises:
    IndexError: Position is out of bounds

Raises:
    ValueError: Value out of range 0-255
{% endraw %}

### `subtract(other: DiscreteMap | int, *, pos=None, source_pos=None, size=None) -> DiscreteMap`

{% raw %}subtract(other: DiscreteMap | int, *, pos=None, source_pos=None, size=None) -> DiscreteMap

Subtract values from another map or a scalar, with saturation to 0-255.

Args:
    other: DiscreteMap to subtract, or int scalar
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    DiscreteMap: self, for method chaining
{% endraw %}

### `to_bytes() -> bytes`

{% raw %}to_bytes() -> bytes

Serialize map data to bytes (row-major, one byte per cell).


Returns:
    bytes: Raw cell data, length = width * height
{% endraw %}

### `to_heightmap(mapping: dict[int, float] = None) -> HeightMap`

{% raw %}to_heightmap(mapping: dict[int, float] = None) -> HeightMap

Convert to HeightMap, optionally mapping values to floats.

Args:
    mapping: Optional {int: float} mapping (default: direct cast)

Returns:
    HeightMap: new heightmap with converted values
{% endraw %}
