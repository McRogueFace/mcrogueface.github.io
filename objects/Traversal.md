---
layout: default
title: Traversal
---

# Traversal

BSP traversal order enumeration.

## Overview

Traversal is an IntEnum that specifies the order in which nodes are visited when iterating through a BSP tree. Different traversal orders are useful for different algorithms and use cases.

## Quick Reference

```python
# Iterate BSP nodes in different orders
for node in bsp.traverse(mcrfpy.Traversal.PRE_ORDER):
    print(node.pos)

# Level order (default) - breadth-first
for node in bsp.traverse(mcrfpy.Traversal.LEVEL_ORDER):
    pass

# String shortcuts also work
for node in bsp.traverse('post'):
    pass
```

## Values

| Value | Int | Description |
|-------|-----|-------------|
| `PRE_ORDER` | 0 | Visit node before children (root first) |
| `IN_ORDER` | 1 | Visit left child, then node, then right child |
| `POST_ORDER` | 2 | Visit children before node (leaves first) |
| `LEVEL_ORDER` | 3 | Visit by depth level, top to bottom (breadth-first) |
| `INVERTED_LEVEL_ORDER` | 4 | Visit by depth level, bottom to top |

## String Shortcuts

The `traverse()` method also accepts string shortcuts:

| String | Equivalent |
|--------|------------|
| `'pre'` or `'PRE_ORDER'` | `Traversal.PRE_ORDER` |
| `'in'` or `'IN_ORDER'` | `Traversal.IN_ORDER` |
| `'post'` or `'POST_ORDER'` | `Traversal.POST_ORDER` |
| `'level'` or `'LEVEL_ORDER'` | `Traversal.LEVEL_ORDER` |
| `'level_inverted'` or `'INVERTED_LEVEL_ORDER'` | `Traversal.INVERTED_LEVEL_ORDER` |

## Use Cases

### PRE_ORDER
Process parent before children. Useful for:
- Copying tree structure
- Serializing the tree
- Top-down algorithms

### IN_ORDER
Standard binary tree ordering. For BSP trees:
- Visits nodes in spatial order along the split axis
- Less commonly used for dungeon generation

### POST_ORDER
Process children before parent. Useful for:
- Bottom-up calculations (e.g., computing room sizes)
- Deleting nodes safely
- Combining child results

### LEVEL_ORDER (Default)
Breadth-first traversal. Useful for:
- Processing all rooms at each depth level
- Finding the shallowest node meeting criteria
- Default iteration order for BSP

### INVERTED_LEVEL_ORDER
Deepest nodes first. Useful for:
- Starting from leaf nodes
- Building corridors from small rooms to large areas

## Example: Finding All Leaf Nodes

```python
# Using traverse with POST_ORDER ensures we see leaves before parents
leaves = []
for node in bsp.traverse(mcrfpy.Traversal.POST_ORDER):
    if node.is_leaf:
        leaves.append(node)

# Or simply iterate the BSP directly (uses LEVEL_ORDER for leaves)
leaves = list(bsp)
```

## Example: Building Corridors Bottom-Up

```python
# Process rooms from smallest (deepest) to largest
for node in bsp.traverse(mcrfpy.Traversal.INVERTED_LEVEL_ORDER):
    if not node.is_leaf:
        # Connect the two child regions
        left_center = node.left.center()
        right_center = node.right.center()
        # Draw corridor between centers...
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="BSP" class="object-link">BSP</a>
<a href="HeightMap" class="object-link">HeightMap</a>
<a href="../systems/procgen" class="object-link">Procgen System</a>
</div>
</div>
