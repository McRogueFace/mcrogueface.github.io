---
layout: default
title: MouseButton
---

# MouseButton

Mouse button constants.

## Overview

`MouseButton` is an IntEnum containing constants for all mouse buttons. These values are passed to mouse input handlers and can be used in on_click callbacks. For backwards compatibility, MouseButton values compare equal to legacy string names.

## Quick Reference

```python
def handle_mouse(button, state, x, y):
    if state == mcrfpy.InputState.PRESSED:
        if button == mcrfpy.MouseButton.LEFT:
            print(f"Left click at ({x}, {y})")
        elif button == mcrfpy.MouseButton.RIGHT:
            print(f"Right click at ({x}, {y})")

scene.on_mouse = handle_mouse

# Legacy string comparison still works
if button == "left":  # Same as MouseButton.LEFT
    pass
```

## Values

| Value | Legacy String | Description |
|-------|---------------|-------------|
| `LEFT` | `"left"` | Left mouse button (primary) |
| `RIGHT` | `"right"` | Right mouse button (secondary) |
| `MIDDLE` | `"middle"` | Middle mouse button (scroll wheel click) |
| `X1` | `"x1"` | Extra button 1 (side button, back) |
| `X2` | `"x2"` | Extra button 2 (side button, forward) |

## Legacy Compatibility

MouseButton values compare equal to their legacy string equivalents:

```python
mcrfpy.MouseButton.LEFT == "left"      # True
mcrfpy.MouseButton.RIGHT == "right"    # True
mcrfpy.MouseButton.MIDDLE == "middle"  # True
```

## Usage Patterns

### UI Click Handler

```python
def button_click(x, y, button):
    if button == mcrfpy.MouseButton.LEFT:
        activate_button()
    elif button == mcrfpy.MouseButton.RIGHT:
        show_context_menu(x, y)

my_button.on_click = button_click
```

### Scene Mouse Handler

```python
def on_mouse(button, state, x, y):
    if state == mcrfpy.InputState.PRESSED:
        if button == mcrfpy.MouseButton.LEFT:
            select_at(x, y)
        elif button == mcrfpy.MouseButton.RIGHT:
            move_to(x, y)
        elif button == mcrfpy.MouseButton.MIDDLE:
            start_pan(x, y)
        elif button == mcrfpy.MouseButton.X1:
            go_back()
        elif button == mcrfpy.MouseButton.X2:
            go_forward()

scene.on_mouse = on_mouse
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
