---
layout: default
title: NoiseSource
---

# NoiseSource

Configured noise generator for procedural generation.

## Overview

NoiseSource wraps libtcod's noise generator, providing coherent noise values for terrain generation, textures, and other procedural content. The same coordinates always produce the same value (deterministic), making it ideal for reproducible world generation.

## Quick Reference

```python
# Create a noise source
noise = mcrfpy.NoiseSource(dimensions=2, algorithm='simplex', seed=42)

# Point queries
value = noise.get((10.5, 20.3))           # Basic noise: -1.0 to 1.0
fbm_val = noise.fbm((10.5, 20.3), octaves=6)  # Fractal brownian motion
turb_val = noise.turbulence((x, y))       # Turbulence (absolute fbm)

# Batch sampling into HeightMap
hmap = noise.sample((100, 100), mode='fbm', octaves=4)

# Direct heightmap integration
hmap.add_noise(noise, scale=0.5)
```

## Constructor

```python
mcrfpy.NoiseSource(
    dimensions: int = 2,
    algorithm: str = 'simplex',
    hurst: float = 0.5,
    lacunarity: float = 2.0,
    seed: int = None
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `dimensions` | int | Number of input dimensions (1-4). Default: 2 |
| `algorithm` | str | Noise algorithm: 'simplex', 'perlin', or 'wavelet'. Default: 'simplex' |
| `hurst` | float | Fractal Hurst exponent for fbm/turbulence (0.0-1.0). Default: 0.5 |
| `lacunarity` | float | Frequency multiplier between octaves. Default: 2.0 |
| `seed` | int | Random seed for reproducibility. None for random seed. |

## Properties

All properties are read-only.

| Property | Type | Description |
|----------|------|-------------|
| `dimensions` | int | Number of input dimensions |
| `algorithm` | str | Noise algorithm name ('simplex', 'perlin', or 'wavelet') |
| `hurst` | float | Hurst exponent |
| `lacunarity` | float | Lacunarity value |
| `seed` | int | Seed used (even if originally None) |

## Methods

### Point Query Methods

| Method | Description |
|--------|-------------|
| `get(pos)` | Get flat noise value at coordinates. Returns -1.0 to 1.0. |
| `fbm(pos, octaves=4)` | Get fractal brownian motion value. Returns -1.0 to 1.0. |
| `turbulence(pos, octaves=4)` | Get turbulence (absolute fbm) value. Returns -1.0 to 1.0. |

### Batch Sampling

```python
sample(
    size: tuple[int, int],
    world_origin: tuple[float, float] = (0.0, 0.0),
    world_size: tuple[float, float] = None,
    mode: str = 'fbm',
    octaves: int = 4
) -> HeightMap
```

Sample noise into a HeightMap for efficient batch processing.

| Parameter | Type | Description |
|-----------|------|-------------|
| `size` | tuple[int, int] | Output dimensions in cells (width, height) |
| `world_origin` | tuple[float, float] | World coordinates of top-left corner |
| `world_size` | tuple[float, float] | World area to sample. Default: same as size |
| `mode` | str | 'flat', 'fbm', or 'turbulence' |
| `octaves` | int | Octaves for fbm/turbulence modes |

Returns a new HeightMap filled with sampled noise values in range [-1.0, 1.0].

## Noise Algorithms

### Simplex (Default)
- Faster than Perlin, especially in higher dimensions
- Fewer directional artifacts
- Recommended for most use cases

### Perlin
- Classic noise algorithm
- Well-understood characteristics
- Good for compatibility with existing algorithms

### Wavelet
- Band-limited noise
- Less aliasing at different scales
- Good for detailed textures

## Fractal Parameters

### Hurst Exponent (hurst)
Controls how quickly amplitude decreases with each octave:
- `0.0`: Each octave has equal weight (rough, detailed)
- `0.5`: Default, natural-looking balance
- `1.0`: Higher octaves dominate (smoother)

### Lacunarity
Frequency multiplier between octaves:
- `2.0`: Default, each octave is twice the frequency
- Higher values create more contrast between scales
- Lower values create smoother transitions

## Example: Terrain Generation

```python
# Create terrain with multiple noise layers
base_noise = mcrfpy.NoiseSource(seed=12345)
detail_noise = mcrfpy.NoiseSource(seed=67890, lacunarity=3.0)

# Start with base terrain
terrain = base_noise.sample((100, 100),
    world_size=(10.0, 10.0),  # Larger scale features
    mode='fbm',
    octaves=4
)

# Normalize to 0-1 range
terrain.add_constant(1.0).scale(0.5)

# Add detail layer
terrain.add_noise(detail_noise,
    world_size=(50.0, 50.0),  # Finer detail
    scale=0.2
)

# Apply erosion and smoothing
terrain.rain_erosion(1000).smooth(2)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="HeightMap" class="object-link">HeightMap</a>
<a href="BSP" class="object-link">BSP</a>
<a href="Grid" class="object-link">Grid</a>
<a href="../systems/procgen" class="object-link">Procgen System</a>
</div>
</div>
