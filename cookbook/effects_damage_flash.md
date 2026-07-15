---
mcrf:
  objects: [ColorLayer, Color, Grid, Timer, Entity]
  diataxis: howto
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Damage Flash Effect

Flash a grid cell red when its occupant is hit, then fade back to normal.

There is no built-in sprite/entity color tint in the engine (`Sprite` and `Entity` have
no `.color` property, and `mcrfpy.Animation` is not a real class — animations are started
via an object's own `.animate()` method, which only works on `Drawable`/`Entity`
properties, not on the plain `Color` values stored in a `ColorLayer`). The supported way
to get a color flash is a **`ColorLayer`** overlay on the grid, faded out manually with a
`Timer`.

## Quick Example

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

grid = mcrfpy.Grid(grid_size=(16, 12), pos=(0, 0), size=(640, 480))
scene.children.append(grid)

for y in range(12):
    for x in range(16):
        grid.at(x, y).tilesprite = 48

# One ColorLayer, reused for every flash effect on this grid.
color_layer = mcrfpy.ColorLayer(z_index=1, name="flash")
grid.add_layer(color_layer)

def flash_cell(x, y, color, duration=0.3, steps=10):
    """Flash a grid cell with a color overlay that fades out over `duration` seconds."""
    r, g, b = color
    step_ms = max(1, int(duration * 1000 / steps))

    def do_fade(timer, runtime, step=[0]):
        step[0] += 1
        alpha = max(0, int(200 * (1 - step[0] / steps)))
        color_layer.set((x, y), mcrfpy.Color(r, g, b, alpha))
        if step[0] >= steps:
            timer.stop()

    color_layer.set((x, y), mcrfpy.Color(r, g, b, 200))
    mcrfpy.Timer(f"flash_{x}_{y}", do_fade, step_ms)

def damage_flash(entity, duration=0.3):
    """Flash red on the cell an entity occupies."""
    flash_cell(entity.cell_x, entity.cell_y, (255, 0, 0), duration)

# Usage
player = mcrfpy.Entity(grid_pos=(8, 6), texture=mcrfpy.default_texture)
grid.entities.append(player)
damage_flash(player)
```

## Grid Cell Flash with ColorLayer

The pattern above generalizes to any cell, not just an entity's current position — handy
for AoE spells, traps, or telegraphed attacks:

```python
import mcrfpy

# Add a color layer to your grid (do this once during setup)
color_layer = mcrfpy.ColorLayer(z_index=1, name="flash")
grid.add_layer(color_layer)

def flash_cell(grid, color_layer, x, y, color, duration=0.3, steps=10):
    """Flash a grid cell with a color overlay, fading alpha to 0 over `duration` seconds."""
    r, g, b = color
    step_ms = max(1, int(duration * 1000 / steps))

    def do_fade(timer, runtime, step=[0]):
        step[0] += 1
        alpha = max(0, int(200 * (1 - step[0] / steps)))
        color_layer.set((x, y), mcrfpy.Color(r, g, b, alpha))
        if step[0] >= steps:
            timer.stop()

    color_layer.set((x, y), mcrfpy.Color(r, g, b, 200))
    mcrfpy.Timer(f"flash_{x}_{y}", do_fade, step_ms)

def damage_at_position(grid, color_layer, x, y, duration=0.3):
    """Flash red at a grid position when damage occurs."""
    flash_cell(grid, color_layer, x, y, (255, 0, 0), duration)

# Usage when entity takes damage
damage_at_position(grid, color_layer, enemy.cell_x, enemy.cell_y)
```

`ColorLayer.at(x, y)` returns a plain `Color` value (a snapshot, not a live handle) — you
can't mutate a cell in place by grabbing it and changing its fields. Always write a new
`Color` back with `color_layer.set((x, y), color)`.

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
        self.color_layer = mcrfpy.ColorLayer(z_index=1, name="flash")
        self.grid.add_layer(self.color_layer)

    def flash_entity(self, entity, color, duration=0.3):
        """Flash the cell an entity currently occupies."""
        self.flash_cell(entity.cell_x, entity.cell_y, color, duration)

    def flash_cell(self, x, y, color, duration=0.3, steps=10):
        """Flash a specific grid cell, fading out over `duration` seconds."""
        if not self.color_layer:
            return

        r, g, b = color
        step_ms = max(1, int(duration * 1000 / steps))

        def do_fade(timer, runtime, step=[0]):
            step[0] += 1
            alpha = max(0, int(180 * (1 - step[0] / steps)))
            self.color_layer.set((x, y), mcrfpy.Color(r, g, b, alpha))
            if step[0] >= steps:
                timer.stop()

        self.color_layer.set((x, y), mcrfpy.Color(r, g, b, 180))
        mcrfpy.Timer(f"flash_{x}_{y}", do_fade, step_ms)

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

Each `flash_cell()` call creates a `Timer` named `flash_<x>_<y>`. Since a `Timer` with a
name that already exists replaces the old one, overlapping flashes on the *same* cell will
cancel and restart the fade rather than stack — good enough for most feedback effects, but
worth knowing if you see a flash cut short.

## Multi-Flash Hit Effect

For more dramatic hits, flash a cell multiple times in succession:

```python
import mcrfpy

def multi_flash(grid, color_layer, x, y, color, flashes=3, flash_duration=0.1):
    """Flash a cell multiple times for emphasis."""
    r, g, b = color
    delay = 0

    for i in range(flashes):
        def do_flash(timer, runtime, fr=r, fg=g, fb=b):
            color_layer.set((x, y), mcrfpy.Color(fr, fg, fb, 200))
            mcrfpy.Timer(f"multiflash_clear_{x}_{y}_{timer.name}",
                         lambda t, rt: color_layer.set((x, y), mcrfpy.Color(fr, fg, fb, 0)),
                         int(flash_duration * 1000), once=True)

        mcrfpy.Timer(f"multiflash_{x}_{y}_{i}", do_flash, max(1, int(delay * 1000)), once=True)
        delay += flash_duration * 1.5  # Gap between flashes

# Usage for critical hit
multi_flash(grid, color_layer, enemy.cell_x, enemy.cell_y, (255, 255, 0), flashes=3)
```

## Key Concepts

1. **`ColorLayer`**: a grid overlay that stores one `Color` per cell — the supported way
   to tint or flash cells without touching tile sprites or entity sprites.
2. **No live cell handle**: `color_layer.at(x, y)` returns a `Color` snapshot; always
   write changes back with `color_layer.set((x, y), color)`.
3. **No `Color.animate()`**: only `Drawable`/`Entity` properties can be animated via
   `.animate()`. Fading a `ColorLayer` cell means stepping the alpha yourself, typically
   with a repeating `Timer`.
4. **Duration**: 0.2-0.4 seconds feels responsive; longer for status effects.

## Tips

- Keep one `ColorLayer` per grid and reuse it for every flash effect — creating a new
  layer per flash is wasteful.
- Give each in-flight flash's `Timer` a unique, cell-based name so unrelated flashes
  don't collide, and be aware that flashing the *same* cell twice in quick succession
  restarts the fade rather than stacking it.
- Alpha fading to 0 effectively hides the overlay once the flash finishes.
