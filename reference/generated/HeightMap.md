---
title: HeightMap
layout: default
mcrf:
  objects:
    - HeightMap
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# HeightMap

{% raw %}HeightMap(size: tuple[int, int], fill: float = 0.0)

A 2D grid of float values for procedural generation.

HeightMap is the universal canvas for procedural generation. It stores float values that can be manipulated, combined, and applied to Grid and Layer objects.

Args:
    size: (width, height) dimensions of the heightmap. Immutable after creation.
    fill: Initial value for all cells. Default 0.0.

Example:
    hmap = mcrfpy.HeightMap((100, 100))
    hmap.fill(0.5).scale(2.0).clamp(0.0, 1.0)
    value = hmap[5, 5]  # Subscript shorthand for get()
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `size` | {% raw %}Dimensions (width, height) of the heightmap. Read-only.{% endraw %} |

## Methods

### `add(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap`

{% raw %}add(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap

Add another heightmap's values to this one in the specified region.

Args:
    other: HeightMap to add values from
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `add_bsp(bsp: BSP, *, pos=None, select: str = 'leaves', nodes: list = None, shrink: int = 0, value: float = 1.0) -> HeightMap`

{% raw %}add_bsp(bsp: BSP, *, pos=None, select: str = 'leaves', nodes: list = None, shrink: int = 0, value: float = 1.0) -> HeightMap

Add BSP node regions to heightmap. More efficient than creating intermediate HeightMap.

Args:
    bsp: BSP tree to sample from
    pos: Where BSP origin maps to in HeightMap (default: origin-relative like to_heightmap)
    select: 'leaves', 'all', or 'internal' (default: 'leaves')
    nodes: Override: specific BSPNodes only (default: None)
    shrink: Pixels to shrink from node bounds (default: 0)
    value: Value to add inside regions (default: 1.0)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `add_constant(value: float, *, pos=None, size=None) -> HeightMap`

{% raw %}add_constant(value: float, *, pos=None, size=None) -> HeightMap

Add a constant value to cells in region.

Args:
    value: The value to add to each cell
    pos: Region start (x, y) in destination (default: (0, 0))
    size: Region (width, height) (default: remaining space)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `add_hill(center, radius: float, height: float) -> HeightMap`

{% raw %}add_hill(center, radius: float, height: float) -> HeightMap

Add a smooth hill at the specified position.

Args:
    center: Center position as (x, y) tuple, list, or Vector
    radius: Radius of the hill in cells
    height: Height of the hill peak

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `add_noise(source: NoiseSource, world_origin: tuple = (0.0, 0.0), world_size: tuple = None, mode: str = 'fbm', octaves: int = 4, scale: float = 1.0) -> HeightMap`

{% raw %}add_noise(source: NoiseSource, world_origin: tuple = (0.0, 0.0), world_size: tuple = None, mode: str = 'fbm', octaves: int = 4, scale: float = 1.0) -> HeightMap

Sample noise and add to current values. More efficient than creating intermediate HeightMap.

Args:
    source: 2D NoiseSource to sample from
    world_origin: World coordinates of top-left (default: (0, 0))
    world_size: World area to sample (default: HeightMap size)
    mode: 'flat', 'fbm', or 'turbulence' (default: 'fbm')
    octaves: Octaves for fbm/turbulence (default: 4)
    scale: Multiplier for sampled values (default: 1.0)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `add_voronoi(num_points: int, coefficients: tuple = (1.0, -0.5), seed: int = None) -> HeightMap`

{% raw %}add_voronoi(num_points: int, coefficients: tuple = (1.0, -0.5), seed: int = None) -> HeightMap

Add Voronoi-based terrain features.

Args:
    num_points: Number of Voronoi seed points
    coefficients: Coefficients for distance calculations (default: (1.0, -0.5))
    seed: Random seed (None for random)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `clamp(min: float = 0.0, max: float = 1.0, *, pos=None, size=None) -> HeightMap`

{% raw %}clamp(min: float = 0.0, max: float = 1.0, *, pos=None, size=None) -> HeightMap

Clamp values in region to the specified range.

Args:
    min: Minimum value (default 0.0)
    max: Maximum value (default 1.0)
    pos: Region start (x, y) in destination (default: (0, 0))
    size: Region (width, height) (default: remaining space)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `clear() -> HeightMap`

{% raw %}clear() -> HeightMap

Set all cells to 0.0. Equivalent to fill(0.0).


Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `copy_from(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap`

{% raw %}copy_from(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap

Copy values from another heightmap into the specified region.

Args:
    other: HeightMap to copy from
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `count_in_range(range: tuple[float, float]) -> int`

{% raw %}count_in_range(range: tuple[float, float]) -> int

Count cells with values in the specified range (inclusive).

Args:
    range: Value range as (min, max) tuple or list

Returns:
    int: Number of cells with values in range

Raises:
    ValueError: min > max
{% endraw %}

### `dig_bezier(points: tuple, start_radius: float, end_radius: float, start_height: float, end_height: float) -> HeightMap`

{% raw %}dig_bezier(points: tuple, start_radius: float, end_radius: float, start_height: float, end_height: float) -> HeightMap

Construct a canal along a cubic Bezier curve with specified heights.

Args:
    points: Four control points as ((x0,y0), (x1,y1), (x2,y2), (x3,y3))
    start_radius: Radius at start of path
    end_radius: Radius at end of path
    start_height: Target height at start of path
    end_height: Target height at end of path

Returns:
    HeightMap: self, for method chaining

Note:
    Only lowers cells; cells below target height are unchanged
{% endraw %}

### `dig_hill(center, radius: float, target_height: float) -> HeightMap`

{% raw %}dig_hill(center, radius: float, target_height: float) -> HeightMap

Construct a pit or crater with the specified center height.

Args:
    center: Center position as (x, y) tuple, list, or Vector
    radius: Radius of the crater in cells
    target_height: Height at the center of the pit

Returns:
    HeightMap: self, for method chaining

Note:
    Only lowers cells; cells below target_height are unchanged
{% endraw %}

### `fill(value: float, *, pos=None, size=None) -> HeightMap`

{% raw %}fill(value: float, *, pos=None, size=None) -> HeightMap

Set cells in region to the specified value.

Args:
    value: The value to set
    pos: Region start (x, y) in destination (default: (0, 0))
    size: Region (width, height) to fill (default: remaining space)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `get(x, y) or (pos) -> float`

{% raw %}get(x, y) or (pos) -> float

Get the height value at integer coordinates.

Args:
    x, y: Position as two ints, tuple, list, or Vector

Returns:
    float: Height value at that position

Raises:
    IndexError: Position is out of bounds
{% endraw %}

### `get_interpolated(x, y) or (pos) -> float`

{% raw %}get_interpolated(x, y) or (pos) -> float

Get interpolated height value at non-integer coordinates.

Args:
    x, y: Position as two floats, tuple, list, or Vector

Returns:
    float: Bilinearly interpolated height value
{% endraw %}

### `get_normal(x, y, water_level=0.0) or (pos, water_level=0.0) -> tuple[float, float, float]`

{% raw %}get_normal(x, y, water_level=0.0) or (pos, water_level=0.0) -> tuple[float, float, float]

Get the normal vector at given coordinates for lighting calculations.

Args:
    x, y: Position as two floats, tuple, list, or Vector
    water_level: Water level below which terrain is considered flat (default 0.0)

Returns:
    tuple[float, float, float]: Normal vector (nx, ny, nz)
{% endraw %}

### `get_slope(x, y) or (pos) -> float`

{% raw %}get_slope(x, y) or (pos) -> float

Get the slope at integer coordinates, from 0 (flat) to pi/2 (vertical).

Args:
    x, y: Position as two ints, tuple, list, or Vector

Returns:
    float: Slope angle in radians (0 to pi/2)

Raises:
    IndexError: Position is out of bounds
{% endraw %}

### `inverse() -> HeightMap`

{% raw %}inverse() -> HeightMap

Return NEW HeightMap with (1.0 - value) for each cell.


Returns:
    HeightMap: New inverted HeightMap (original is unchanged)
{% endraw %}

### `lerp(other: HeightMap, t: float, *, pos=None, source_pos=None, size=None) -> HeightMap`

{% raw %}lerp(other: HeightMap, t: float, *, pos=None, source_pos=None, size=None) -> HeightMap

Linear interpolation between this and another heightmap in the specified region.

Args:
    other: HeightMap to interpolate towards
    t: Interpolation factor (0.0 = this, 1.0 = other)
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `max(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap`

{% raw %}max(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap

Set each cell in region to the maximum of this and another heightmap.

Args:
    other: HeightMap to compare with
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `mid_point_displacement(roughness: float = 0.5, seed: int = None) -> HeightMap`

{% raw %}mid_point_displacement(roughness: float = 0.5, seed: int = None) -> HeightMap

Generate terrain using midpoint displacement algorithm (diamond-square).

Args:
    roughness: Controls terrain roughness (0.0-1.0, default 0.5)
    seed: Random seed (None for random)

Returns:
    HeightMap: self, for method chaining

Note:
    Works best with power-of-2+1 dimensions (e.g., 65x65, 129x129)
{% endraw %}

### `min(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap`

{% raw %}min(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap

Set each cell in region to the minimum of this and another heightmap.

Args:
    other: HeightMap to compare with
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `min_max() -> tuple[float, float]`

{% raw %}min_max() -> tuple[float, float]

Get the minimum and maximum height values in the map.


Returns:
    tuple[float, float]: (min_value, max_value)
{% endraw %}

### `multiply(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap`

{% raw %}multiply(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap

Multiply this heightmap by another in the specified region (useful for masking).

Args:
    other: HeightMap to multiply by
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `multiply_bsp(bsp: BSP, *, pos=None, select: str = 'leaves', nodes: list = None, shrink: int = 0, value: float = 1.0) -> HeightMap`

{% raw %}multiply_bsp(bsp: BSP, *, pos=None, select: str = 'leaves', nodes: list = None, shrink: int = 0, value: float = 1.0) -> HeightMap

Multiply by BSP regions. Effectively masks the heightmap to node interiors.

Args:
    bsp: BSP tree to sample from
    pos: Where BSP origin maps to in HeightMap (default: origin-relative like to_heightmap)
    select: 'leaves', 'all', or 'internal' (default: 'leaves')
    nodes: Override: specific BSPNodes only (default: None)
    shrink: Pixels to shrink from node bounds (default: 0)
    value: Value to multiply inside regions (default: 1.0)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `multiply_noise(source: NoiseSource, world_origin: tuple = (0.0, 0.0), world_size: tuple = None, mode: str = 'fbm', octaves: int = 4, scale: float = 1.0) -> HeightMap`

{% raw %}multiply_noise(source: NoiseSource, world_origin: tuple = (0.0, 0.0), world_size: tuple = None, mode: str = 'fbm', octaves: int = 4, scale: float = 1.0) -> HeightMap

Sample noise and multiply with current values. Useful for applying noise-based masks.

Args:
    source: 2D NoiseSource to sample from
    world_origin: World coordinates of top-left (default: (0, 0))
    world_size: World area to sample (default: HeightMap size)
    mode: 'flat', 'fbm', or 'turbulence' (default: 'fbm')
    octaves: Octaves for fbm/turbulence (default: 4)
    scale: Multiplier for sampled values (default: 1.0)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `normalize(min: float = 0.0, max: float = 1.0, *, pos=None, size=None) -> HeightMap`

{% raw %}normalize(min: float = 0.0, max: float = 1.0, *, pos=None, size=None) -> HeightMap

Linearly rescale values in region. Current min becomes new min, current max becomes new max.

Args:
    min: Target minimum value (default 0.0)
    max: Target maximum value (default 1.0)
    pos: Region start (x, y) in destination (default: (0, 0))
    size: Region (width, height) (default: remaining space)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `rain_erosion(drops: int, erosion: float = 0.1, sedimentation: float = 0.05, seed: int = None) -> HeightMap`

{% raw %}rain_erosion(drops: int, erosion: float = 0.1, sedimentation: float = 0.05, seed: int = None) -> HeightMap

Simulate rain erosion on the terrain.

Args:
    drops: Number of rain drops to simulate
    erosion: Erosion coefficient (default 0.1)
    sedimentation: Sedimentation coefficient (default 0.05)
    seed: Random seed (None for random)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `scale(factor: float, *, pos=None, size=None) -> HeightMap`

{% raw %}scale(factor: float, *, pos=None, size=None) -> HeightMap

Multiply cells in region by a factor.

Args:
    factor: The multiplier for each cell
    pos: Region start (x, y) in destination (default: (0, 0))
    size: Region (width, height) (default: remaining space)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `smooth(iterations: int = 1) -> HeightMap`

{% raw %}smooth(iterations: int = 1) -> HeightMap

Smooth the heightmap by averaging neighboring cells.

Args:
    iterations: Number of smoothing passes (default 1)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `sparse_kernel(weights: dict[tuple[int, int], float]) -> HeightMap`

{% raw %}sparse_kernel(weights: dict[tuple[int, int], float]) -> HeightMap

Apply sparse convolution kernel, returning a NEW HeightMap with results.

Args:
    weights: Dict mapping (dx, dy) offsets to weight values

Returns:
    HeightMap: new heightmap with convolution result
{% endraw %}

### `sparse_kernel_from(source: HeightMap, weights: dict[tuple[int, int], float]) -> None`

{% raw %}sparse_kernel_from(source: HeightMap, weights: dict[tuple[int, int], float]) -> None

Apply sparse convolution from source heightmap into self (for reusing destination buffers).

Args:
    source: Source HeightMap to convolve from
    weights: Dict mapping (dx, dy) offsets to weight values

Returns:
    None
{% endraw %}

### `subtract(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap`

{% raw %}subtract(other: HeightMap, *, pos=None, source_pos=None, size=None) -> HeightMap

Subtract another heightmap's values from this one in the specified region.

Args:
    other: HeightMap to subtract values from
    pos: Destination start (x, y) in self (default: (0, 0))
    source_pos: Source start (x, y) in other (default: (0, 0))
    size: Region (width, height) (default: max overlapping area)

Returns:
    HeightMap: self, for method chaining
{% endraw %}

### `threshold(range: tuple[float, float]) -> HeightMap`

{% raw %}threshold(range: tuple[float, float]) -> HeightMap

Return NEW HeightMap with original values where in range, 0.0 elsewhere.

Args:
    range: Value range as (min, max) tuple or list, inclusive

Returns:
    HeightMap: New HeightMap (original is unchanged)

Raises:
    ValueError: min > max
{% endraw %}

### `threshold_binary(range: tuple[float, float], value: float = 1.0) -> HeightMap`

{% raw %}threshold_binary(range: tuple[float, float], value: float = 1.0) -> HeightMap

Return NEW HeightMap with uniform value where in range, 0.0 elsewhere.

Args:
    range: Value range as (min, max) tuple or list, inclusive
    value: Value to set for cells in range (default 1.0)

Returns:
    HeightMap: New HeightMap (original is unchanged)

Raises:
    ValueError: min > max
{% endraw %}
