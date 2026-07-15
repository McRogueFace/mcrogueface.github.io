---
layout: default
title: Animation
mcrf:
  objects: [Animation]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Animation

Property interpolation over time, created with the `animate()` method.

## Overview

There is **no constructible `mcrfpy.Animation` class**. Animations are created by calling `animate()` on the object you want to animate: every drawable (`Frame`, `Caption`, `Sprite`, `Grid`, `Line`, `Circle`, `Arc`) and `Entity` exposes it. The call creates the animation, starts it, and registers it with the engine's animation manager in one step, then returns an `Animation` handle you can use to monitor or cancel it.

The handle's type displays as `mcrfpy.Animation`, but the class is not exported from the module — the only way to obtain one is as the return value of `animate()`.

## Quick Reference

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
scene.children.append(frame)

# Animate a property: creates, starts, and registers the animation
frame.animate("x", 500.0, 2.0, mcrfpy.Easing.EASE_OUT_QUAD)

# With a completion callback
def on_done(target, prop, value):
    print(f"{prop} finished at {value}")

frame.animate("opacity", 0.0, 1.0, callback=on_done)

# The returned Animation handle can be inspected and controlled
anim = frame.animate("w", 300.0, 1.5)
print(anim.property, anim.duration, anim.is_complete)
anim.stop()  # cancel without applying the final value
```

## The animate() Method

```python
obj.animate(property, target, duration, easing=None, delta=False,
            loop=False, callback=None, conflict_mode='replace') -> Animation
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `property` | str | required | Name of the property to animate (see [Animatable Properties](#animatable-properties)) |
| `target` | varies | required | Target value; type depends on the property (see [Target Value Types](#target-value-types)) |
| `duration` | float | required | Animation duration in seconds |
| `easing` | Easing / str | None | `mcrfpy.Easing` enum value, legacy string name (e.g. `'easeInOut'`), or None for linear |
| `delta` | bool | False | If True, `target` is relative to the current value instead of absolute |
| `loop` | bool | False | If True, the animation repeats from the start when it reaches the end |
| `callback` | callable | None | Called once when the animation completes (never called for looping animations) |
| `conflict_mode` | str | 'replace' | `'replace'`, `'queue'`, or `'error'` — behavior when the property is already animating |

**Raises:**

- `ValueError` — the property name is not animatable on this object type, the easing string is unknown, or `conflict_mode` is not one of the three accepted values.
- `RuntimeError` — `conflict_mode='error'` and the property is already being animated.
- `TypeError` — `callback` is not callable.

`Entity.animate()` takes the same arguments; only its set of valid property names differs (see below).

### Callback Signature

The completion callback receives three arguments:

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
scene.children.append(frame)

def on_arrival(target, prop, value):
    # target: the Frame that was animated
    # prop:   "x"
    # value:  500.0
    print(f"{type(target).__name__}.{prop} reached {value}")

frame.animate("x", 500.0, 2.0, mcrfpy.Easing.EASE_OUT_CUBIC, callback=on_arrival)
```

The callback fires when the animation finishes naturally or when `complete()` is called on the handle. It does **not** fire when the animation is cancelled with `stop()`, and looping animations never fire it (they never complete).

### Conflict Handling

Each (object, property) pair can have only one active animation. `conflict_mode` controls what happens when you call `animate()` for a property that is already animating:

| Mode | Behavior |
|------|----------|
| `'replace'` (default) | The existing animation ends immediately (jumping to its final value) and the new one starts |
| `'queue'` | The new animation waits and starts when the current one finishes |
| `'error'` | Raises `RuntimeError` |

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
scene.children.append(frame)

frame.animate("x", 100.0, 1.0)

# replace (default): the running animation jumps to its final value,
# then the new animation starts
frame.animate("x", 200.0, 1.0)

# queue: run after the current animation on "x" finishes
frame.animate("x", 300.0, 1.0, conflict_mode="queue")

# error: raise RuntimeError if "x" is already animating
try:
    frame.animate("x", 400.0, 1.0, conflict_mode="error")
except RuntimeError as e:
    print(e)
```

Notes:

- When `animate()` is called from inside an animation callback, a replaced animation is cancelled in place rather than jumped to its final value.
- The per-property lock is released when the finished `Animation` object is destroyed, not at the moment it completes. If you hold a reference to a completed animation, a queued animation on the same property will not start until you drop that reference. When using `conflict_mode='queue'`, discard handles you don't need.
- Sub-properties are locked independently of their parent: `"fill_color"` and `"fill_color.a"` are separate keys and can animate simultaneously.

## The Animation Handle

`animate()` returns an `Animation` object. All of its data attributes are read-only.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `property` | str | Name of the property being animated |
| `duration` | float | Total duration in seconds |
| `elapsed` | float | Seconds since the animation started (clamped to `duration`) |
| `is_complete` | bool | True when `elapsed >= duration` or `complete()` was called |
| `is_delta` | bool | Whether the animation uses delta (relative) mode |
| `is_looping` | bool | Whether the animation repeats when it reaches the end |

### Methods

| Method | Description |
|--------|-------------|
| `complete()` | Jump to the final value immediately; fires the callback if one was set |
| `stop()` | Cancel without applying the final value; the callback is NOT fired |
| `get_current_value()` | Current interpolated value (type matches the property) |
| `hasValidTarget()` | True if the animated object still exists; animations self-clean when their target is destroyed |
| `start(target, conflict_mode='replace')` | Attach and start on a target object (used internally by `animate()`; rarely needed) |
| `update(delta_time)` | Advance by `delta_time` seconds; returns True while running (called automatically by the engine) |

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
scene.children.append(frame)

anim = frame.animate("x", 500.0, 2.0)

print(anim.property)      # "x"
print(anim.duration)      # 2.0
print(anim.elapsed)       # seconds since start
print(anim.is_complete)   # False until finished (or complete() called)
print(anim.get_current_value())  # current interpolated value

anim.complete()   # jump to x=500 immediately; fires the callback if set
print(frame.x)    # 500.0
```

## Animatable Properties

`animate()` raises `ValueError` for property names the object doesn't support. The lists below were verified against the engine (each name accepted or rejected at runtime).

### Frame

| Property | Value type | Description |
|----------|------------|-------------|
| `x`, `y`, `w`, `h` | float | Position and size |
| `pos`, `position` | (x, y) | Position as a pair |
| `size` | (w, h) | Size as a pair |
| `fill_color`, `outline_color` | (r, g, b[, a]) | Colors (all channels interpolate) |
| `fill_color.r/.g/.b/.a`, `outline_color.r/.g/.b/.a` | float | Individual color channels |
| `outline` | float | Outline thickness |
| `opacity` | float | 0.0 (transparent) to 1.0 (opaque) |
| `rotation` | float | Rotation in degrees |
| `origin`, `origin_x`, `origin_y` | (x, y) / float | Transform origin (rotation pivot) |

### Caption

Same as Frame, minus `w`/`h`/`size`-as-a-pair, plus:

| Property | Value type | Description |
|----------|------------|-------------|
| `text` | str | Typewriter-style text transition (see [Typewriter Text](#typewriter-text)) |
| `font_size` | float | Font size in points |
| `size` | float | Alias for `font_size` (a float here, unlike Frame's `size`) |

### Sprite

| Property | Value type | Description |
|----------|------------|-------------|
| `x`, `y`, `pos`, `position` | float / (x, y) | Position |
| `sprite_index` | int or list[int] | Texture frame; a list plays a frame sequence |
| `scale` | float | Uniform scale factor |
| `scale_x`, `scale_y` | float | Per-axis scale |
| `opacity` | float | 0.0 to 1.0 |
| `rotation` | float | Rotation in degrees |
| `origin`, `origin_x`, `origin_y` | (x, y) / float | Transform origin |
| `z_index` | float | Render order |

### Grid

Only the **camera** properties of a Grid are animatable:

| Property | Value type | Description |
|----------|------------|-------------|
| `center` | (x, y) | Camera center in **pixels** |
| `center_x`, `center_y` | float | Camera center components (pixels) |
| `zoom` | float | Camera zoom level |
| `camera_rotation` | float | Camera rotation in degrees |

A Grid's geometry (`x`, `y`, `w`, `h`, `pos`, `size`) and `fill_color` are not animatable — set them directly, or animate a parent Frame instead.

### Line, Circle, Arc

All three also accept `x`, `y`, `opacity`, `rotation`, `origin_x`, and `origin_y`. Whole-color animation is supported, but per-channel sub-properties (e.g. `color.r`) are not.

| Type | Properties |
|------|------------|
| `Line` | `start`, `end`, `start_x`, `start_y`, `end_x`, `end_y`, `thickness`, `color`, `origin` |
| `Circle` | `center`, `position`, `radius`, `outline`, `fill_color`, `outline_color`, `origin` |
| `Arc` | `center`, `radius`, `start_angle`, `end_angle`, `thickness`, `color` |

### Entity

Entities animate their **draw position** in tile coordinates; the logical cell (`cell_pos`) is unchanged by animation.

| Property | Value type | Description |
|----------|------------|-------------|
| `draw_x`, `draw_y` | float | Drawn position in tile coordinates (`x`/`y` accepted as aliases) |
| `sprite_index` | int or list[int] | Texture frame or frame sequence |
| `sprite_scale` | float | Sprite scale factor |
| `sprite_offset_x`, `sprite_offset_y` | float | Pixel offset of the sprite within its cell |

Uniforms exposed by a shader attached to a Sprite, Grid, or Entity are also accepted as animatable property names.

## Target Value Types

| Target type | Used for |
|-------------|----------|
| float | Numeric properties (`x`, `w`, `opacity`, `zoom`, `radius`, ...) |
| int | `sprite_index` |
| (r, g, b) or (r, g, b, a) | Color properties |
| (x, y) | Vector properties (`pos`, `size`, `center`, `start`, `end`) |
| list[int] | Sprite frame sequences (combine with `loop=True`) |
| str | `text` on Caption |

## Easing

Pass a `mcrfpy.Easing` enum value (preferred) or a legacy string name (`'linear'`, `'easeIn'`, `'easeOut'`, `'easeInOut'`, `'easeInQuad'`, `'easeOutBounce'`, ...). `None` means linear. Unknown string names raise `ValueError`. See [Easing](Easing) for the full list of enum values and guidance on choosing one.

## Examples

### Chained Animations

Each callback starts the next leg of the sequence:

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

frame = mcrfpy.Frame(pos=(0, 0), size=(50, 50))
scene.children.append(frame)

def step2(target, prop, value):
    target.animate("y", 100.0, 0.3, callback=step3)

def step3(target, prop, value):
    target.animate("x", 0.0, 0.3, callback=step4)

def step4(target, prop, value):
    target.animate("y", 0.0, 0.3)

# Trace a rectangle: each callback starts the next leg
frame.animate("x", 100.0, 0.3, callback=step2)
```

### Looping Sprite Frames

A list target with `loop=True` cycles through frames indefinitely:

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)
sprite = mcrfpy.Sprite(texture=texture, sprite_index=84, pos=(100, 100))
scene.children.append(sprite)

# Cycle through frames 84-87 forever (0.6 seconds per cycle)
walk = sprite.animate("sprite_index", [84, 85, 86, 87], 0.6, loop=True)

# Later, to stop the loop:
walk.stop()
```

### Camera Pan and Zoom

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)
grid = mcrfpy.Grid(grid_size=(30, 20), pos=(0, 0), size=(480, 320), texture=texture)
scene.children.append(grid)

# grid.center is in PIXELS. To pan to tile (14, 8) with 16x16 tiles,
# target the middle of that tile:
tile_x, tile_y = 14, 8
target = (tile_x * 16 + 8, tile_y * 16 + 8)

grid.animate("center", target, 0.4, mcrfpy.Easing.EASE_OUT_CUBIC)
grid.animate("zoom", 2.0, 0.4, mcrfpy.Easing.EASE_IN_OUT)
```

For an instant (non-animated) camera move in tile coordinates, use `grid.center_camera((tx, ty))` instead.

### Smooth Entity Movement

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)
grid = mcrfpy.Grid(grid_size=(10, 10), pos=(0, 0), size=(160, 160), texture=texture)
scene.children.append(grid)

player = mcrfpy.Entity(grid_pos=(1, 1), texture=texture, sprite_index=84)
grid.entities.append(player)

# Slide the drawn position across the grid in tile coordinates.
# cell_pos (the logical cell) is NOT changed by this animation.
player.animate("draw_x", 5.0, 0.5, mcrfpy.Easing.EASE_OUT_QUAD)
```

Note: entities moved by the turn manager (`grid.step()` with behaviors) animate their draw position automatically over `entity.move_speed` seconds; manual `draw_x`/`draw_y` animation is for movement outside the turn system.

### Colors and Delta Mode

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

frame = mcrfpy.Frame(pos=(100, 100), size=(200, 80))
scene.children.append(frame)

# Animate a whole color (interpolates R, G, B, and A together)
frame.animate("fill_color", (255, 0, 0, 255), 1.0)

# Animate a single channel
frame.animate("fill_color.a", 0.0, 0.5)

# Delta mode: move 50 pixels down from wherever the frame is now
frame.animate("y", 50.0, 0.5, delta=True)
```

### Typewriter Text

Animating `text` transitions between strings: the first half of the duration deletes the current text character by character, the second half types out the target. With `delta=True`, the target is appended character by character instead.

```python
import mcrfpy

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

caption = mcrfpy.Caption(text="", pos=(20, 20))
scene.children.append(caption)

# Typewriter effect: reveals the target string over 2 seconds
caption.animate("text", "You awaken in a dark cell.", 2.0)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Easing" class="object-link">Easing</a>
<a href="Timer" class="object-link">Timer</a>
<a href="Drawable" class="object-link">Drawable</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Sprite" class="object-link">Sprite</a>
<a href="Caption" class="object-link">Caption</a>
<a href="Grid" class="object-link">Grid</a>
<a href="Entity" class="object-link">Entity</a>
</div>
</div>
