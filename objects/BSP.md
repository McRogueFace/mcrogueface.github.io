---
layout: default
title: BSP
---

# BSP

Binary Space Partitioning tree for procedural dungeon generation.

## Overview

BSP recursively divides a rectangular region into smaller sub-regions, creating a tree structure perfect for generating dungeon rooms and corridors. Each leaf node represents a potential room, while the tree structure provides natural relationships for connecting them.

## Quick Reference

```python
# Create a BSP tree covering a dungeon area
bsp = mcrfpy.BSP(pos=(0, 0), size=(80, 50))

# Split recursively into rooms
bsp.split_recursive(depth=4, min_size=(8, 8))

# Iterate over leaf nodes (rooms)
for leaf in bsp:
    print(f"Room at {leaf.pos}, size {leaf.size}")
    # Create room in your grid...

# Use adjacency graph for corridor placement
for i, neighbors in enumerate(bsp.adjacency):
    leaf = bsp.get_leaf(i)
    for neighbor_idx in neighbors:
        # leaf and bsp.get_leaf(neighbor_idx) share a wall
        tiles = leaf.adjacent_tiles[neighbor_idx]
        # tiles contains Vector coordinates for corridor placement
```

## Constructor

```python
mcrfpy.BSP(pos: tuple[int, int], size: tuple[int, int])
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `pos` | tuple[int, int] | Top-left position (x, y) of the root region |
| `size` | tuple[int, int] | Width and height of the root region |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `pos` | tuple[int, int] | Top-left position (x, y). Read-only. |
| `size` | tuple[int, int] | Dimensions (width, height). Read-only. |
| `bounds` | tuple | Combined position and size as ((x, y), (w, h)). Read-only. |
| `root` | BSPNode | Reference to the root node. Read-only. |
| `adjacency` | BSPAdjacency | Leaf adjacency graph. `adjacency[i]` returns tuple of neighbor indices. Read-only. |

## Methods

| Method | Description |
|--------|-------------|
| `split_recursive(depth, min_size, max_ratio=1.5, seed=None)` | Recursively split to specified depth. Returns self. |
| `split_once(horizontal, position)` | Split root node once at specified position. Returns self. |
| `clear()` | Remove all children, keeping only root with original bounds. Returns self. |
| `leaves()` | Iterate all leaf nodes (rooms). Same as iterating BSP directly. |
| `traverse(order=Traversal.LEVEL_ORDER)` | Iterate all nodes in specified order. |
| `find(pos)` | Find smallest node containing position. Returns BSPNode or None. |
| `get_leaf(index)` | Get leaf node by index (0 to len(bsp)-1). |
| `to_heightmap(size=None, select='leaves', shrink=0, value=1.0)` | Convert to HeightMap with selected regions filled. |

## BSPNode

BSPNode provides read-only access to individual nodes in the tree.

### BSPNode Properties

| Property | Type | Description |
|----------|------|-------------|
| `pos` | tuple[int, int] | Top-left position (x, y) |
| `size` | tuple[int, int] | Dimensions (width, height) |
| `bounds` | tuple | Combined position and size |
| `level` | int | Depth in tree (0 for root) |
| `is_leaf` | bool | True if this node has no children |
| `split_horizontal` | bool or None | Split orientation, None if leaf |
| `split_position` | int or None | Split coordinate, None if leaf |
| `left` | BSPNode or None | Left child, or None if leaf |
| `right` | BSPNode or None | Right child, or None if leaf |
| `parent` | BSPNode or None | Parent node, or None if root |
| `sibling` | BSPNode or None | Other child of parent, or None |
| `leaf_index` | int or None | Index in adjacency graph, None if not a leaf |
| `adjacent_tiles` | BSPAdjacentTiles | Mapping of neighbor_index to wall tile coordinates |

### BSPNode Methods

| Method | Description |
|--------|-------------|
| `contains(pos)` | Check if position is inside this node's bounds |
| `center()` | Return the center point of this node's bounds |

## Iteration and Sequence Protocol

```python
# len() returns number of leaf nodes
num_rooms = len(bsp)

# Iterate directly over leaves
for leaf in bsp:
    pass

# Or use leaves() explicitly
for leaf in bsp.leaves():
    pass

# Traverse all nodes (including internal)
for node in bsp.traverse(mcrfpy.Traversal.PRE_ORDER):
    if node.is_leaf:
        print("Leaf:", node.pos)
    else:
        print("Split at:", node.split_position)
```

## Adjacency System

The adjacency system helps connect rooms with corridors:

```python
# Get all neighbor relationships
for i, neighbors in enumerate(bsp.adjacency):
    print(f"Leaf {i} is adjacent to: {neighbors}")

# Get wall tiles between adjacent leaves
leaf = bsp.get_leaf(0)
for neighbor_idx in leaf.adjacent_tiles.keys():
    tiles = leaf.adjacent_tiles[neighbor_idx]
    # tiles is a tuple of Vector objects representing
    # coordinates on THIS leaf's edge that border the neighbor
    for tile in tiles:
        print(f"Wall tile at ({tile.x}, {tile.y})")
```

## Important Notes

- BSPNode references become invalid after `clear()` or `split_recursive()`. Re-fetch nodes from the BSP object after these operations.
- The adjacency graph is computed lazily and cached. It's automatically invalidated when the tree structure changes.
- Maximum recursion depth is 16 to prevent memory exhaustion.

## Related

<div class="related-objects">
<div class="object-links">
<a href="HeightMap" class="object-link">HeightMap</a>
<a href="Grid" class="object-link">Grid</a>
<a href="Traversal" class="object-link">Traversal</a>
<a href="../systems/procgen" class="object-link">Procgen System</a>
</div>
</div>
