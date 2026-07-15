---
layout: default
title: FOV
mcrf:
  objects: [FOV, Grid]
  diataxis: reference
  disposition: needs-review
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# FOV

Field of view algorithm enumeration.

## Overview

`FOV` is an IntEnum that specifies which algorithm to use when computing field of view on a Grid. Different algorithms offer trade-offs between performance, accuracy, and visual characteristics. The algorithms are provided by libtcod.

## Quick Reference

```python
# Set FOV algorithm on grid
grid.fov = mcrfpy.FOV.SHADOW

# Compute FOV from a tile position (accepts a tuple or Vector)
grid.compute_fov(player.grid_pos, radius=8)

# Check visibility
if grid.is_in_fov(target_x, target_y):
    print("Target is visible!")

# Available algorithms
mcrfpy.FOV.BASIC
mcrfpy.FOV.DIAMOND
mcrfpy.FOV.SHADOW
mcrfpy.FOV.PERMISSIVE_0  # through PERMISSIVE_8
mcrfpy.FOV.RESTRICTIVE
mcrfpy.FOV.SYMMETRIC_SHADOWCAST
```

## Constructor

`FOV` is an IntEnum and its values are accessed as class attributes.

```python
algorithm = mcrfpy.FOV.SHADOW
```

## Values

| Value | Description |
|-------|-------------|
| `BASIC` | Basic raycasting algorithm. Fast but can miss corners. |
| `DIAMOND` | Diamond-shaped FOV. Symmetric and predictable. |
| `SHADOW` | Shadow casting algorithm. Most commonly used, good balance. |
| `PERMISSIVE_0` | Permissive FOV, strictest. Narrowest field of view. |
| `PERMISSIVE_1` | Permissive FOV level 1 |
| `PERMISSIVE_2` | Permissive FOV level 2 |
| `PERMISSIVE_3` | Permissive FOV level 3 |
| `PERMISSIVE_4` | Permissive FOV level 4 (middle) |
| `PERMISSIVE_5` | Permissive FOV level 5 |
| `PERMISSIVE_6` | Permissive FOV level 6 |
| `PERMISSIVE_7` | Permissive FOV level 7 |
| `PERMISSIVE_8` | Permissive FOV, most permissive. Widest field of view. |
| `RESTRICTIVE` | Restrictive precise permissive FOV. |
| `SYMMETRIC_SHADOWCAST` | Symmetric shadowcasting algorithm. |

Note: the enum members are `BASIC`, `DIAMOND`, `SHADOW`, etc. — not `FOV_BASIC` and friends (that naming is the underlying libtcod C constant, not the Python attribute).

## Algorithm Comparison

### BASIC
Simple raycasting from the viewer to each cell. Fast computation but can produce asymmetric results where the player can see a cell but an enemy at that cell cannot see the player.

### DIAMOND
Creates a diamond-shaped visible area. Produces symmetric results and is easy to understand, but may not look as natural as shadow casting.

### SHADOW (Recommended)
The most popular algorithm for roguelikes. Casts shadows from obstacles to determine visibility. Produces natural-looking results with good performance. This is the default choice for most games.

### PERMISSIVE_0 through PERMISSIVE_8
A family of algorithms that vary in how "permissive" they are about visibility around corners. Lower numbers (0-3) are stricter and show less around corners. Higher numbers (5-8) are more permissive and reveal more. Level 4 is the middle ground.

## Usage Patterns

### Basic FOV Setup

```python
import mcrfpy

scene = mcrfpy.Scene("fov-demo")
mcrfpy.current_scene = scene

# Create grid and set algorithm
grid = mcrfpy.Grid(grid_size=(80, 45), texture=mcrfpy.default_texture, pos=(0, 0), size=(800, 450))
grid.fov = mcrfpy.FOV.SHADOW
grid.fov_radius = 10
scene.children.append(grid)

player = mcrfpy.Entity(grid_pos=(5, 5), texture=mcrfpy.default_texture, sprite_index=84)
grid.entities.append(player)

enemies = [mcrfpy.Entity(grid_pos=(10, 10), texture=mcrfpy.default_texture, sprite_index=85)]
for enemy in enemies:
    grid.entities.append(enemy)

# Compute FOV from the player's tile position (radius defaults to 0 = unlimited when omitted)
grid.compute_fov(player.grid_pos)

# Use in visibility checks
for enemy in enemies:
    if grid.is_in_fov(enemy.grid_x, enemy.grid_y):
        enemy.visible = True
```

### FOV with Color Layer

`ColorLayer.draw_fov()` computes FOV internally and paints the layer in one call — no
separate `grid.compute_fov()` step is needed for this pattern:

```python
fog = mcrfpy.ColorLayer(z_index=10, name="fog")
grid.add_layer(fog)
fog.fill(mcrfpy.Color(0, 0, 0, 255))  # Start dark

def update_visibility():
    fog.draw_fov((player.grid_x, player.grid_y), radius=8)  # Reveal visible cells, re-fog the rest
```

### Algorithm Selection

```python
# For classic roguelike feel
grid.fov = mcrfpy.FOV.SHADOW

# For tactical games where seeing around corners matters
grid.fov = mcrfpy.FOV.PERMISSIVE_6

# For symmetric stealth games
grid.fov = mcrfpy.FOV.DIAMOND

# For fast computation in large maps
grid.fov = mcrfpy.FOV.BASIC
```

### Dynamic Algorithm Switching

```python
# Different FOV for different game modes
def set_stealth_mode():
    grid.fov = mcrfpy.FOV.PERMISSIVE_2  # Limited vision
    grid.fov_radius = 5

def set_alert_mode():
    grid.fov = mcrfpy.FOV.SHADOW
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
