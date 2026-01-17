---
layout: default
title: Animation
---

# Animation

Interpolates property values over time with easing functions.

## Overview

The `Animation` class provides smooth property transitions for UI elements and entities. Animations interpolate numeric values over a specified duration using configurable easing functions. Use the `animate()` method on any drawable object for the simplest approach, or create Animation objects directly for more control.

## Quick Reference

```python
import mcrfpy

# Preferred: Use the animate() method on any drawable
frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
frame.animate("x", 500, duration=2.0, easing=mcrfpy.Easing.EASE_OUT_QUAD)

# With completion callback
def on_done():
    print("Animation complete!")

sprite.animate("opacity", 0.0, duration=1.0, callback=on_done)

# Delta mode (relative change)
frame.animate("y", 50, duration=0.5, delta=True)  # Move 50 pixels down

# Direct Animation object (advanced)
anim = mcrfpy.Animation(
    "x", 200.0, 1.5,
    easing="easeInOutQuad",
    delta=False,
    callback=my_callback
)
anim.start(target_object)
```

## Constructor

```python
mcrfpy.Animation(
    property: str,
    target: float,
    duration: float,
    easing: str = "linear",
    delta: bool = False,
    callback: callable = None
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `property` | str | required | Property name to animate |
| `target` | float | required | Target value (or delta if delta=True) |
| `duration` | float | required | Animation duration in seconds |
| `easing` | str | "linear" | Easing function name |
| `delta` | bool | False | If True, target is relative change |
| `callback` | callable | None | Called when animation completes |

## Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `duration` | float | read-only | Total duration in seconds |
| `elapsed` | float | read-only | Time elapsed since start |
| `is_complete` | bool | read-only | True when animation finished |
| `is_delta` | bool | read-only | Whether using delta mode |
| `property` | str | read-only | Name of animated property |

## Methods

| Method | Description |
|--------|-------------|
| `start(target, conflict_mode='replace')` | Begin animating the target object |
| `complete()` | Immediately finish the animation |
| `update(delta_time)` | Advance animation by delta time |
| `get_current_value()` | Get the current interpolated value |
| `hasValidTarget()` | Check if target object still exists |

### start()

```python
anim.start(target, conflict_mode='replace')
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target` | drawable | required | Object to animate |
| `conflict_mode` | str | 'replace' | How to handle existing animations: 'replace', 'cancel', 'parallel' |

## Animatable Properties

These properties can be animated on UI elements:

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | float | Position coordinates |
| `w`, `h` | float | Size dimensions |
| `pos` | tuple | Position as (x, y) |
| `size` | tuple | Size as (w, h) |
| `fill_color` | Color | Background color |
| `outline_color` | Color | Border color |
| `outline` | float | Border thickness |
| `opacity` | float | Transparency (0.0-1.0) |
| `scale` | float | Scale factor |

### Grid-Specific Properties

| Property | Type | Description |
|----------|------|-------------|
| `center` | tuple | Camera center position (pixels) |
| `zoom` | float | Camera zoom level |

### Sprite/Entity Properties

| Property | Type | Description |
|----------|------|-------------|
| `sprite_index` | int | Current sprite frame |

### Caption Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | str | Caption text content |

## Easing Functions

Access easing functions via the `mcrfpy.Easing` enum:

### Linear
- `Easing.LINEAR` - Constant speed

### Quadratic
- `Easing.EASE_IN_QUAD` - Accelerate from zero
- `Easing.EASE_OUT_QUAD` - Decelerate to zero
- `Easing.EASE_IN_OUT_QUAD` - Accelerate then decelerate

### Cubic
- `Easing.EASE_IN_CUBIC` - Stronger acceleration
- `Easing.EASE_OUT_CUBIC` - Stronger deceleration
- `Easing.EASE_IN_OUT_CUBIC` - Stronger ease in/out

### Quartic
- `Easing.EASE_IN_QUART`
- `Easing.EASE_OUT_QUART`
- `Easing.EASE_IN_OUT_QUART`

### Exponential
- `Easing.EASE_IN_EXPO` - Exponential acceleration
- `Easing.EASE_OUT_EXPO` - Exponential deceleration
- `Easing.EASE_IN_OUT_EXPO`

### Back (Overshoot)
- `Easing.EASE_IN_BACK` - Pull back then accelerate
- `Easing.EASE_OUT_BACK` - Overshoot then settle
- `Easing.EASE_IN_OUT_BACK`

### Bounce
- `Easing.EASE_OUT_BOUNCE` - Bounce effect at end

### Elastic
- `Easing.EASE_IN_ELASTIC` - Elastic snap at start
- `Easing.EASE_OUT_ELASTIC` - Elastic snap at end
- `Easing.EASE_IN_OUT_ELASTIC`

## Examples

### Basic Position Animation

```python
import mcrfpy

frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
scene.children.append(frame)

# Slide to the right
frame.animate("x", 500, duration=1.0, easing=mcrfpy.Easing.EASE_OUT_QUAD)
```

### Fade Out Effect

```python
def fade_and_remove():
    def on_fade_complete():
        scene.children.remove(frame)

    frame.animate("opacity", 0.0, duration=0.5, callback=on_fade_complete)
```

### Chained Animations

```python
def animate_sequence(sprite):
    def step2():
        sprite.animate("y", 100, duration=0.3, callback=step3)

    def step3():
        sprite.animate("x", 0, duration=0.3, callback=step4)

    def step4():
        sprite.animate("y", 0, duration=0.3)

    # Start the chain
    sprite.animate("x", 100, duration=0.3, callback=step2)
```

### Pulsing Effect

```python
def create_pulse(element):
    def pulse_out():
        element.animate("scale", 1.0, duration=0.5,
                       easing=mcrfpy.Easing.EASE_IN_OUT_QUAD,
                       callback=pulse_in)

    def pulse_in():
        element.animate("scale", 1.2, duration=0.5,
                       easing=mcrfpy.Easing.EASE_IN_OUT_QUAD,
                       callback=pulse_out)

    pulse_in()
```

### Camera Pan

```python
# Smoothly pan grid camera to player position
def focus_on_player(grid, player):
    target_x = player.x * grid.cell_width
    target_y = player.y * grid.cell_height

    grid.animate("center", (target_x, target_y),
                duration=0.3,
                easing=mcrfpy.Easing.EASE_OUT_CUBIC)
```

### Delta Mode (Relative Animation)

```python
# Move 100 pixels right from current position
frame.animate("x", 100, duration=0.5, delta=True)

# Useful for repeated movements
def hop():
    sprite.animate("y", -20, duration=0.2, delta=True, callback=land)

def land():
    sprite.animate("y", 20, duration=0.2, delta=True)
```

### Color Animation

```python
# Animate fill color (animates all RGBA components)
frame.animate("fill_color", mcrfpy.Color(255, 0, 0, 255),
             duration=1.0)

# Flash effect
def flash_red(element):
    original = element.fill_color
    element.fill_color = mcrfpy.Color(255, 0, 0)
    element.animate("fill_color", original, duration=0.3)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Easing" class="object-link">Easing</a>
<a href="Timer" class="object-link">Timer</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Sprite" class="object-link">Sprite</a>
<a href="Caption" class="object-link">Caption</a>
<a href="Grid" class="object-link">Grid</a>
<a href="Entity" class="object-link">Entity</a>
</div>
</div>
