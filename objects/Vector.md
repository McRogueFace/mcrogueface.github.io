---
layout: default
title: Vector
---

# Vector

SFML Vector object for 2D coordinates.

## Overview

The `Vector` class represents 2D coordinates and provides mathematical operations for working with positions, directions, and velocities. Vectors are used throughout McRogueFace for positioning and movement.

## Quick Reference

```python
# Create vectors
pos = mcrfpy.Vector(100, 200)
direction = mcrfpy.Vector(1, 0)  # Unit vector pointing right

# Arithmetic operations
new_pos = pos + direction * 50
offset = mcrfpy.Vector(10, 10)
pos += offset

# Distance and magnitude
dist = pos.distance_to(other_pos)
length = direction.magnitude()
unit = direction.normalize()

# Use as dict key
positions = {}
positions[pos.int] = "player"
```

## Constructor

```python
mcrfpy.Vector(x: float = 0, y: float = 0)
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `x` | float | 0 | X coordinate |
| `y` | float | 0 | Y coordinate |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `x` | float | X coordinate |
| `y` | float | Y coordinate |
| `int` | tuple | Floor as (int, int) tuple (read-only, for dict keys) |

## Methods

| Method | Description |
|--------|-------------|
| `magnitude()` | Get vector length |
| `magnitude_squared()` | Get squared length (faster, for comparisons) |
| `normalize()` | Return unit vector (length 1) |
| `dot(other)` | Dot product with another vector |
| `distance_to(other)` | Distance to another vector |
| `angle()` | Angle in radians from positive X axis |
| `floor()` | Return new Vector with floored components |
| `copy()` | Return a copy of this vector |

## Arithmetic Operations

Vectors support standard arithmetic:

```python
a = mcrfpy.Vector(10, 20)
b = mcrfpy.Vector(5, 10)

# Addition and subtraction
c = a + b  # Vector(15, 30)
d = a - b  # Vector(5, 10)

# Scalar multiplication and division
e = a * 2  # Vector(20, 40)
f = a / 2  # Vector(5, 10)

# In-place operations
a += b
a -= b
a *= 2
a /= 2

# Comparison
if a == b:
    print("Same position")
if a != b:
    print("Different positions")
```

## Common Patterns

### Movement

```python
# Move entity by velocity
entity_pos = mcrfpy.Vector(100, 100)
velocity = mcrfpy.Vector(5, 0)
entity_pos += velocity

# Move toward target
def move_toward(current, target, speed):
    direction = target - current
    if direction.magnitude() < speed:
        return target.copy()
    return current + direction.normalize() * speed
```

### Distance Checks

```python
# Check if in range (use magnitude_squared for performance)
def in_range(a, b, max_dist):
    diff = b - a
    return diff.magnitude_squared() <= max_dist * max_dist

# Get distance
dist = pos_a.distance_to(pos_b)
```

### Using as Dictionary Keys

```python
# The 'int' property provides a hashable tuple
tile_data = {}
pos = mcrfpy.Vector(10.5, 20.7)
tile_data[pos.int] = "wall"  # Key is (10, 20)

# Look up
key = mcrfpy.Vector(10.3, 20.9).int  # Also (10, 20)
print(tile_data[key])  # "wall"
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Frame" class="object-link">Frame</a>
<a href="Entity" class="object-link">Entity</a>
<a href="Sprite" class="object-link">Sprite</a>
</div>
</div>
