---
layout: default
title: Mouse
mcrf:
  objects: [Mouse, MouseButton, InputState]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Mouse

Mouse state singleton for position and button state.

## Overview

`Mouse` is a singleton object that provides real-time access to mouse state including position, button states, and cursor properties. Use it to poll mouse state outside of event callbacks or to control cursor visibility and grabbing.

## Quick Reference

```python
# Check mouse position
x, y = mcrfpy.mouse.pos
print(f"Mouse at ({x}, {y})")

# Check button states
if mcrfpy.mouse.left:
    print("Left button is held")

# Hide cursor for custom cursor sprite
mcrfpy.mouse.visible = False

# Grab mouse for camera control
mcrfpy.mouse.grabbed = True
```

## Properties

### Position

| Property | Type | Description |
|----------|------|-------------|
| `pos` | Vector | Current mouse position as Vector (read-only) |
| `x` | int | Current mouse X position (read-only) |
| `y` | int | Current mouse Y position (read-only) |

### Button States

| Property | Type | Description |
|----------|------|-------------|
| `left` | bool | True if left button is held (read-only) |
| `middle` | bool | True if middle button is held (read-only) |
| `right` | bool | True if right button is held (read-only) |

### Cursor Control

| Property | Type | Description |
|----------|------|-------------|
| `visible` | bool | Show/hide system cursor (read-write) |
| `grabbed` | bool | Lock cursor to window (read-write) |

## Usage Patterns

### Custom Cursor

```python
import mcrfpy

scene = mcrfpy.Scene("custom_cursor")
mcrfpy.current_scene = scene

# Create a custom cursor sprite (uses the default texture atlas)
cursor = mcrfpy.Sprite(pos=(0, 0), sprite_index=1)
scene.children.append(cursor)

# Hide the system cursor
mcrfpy.mouse.visible = False

# Update the cursor's position every frame via a Timer
def update(timer, runtime):
    pos = mcrfpy.mouse.pos
    cursor.x, cursor.y = pos.x, pos.y

mcrfpy.Timer("cursor_follow", update, 16)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="MouseButton" class="object-link">MouseButton</a>
<a href="Keyboard" class="object-link">Keyboard</a>
<a href="InputState" class="object-link">InputState</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/input" class="object-link">Input System</a>
</div>
</div>
