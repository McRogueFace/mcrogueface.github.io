---
layout: default
title: HeightMap
---

# HeightMap

2D grid of float values for procedural generation.

## Overview

HeightMap is the universal canvas for procedural generation. It stores float values that can be manipulated, combined, and applied to Grid and Layer objects. All terrain generation, noise sampling, and BSP operations produce or consume HeightMaps.

## Quick Reference

```python
# Create a heightmap
hmap = mcrfpy.HeightMap((100, 100))

# Method chaining for terrain generation
hmap.fill(0.5).add_hill((50, 50), 20, 0.3).normalize()

# Subscript access
value = hmap[25, 30]

# Combine multiple heightmaps
noise_map = noise_source.sample((100, 100))
hmap.multiply(noise_map)  # Apply as mask

# Convert BSP to heightmap
rooms = bsp.to_heightmap(select='leaves', shrink=1)
hmap.add(rooms)
```

## Constructor

```python
mcrfpy.HeightMap(size: tuple[int, int], fill: float = 0.0)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `size` | tuple[int, int] | Dimensions (width, height). Immutable after creation. |
| `fill` | float | Initial value for all cells. Default: 0.0 |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `size` | tuple[int, int] | Dimensions (width, height). Read-only. |

## Query Methods

| Method | Description |
|--------|-------------|
| `get(x, y)` | Get height value at integer coordinates |
| `get_interpolated(x, y)` | Get bilinearly interpolated value at float coordinates |
| `get_slope(x, y)` | Get slope angle (0 to pi/2) at coordinates |
| `get_normal(x, y, water_level=0.0)` | Get normal vector (nx, ny, nz) for lighting |
| `min_max()` | Returns (min_value, max_value) tuple |
| `count_in_range((min, max))` | Count cells with values in range |

## Scalar Operations

All scalar operations support optional region parameters and return self for chaining.

| Method | Description |
|--------|-------------|
| `fill(value, *, pos=None, size=None)` | Set cells to specified value |
| `clear()` | Set all cells to 0.0 |
| `add_constant(value, *, pos=None, size=None)` | Add constant to each cell |
| `scale(factor, *, pos=None, size=None)` | Multiply each cell by factor |
| `clamp(min=0.0, max=1.0, *, pos=None, size=None)` | Clamp values to range |
| `normalize(min=0.0, max=1.0, *, pos=None, size=None)` | Rescale values to target range |

## Combination Operations

Combine two heightmaps with optional region parameters. All return self for chaining.

| Method | Description |
|--------|-------------|
| `add(other, *, pos=None, source_pos=None, size=None)` | Add other's values |
| `subtract(other, *, pos=None, source_pos=None, size=None)` | Subtract other's values |
| `multiply(other, *, pos=None, source_pos=None, size=None)` | Multiply by other (masking) |
| `lerp(other, t, *, pos=None, source_pos=None, size=None)` | Linear interpolation |
| `copy_from(other, *, pos=None, source_pos=None, size=None)` | Copy values from other |
| `max(other, *, pos=None, source_pos=None, size=None)` | Take maximum of each cell |
| `min(other, *, pos=None, source_pos=None, size=None)` | Take minimum of each cell |

## Threshold Operations

These return NEW HeightMap objects (original unchanged).

| Method | Description |
|--------|-------------|
| `threshold((min, max))` | Original values where in range, 0.0 elsewhere |
| `threshold_binary((min, max), value=1.0)` | Uniform value where in range, 0.0 elsewhere |
| `inverse()` | Returns (1.0 - value) for each cell |

## Terrain Generation

Methods that add procedural terrain features. All return self for chaining.

| Method | Description |
|--------|-------------|
| `add_hill(center, radius, height)` | Add smooth hill at position |
| `dig_hill(center, radius, target_height)` | Dig pit/crater (only lowers cells) |
| `add_voronoi(num_points, coefficients=(1.0, -0.5), seed=None)` | Add Voronoi terrain |
| `mid_point_displacement(roughness=0.5, seed=None)` | Diamond-square terrain |
| `rain_erosion(drops, erosion=0.1, sedimentation=0.05, seed=None)` | Simulate erosion |
| `dig_bezier(points, start_radius, end_radius, start_height, end_height)` | Dig canal along Bezier curve |
| `smooth(iterations=1)` | Average neighboring cells |
| `kernel_transform(weights, *, min=0.0, max=1e6)` | Apply convolution kernel |

## Direct Source Sampling

Sample from NoiseSource or BSP directly without intermediate HeightMaps.

| Method | Description |
|--------|-------------|
| `add_noise(source, world_origin=(0,0), world_size=None, mode='fbm', octaves=4, scale=1.0)` | Add sampled noise |
| `multiply_noise(source, world_origin=(0,0), world_size=None, mode='fbm', octaves=4, scale=1.0)` | Multiply by sampled noise |
| `add_bsp(bsp, *, pos=None, select='leaves', nodes=None, shrink=0, value=1.0)` | Add BSP regions |
| `multiply_bsp(bsp, *, pos=None, select='leaves', nodes=None, shrink=0, value=1.0)` | Multiply by BSP regions |

## Subscript Access

```python
# Get value at coordinates
value = hmap[x, y]

# Equivalent to get()
value = hmap.get(x, y)
```

## Region Parameters

Many methods accept region parameters for operating on subsets:

```python
# pos: destination start (x, y)
# source_pos: source start (x, y) for binary operations
# size: region dimensions (width, height)

# Fill a 10x10 region starting at (5, 5)
hmap.fill(1.0, pos=(5, 5), size=(10, 10))

# Copy from source region to destination region
hmap.copy_from(other, pos=(10, 10), source_pos=(0, 0), size=(20, 20))
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="BSP" class="object-link">BSP</a>
<a href="NoiseSource" class="object-link">NoiseSource</a>
<a href="Grid" class="object-link">Grid</a>
<a href="../systems/procgen" class="object-link">Procgen System</a>
</div>
</div>
