---
title: Vector
layout: default
mcrf:
  objects:
    - Vector
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Vector

{% raw %}Vector(x: float = 0, y: float = 0)

2D vector for positions, sizes, and directions.

Args:
    x: X component.
    y: Y component.

Supports arithmetic (+, -, *, /), abs(), len() == 2,
indexing ([0] for x, [1] for y), hashing, and equality.

Properties:
    x (float): X component.
    y (float): Y component.
    int (tuple[int, int], read-only): Integer floor of (x, y).

Note:
    Vector is a VALUE TYPE (frozen 1.0 contract): properties that return a
    Vector return a fresh COPY, so mutating a component of the returned object
    is a silent no-op on the original. Use read-modify-writeback
    (v = obj.pos; v.x = 5; obj.pos = v) or whole-value assignment
    (obj.pos = mcrfpy.Vector(5, 0)).
    See also: API stability policy (docs/api-stability.md)
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `int` | {% raw %}Integer tuple (floor of x and y) for use as dict keys. Read-only.{% endraw %} |
| `x` | {% raw %}X coordinate of the vector (float){% endraw %} |
| `y` | {% raw %}Y coordinate of the vector (float){% endraw %} |

## Methods

### `angle() -> float`

{% raw %}angle() -> float

Get the angle of this vector in radians.


Returns:
    float: Angle in radians from positive x-axis
{% endraw %}

### `copy() -> Vector`

{% raw %}copy() -> Vector

Create a copy of this vector.


Returns:
    Vector: New Vector object with same x and y values
{% endraw %}

### `distance_to(other: Vector) -> float`

{% raw %}distance_to(other: Vector) -> float

Calculate the distance to another vector.

Args:
    other: The other vector

Returns:
    float: Distance between the two vectors
{% endraw %}

### `dot(other: Vector) -> float`

{% raw %}dot(other: Vector) -> float

Calculate the dot product with another vector.

Args:
    other: The other vector

Returns:
    float: Dot product of the two vectors
{% endraw %}

### `floor() -> Vector`

{% raw %}floor() -> Vector

Return a new vector with floored (integer) coordinates.


Returns:
    Vector: New Vector with floor(x) and floor(y)

Note:
    Useful for grid-based positioning. For a hashable tuple, use the .int property instead.
{% endraw %}

### `magnitude() -> float`

{% raw %}magnitude() -> float

Calculate the length/magnitude of this vector.


Returns:
    float: The magnitude of the vector
{% endraw %}

### `magnitude_squared() -> float`

{% raw %}magnitude_squared() -> float

Calculate the squared magnitude of this vector.


Returns:
    float: The squared magnitude (faster than magnitude())

Note:
    Use this for comparisons to avoid expensive square root calculation.
{% endraw %}

### `normalize() -> Vector`

{% raw %}normalize() -> Vector

Return a unit vector in the same direction.


Returns:
    Vector: New normalized vector with magnitude 1.0

Note:
    For zero vectors (magnitude 0.0), returns a zero vector rather than raising an exception
{% endraw %}
