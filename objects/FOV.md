---
layout: default
title: FOV
---

# FOV

Field of view algorithm enumeration.

## Overview

`FOV` is an IntEnum that specifies which algorithm to use when computing field of view on a Grid. Different algorithms offer trade-offs between performance, accuracy, and visual characteristics. The algorithms are provided by libtcod.

## Quick Reference

```python
# Set FOV algorithm on grid
grid.fov = mcrfpy.FOV.FOV_SHADOW

# Compute FOV from position
grid.compute_fov(player.x, player.y, radius=8)

# Check visibility
if grid.is_in_fov(target_x, target_y):
    print("Target is visible!")

# Available algorithms
mcrfpy.FOV.FOV_BASIC
mcrfpy.FOV.FOV_DIAMOND
mcrfpy.FOV.FOV_SHADOW
mcrfpy.FOV.FOV_PERMISSIVE_0  # through FOV_PERMISSIVE_8
```

## Constructor

`FOV` is an IntEnum and its values are accessed as class attributes.

```python
algorithm = mcrfpy.FOV.FOV_SHADOW
```

## Values

| Value | Description |
|-------|-------------|
| `FOV_BASIC` | Basic raycasting algorithm. Fast but can miss corners. |
| `FOV_DIAMOND` | Diamond-shaped FOV. Symmetric and predictable. |
| `FOV_SHADOW` | Shadow casting algorithm. Most commonly used, good balance. |
| `FOV_PERMISSIVE_0` | Permissive FOV, strictest. Narrowest field of view. |
| `FOV_PERMISSIVE_1` | Permissive FOV level 1 |
| `FOV_PERMISSIVE_2` | Permissive FOV level 2 |
| `FOV_PERMISSIVE_3` | Permissive FOV level 3 |
| `FOV_PERMISSIVE_4` | Permissive FOV level 4 (middle) |
| `FOV_PERMISSIVE_5` | Permissive FOV level 5 |
| `FOV_PERMISSIVE_6` | Permissive FOV level 6 |
| `FOV_PERMISSIVE_7` | Permissive FOV level 7 |
| `FOV_PERMISSIVE_8` | Permissive FOV, most permissive. Widest field of view. |

## Algorithm Comparison

### FOV_BASIC
Simple raycasting from the viewer to each cell. Fast computation but can produce asymmetric results where the player can see a cell but an enemy at that cell cannot see the player.

### FOV_DIAMOND
Creates a diamond-shaped visible area. Produces symmetric results and is easy to understand, but may not look as natural as shadow casting.

### FOV_SHADOW (Recommended)
The most popular algorithm for roguelikes. Casts shadows from obstacles to determine visibility. Produces natural-looking results with good performance. This is the default choice for most games.

### FOV_PERMISSIVE_0 through FOV_PERMISSIVE_8
A family of algorithms that vary in how "permissive" they are about visibility around corners. Lower numbers (0-3) are stricter and show less around corners. Higher numbers (5-8) are more permissive and reveal more. Level 4 is the middle ground.

## Usage Patterns

### Basic FOV Setup

```python
# Create grid and set algorithm
grid = mcrfpy.Grid(grid_size=(80, 45), texture=texture)
grid.fov = mcrfpy.FOV.FOV_SHADOW
grid.fov_radius = 10

# Compute FOV from player position
grid.compute_fov(player.x, player.y)

# Use in visibility checks
for enemy in enemies:
    if grid.is_in_fov(enemy.x, enemy.y):
        enemy.visible = True
```

### FOV with Color Layer

```python
fog = grid.add_layer('color', z_index=10)
fog.fill(mcrfpy.Color(0, 0, 0, 255))  # Start dark

def update_visibility():
    grid.compute_fov(player.x, player.y, radius=8)
    fog.draw_fov(grid)  # Reveal visible cells
```

### Algorithm Selection

```python
# For classic roguelike feel
grid.fov = mcrfpy.FOV.FOV_SHADOW

# For tactical games where seeing around corners matters
grid.fov = mcrfpy.FOV.FOV_PERMISSIVE_6

# For symmetric stealth games
grid.fov = mcrfpy.FOV.FOV_DIAMOND

# For fast computation in large maps
grid.fov = mcrfpy.FOV.FOV_BASIC
```

### Dynamic Algorithm Switching

```python
# Different FOV for different game modes
def set_stealth_mode():
    grid.fov = mcrfpy.FOV.FOV_PERMISSIVE_2  # Limited vision
    grid.fov_radius = 5

def set_alert_mode():
    grid.fov = mcrfpy.FOV.FOV_SHADOW
    grid.fov_radius = 12
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Grid" class="object-link">Grid</a>
<a href="Entity" class="object-link">Entity</a>
<a href="GridPoint" class="object-link">GridPoint</a>
<a href="ColorLayer" class="object-link">ColorLayer</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
