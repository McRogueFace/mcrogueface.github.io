---
layout: default
title: Multi-Layer Tiles
parent: Cookbook
nav_order: 5
---

# Multi-Layer Tiles

Stack base tiles, decorations, and effects for rich visual environments.

---

## Overview

Grid layers allow stacking multiple visual elements:
- **Base tiles**: Floor, walls, terrain
- **Decoration layer**: Furniture, debris, blood stains
- **Effect layer**: Fog, fire, magic effects
- **UI layer**: Selection cursors, path indicators

---

## Quick Start

```python
import mcrfpy

# Add layers with different z-indices
base_layer = grid.add_layer("tile", z_index=0)      # Base terrain
decor_layer = grid.add_layer("tile", z_index=1)     # Decorations
effect_layer = grid.add_layer("color", z_index=2)   # Color effects
ui_layer = grid.add_layer("color", z_index=3)       # UI highlights

# Set tiles on each layer
base_layer.set(5, 5, TILE_FLOOR)
decor_layer.set(5, 5, TILE_RUG)  # Rug on top of floor
```

---

## Layer Types

### Tile Layers

Display sprite tiles from the grid's texture:

```python
# Create tile layer
decor = grid.add_layer("tile", z_index=1)

# Set decoration tiles
decor.set(10, 10, TILE_TABLE)
decor.set(11, 10, TILE_CHAIR)
decor.set(10, 15, TILE_CHEST)

# Clear a tile (make transparent)
decor.clear(10, 10)
```

### Color Layers

Apply color overlays to cells:

```python
# Create color layer
effects = grid.add_layer("color", z_index=2)

# Set color at position
effects.set(5, 5, mcrfpy.Color(255, 0, 0, 128))  # Red overlay

# Clear color
effects.set(5, 5, mcrfpy.Color(0, 0, 0, 0))  # Transparent

# Clear entire layer
effects.clear()
```

---

## Decoration System

Manage static decorations efficiently:

```python
class DecorationManager:
    """Manage decorative tile overlays."""

    # Decoration categories with sprite indices
    DECORATIONS = {
        'furniture': {
            'table': 100,
            'chair': 101,
            'bed': 102,
            'chest': 103,
            'bookshelf': 104,
        },
        'debris': {
            'bones': 110,
            'rubble': 111,
            'cobweb': 112,
        },
        'nature': {
            'grass_tuft': 120,
            'mushroom': 121,
            'flower': 122,
            'moss': 123,
        },
        'stains': {
            'blood': 130,
            'water': 131,
            'acid': 132,
        }
    }

    def __init__(self, grid):
        self.grid = grid
        self.layer = grid.add_layer("tile", z_index=1)
        self.placed = {}  # (x, y) -> decoration_name

    def place(self, x, y, category, name):
        """Place a decoration."""
        if category in self.DECORATIONS:
            if name in self.DECORATIONS[category]:
                sprite_idx = self.DECORATIONS[category][name]
                self.layer.set(x, y, sprite_idx)
                self.placed[(x, y)] = (category, name)

    def remove(self, x, y):
        """Remove a decoration."""
        self.layer.clear(x, y)
        if (x, y) in self.placed:
            del self.placed[(x, y)]

    def get(self, x, y):
        """Get decoration at position."""
        return self.placed.get((x, y))

    def scatter(self, category, count, walkable_only=True):
        """Randomly scatter decorations."""
        import random

        if category not in self.DECORATIONS:
            return

        names = list(self.DECORATIONS[category].keys())
        grid_w, grid_h = self.grid.grid_size

        placed = 0
        attempts = 0
        max_attempts = count * 10

        while placed < count and attempts < max_attempts:
            attempts += 1

            x = random.randint(0, grid_w - 1)
            y = random.randint(0, grid_h - 1)

            # Check if position is valid
            point = self.grid.at(x, y)
            if walkable_only and not point.walkable:
                continue
            if (x, y) in self.placed:
                continue

            name = random.choice(names)
            self.place(x, y, category, name)
            placed += 1


# Usage
decor = DecorationManager(grid)

# Place specific decorations
decor.place(10, 10, 'furniture', 'table')
decor.place(11, 10, 'furniture', 'chair')

# Scatter random debris
decor.scatter('debris', 20)
decor.scatter('nature', 15)
```

---

## Effect Layer System

Dynamic visual effects:

```python
class EffectLayer:
    """Manage visual effects with color overlays."""

    def __init__(self, grid, z_index=2):
        self.grid = grid
        self.layer = grid.add_layer("color", z_index=z_index)
        self.effects = {}  # (x, y) -> effect_data

    def add_effect(self, x, y, effect_type, duration=None, **kwargs):
        """Add a visual effect."""
        self.effects[(x, y)] = {
            'type': effect_type,
            'duration': duration,
            'time': 0,
            **kwargs
        }

    def remove_effect(self, x, y):
        """Remove an effect."""
        if (x, y) in self.effects:
            del self.effects[(x, y)]
            self.layer.set(x, y, mcrfpy.Color(0, 0, 0, 0))

    def update(self, dt):
        """Update all effects."""
        import math

        to_remove = []

        for (x, y), effect in self.effects.items():
            effect['time'] += dt

            # Check expiration
            if effect['duration'] and effect['time'] >= effect['duration']:
                to_remove.append((x, y))
                continue

            # Calculate color based on effect type
            color = self._calculate_color(effect)
            self.layer.set(x, y, color)

        for pos in to_remove:
            self.remove_effect(*pos)

    def _calculate_color(self, effect):
        """Get color for an effect at current time."""
        import math

        t = effect['time']
        effect_type = effect['type']

        if effect_type == 'fire':
            # Flickering orange/red
            flicker = 0.7 + 0.3 * math.sin(t * 10)
            return mcrfpy.Color(
                255,
                int(100 + 50 * math.sin(t * 8)),
                0,
                int(180 * flicker)
            )

        elif effect_type == 'poison':
            # Pulsing green
            pulse = 0.5 + 0.5 * math.sin(t * 3)
            return mcrfpy.Color(0, 200, 0, int(100 * pulse))

        elif effect_type == 'ice':
            # Static blue with shimmer
            shimmer = 0.8 + 0.2 * math.sin(t * 5)
            return mcrfpy.Color(100, 150, 255, int(120 * shimmer))

        elif effect_type == 'blood':
            # Fading red
            duration = effect.get('duration', 5)
            fade = 1 - (t / duration) if duration else 1
            return mcrfpy.Color(150, 0, 0, int(150 * fade))

        elif effect_type == 'highlight':
            # Pulsing highlight
            pulse = 0.5 + 0.5 * math.sin(t * 4)
            base = effect.get('color', mcrfpy.Color(255, 255, 0, 100))
            return mcrfpy.Color(base.r, base.g, base.b, int(base.a * pulse))

        return mcrfpy.Color(128, 128, 128, 50)


# Usage
effects = EffectLayer(grid)

# Add fire effect (permanent)
effects.add_effect(5, 5, 'fire')

# Add blood stain (fades over 10 seconds)
effects.add_effect(10, 10, 'blood', duration=10)

# Add poison cloud
for x in range(8, 12):
    for y in range(8, 12):
        effects.add_effect(x, y, 'poison', duration=5)

# Update in game loop
def game_update(runtime):
    effects.update(0.016)  # 60 FPS

mcrfpy.setTimer("effects", game_update, 16)
```

---

## Complete Layer Stack

Combine all layers:

```python
class LayeredGrid:
    """Complete multi-layer grid system."""

    def __init__(self, grid):
        self.grid = grid

        # Layer stack (bottom to top)
        self.fog = grid.add_layer("color", z_index=-1)      # Fog of war
        # z_index=0 is the base grid tiles
        self.decor = grid.add_layer("tile", z_index=1)      # Decorations
        self.effects = grid.add_layer("color", z_index=2)   # Effects
        self.highlight = grid.add_layer("color", z_index=3) # UI highlights

        # Managers
        self.decor_manager = DecorationManager(self.decor)
        self.effect_manager = EffectManager(self.effects)

    def update(self, dt):
        """Update all animated layers."""
        self.effect_manager.update(dt)

    def set_fog(self, entity):
        """Apply fog of war from entity perspective."""
        self.fog.apply_perspective(
            entity=entity,
            visible=mcrfpy.Color(0, 0, 0, 0),
            discovered=mcrfpy.Color(20, 20, 40, 160),
            unknown=mcrfpy.Color(0, 0, 0, 255)
        )

    def highlight_cells(self, cells, color):
        """Highlight cells for targeting/movement."""
        self.highlight.clear()
        for x, y in cells:
            self.highlight.set(x, y, color)

    def clear_highlights(self):
        """Clear all highlights."""
        self.highlight.clear()


# Usage
layers = LayeredGrid(grid)

# Setup fog of war
layers.set_fog(player)

# Add decorations
layers.decor_manager.place(10, 10, 'furniture', 'chest')

# Add effect
layers.effect_manager.add_effect(15, 15, 'fire')

# Highlight movement range
movement_cells = get_movement_range(player.pos, 5)
layers.highlight_cells(movement_cells, mcrfpy.Color(50, 100, 255, 80))

# Game loop
def update(runtime):
    layers.update(0.016)

mcrfpy.setTimer("layers", update, 16)
```

---

## Performance Considerations

```python
class OptimizedLayers:
    """Performance-optimized layer management."""

    def __init__(self, grid):
        self.grid = grid
        self.dirty_effects = set()  # Only update changed cells
        self.batch_updates = []

    def mark_dirty(self, x, y):
        """Mark a cell as needing update."""
        self.dirty_effects.add((x, y))

    def batch_set(self, layer, cells_and_values):
        """Queue batch updates."""
        self.batch_updates.append((layer, cells_and_values))

    def flush(self):
        """Apply all queued updates."""
        for layer, updates in self.batch_updates:
            for x, y, value in updates:
                layer.set(x, y, value)
        self.batch_updates = []

    def update_dirty_only(self, effect_layer, effect_calculator):
        """Only update cells marked dirty."""
        for x, y in self.dirty_effects:
            color = effect_calculator(x, y)
            effect_layer.set(x, y, color)
        self.dirty_effects.clear()
```

---

## Tips

1. **Z-index order**: Lower numbers render first (behind higher numbers)
2. **Alpha blending**: Layers blend - use alpha for transparency
3. **Performance**: Minimize layer count; combine when possible
4. **Clear strategically**: clear() is faster than setting each cell transparent
5. **Fog on bottom**: Use negative z-index for fog of war

---

## Layer Z-Index Reference

| Z-Index | Layer | Purpose |
|---------|-------|---------|
| -1 | Fog | Fog of war overlay |
| 0 | Base | Base tiles (floors, walls) |
| 1 | Decor | Static decorations |
| 2 | Effects | Animated effects |
| 3 | UI | Selection, targeting |

---

## Related Recipes

- [Fog of War](grid_fog_of_war.md) - Fog layer implementation
- [Cell Highlighting](grid_cell_highlighting.md) - UI layer usage
- [Dungeon Generator](grid_dungeon_generator.md) - Base tile generation
