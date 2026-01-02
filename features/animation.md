# Animation System

McRogueFace provides a built-in animation system for smooth property transitions. Animate positions, colors, opacity, and more with easing functions and completion callbacks.

## Basic Animation

Create an animation by specifying the property to animate, target value, duration, and easing:

```python
import mcrfpy

# Create a frame
frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
frame.fill_color = mcrfpy.Color(255, 0, 0)

# Animate x position from current to 500 over 2 seconds
anim = mcrfpy.Animation("x", 500.0, 2.0, "easeInOut")
anim.start(frame)
```

## Animation Constructor

```python
mcrfpy.Animation(property, target, duration, easing, callback=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `property` | str | Name of the property to animate |
| `target` | float | Target value to animate toward |
| `duration` | float | Duration in seconds |
| `easing` | str | Easing function name |
| `callback` | callable | Optional function called when animation completes |

## Animatable Properties

### Position and Size

```python
# Position
mcrfpy.Animation("x", 200.0, 1.0, "linear").start(element)
mcrfpy.Animation("y", 150.0, 1.0, "linear").start(element)

# Size (for frames)
mcrfpy.Animation("w", 300.0, 0.5, "easeOut").start(frame)
mcrfpy.Animation("h", 200.0, 0.5, "easeOut").start(frame)
```

### Scale

```python
# Uniform scale
mcrfpy.Animation("scale", 2.0, 1.0, "easeInOut").start(sprite)

# Non-uniform scale
mcrfpy.Animation("scale_x", 1.5, 0.5, "easeIn").start(sprite)
mcrfpy.Animation("scale_y", 2.0, 0.5, "easeIn").start(sprite)
```

### Opacity

```python
# Fade out
mcrfpy.Animation("opacity", 0.0, 1.0, "easeOut").start(element)

# Fade in
element.opacity = 0.0
mcrfpy.Animation("opacity", 1.0, 0.5, "easeIn").start(element)
```

### Color Components

```python
# Animate individual color channels
mcrfpy.Animation("r", 255, 0.5, "linear").start(element.fill_color)
mcrfpy.Animation("g", 0, 0.5, "linear").start(element.fill_color)
mcrfpy.Animation("b", 128, 0.5, "linear").start(element.fill_color)
mcrfpy.Animation("a", 200, 0.5, "linear").start(element.fill_color)
```

## Easing Functions

Easing functions control the rate of change during animation:

| Easing | Description | Use Case |
|--------|-------------|----------|
| `"linear"` | Constant speed | Mechanical movement, progress bars |
| `"easeIn"` | Slow start, fast end | Objects falling, acceleration |
| `"easeOut"` | Fast start, slow end | Deceleration, landing |
| `"easeInOut"` | Slow start and end | UI transitions, smooth movement |

### Visual Comparison

```
linear:     ████████████████
easeIn:     ▁▂▃▄▅▆▇████████
easeOut:    ████████▇▆▅▄▃▂▁
easeInOut:  ▁▂▄▆████████▆▄▂▁
```

## Callbacks

Execute code when an animation completes:

```python
def on_complete(animation, target):
    print("Animation finished!")
    # Start another animation, change state, etc.

anim = mcrfpy.Animation("x", 500.0, 1.0, "easeInOut", callback=on_complete)
anim.start(frame)
```

### Chaining Animations

```python
def move_back(anim, target):
    # Return to start
    mcrfpy.Animation("x", 0.0, 1.0, "easeInOut").start(target)

def move_forward(anim, target):
    # Move right, then move back
    return_anim = mcrfpy.Animation("x", 500.0, 1.0, "easeInOut", callback=move_back)
    return_anim.start(target)

# Start the chain
move_forward(None, frame)
```

## Multiple Simultaneous Animations

Animate multiple properties at once:

```python
# Animate position and size together
mcrfpy.Animation("x", 200.0, 1.0, "easeInOut").start(frame)
mcrfpy.Animation("y", 150.0, 1.0, "easeInOut").start(frame)
mcrfpy.Animation("w", 300.0, 1.0, "easeInOut").start(frame)
mcrfpy.Animation("h", 200.0, 1.0, "easeInOut").start(frame)

# Fade while moving
mcrfpy.Animation("x", 400.0, 2.0, "easeInOut").start(element)
mcrfpy.Animation("opacity", 0.0, 2.0, "easeIn").start(element)
```

## Path Animation Pattern

Animate an entity smoothly along a pathfinding result:

```python
class PathAnimator:
    """Animate an entity along a path step by step."""

    def __init__(self, entity, path, step_duration=0.3, on_complete=None):
        self.entity = entity
        self.path = path
        self.step_duration = step_duration
        self.on_complete = on_complete
        self.current_step = 0
        self.animating = False

    def start(self):
        """Begin path animation."""
        if not self.path or self.animating:
            return

        self.current_step = 0
        self.animating = True
        self._animate_next_step()

    def _animate_next_step(self):
        """Animate to the next position in the path."""
        if self.current_step >= len(self.path):
            self.animating = False
            if self.on_complete:
                self.on_complete()
            return

        target_x, target_y = self.path[self.current_step]

        # Create position animations
        anim_x = mcrfpy.Animation("x", float(target_x), self.step_duration, "easeInOut")
        anim_y = mcrfpy.Animation("y", float(target_y), self.step_duration, "easeInOut",
                                   callback=self._on_step_complete)

        anim_x.start(self.entity)
        anim_y.start(self.entity)

    def _on_step_complete(self, anim, target):
        """Called when a single step animation finishes."""
        self.current_step += 1
        self._animate_next_step()


# Usage
path = player.path_to(20, 15)
if path:
    animator = PathAnimator(player, path, step_duration=0.2)
    animator.start()
```

## UI Animation Examples

### Slide-in Panel

```python
def show_panel(panel):
    """Slide panel in from the right."""
    panel.x = 800  # Start off-screen
    panel.visible = True
    mcrfpy.Animation("x", 500.0, 0.3, "easeOut").start(panel)

def hide_panel(panel):
    """Slide panel out to the right."""
    def on_hidden(anim, target):
        target.visible = False

    mcrfpy.Animation("x", 800.0, 0.3, "easeIn", callback=on_hidden).start(panel)
```

### Pulsing Effect

```python
def pulse_element(element):
    """Create a pulsing scale effect."""
    def grow(anim, target):
        mcrfpy.Animation("scale", 1.0, 0.5, "easeInOut", callback=shrink).start(target)

    def shrink(anim, target):
        mcrfpy.Animation("scale", 1.2, 0.5, "easeInOut", callback=grow).start(target)

    # Start the cycle
    shrink(None, element)
```

### Damage Flash

```python
def damage_flash(entity):
    """Flash entity red then back to normal."""
    original_color = entity.fill_color

    def restore_color(anim, target):
        mcrfpy.Animation("r", original_color.r, 0.1, "linear").start(target.fill_color)
        mcrfpy.Animation("g", original_color.g, 0.1, "linear").start(target.fill_color)
        mcrfpy.Animation("b", original_color.b, 0.1, "linear").start(target.fill_color)

    # Flash to red
    entity.fill_color = mcrfpy.Color(255, 0, 0)

    # Wait then restore
    mcrfpy.setTimer("damage_flash", lambda dt: restore_color(None, entity), 100)
    mcrfpy.setTimer("damage_flash_cleanup", lambda dt: mcrfpy.delTimer("damage_flash"), 200)
```

### Floating Damage Numbers

```python
def show_damage_number(x, y, damage):
    """Display floating damage number that fades up."""
    text = mcrfpy.Caption(
        pos=(x, y),
        text=str(damage),
        font_size=16
    )
    text.fill_color = mcrfpy.Color(255, 100, 100)
    mcrfpy.sceneUI("game").append(text)

    def remove_text(anim, target):
        mcrfpy.sceneUI("game").remove(target)

    # Float up and fade out
    mcrfpy.Animation("y", y - 30, 1.0, "easeOut").start(text)
    mcrfpy.Animation("opacity", 0.0, 1.0, "easeIn", callback=remove_text).start(text)
```

## Complete Example

```python
import mcrfpy

# Setup scene
mcrfpy.createScene("animation_demo")
mcrfpy.setScene("animation_demo")
ui = mcrfpy.sceneUI("animation_demo")

# Create animated elements
box = mcrfpy.Frame(pos=(50, 50), size=(100, 100))
box.fill_color = mcrfpy.Color(255, 0, 0)
ui.append(box)

label = mcrfpy.Caption(pos=(400, 300), text="Animation Demo")
label.fill_color = mcrfpy.Color(255, 255, 255)
ui.append(label)

# Animation state
animation_running = False

def run_demo():
    global animation_running
    if animation_running:
        return
    animation_running = True

    # Step 1: Move box to center
    def step2(anim, target):
        # Step 2: Grow the box
        mcrfpy.Animation("w", 200.0, 0.5, "easeInOut").start(target)
        mcrfpy.Animation("h", 200.0, 0.5, "easeInOut", callback=step3).start(target)

    def step3(anim, target):
        # Step 3: Change color to blue
        mcrfpy.Animation("r", 0, 0.5, "linear").start(target.fill_color)
        mcrfpy.Animation("b", 255, 0.5, "linear", callback=step4).start(target.fill_color)

    def step4(anim, target):
        # Step 4: Fade out
        mcrfpy.Animation("opacity", 0.0, 1.0, "easeIn", callback=step5).start(box)

    def step5(anim, target):
        # Reset for next run
        global animation_running
        box.x = 50
        box.y = 50
        box.w = 100
        box.h = 100
        box.fill_color = mcrfpy.Color(255, 0, 0)
        box.opacity = 1.0
        animation_running = False

    # Start the sequence
    mcrfpy.Animation("x", 362.0, 0.5, "easeInOut").start(box)
    mcrfpy.Animation("y", 284.0, 0.5, "easeInOut", callback=step2).start(box)

# Input handler
def on_key(key, action):
    if action == "start" and key.lower() == "space":
        run_demo()

mcrfpy.keypressScene(on_key)

# Instructions
instructions = mcrfpy.Caption(pos=(300, 550), text="Press SPACE to run animation")
instructions.fill_color = mcrfpy.Color(200, 200, 200)
ui.append(instructions)
```

## Performance Considerations

- Animations are processed every frame by the engine
- Many simultaneous animations on the same property may conflict
- For complex sequences, manage state carefully to avoid overlapping animations
- Use callbacks for sequencing rather than timers when possible

## Notes and Caveats

- Animation targets must be numeric (float or int)
- Color animations target individual r, g, b, a components
- Starting a new animation on the same property interrupts the previous one
- The callback receives `(animation, target)` arguments
- Duration is in seconds, not milliseconds
- Animations continue even when elements are not visible

## Related Topics

- [Grid System](grid_system.md) - Animating entities on grids
- [Pathfinding](pathfinding.md) - Getting paths to animate along
- [Scene Management](scenes.md) - Scene transition animations
