---
layout: default
title: Perlin
---

# Perlin

Perlin noise generation.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

`Perlin` generates Perlin noise - smooth, continuous random values useful for terrain generation, textures, and natural-looking randomness.

## Quick Reference

```python
# Create a noise generator
noise = mcrfpy.Perlin(seed=42)

# Sample noise at a point
value = noise.at(x * 0.1, y * 0.1)  # Returns -1.0 to 1.0

# Use for terrain
for y in range(grid.height):
    for x in range(grid.width):
        height = noise.at(x * 0.1, y * 0.1)
        cell = grid.at(x, y)

        if height < 0:
            cell.tilesprite = WATER
        elif height < 0.5:
            cell.tilesprite = GRASS
        else:
            cell.tilesprite = MOUNTAIN
```

## Constructor

```python
mcrfpy.Perlin(seed: int = None)
```

## Methods

| Method | Description |
|--------|-------------|
| `at(x, y)` | Sample noise at coordinates |

## Tips

- **Scale**: Multiply coordinates by small values (0.01-0.1) for large features, larger values (0.5-1.0) for detail
- **Octaves**: Combine multiple samples at different scales for realistic terrain
- **Seeds**: Same seed produces identical output - useful for reproducible worlds

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="../systems/procgen" class="object-link">Procedural Generation</a>
<a href="../systems/procgen#noise" class="object-link">Noise Subsystem</a>
</div>
</div>
