---
title: BSP
layout: default
mcrf:
  objects:
    - BSP
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# BSP

{% raw %}BSP(pos: tuple[int, int], size: tuple[int, int])

Binary Space Partitioning tree for procedural dungeon generation.

BSP recursively divides a rectangular region into smaller sub-regions, creating a tree structure perfect for generating dungeon rooms and corridors.

Args:
    pos: (x, y) - Top-left position of the root region.
    size: (w, h) - Width and height of the root region.

Properties:
    pos (tuple[int, int]): Read-only. Top-left position (x, y).
    size (tuple[int, int]): Read-only. Dimensions (width, height).
    bounds ((pos), (size)): Read-only. Combined position and size.
    root (BSPNode): Read-only. Reference to the root node.

Iteration:
    for leaf in bsp:  # Iterates over leaf nodes (rooms)
    len(bsp)          # Returns number of leaf nodes

Example:
    bsp = mcrfpy.BSP(pos=(0, 0), size=(80, 50))
    bsp.split_recursive(depth=4, min_size=(8, 8))
    for leaf in bsp:
        print(f'Room at {leaf.pos}, size {leaf.size}')
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `adjacency` | {% raw %}Leaf adjacency graph. adjacency[i] returns tuple of neighbor indices. Read-only.{% endraw %} |
| `bounds` | {% raw %}Root node bounds as ((x, y), (w, h)). Read-only.{% endraw %} |
| `pos` | {% raw %}Top-left position (x, y). Read-only.{% endraw %} |
| `root` | {% raw %}Reference to the root BSPNode. Read-only.{% endraw %} |
| `size` | {% raw %}Dimensions (width, height). Read-only.{% endraw %} |

## Methods

### `clear() -> BSP`

{% raw %}clear() -> BSP

Remove all children, keeping only the root node with original bounds. WARNING: Invalidates all existing BSPNode references from this tree.


Returns:
    BSP: self, for method chaining
{% endraw %}

### `find(pos: tuple[int, int] | list | Vector) -> BSPNode | None`

{% raw %}find(pos: tuple[int, int] | list | Vector) -> BSPNode | None

Find the smallest (deepest) node containing the position.

Args:
    pos: Position as (x, y) tuple, list, or Vector

Returns:
    BSPNode if found, None if position is outside bounds

Note:
    Also accepts two separate int arguments: find(x, y)
{% endraw %}

### `get_leaf(index: int) -> BSPNode`

{% raw %}get_leaf(index: int) -> BSPNode

Get a leaf node by its index (0 to len(bsp)-1). This is useful when working with adjacency data, which returns leaf indices.

Args:
    index: Leaf index (0 to len(bsp)-1). Negative indices supported.

Returns:
    BSPNode at the specified index

Raises:
    IndexError: If index is out of range
{% endraw %}

### `leaves() -> Iterator[BSPNode]`

{% raw %}leaves() -> Iterator[BSPNode]

Iterate all leaf nodes (the actual rooms). Same as iterating the BSP directly.


Returns:
    Iterator yielding BSPNode objects
{% endraw %}

### `split_once(horizontal: bool, position: int) -> BSP`

{% raw %}split_once(horizontal: bool, position: int) -> BSP

Split the root node once at the specified position. horizontal=True creates a horizontal divider, producing top/bottom rooms. horizontal=False creates a vertical divider, producing left/right rooms.

Args:
    horizontal: True for horizontal divider (top/bottom), False for vertical (left/right)
    position: Split coordinate (y for horizontal, x for vertical)

Returns:
    BSP: self, for method chaining
{% endraw %}

### `split_recursive(depth: int, min_size: tuple[int, int], max_ratio: float = 1.5, seed: int | None = None) -> BSP`

{% raw %}split_recursive(depth: int, min_size: tuple[int, int], max_ratio: float = 1.5, seed: int | None = None) -> BSP

Recursively split to the specified depth. WARNING: Invalidates all existing BSPNode references from this tree.

Args:
    depth: Maximum recursion depth (1-16). Creates up to 2^depth leaves.
    min_size: Minimum (width, height) for a node to be split.
    max_ratio: Maximum aspect ratio before forcing split direction. Default: 1.5.
    seed: Random seed. None for random.

Returns:
    BSP: self, for method chaining
{% endraw %}

### `to_heightmap(size: tuple[int, int] | None = None, select: str = 'leaves', shrink: int = 0, value: float = 1.0) -> HeightMap`

{% raw %}to_heightmap(size: tuple[int, int] | None = None, select: str = 'leaves', shrink: int = 0, value: float = 1.0) -> HeightMap

Convert BSP node selection to a HeightMap.

Args:
    size: Output size (width, height). Default: bounds size.
    select: 'leaves', 'all', or 'internal'. Default: 'leaves'.
    shrink: Pixels to shrink from each node's bounds. Default: 0.
    value: Value inside selected regions. Default: 1.0.

Returns:
    HeightMap with selected regions filled
{% endraw %}

### `traverse(order: Traversal = Traversal.LEVEL_ORDER) -> Iterator[BSPNode]`

{% raw %}traverse(order: Traversal = Traversal.LEVEL_ORDER) -> Iterator[BSPNode]

Iterate all nodes in the specified order.

Args:
    order: Traversal order from Traversal enum. Default: LEVEL_ORDER.

Returns:
    Iterator yielding BSPNode objects

Note:
    Orders: PRE_ORDER, IN_ORDER, POST_ORDER, LEVEL_ORDER, INVERTED_LEVEL_ORDER
{% endraw %}
