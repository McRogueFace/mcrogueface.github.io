---
layout: default
title: Procedural Generation
---

# Procedural Generation

The Procedural Generation System provides tools for creating randomized content - dungeons, terrain, and other game environments. It includes heightmaps for terrain generation, BSP for room-based dungeons, and noise functions for natural patterns.

## Overview

McRogueFace's procgen tools work together:

1. **Noise** generates natural-looking random values
2. **HeightMaps** store and manipulate 2D value grids
3. **BSP** partitions space for room-based layouts

```python
# Generate a noise-based terrain
noise = mcrfpy.Perlin(seed=42)
heightmap = mcrfpy.HeightMap(width=80, height=45)
heightmap.fill_noise(noise, scale=0.1)
```

## Objects

| Object | Purpose |
|--------|---------|
| [Perlin](../objects/Perlin) | Perlin noise generation |

---

## Noise Subsystem {#noise}

Noise functions generate pseudo-random values that vary smoothly across space, perfect for natural-looking terrain and textures.

### Perlin Noise

[Perlin noise](../objects/Perlin) produces smooth, continuous random values:

```python
noise = mcrfpy.Perlin(seed=42)

# Sample at any point
value = noise.at(x * 0.1, y * 0.1)  # Returns -1.0 to 1.0
```

### Scale and Octaves

The sampling scale controls feature size:

```python
# Large features (continents)
large = noise.at(x * 0.01, y * 0.01)

# Small features (rocks)
small = noise.at(x * 0.5, y * 0.5)

# Combine for detail at multiple scales
combined = large * 0.6 + small * 0.4
```

### Noise to Tiles

Convert noise values to tile types:

```python
for y in range(grid.height):
    for x in range(grid.width):
        value = noise.at(x * 0.1, y * 0.1)
        cell = grid.at(x, y)

        if value < -0.2:
            cell.tilesprite = WATER
            cell.walkable = False
        elif value < 0.3:
            cell.tilesprite = GRASS
            cell.walkable = True
        else:
            cell.tilesprite = MOUNTAIN
            cell.walkable = False
```

---

## HeightMap Subsystem {#heightmap}

HeightMaps are 2D arrays of float values, useful for terrain generation and cellular automata.

### Creating HeightMaps

```python
heightmap = mcrfpy.HeightMap(width=80, height=45)

# Fill with noise
heightmap.fill_noise(noise, scale=0.1)

# Or fill with a constant
heightmap.fill(0.5)
```

### Operators

HeightMaps support mathematical operations:

```python
# Unary operations
heightmap.normalize()      # Scale to 0.0-1.0
heightmap.invert()         # Flip values
heightmap.clamp(0.0, 1.0)  # Limit range

# Binary operations
combined = heightmap1.add(heightmap2)
combined = heightmap1.multiply(heightmap2)
```

### Kernel Operations

Apply convolution kernels for effects like blur and edge detection:

```python
# Smooth the heightmap
blur_kernel = [
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
]
heightmap.apply_kernel(blur_kernel, normalize=True)
```

### Cellular Automata

Use heightmaps for cellular automata cave generation:

```python
# Initialize with random values
import random
for y in range(height):
    for x in range(width):
        heightmap.set(x, y, 1.0 if random.random() < 0.45 else 0.0)

# Apply cellular automata rules
for _ in range(5):
    new_map = mcrfpy.HeightMap(width, height)
    for y in range(height):
        for x in range(width):
            neighbors = count_neighbors(heightmap, x, y)
            if neighbors >= 5:
                new_map.set(x, y, 1.0)
            else:
                new_map.set(x, y, 0.0)
    heightmap = new_map
```

---

## BSP Subsystem {#bsp}

Binary Space Partitioning creates room-based dungeon layouts by recursively dividing space.

### BSP Algorithm Overview

1. Start with the full map area
2. Recursively split into smaller areas
3. Place rooms within leaf nodes
4. Connect rooms with corridors

### Basic BSP Generation

```python
def generate_bsp_dungeon(width, height, min_room=6):
    # Create BSP tree
    bsp = mcrfpy.BSP(0, 0, width, height)
    bsp.split_recursive(
        depth=4,
        min_width=min_room + 2,
        min_height=min_room + 2
    )

    rooms = []

    # Create rooms in leaf nodes
    for node in bsp.leaves():
        # Leave space for walls
        room_x = node.x + 1
        room_y = node.y + 1
        room_w = node.width - 2
        room_h = node.height - 2

        rooms.append((room_x, room_y, room_w, room_h))

    return rooms
```

### BSP to HeightMap

Convert BSP results to a heightmap for further processing:

```python
heightmap = mcrfpy.HeightMap(width, height)
heightmap.fill(0.0)  # Start with walls

for room_x, room_y, room_w, room_h in rooms:
    for y in range(room_y, room_y + room_h):
        for x in range(room_x, room_x + room_w):
            heightmap.set(x, y, 1.0)  # Floor
```

### Connecting Rooms

Connect adjacent BSP nodes with corridors:

```python
def connect_rooms(heightmap, room1, room2):
    # Get room centers
    x1 = room1[0] + room1[2] // 2
    y1 = room1[1] + room1[3] // 2
    x2 = room2[0] + room2[2] // 2
    y2 = room2[1] + room2[3] // 2

    # L-shaped corridor
    for x in range(min(x1, x2), max(x1, x2) + 1):
        heightmap.set(x, y1, 1.0)
    for y in range(min(y1, y2), max(y1, y2) + 1):
        heightmap.set(x2, y, 1.0)
```

---

## Combining Techniques {#combining}

Real dungeon generation often combines multiple techniques:

```python
def generate_dungeon(grid):
    # 1. BSP for room layout
    rooms = generate_bsp_dungeon(grid.width, grid.height)

    # 2. Apply rooms to grid
    for x, y, w, h in rooms:
        for ry in range(y, y + h):
            for rx in range(x, x + w):
                cell = grid.at(rx, ry)
                cell.tilesprite = FLOOR
                cell.walkable = True

    # 3. Connect rooms
    for i in range(len(rooms) - 1):
        connect_rooms_on_grid(grid, rooms[i], rooms[i+1])

    # 4. Add noise-based decorations
    noise = mcrfpy.Perlin(seed=random.randint(0, 99999))
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.at(x, y)
            if cell.walkable and noise.at(x * 0.3, y * 0.3) > 0.5:
                cell.tilesprite = DECORATED_FLOOR
```

---

## Related Objects

<div class="related-objects">
<div class="object-links">
<a href="../objects/Perlin" class="object-link">Perlin</a>
<a href="../objects/Grid" class="object-link">Grid</a>
</div>
</div>
