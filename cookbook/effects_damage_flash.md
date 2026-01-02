# Damage Flash Effect

Flash an entity red when hit, then return to normal color.

## Quick Example

```python
import mcrfpy

def damage_flash(entity, duration=0.3):
    """Flash entity red, then restore original color."""
    # Store original color
    original_r = entity.sprite.color.r if hasattr(entity.sprite, 'color') else 255
    original_g = entity.sprite.color.g if hasattr(entity.sprite, 'color') else 255
    original_b = entity.sprite.color.b if hasattr(entity.sprite, 'color') else 255

    # Set to red immediately
    entity.sprite.color = mcrfpy.Color(255, 0, 0, 255)

    # Animate back to original over duration
    anim_r = mcrfpy.Animation("r", float(original_r), duration, "easeOut")
    anim_g = mcrfpy.Animation("g", float(original_g), duration, "easeOut")
    anim_b = mcrfpy.Animation("b", float(original_b), duration, "easeOut")

    anim_r.start(entity.sprite.color)
    anim_g.start(entity.sprite.color)
    anim_b.start(entity.sprite.color)

# Usage
damage_flash(player)
```

## Grid Cell Flash with ColorLayer

For grid-based games, flash the cell at the entity's position:

```python
import mcrfpy

# Add a color layer to your grid (do this once during setup)
grid.add_layer("color")
color_layer = grid.layers[-1]  # Get the color layer

def flash_cell(grid, x, y, color, duration=0.3):
    """Flash a grid cell with a color overlay."""
    # Get the color layer (assumes it's the last layer added)
    color_layer = None
    for layer in grid.layers:
        if isinstance(layer, mcrfpy.ColorLayer):
            color_layer = layer
            break

    if not color_layer:
        return

    # Set cell to flash color
    cell = color_layer.at(x, y)
    cell.color = mcrfpy.Color(color[0], color[1], color[2], 200)

    # Animate alpha back to 0
    anim = mcrfpy.Animation("a", 0.0, duration, "easeOut")
    anim.start(cell.color)

def damage_at_position(grid, x, y, duration=0.3):
    """Flash red at a grid position when damage occurs."""
    flash_cell(grid, x, y, (255, 0, 0), duration)

# Usage when entity takes damage
damage_at_position(grid, int(enemy.x), int(enemy.y))
```

## Complete Damage System

A reusable damage flash system with multiple flash types:

```python
import mcrfpy

class DamageEffects:
    """Manages visual damage feedback effects."""

    # Color presets
    DAMAGE_RED = (255, 50, 50)
    HEAL_GREEN = (50, 255, 50)
    POISON_PURPLE = (150, 50, 200)
    FIRE_ORANGE = (255, 150, 50)
    ICE_BLUE = (100, 200, 255)

    def __init__(self, grid):
        self.grid = grid
        self.color_layer = None
        self._setup_color_layer()

    def _setup_color_layer(self):
        """Ensure grid has a color layer for effects."""
        self.grid.add_layer("color")
        self.color_layer = self.grid.layers[-1]

    def flash_entity(self, entity, color, duration=0.3):
        """Flash an entity with a color tint."""
        # Flash at entity's grid position
        x, y = int(entity.x), int(entity.y)
        self.flash_cell(x, y, color, duration)

    def flash_cell(self, x, y, color, duration=0.3):
        """Flash a specific grid cell."""
        if not self.color_layer:
            return

        cell = self.color_layer.at(x, y)
        if cell:
            cell.color = mcrfpy.Color(color[0], color[1], color[2], 180)

            # Fade out
            anim = mcrfpy.Animation("a", 0.0, duration, "easeOut")
            anim.start(cell.color)

    def damage(self, entity, amount, duration=0.3):
        """Standard damage flash."""
        self.flash_entity(entity, self.DAMAGE_RED, duration)

    def heal(self, entity, amount, duration=0.4):
        """Healing effect - green flash."""
        self.flash_entity(entity, self.HEAL_GREEN, duration)

    def poison(self, entity, duration=0.5):
        """Poison damage - purple flash."""
        self.flash_entity(entity, self.POISON_PURPLE, duration)

    def fire(self, entity, duration=0.3):
        """Fire damage - orange flash."""
        self.flash_entity(entity, self.FIRE_ORANGE, duration)

    def ice(self, entity, duration=0.4):
        """Ice damage - blue flash."""
        self.flash_entity(entity, self.ICE_BLUE, duration)

    def area_damage(self, center_x, center_y, radius, color, duration=0.4):
        """Flash all cells in a radius."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    self.flash_cell(center_x + dx, center_y + dy, color, duration)

# Setup
effects = DamageEffects(grid)

# Usage examples
effects.damage(player, 10)           # Red flash
effects.heal(player, 5)              # Green flash
effects.poison(enemy)                # Purple flash
effects.area_damage(5, 5, 3, effects.FIRE_ORANGE)  # Area effect
```

## Multi-Flash Hit Effect

For more dramatic hits, flash multiple times:

```python
import mcrfpy

def multi_flash(grid, x, y, color, flashes=3, flash_duration=0.1):
    """Flash a cell multiple times for emphasis."""
    delay = 0

    for i in range(flashes):
        # Schedule each flash with increasing delay
        def do_flash(timer_name, fx=x, fy=y, fc=color, fd=flash_duration):
            flash_cell(grid, fx, fy, fc, fd)

        mcrfpy.Timer(f"flash_{x}_{y}_{i}", do_flash, int(delay * 1000), once=True)
        delay += flash_duration * 1.5  # Gap between flashes

# Usage for critical hit
multi_flash(grid, int(enemy.x), int(enemy.y), (255, 255, 0), flashes=3)
```

## Key Concepts

1. **Animation properties**: `r`, `g`, `b`, `a` for color components
2. **ColorLayer**: Grid overlay for cell-based effects without modifying tiles
3. **Easing**: Use "easeOut" for natural fade-out, "easeIn" for building intensity
4. **Duration**: 0.2-0.4 seconds feels responsive; longer for status effects

## Tips

- Store original colors before modifying if you need to restore exactly
- Use ColorLayer for grid-based games to avoid sprite color issues
- Chain effects using Timer for complex sequences
- Alpha animation (0->0) effectively hides the overlay after flash
