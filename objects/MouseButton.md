---
layout: default
title: MouseButton
mcrf:
  objects: [MouseButton, InputState]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# MouseButton

Mouse button constants.

## Overview

`MouseButton` is an IntEnum containing constants for all mouse buttons and the scroll wheel. Values are delivered to `on_click` (and `on_cell_click`) callbacks on drawables and grids as the `button` argument, paired with an `InputState` (`PRESSED`/`RELEASED`) telling you which edge of the click fired.

## Quick Reference

```python
def on_click(pos, button, action):
    if action == mcrfpy.InputState.PRESSED:
        if button == mcrfpy.MouseButton.LEFT:
            print(f"Left click at ({pos.x}, {pos.y})")
        elif button == mcrfpy.MouseButton.RIGHT:
            print(f"Right click at ({pos.x}, {pos.y})")

frame.on_click = on_click
```

## Values

| Value | Description |
|-------|-------------|
| `LEFT` | Left mouse button (primary) |
| `RIGHT` | Right mouse button (secondary) |
| `MIDDLE` | Middle mouse button (scroll wheel click) |
| `X1` | Extra button 1 (side button, back) |
| `X2` | Extra button 2 (side button, forward) |
| `SCROLL_UP` | Scroll wheel up |
| `SCROLL_DOWN` | Scroll wheel down |

## Usage Patterns

### UI Click Handler

Any `Drawable` (`Frame`, `Caption`, `Sprite`, `Entity`, etc.) exposes `on_click`. The callback receives `(pos: Vector, button: MouseButton, action: InputState)`:

```python
def button_click(pos, button, action):
    if action != mcrfpy.InputState.PRESSED:
        return
    if button == mcrfpy.MouseButton.LEFT:
        activate_button()
    elif button == mcrfpy.MouseButton.RIGHT:
        show_context_menu(pos.x, pos.y)

my_button.on_click = button_click
```

### Grid Cell Click Handler

`Grid`/`GridView` has `on_cell_click`, which receives `(cell_pos: Vector, button: MouseButton, action: InputState)` in grid cell coordinates instead of pixels:

```python
def on_cell_click(cell_pos, button, action):
    if action == mcrfpy.InputState.PRESSED:
        if button == mcrfpy.MouseButton.LEFT:
            select_at(cell_pos.x, cell_pos.y)
        elif button == mcrfpy.MouseButton.RIGHT:
            move_to(cell_pos.x, cell_pos.y)
        elif button == mcrfpy.MouseButton.MIDDLE:
            start_pan(cell_pos.x, cell_pos.y)
        elif button == mcrfpy.MouseButton.X1:
            go_back()
        elif button == mcrfpy.MouseButton.X2:
            go_forward()

grid.on_cell_click = on_cell_click
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Mouse" class="object-link">Mouse</a>
<a href="InputState" class="object-link">InputState</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/input" class="object-link">Input System</a>
</div>
</div>
