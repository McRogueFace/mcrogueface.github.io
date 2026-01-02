---
layout: default
title: Cell Highlighting
parent: Cookbook
nav_order: 3
---

# Cell Highlighting (Targeting)

Use ColorLayer to highlight cells for targeting, movement ranges, and area effects.

---

## Overview

Cell highlighting is essential for:
- Showing valid movement destinations
- Displaying attack/spell ranges
- Indicating area-of-effect zones
- Providing path previews

---

## Quick Start

```python
import mcrfpy

# Create a highlight layer (above tiles, below entities)
highlight_layer = grid.add_layer("color", z_index=1)

def highlight_cells(cells, color):
    """Highlight a list of (x, y) coordinates."""
    highlight_layer.clear()
    for x, y in cells:
        highlight_layer.set(x, y, color)

def clear_highlights():
    """Remove all highlighting."""
    highlight_layer.clear()
```

---

## Movement Range Highlighting

Show where the player can move:

```python
def get_movement_range(start_x, start_y, max_distance):
    """Get all reachable cells within movement range."""
    reachable = set()
    reachable.add((start_x, start_y))

    frontier = [(start_x, start_y, 0)]

    while frontier:
        x, y, dist = frontier.pop(0)

        if dist >= max_distance:
            continue

        # Check all adjacent cells
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy

            # Skip if already visited
            if (nx, ny) in reachable:
                continue

            # Check if walkable
            if grid.at(nx, ny).walkable:
                reachable.add((nx, ny))
                frontier.append((nx, ny, dist + 1))

    return reachable

def show_movement_range():
    """Display valid movement destinations."""
    px, py = player.pos
    movement_points = 5  # Player can move 5 tiles

    reachable = get_movement_range(px, py, movement_points)

    # Blue highlight for movement
    highlight_cells(reachable, mcrfpy.Color(50, 100, 255, 100))
```

---

## Attack Range Highlighting

Different range patterns for attacks:

```python
def get_line_range(start_x, start_y, max_range):
    """Get cells in cardinal directions (ranged attack)."""
    cells = set()

    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        for dist in range(1, max_range + 1):
            x = start_x + dx * dist
            y = start_y + dy * dist

            # Stop if wall blocks line of sight
            if not grid.at(x, y).transparent:
                break

            cells.add((x, y))

    return cells

def get_radius_range(center_x, center_y, radius, include_center=False):
    """Get cells within a radius (spell area)."""
    cells = set()

    for x in range(center_x - radius, center_x + radius + 1):
        for y in range(center_y - radius, center_y + radius + 1):
            # Euclidean distance
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            if dist <= radius:
                if include_center or (x, y) != (center_x, center_y):
                    cells.add((x, y))

    return cells

def get_cone_range(origin_x, origin_y, direction, length, spread):
    """Get cells in a cone (breath attack)."""
    import math
    cells = set()

    # Direction angles (in radians)
    angles = {
        'n': -math.pi / 2,
        's': math.pi / 2,
        'e': 0,
        'w': math.pi,
        'ne': -math.pi / 4,
        'nw': -3 * math.pi / 4,
        'se': math.pi / 4,
        'sw': 3 * math.pi / 4
    }

    base_angle = angles.get(direction, 0)
    half_spread = math.radians(spread / 2)

    for x in range(origin_x - length, origin_x + length + 1):
        for y in range(origin_y - length, origin_y + length + 1):
            dx = x - origin_x
            dy = y - origin_y
            dist = (dx * dx + dy * dy) ** 0.5

            if dist > 0 and dist <= length:
                angle = math.atan2(dy, dx)
                angle_diff = abs((angle - base_angle + math.pi) % (2 * math.pi) - math.pi)

                if angle_diff <= half_spread:
                    cells.add((x, y))

    return cells
```

---

## Multi-Color Highlighting

Layer different highlight types:

```python
class HighlightManager:
    """Manage multiple highlight layers."""

    COLORS = {
        'move': mcrfpy.Color(50, 100, 255, 80),      # Blue
        'attack': mcrfpy.Color(255, 50, 50, 100),     # Red
        'heal': mcrfpy.Color(50, 255, 50, 100),       # Green
        'danger': mcrfpy.Color(255, 100, 0, 120),     # Orange
        'select': mcrfpy.Color(255, 255, 50, 150),    # Yellow
        'path': mcrfpy.Color(255, 255, 255, 80),      # White
    }

    def __init__(self, grid):
        self.grid = grid
        self.layer = grid.add_layer("color", z_index=1)
        self.highlights = {}  # category -> set of cells

    def add(self, category, cells):
        """Add highlights for a category."""
        self.highlights[category] = set(cells)
        self._refresh()

    def remove(self, category):
        """Remove highlights for a category."""
        if category in self.highlights:
            del self.highlights[category]
            self._refresh()

    def clear(self):
        """Clear all highlights."""
        self.highlights = {}
        self.layer.clear()

    def _refresh(self):
        """Redraw all highlights with proper layering."""
        self.layer.clear()

        # Draw in priority order (later categories draw on top)
        priority = ['move', 'attack', 'heal', 'danger', 'path', 'select']

        for category in priority:
            if category in self.highlights:
                color = self.COLORS.get(category, mcrfpy.Color(128, 128, 128, 100))
                for x, y in self.highlights[category]:
                    self.layer.set(x, y, color)


# Usage example
highlights = HighlightManager(grid)

def on_ability_select(ability):
    """Show range when ability is selected."""
    highlights.clear()

    px, py = player.pos

    if ability == 'move':
        cells = get_movement_range(px, py, 5)
        highlights.add('move', cells)

    elif ability == 'attack':
        cells = get_radius_range(px, py, 3)
        highlights.add('attack', cells)

    elif ability == 'fireball':
        # Show cast range
        cast_range = get_radius_range(px, py, 8)
        highlights.add('move', cast_range)  # Blue for "where can I cast"
        # AoE preview added when hovering

def on_cell_hover(x, y):
    """Preview effect when hovering over a cell."""
    if current_ability == 'fireball':
        # Show explosion radius at cursor
        highlights.remove('danger')
        if (x, y) in highlights.highlights.get('move', set()):
            aoe = get_radius_range(x, y, 2, include_center=True)
            highlights.add('danger', aoe)
```

---

## Path Preview

Show the path the player will take:

```python
def show_path_preview(start, end):
    """Highlight the path between two points."""
    path = find_path(start, end)  # Your pathfinding function

    if path:
        highlights.add('path', path)

        # Highlight destination specially
        highlights.add('select', [end])

def hide_path_preview():
    """Clear path display."""
    highlights.remove('path')
    highlights.remove('select')
```

---

## Animated Highlighting

Pulsing highlights for attention:

```python
class AnimatedHighlight:
    """Highlights that pulse or animate."""

    def __init__(self, grid, layer_z=1):
        self.grid = grid
        self.layer = grid.add_layer("color", z_index=layer_z)
        self.animated_cells = {}  # (x, y) -> base_color
        self.phase = 0

    def add_pulse(self, cells, base_color):
        """Add cells that will pulse."""
        for cell in cells:
            self.animated_cells[cell] = base_color

    def clear(self):
        """Stop all animations."""
        self.animated_cells = {}
        self.layer.clear()

    def update(self, dt):
        """Update animation state."""
        import math

        self.phase += dt * 3  # Speed of pulse

        # Calculate current alpha multiplier (0.5 to 1.0)
        pulse = 0.75 + 0.25 * math.sin(self.phase)

        for (x, y), base_color in self.animated_cells.items():
            # Modulate alpha
            animated_color = mcrfpy.Color(
                base_color.r,
                base_color.g,
                base_color.b,
                int(base_color.a * pulse)
            )
            self.layer.set(x, y, animated_color)


# Update in game loop
animated_highlights = AnimatedHighlight(grid)

def game_update(runtime):
    dt = 0.016  # ~60 FPS
    animated_highlights.update(dt)

mcrfpy.setTimer("highlight_anim", game_update, 16)
```

---

## Integration with Targeting System

Complete targeting workflow:

```python
class TargetingSystem:
    """Handle ability targeting with visual feedback."""

    def __init__(self, grid, player):
        self.grid = grid
        self.player = player
        self.highlights = HighlightManager(grid)
        self.current_ability = None
        self.valid_targets = set()

    def start_targeting(self, ability):
        """Begin targeting for an ability."""
        self.current_ability = ability
        px, py = self.player.pos

        # Get valid targets based on ability
        if ability.target_type == 'self':
            self.valid_targets = {(px, py)}
        elif ability.target_type == 'adjacent':
            self.valid_targets = get_adjacent(px, py)
        elif ability.target_type == 'ranged':
            self.valid_targets = get_radius_range(px, py, ability.range)
        elif ability.target_type == 'line':
            self.valid_targets = get_line_range(px, py, ability.range)

        # Filter to visible tiles only
        self.valid_targets = {
            (x, y) for x, y in self.valid_targets
            if grid.is_in_fov(x, y)
        }

        # Show valid targets
        self.highlights.add('attack', self.valid_targets)

    def update_hover(self, x, y):
        """Update when cursor moves."""
        if not self.current_ability:
            return

        # Clear previous AoE preview
        self.highlights.remove('danger')

        if (x, y) in self.valid_targets:
            # Valid target - highlight it
            self.highlights.add('select', [(x, y)])

            # Show AoE if applicable
            if self.current_ability.aoe_radius > 0:
                aoe = get_radius_range(x, y, self.current_ability.aoe_radius, True)
                self.highlights.add('danger', aoe)
        else:
            self.highlights.remove('select')

    def confirm_target(self, x, y):
        """Confirm target selection."""
        if (x, y) in self.valid_targets:
            self.cancel_targeting()
            return (x, y)
        return None

    def cancel_targeting(self):
        """Cancel targeting mode."""
        self.current_ability = None
        self.valid_targets = set()
        self.highlights.clear()
```

---

## Tips

1. **Z-index matters**: Use z_index=1 for highlights above tiles but below entities
2. **Alpha blending**: Lower alpha values (80-150) look better than opaque
3. **Performance**: Clear and redraw is simpler than tracking changes
4. **Color coding**: Use consistent colors (blue=move, red=attack, etc.)
5. **Combine with FOV**: Only highlight visible cells for realism

---

## Related Recipes

- [Fog of War](grid_fog_of_war.md) - Visibility affects valid targets
- [Dijkstra Maps](grid_dijkstra.md) - Calculate movement costs
- [Multi-Layer Tiles](grid_multi_layer.md) - Layer highlights with decorations
