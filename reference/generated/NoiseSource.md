---
title: NoiseSource
layout: default
mcrf:
  objects:
    - NoiseSource
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# NoiseSource

{% raw %}NoiseSource(dimensions: int = 2, algorithm: str = 'simplex', hurst: float = 0.5, lacunarity: float = 2.0, seed: int = None)

A configured noise generator for procedural generation.

NoiseSource wraps libtcod's noise generator, providing coherent noise values that can be used for terrain generation, textures, and other procedural content. The same coordinates always produce the same value (deterministic).

Args:
    dimensions: Number of input dimensions (1-4). Default: 2.
    algorithm: Noise algorithm - 'simplex', 'perlin', or 'wavelet'. Default: 'simplex'.
    hurst: Fractal Hurst exponent for fbm/turbulence (0.0-1.0). Default: 0.5.
    lacunarity: Frequency multiplier between octaves. Default: 2.0.
    seed: Random seed for reproducibility. None for random seed.

Properties:
    dimensions (int): Read-only. Number of input dimensions.
    algorithm (str): Read-only. Noise algorithm name.
    hurst (float): Read-only. Hurst exponent.
    lacunarity (float): Read-only. Lacunarity value.
    seed (int): Read-only. Seed used (even if originally None).

Example:
    noise = mcrfpy.NoiseSource(dimensions=2, algorithm='simplex', seed=42)
    value = noise.get((10.5, 20.3))  # Returns -1.0 to 1.0
    fbm_val = noise.fbm((10.5, 20.3), octaves=6)
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `algorithm` | {% raw %}Noise algorithm name ('simplex', 'perlin', or 'wavelet'). Read-only.{% endraw %} |
| `dimensions` | {% raw %}Number of input dimensions (1-4). Read-only.{% endraw %} |
| `hurst` | {% raw %}Hurst exponent for fbm/turbulence. Read-only.{% endraw %} |
| `lacunarity` | {% raw %}Frequency multiplier between octaves. Read-only.{% endraw %} |
| `seed` | {% raw %}Random seed used (even if originally None). Read-only.{% endraw %} |

## Methods

### `fbm(pos: tuple[float, ...], octaves: int = 4) -> float`

{% raw %}fbm(pos: tuple[float, ...], octaves: int = 4) -> float

Get fractal brownian motion value at coordinates.

Args:
    pos: Position tuple with length matching dimensions
    octaves: Number of noise octaves to combine (default: 4)

Returns:
    float: FBM noise value in range [-1.0, 1.0]

Raises:
    ValueError: Position tuple length doesn't match dimensions
{% endraw %}

### `get(pos: tuple[float, ...]) -> float`

{% raw %}get(pos: tuple[float, ...]) -> float

Get flat noise value at coordinates.

Args:
    pos: Position tuple with length matching dimensions

Returns:
    float: Noise value in range [-1.0, 1.0]

Raises:
    ValueError: Position tuple length doesn't match dimensions
{% endraw %}

### `sample(size: tuple[int, int], world_origin: tuple[float, float] = (0.0, 0.0), world_size: tuple[float, float] = None, mode: str = 'fbm', octaves: int = 4) -> HeightMap`

{% raw %}sample(size: tuple[int, int], world_origin: tuple[float, float] = (0.0, 0.0), world_size: tuple[float, float] = None, mode: str = 'fbm', octaves: int = 4) -> HeightMap

Sample noise into a HeightMap for batch processing.

Args:
    size: Output dimensions in cells as (width, height)
    world_origin: World coordinates of top-left corner (default: (0, 0))
    world_size: World area to sample (default: same as size)
    mode: Sampling mode: 'flat', 'fbm', or 'turbulence' (default: 'fbm')
    octaves: Octaves for fbm/turbulence modes (default: 4)

Returns:
    HeightMap: New HeightMap filled with sampled noise values

Note:
    Requires dimensions=2. Values are in range [-1.0, 1.0].
{% endraw %}

### `turbulence(pos: tuple[float, ...], octaves: int = 4) -> float`

{% raw %}turbulence(pos: tuple[float, ...], octaves: int = 4) -> float

Get turbulence (absolute fbm) value at coordinates.

Args:
    pos: Position tuple with length matching dimensions
    octaves: Number of noise octaves to combine (default: 4)

Returns:
    float: Turbulence noise value in range [-1.0, 1.0]

Raises:
    ValueError: Position tuple length doesn't match dimensions
{% endraw %}
