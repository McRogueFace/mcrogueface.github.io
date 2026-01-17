---
layout: default
title: Animation System
---

# Animation System

The Animation System provides smooth property transitions for UI elements and entities. Animate position, size, color, and other properties with configurable easing functions and completion callbacks.

## Overview

Animations in McRogueFace work by interpolating a property from its current value to a target value over a duration. The `.animate()` method is available on all UI elements.

```python
# Move a sprite from current position to (200, 100) over 0.5 seconds
sprite.animate("x", 200, duration=0.5, easing="easeOutQuad")
sprite.animate("y", 100, duration=0.5, easing="easeOutQuad")
```

## Objects

| Object | Purpose |
|--------|---------|
| [Animation](../objects/Animation) | Property interpolation with easing |

---

## The animate() Method {#animate-method}

All UI elements and entities have an `.animate()` method.

### Signature

```python
element.animate(
    property: str,
    target: float,
    duration: float = 1.0,
    easing: str = "linear",
    callback: callable = None
)
```

- `property`: Name of the property to animate ("x", "y", "scale", etc.)
- `target`: Target value at end of animation
- `duration`: Animation duration in seconds
- `easing`: Easing function name
- `callback`: Function called when animation completes

### Animatable Properties

**Position and Size:**
- `x`, `y` - Position
- `w`, `h` - Size (for Frame, Grid)
- `scale` - Scale factor (for Sprite, Entity)

**Visual:**
- `opacity` - Transparency (0.0 to 1.0)
- `zoom` - Camera zoom (for Grid)

**Entity-specific:**
- `sprite_index` - Animated sprite sequences (discrete)

---

## Easing Functions {#easing}

Easing functions control the rate of change during animation.

### Linear
```python
element.animate("x", 100, easing="linear")
```
Constant speed from start to finish.

### Ease In (Accelerating)
```python
element.animate("x", 100, easing="easeInQuad")    # Quadratic
element.animate("x", 100, easing="easeInCubic")   # Cubic
element.animate("x", 100, easing="easeInExpo")    # Exponential
```
Starts slow, accelerates toward the end.

### Ease Out (Decelerating)
```python
element.animate("x", 100, easing="easeOutQuad")   # Quadratic
element.animate("x", 100, easing="easeOutCubic")  # Cubic
element.animate("x", 100, easing="easeOutExpo")   # Exponential
element.animate("x", 100, easing="easeOutBounce") # Bounce effect
```
Starts fast, decelerates toward the end.

### Ease In-Out (Smooth)
```python
element.animate("x", 100, easing="easeInOutQuad")
element.animate("x", 100, easing="easeInOutCubic")
```
Smooth acceleration and deceleration.

---

## Completion Callbacks {#callbacks}

Execute code when an animation finishes using the `callback` parameter.

### Basic Callback

```python
def on_complete():
    print("Animation finished!")

sprite.animate("x", 200, duration=1.0, callback=on_complete)
```

### Chained Animations

Chain animations by starting the next in a callback:

```python
def move_right():
    sprite.animate("x", 200, callback=move_down)

def move_down():
    sprite.animate("y", 200, callback=move_left)

def move_left():
    sprite.animate("x", 0, callback=move_up)

def move_up():
    sprite.animate("y", 0, callback=move_right)

move_right()  # Start infinite square movement
```

### State Changes

Use callbacks to change game state after animations:

```python
def on_death_animation_complete():
    grid.entities.remove(enemy)
    check_victory_condition()

enemy.animate("opacity", 0, duration=0.3, callback=on_death_animation_complete)
```

---

## Animation Patterns {#patterns}

### Smooth Entity Movement

```python
def move_entity(entity, target_x, target_y, duration=0.2):
    entity.animate("x", target_x, duration=duration, easing="easeOutQuad")
    entity.animate("y", target_y, duration=duration, easing="easeOutQuad")

# Player moves smoothly instead of snapping
move_entity(player, player.x + 1, player.y)
```

### Damage Flash

```python
def flash_damage(entity):
    original = entity.color
    entity.color = mcrfpy.Color(255, 0, 0)

    def restore():
        entity.color = original

    mcrfpy.Timer("flash", restore, 100)
```

### Screen Shake

```python
import random

def screen_shake(grid, intensity=5, duration=0.3):
    original_x, original_y = grid.x, grid.y
    shake_count = [0]

    def shake():
        shake_count[0] += 1
        if shake_count[0] > duration * 20:
            grid.x, grid.y = original_x, original_y
            mcrfpy.Timer.cancel("shake")
            return

        grid.x = original_x + random.randint(-intensity, intensity)
        grid.y = original_y + random.randint(-intensity, intensity)

    mcrfpy.Timer("shake", shake, 50)
```

### Floating Text

```python
def floating_text(scene, text, x, y):
    caption = mcrfpy.Caption(pos=(x, y), text=text)
    caption.color = mcrfpy.Color(255, 255, 0)
    scene.children.append(caption)

    def remove():
        scene.children.remove(caption)

    caption.animate("y", y - 30, duration=0.5, easing="easeOutQuad")
    caption.animate("opacity", 0, duration=0.5, callback=remove)
```

---

## Related Objects

<div class="related-objects">
<div class="object-links">
<a href="../objects/Animation" class="object-link">Animation</a>
<a href="../objects/Timer" class="object-link">Timer</a>
<a href="../objects/Entity" class="object-link">Entity</a>
<a href="../objects/Sprite" class="object-link">Sprite</a>
</div>
</div>
