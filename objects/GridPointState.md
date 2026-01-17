---
layout: default
title: GridPointState
---

# GridPointState

Entity-specific visibility state for grid cells.

## Overview

A `GridPointState` represents an entity's knowledge about a specific grid cell - whether it's currently visible and whether it has been discovered. This enables fog-of-war gameplay where entities have their own view of the world. GridPointStates cannot be instantiated directly - they are returned by `Entity.at()` or accessed through `Entity.gridstate`.

## Quick Reference

```python
# Get entity's view of a cell
state = entity.at(5, 10)

# Check visibility
if state.visible:
    print("Entity can currently see this cell")

if state.discovered:
    print("Entity has seen this cell before")

# Access the underlying GridPoint (if discovered)
if state.discovered:
    point = state.point
    print(f"Walkable: {point.walkable}")
```

## Obtaining GridPointState

GridPointStates are obtained through `Entity.at()`:

```python
# By coordinates
state = entity.at(x, y)

# By tuple/Vector
state = entity.at((x, y))
state = entity.at(some_vector)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `visible` | bool | Whether the entity can currently see this cell |
| `discovered` | bool | Whether the entity has ever seen this cell |
| `point` | GridPoint | The underlying GridPoint (None if not discovered) |

## Visibility States

Cells can be in three states from an entity's perspective:

| State | visible | discovered | Description |
|-------|---------|------------|-------------|
| Unknown | False | False | Never seen - typically rendered as black |
| Discovered | False | True | Previously seen but not currently visible - rendered dimmed |
| Visible | True | True | Currently in line of sight - rendered normally |

## Usage Patterns

### Fog of War Rendering

```python
def get_cell_appearance(entity, x, y):
    """Determine how to render a cell for this entity."""
    state = entity.at(x, y)

    if not state.discovered:
        return "black"  # Unknown
    elif not state.visible:
        return "dim"    # Remembered but not visible
    else:
        return "normal" # Currently visible
```

### Information Gathering

```python
def describe_cell(entity, x, y):
    """Describe what the entity knows about a cell."""
    state = entity.at(x, y)

    if not state.discovered:
        return "You haven't explored this area."

    point = state.point
    description = []

    if not point.walkable:
        description.append("There's an obstacle here.")

    if state.visible:
        # Can see current contents
        for e in point.entities:
            description.append(f"You see {e.name}.")
    else:
        description.append("You remember this area, but can't see it now.")

    return " ".join(description)
```

### Updating Visibility

```python
# Visibility is typically updated automatically, but can be forced:
entity.update_visibility()

# After moving the entity, visibility is recalculated
entity.grid_pos = (new_x, new_y)
entity.update_visibility()  # Optional - may be automatic
```

### Checking Visible Enemies

```python
def get_visible_enemies(player, all_enemies):
    """Get list of enemies the player can currently see."""
    visible = []
    for enemy in all_enemies:
        state = player.at(enemy.grid_x, enemy.grid_y)
        if state.visible:
            visible.append(enemy)
    return visible

# Or use the built-in method:
visible_entities = player.visible_entities()
```

### Stealth Gameplay

```python
def can_enemy_see_player(enemy, player):
    """Check if enemy has line of sight to player."""
    state = enemy.at(player.grid_x, player.grid_y)
    return state.visible

def is_player_hidden(player, enemies):
    """Check if player is hidden from all enemies."""
    for enemy in enemies:
        if can_enemy_see_player(enemy, player):
            return False
    return True
```

## ColorLayer Integration

GridPointState works with ColorLayer's perspective system for automatic fog-of-war rendering:

```python
# Create visibility layer
fog_layer = grid.add_layer('color', z_index=10)

# Bind to entity's perspective
fog_layer.apply_perspective(
    player,
    visible=mcrfpy.Color(0, 0, 0, 0),      # Transparent when visible
    discovered=mcrfpy.Color(0, 0, 0, 128),  # Semi-transparent when discovered
    unknown=mcrfpy.Color(0, 0, 0, 255)      # Opaque when unknown
)

# Layer automatically updates when entity moves
```

## Notes

- Each entity maintains its own GridPointState data for every cell
- Visibility is calculated using the Grid's FOV algorithm (set via `grid.fov`)
- The `point` property returns None for undiscovered cells, preventing information leakage
- Setting `visible = True` also sets `discovered = True` automatically
- Use `Entity.update_visibility()` to recalculate FOV after movement

## Related

<div class="related-objects">
<div class="object-links">
<a href="GridPoint" class="object-link">GridPoint</a>
<a href="Entity" class="object-link">Entity</a>
<a href="Grid" class="object-link">Grid</a>
<a href="ColorLayer" class="object-link">ColorLayer</a>
<a href="FOV" class="object-link">FOV</a>
<a href="../systems/grid" class="object-link">Grid System</a>
</div>
</div>
