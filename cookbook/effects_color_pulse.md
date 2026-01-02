# Color Pulse Effect

Animate a grid cell's color layer to pulse, useful for highlighting interactable tiles, objectives, warnings, or magical effects.

## Quick Example

```python
import mcrfpy

def pulse_cell(grid, x, y, color, duration=1.0):
    """
    Pulse a cell's color overlay from transparent to visible and back.

    Args:
        grid: Grid with a color layer
        x, y: Cell coordinates
        color: RGB tuple (r, g, b)
        duration: Full cycle duration in seconds
    """
    # Get or create color layer
    color_layer = None
    for layer in grid.layers:
        if isinstance(layer, mcrfpy.ColorLayer):
            color_layer = layer
            break

    if not color_layer:
        grid.add_layer("color")
        color_layer = grid.layers[-1]

    # Get the cell
    cell = color_layer.at(x, y)
    if not cell:
        return

    # Set initial color with 0 alpha
    cell.color = mcrfpy.Color(color[0], color[1], color[2], 0)

    # Animate alpha up
    half_duration = duration / 2
    anim_up = mcrfpy.Animation("a", 200.0, half_duration, "easeInOut")
    anim_up.start(cell.color)

    # Schedule fade out
    def fade_out(timer_name):
        anim_down = mcrfpy.Animation("a", 0.0, half_duration, "easeInOut")
        anim_down.start(cell.color)

    mcrfpy.Timer("pulse_fade", fade_out, int(half_duration * 1000), once=True)


# Usage
pulse_cell(grid, 5, 5, (255, 200, 0), duration=1.5)  # Golden pulse
```

## Continuous Pulsing

Keep a cell pulsing until stopped:

```python
import mcrfpy

class PulsingCell:
    """A cell that continuously pulses until stopped."""

    def __init__(self, grid, x, y, color, period=1.0, max_alpha=180):
        """
        Args:
            grid: Grid with color layer
            x, y: Cell position
            color: RGB tuple
            period: Time for one complete pulse cycle
            max_alpha: Maximum alpha value (0-255)
        """
        self.grid = grid
        self.x = x
        self.y = y
        self.color = color
        self.period = period
        self.max_alpha = max_alpha
        self.is_pulsing = False
        self.pulse_id = 0
        self.cell = None

        self._setup_layer()

    def _setup_layer(self):
        """Ensure color layer exists and get cell reference."""
        color_layer = None
        for layer in self.grid.layers:
            if isinstance(layer, mcrfpy.ColorLayer):
                color_layer = layer
                break

        if not color_layer:
            self.grid.add_layer("color")
            color_layer = self.grid.layers[-1]

        self.cell = color_layer.at(self.x, self.y)
        if self.cell:
            self.cell.color = mcrfpy.Color(self.color[0], self.color[1],
                                            self.color[2], 0)

    def start(self):
        """Start continuous pulsing."""
        if self.is_pulsing or not self.cell:
            return

        self.is_pulsing = True
        self.pulse_id += 1
        self._pulse_up()

    def _pulse_up(self):
        """Animate alpha increasing."""
        if not self.is_pulsing:
            return

        current_id = self.pulse_id
        half_period = self.period / 2

        anim = mcrfpy.Animation("a", float(self.max_alpha), half_period, "easeInOut")
        anim.start(self.cell.color)

        def next_phase(timer_name):
            if self.is_pulsing and self.pulse_id == current_id:
                self._pulse_down()

        mcrfpy.Timer(f"pulse_up_{id(self)}_{current_id}",
                     next_phase, int(half_period * 1000), once=True)

    def _pulse_down(self):
        """Animate alpha decreasing."""
        if not self.is_pulsing:
            return

        current_id = self.pulse_id
        half_period = self.period / 2

        anim = mcrfpy.Animation("a", 0.0, half_period, "easeInOut")
        anim.start(self.cell.color)

        def next_phase(timer_name):
            if self.is_pulsing and self.pulse_id == current_id:
                self._pulse_up()

        mcrfpy.Timer(f"pulse_down_{id(self)}_{current_id}",
                     next_phase, int(half_period * 1000), once=True)

    def stop(self):
        """Stop pulsing and fade out."""
        self.is_pulsing = False
        if self.cell:
            anim = mcrfpy.Animation("a", 0.0, 0.2, "easeOut")
            anim.start(self.cell.color)

    def set_color(self, color):
        """Change pulse color."""
        self.color = color
        if self.cell:
            current_alpha = self.cell.color.a
            self.cell.color = mcrfpy.Color(color[0], color[1], color[2], current_alpha)


# Usage
objective_pulse = PulsingCell(grid, 10, 10, (0, 255, 100), period=1.5)
objective_pulse.start()

# Later, when objective is reached:
objective_pulse.stop()
```

## Multiple Pulsing Cells Manager

Manage multiple pulsing effects:

```python
import mcrfpy

class PulseManager:
    """Manages multiple pulsing cell effects."""

    # Preset colors
    OBJECTIVE = (0, 255, 100)    # Green - goals, exits
    WARNING = (255, 100, 0)      # Orange - danger zones
    TREASURE = (255, 215, 0)     # Gold - loot
    MAGIC = (150, 50, 255)       # Purple - magical
    HEAL = (100, 200, 255)       # Light blue - healing
    DAMAGE = (255, 50, 50)       # Red - damage zones

    def __init__(self, grid):
        self.grid = grid
        self.pulses = {}  # (x, y) -> PulsingCell
        self._ensure_layer()

    def _ensure_layer(self):
        """Ensure grid has a color layer."""
        has_color_layer = False
        for layer in self.grid.layers:
            if isinstance(layer, mcrfpy.ColorLayer):
                has_color_layer = True
                break

        if not has_color_layer:
            self.grid.add_layer("color")

    def add(self, x, y, color, period=1.0, max_alpha=180):
        """Add a pulsing cell."""
        key = (x, y)
        if key in self.pulses:
            self.pulses[key].stop()

        pulse = PulsingCell(self.grid, x, y, color, period, max_alpha)
        pulse.start()
        self.pulses[key] = pulse
        return pulse

    def remove(self, x, y):
        """Stop and remove a pulsing cell."""
        key = (x, y)
        if key in self.pulses:
            self.pulses[key].stop()
            del self.pulses[key]

    def clear(self):
        """Stop all pulsing cells."""
        for pulse in self.pulses.values():
            pulse.stop()
        self.pulses.clear()

    def has_pulse(self, x, y):
        """Check if a cell is pulsing."""
        return (x, y) in self.pulses

    # Convenience methods with presets
    def mark_objective(self, x, y):
        """Mark a cell as an objective."""
        return self.add(x, y, self.OBJECTIVE, period=1.5)

    def mark_warning(self, x, y):
        """Mark a cell as dangerous."""
        return self.add(x, y, self.WARNING, period=0.8, max_alpha=150)

    def mark_treasure(self, x, y):
        """Mark a cell with treasure."""
        return self.add(x, y, self.TREASURE, period=1.2)

    def mark_magic(self, x, y):
        """Mark a magical cell."""
        return self.add(x, y, self.MAGIC, period=2.0)


# Usage
pulses = PulseManager(grid)

# Mark various cells
pulses.mark_objective(15, 10)   # Exit door
pulses.mark_treasure(8, 5)      # Chest location
pulses.mark_warning(12, 12)     # Trap

# When player reaches objective
pulses.remove(15, 10)

# Clear all when changing levels
pulses.clear()
```

## Area Pulse Effect

Pulse a group of cells together:

```python
import mcrfpy

class AreaPulse:
    """Pulse a rectangular or circular area."""

    def __init__(self, grid):
        self.grid = grid
        self.cells = []
        self.is_pulsing = False
        self._ensure_layer()

    def _ensure_layer(self):
        has_color_layer = False
        for layer in self.grid.layers:
            if isinstance(layer, mcrfpy.ColorLayer):
                self.color_layer = layer
                has_color_layer = True
                break

        if not has_color_layer:
            self.grid.add_layer("color")
            self.color_layer = self.grid.layers[-1]

    def set_rect(self, x, y, width, height, color):
        """Set a rectangular area to pulse."""
        self.cells = []
        for dy in range(height):
            for dx in range(width):
                cell = self.color_layer.at(x + dx, y + dy)
                if cell:
                    cell.color = mcrfpy.Color(color[0], color[1], color[2], 0)
                    self.cells.append(cell)

    def set_circle(self, center_x, center_y, radius, color):
        """Set a circular area to pulse."""
        self.cells = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    cell = self.color_layer.at(center_x + dx, center_y + dy)
                    if cell:
                        cell.color = mcrfpy.Color(color[0], color[1], color[2], 0)
                        self.cells.append(cell)

    def pulse_once(self, duration=0.5, max_alpha=180):
        """Single pulse of the area."""
        half = duration / 2

        # Fade in all cells
        for cell in self.cells:
            anim = mcrfpy.Animation("a", float(max_alpha), half, "easeOut")
            anim.start(cell.color)

        # Fade out after delay
        def fade_out(timer_name):
            for cell in self.cells:
                anim = mcrfpy.Animation("a", 0.0, half, "easeIn")
                anim.start(cell.color)

        mcrfpy.Timer("area_fade", fade_out, int(half * 1000), once=True)

    def start_continuous(self, period=1.0, max_alpha=150):
        """Start continuous pulsing."""
        self.is_pulsing = True
        self._pulse_up(period, max_alpha)

    def _pulse_up(self, period, max_alpha):
        if not self.is_pulsing:
            return

        half = period / 2
        for cell in self.cells:
            anim = mcrfpy.Animation("a", float(max_alpha), half, "easeInOut")
            anim.start(cell.color)

        def next_phase(timer_name):
            self._pulse_down(period, max_alpha)

        mcrfpy.Timer("area_up", next_phase, int(half * 1000), once=True)

    def _pulse_down(self, period, max_alpha):
        if not self.is_pulsing:
            return

        half = period / 2
        for cell in self.cells:
            anim = mcrfpy.Animation("a", 0.0, half, "easeInOut")
            anim.start(cell.color)

        def next_phase(timer_name):
            self._pulse_up(period, max_alpha)

        mcrfpy.Timer("area_down", next_phase, int(half * 1000), once=True)

    def stop(self):
        """Stop pulsing and clear."""
        self.is_pulsing = False
        for cell in self.cells:
            anim = mcrfpy.Animation("a", 0.0, 0.2, "easeOut")
            anim.start(cell.color)


# Usage
area = AreaPulse(grid)

# Highlight a room
area.set_rect(5, 5, 4, 4, (100, 200, 255))
area.start_continuous(period=2.0)

# Or highlight explosion radius
area.set_circle(10, 10, 3, (255, 100, 0))
area.pulse_once(duration=0.8)
```

## Ripple Effect

Animate an expanding ring of color:

```python
import mcrfpy

def ripple_effect(grid, center_x, center_y, color, max_radius=5, duration=1.0):
    """
    Create an expanding ripple effect.

    Args:
        grid: Grid with color layer
        center_x, center_y: Ripple origin
        color: RGB tuple
        max_radius: Maximum ripple size
        duration: Total animation time
    """
    # Get color layer
    color_layer = None
    for layer in grid.layers:
        if isinstance(layer, mcrfpy.ColorLayer):
            color_layer = layer
            break

    if not color_layer:
        grid.add_layer("color")
        color_layer = grid.layers[-1]

    step_duration = duration / max_radius

    for radius in range(max_radius + 1):
        # Get cells at this radius (ring, not filled)
        ring_cells = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                dist_sq = dx * dx + dy * dy
                # Include cells approximately on the ring edge
                if radius * radius - radius <= dist_sq <= radius * radius + radius:
                    cell = color_layer.at(center_x + dx, center_y + dy)
                    if cell:
                        ring_cells.append(cell)

        # Schedule this ring to animate
        def animate_ring(timer_name, cells=ring_cells, c=color):
            for cell in cells:
                cell.color = mcrfpy.Color(c[0], c[1], c[2], 200)
                # Fade out
                anim = mcrfpy.Animation("a", 0.0, step_duration * 2, "easeOut")
                anim.start(cell.color)

        delay = int(radius * step_duration * 1000)
        mcrfpy.Timer(f"ripple_{radius}", animate_ring, delay, once=True)


# Usage
ripple_effect(grid, 10, 10, (100, 200, 255), max_radius=6, duration=0.8)
```

## Key Concepts

1. **ColorLayer**: Grid overlay for cell-based color effects
2. **Alpha animation**: Animate `a` property for fade in/out
3. **Timer coordination**: Use timers to sequence fade up/down phases
4. **ID tracking**: Track pulse IDs to prevent orphaned animations when stopping

## Tips

- Use lower `max_alpha` (120-180) for subtle, non-intrusive highlights
- Longer periods (1.5-2.0s) feel calmer; shorter (0.5-0.8s) feel urgent
- Combine with other effects (floating text, sound) for important events
- Consider color blindness: don't rely solely on color for meaning
- Clean up pulses when cells become irrelevant (player moves, item collected)
