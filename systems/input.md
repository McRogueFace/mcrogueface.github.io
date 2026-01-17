---
layout: default
title: Input & Callbacks
---

# Input & Callbacks

The Input & Callback System handles all user interaction and timed events in McRogueFace. It provides keyboard and mouse input through scene callbacks, and scheduled execution through timers.

## Overview

McRogueFace uses a callback-based input model. Instead of polling for input in a game loop, you register callback functions that are invoked when events occur.

```python
def on_key(key, state):
    if key == "W" and state == "start":
        move_player(0, -1)

scene.on_key = on_key
```

## Objects

| Object | Purpose |
|--------|---------|
| [Timer](../objects/Timer) | Scheduled callbacks at intervals |

---

## Keyboard Input {#keyboard}

Keyboard input is handled through the scene's `on_key` callback.

### Key Callback Signature

```python
def on_key(key: str, state: str) -> None:
    pass
```

- `key`: The key name (e.g., "W", "Space", "Return", "Escape")
- `state`: One of "start" (pressed), "repeat" (held), or "end" (released)

### Example: Movement

```python
def on_key(key, state):
    if state != "start":
        return

    dx, dy = 0, 0
    if key == "W" or key == "Up": dy = -1
    elif key == "S" or key == "Down": dy = 1
    elif key == "A" or key == "Left": dx = -1
    elif key == "D" or key == "Right": dx = 1

    if dx or dy:
        new_x = player.x + dx
        new_y = player.y + dy
        if grid.at(new_x, new_y).walkable:
            player.x, player.y = new_x, new_y

scene.on_key = on_key
```

### Key Names

Common key names:
- Letters: "A" through "Z"
- Numbers: "0" through "9"
- Arrows: "Up", "Down", "Left", "Right"
- Modifiers: "LShift", "RShift", "LControl", "RControl", "LAlt", "RAlt"
- Special: "Space", "Return", "Escape", "Tab", "Backspace"

---

## Mouse Input {#mouse}

Mouse input is handled through the scene's `on_mouse` callback.

### Mouse Callback Signature

```python
def on_mouse(x: int, y: int, button: str, state: str) -> None:
    pass
```

- `x`, `y`: Mouse position in pixels
- `button`: "left", "right", "middle", or "none" (for movement)
- `state`: "start" (pressed), "end" (released), or "move"

### Example: Click Detection

```python
def on_mouse(x, y, button, state):
    if button == "left" and state == "start":
        # Convert pixel position to grid coordinates
        grid_x = (x - grid.x) // (grid.tile_size * grid.zoom)
        grid_y = (y - grid.y) // (grid.tile_size * grid.zoom)

        print(f"Clicked tile: ({grid_x}, {grid_y})")

scene.on_mouse = on_mouse
```

### UI Element Interaction

UI elements can have their own click handlers:

```python
button = mcrfpy.Frame(pos=(100, 100), size=(120, 40))
button.on_click = lambda: print("Button clicked!")
```

---

## Timers {#timers}

[Timers](../objects/Timer) execute callbacks at specified intervals.

### Creating Timers

```python
# Call every 500ms
def update():
    print("Timer tick!")

mcrfpy.Timer("update_timer", update, 500)
```

### One-Shot Timers

For single execution, cancel the timer in the callback:

```python
def delayed_action():
    print("Delayed!")
    mcrfpy.Timer.cancel("delay_timer")

mcrfpy.Timer("delay_timer", delayed_action, 1000)
```

### Timer Control

```python
# Pause a timer
mcrfpy.Timer.pause("update_timer")

# Resume a timer
mcrfpy.Timer.resume("update_timer")

# Cancel a timer
mcrfpy.Timer.cancel("update_timer")
```

### Animation Timers

Timers are commonly used for animations:

```python
frame = 0
def animate():
    global frame
    sprite.sprite_index = animation_frames[frame]
    frame = (frame + 1) % len(animation_frames)

mcrfpy.Timer("animation", animate, 100)  # 10 FPS animation
```

---

## Scene Lifecycle {#lifecycle}

Scenes have lifecycle callbacks for initialization and cleanup.

### on_enter

Called when a scene becomes active:

```python
def on_enter():
    print("Scene activated!")
    # Initialize game state, start timers, etc.

scene.on_enter = on_enter
```

### on_exit

Called when leaving a scene:

```python
def on_exit():
    print("Leaving scene")
    # Clean up timers, save state, etc.

scene.on_exit = on_exit
```

---

## Related Objects

<div class="related-objects">
<div class="object-links">
<a href="../objects/Scene" class="object-link">Scene</a>
<a href="../objects/Timer" class="object-link">Timer</a>
</div>
</div>
