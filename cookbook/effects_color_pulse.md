---
mcrf:
  objects: [ColorLayer, Color, Grid, Timer]
  diataxis: howto
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Color Pulse Effect

Animate a grid cell's color layer to pulse, useful for highlighting interactable tiles, objectives, warnings, or magical effects.

`ColorLayer` stores plain `Color` values per cell — `layer.at(x, y)` returns a
snapshot `Color`, not a live, animatable object, and `ColorLayer` itself has no
`.animate()` method (only `Drawable`/`Entity`-family objects do). So a "pulse"
is driven by a repeating `mcrfpy.Timer` that recomputes the alpha each tick and
writes it back with `layer.set((x, y), color)`.

## Quick Example

```python
import mcrfpy
import math

def get_or_create_layer(grid, name="pulse", z_index=1):
    """Find grid's named ColorLayer, or create and attach one."""
    existing = grid.layer(name)
    if existing is not None:
        return existing
    layer = mcrfpy.ColorLayer(z_index=z_index, name=name)
    grid.add_layer(layer)
    return layer

def pulse_cell(grid, x, y, color, duration=1.0):
    """
    Pulse a cell's color overlay from transparent to visible and back once.

    Args:
        grid: Grid to overlay
        x, y: Cell coordinates
        color: RGB tuple (r, g, b)
        duration: Full cycle duration in seconds
    """
    layer = get_or_create_layer(grid)
    r, g, b = color
    half_duration = duration / 2.0
    state = {"t0": None}

    def tick(timer, runtime):
        if state["t0"] is None:
            state["t0"] = runtime
        t = (runtime - state["t0"]) / 1000.0
        if t >= duration:
            layer.set((x, y), mcrfpy.Color(r, g, b, 0))
            timer.stop()
            return
        # Triangle wave: 0 -> 1 over the first half, 1 -> 0 over the second
        phase = t / half_duration
        alpha_frac = phase if phase <= 1.0 else 2.0 - phase
        layer.set((x, y), mcrfpy.Color(r, g, b, int(200 * alpha_frac)))

    mcrfpy.Timer(f"pulse_{x}_{y}", tick, 33)


# Usage
scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

grid = mcrfpy.Grid(grid_size=(16, 12), pos=(0, 0), size=(512, 384))
scene.children.append(grid)

pulse_cell(grid, 5, 5, (255, 200, 0), duration=1.5)  # Golden pulse
```

## Continuous Pulsing

Keep a cell pulsing until stopped, using a single repeating `Timer` driven by
`math.sin` instead of chained one-shot animations:

```python
import mcrfpy
import math

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
        self.layer = self._get_or_create_layer()
        self.timer = None
        self.t0 = None

    def _get_or_create_layer(self):
        """Ensure a named color layer exists on the grid."""
        existing = self.grid.layer("pulse")
        if existing is not None:
            return existing
        layer = mcrfpy.ColorLayer(z_index=1, name="pulse")
        self.grid.add_layer(layer)
        return layer

    def _tick(self, timer, runtime):
        if not self.is_pulsing:
            return
        if self.t0 is None:
            self.t0 = runtime
        r, g, b = self.color
        # Sine wave oscillating between 0 and max_alpha
        t = (runtime - self.t0) / 1000.0
        wave = (math.sin(2 * math.pi * t / self.period) + 1.0) / 2.0
        alpha = int(self.max_alpha * wave)
        self.layer.set((self.x, self.y), mcrfpy.Color(r, g, b, alpha))

    def start(self):
        """Start continuous pulsing."""
        if self.is_pulsing:
            return
        self.is_pulsing = True
        self.t0 = None
        self.timer = mcrfpy.Timer(f"pulse_{id(self)}", self._tick, 33)

    def stop(self):
        """Stop pulsing and clear the cell."""
        self.is_pulsing = False
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        r, g, b = self.color
        self.layer.set((self.x, self.y), mcrfpy.Color(r, g, b, 0))

    def set_color(self, color):
        """Change pulse color for subsequent ticks."""
        self.color = color


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

Pulse a group of cells together with one shared timer:

```python
import mcrfpy
import math

class AreaPulse:
    """Pulse a rectangular or circular area."""

    def __init__(self, grid):
        self.grid = grid
        self.cells = []  # list of (x, y)
        self.is_pulsing = False
        self.timer = None
        self.color_layer = self._get_or_create_layer()

    def _get_or_create_layer(self):
        existing = self.grid.layer("area_pulse")
        if existing is not None:
            return existing
        layer = mcrfpy.ColorLayer(z_index=1, name="area_pulse")
        self.grid.add_layer(layer)
        return layer

    def set_rect(self, x, y, width, height, color):
        """Set a rectangular area to pulse."""
        self.color = color
        self.cells = [
            (x + dx, y + dy)
            for dy in range(height)
            for dx in range(width)
        ]

    def set_circle(self, center_x, center_y, radius, color):
        """Set a circular area to pulse."""
        self.color = color
        self.cells = [
            (center_x + dx, center_y + dy)
            for dy in range(-radius, radius + 1)
            for dx in range(-radius, radius + 1)
            if dx * dx + dy * dy <= radius * radius
        ]

    def _write(self, alpha):
        r, g, b = self.color
        for (x, y) in self.cells:
            self.color_layer.set((x, y), mcrfpy.Color(r, g, b, alpha))

    def pulse_once(self, duration=0.5, max_alpha=180):
        """Single pulse of the area: fade in, then fade out."""
        half = duration / 2.0
        state = {"t0": None}

        def tick(timer, runtime):
            if state["t0"] is None:
                state["t0"] = runtime
            t = (runtime - state["t0"]) / 1000.0
            if t >= duration:
                self._write(0)
                timer.stop()
                return
            phase = t / half
            frac = phase if phase <= 1.0 else 2.0 - phase
            self._write(int(max_alpha * frac))

        mcrfpy.Timer(f"area_once_{id(self)}", tick, 33)

    def start_continuous(self, period=1.0, max_alpha=150):
        """Start continuous pulsing of the area."""
        self.is_pulsing = True
        state = {"t0": None}

        def tick(timer, runtime):
            if not self.is_pulsing:
                return
            if state["t0"] is None:
                state["t0"] = runtime
            t = (runtime - state["t0"]) / 1000.0
            wave = (math.sin(2 * math.pi * t / period) + 1.0) / 2.0
            self._write(int(max_alpha * wave))

        self.timer = mcrfpy.Timer(f"area_continuous_{id(self)}", tick, 33)

    def stop(self):
        """Stop pulsing and clear."""
        self.is_pulsing = False
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        self._write(0)


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

Animate an expanding ring of color, each ring fading independently:

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
    layer = grid.layer("ripple")
    if layer is None:
        layer = mcrfpy.ColorLayer(z_index=1, name="ripple")
        grid.add_layer(layer)

    step_duration = duration / max_radius
    r, g, b = color

    for radius in range(max_radius + 1):
        # Cells approximately on the ring edge at this radius
        ring_cells = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                dist_sq = dx * dx + dy * dy
                if radius * radius - radius <= dist_sq <= radius * radius + radius:
                    ring_cells.append((center_x + dx, center_y + dy))

        fade_duration = step_duration * 2

        def make_ring_animator(cells):
            state = {"t0": None}

            def tick(timer, runtime):
                if state["t0"] is None:
                    state["t0"] = runtime
                t = (runtime - state["t0"]) / 1000.0
                frac = max(0.0, 1.0 - t / fade_duration)
                alpha = int(200 * frac)
                for cx, cy in cells:
                    layer.set((cx, cy), mcrfpy.Color(r, g, b, alpha))
                if t >= fade_duration:
                    for cx, cy in cells:
                        layer.set((cx, cy), mcrfpy.Color(r, g, b, 0))
                    timer.stop()
            return tick

        def start_ring(timer, runtime, cells=ring_cells):
            mcrfpy.Timer(f"ripple_fade_{id(cells)}", make_ring_animator(cells), 33)
            timer.stop()

        delay = int(radius * step_duration * 1000)
        mcrfpy.Timer(f"ripple_{radius}", start_ring, max(delay, 1), once=True)


# Usage
ripple_effect(grid, 10, 10, (100, 200, 255), max_radius=6, duration=0.8)
```

## Key Concepts

1. **ColorLayer**: Grid overlay for cell-based color effects; created standalone
   with `mcrfpy.ColorLayer(z_index=..., name=...)` and attached with
   `grid.add_layer(layer)` (never `grid.add_layer("color")` — the argument is
   always a layer object). Look layers up with `grid.layer(name)`.
2. **No live cell handle**: `layer.at(x, y)` returns a snapshot `Color`, and
   `ColorLayer` has no `.animate()`. Pulsing means recomputing alpha yourself
   (triangle wave for a single pulse, `math.sin` for continuous) and writing
   it with `layer.set((x, y), color)` on every `Timer` tick.
3. **Timer coordination**: A repeating `mcrfpy.Timer(name, callback, interval_ms)`
   drives each pulse; the callback receives `(timer, runtime_ms)`, where
   `runtime_ms` is the total engine runtime in milliseconds (NOT relative to
   when the timer started); one-shot effects should record the runtime of
   their first tick and measure elapsed time from it. Call `timer.stop()`
   to end it.
4. **Alpha animation**: All effects here only animate the `a` channel of a
   `Color`, leaving `r`, `g`, `b` fixed.

## Tips

- Use lower `max_alpha` (120-180) for subtle, non-intrusive highlights
- Longer periods (1.5-2.0s) feel calmer; shorter (0.5-0.8s) feel urgent
- Combine with other effects (floating text, sound) for important events
- Consider color blindness: don't rely solely on color for meaning
- Clean up pulses when cells become irrelevant (player moves, item collected) —
  always call `timer.stop()`, since a running `Timer` keeps firing even if its
  target cell no longer matters
