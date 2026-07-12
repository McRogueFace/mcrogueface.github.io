---
layout: default
title: Keyboard
mcrf:
  objects: [Keyboard]
  diataxis: reference
  disposition: needs-review
---

# Keyboard

Keyboard state singleton for checking modifier keys.

## Overview

`Keyboard` is a singleton object that provides real-time access to modifier key states. Unlike event-based input which fires callbacks, `Keyboard` lets you poll whether shift, ctrl, alt, or system keys are currently held down. The singleton instance is `mcrfpy.keyboard` (lowercase) — the `Keyboard` class itself is not the instance.

## Quick Reference

```python
def handle_key(key, state):
    if state == mcrfpy.InputState.PRESSED:
        if key == mcrfpy.Key.S:
            if mcrfpy.keyboard.ctrl:
                save_game()  # Ctrl+S
            elif mcrfpy.keyboard.shift:
                save_as()    # Shift+S
            else:
                move_south() # Just S

scene.on_key = handle_key

# Check modifier states anywhere
if mcrfpy.keyboard.shift:
    print("Shift is currently held")
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `shift` | bool | True if either shift key is held (read-only) |
| `ctrl` | bool | True if either control key is held (read-only) |
| `alt` | bool | True if either alt key is held (read-only) |
| `system` | bool | True if either system key is held (read-only) |

## Usage Patterns

### Modifier Combinations

```python
def on_key(key, state):
    if state != mcrfpy.InputState.PRESSED:
        return

    # Check for key combinations
    if key == mcrfpy.Key.Z:
        if mcrfpy.keyboard.ctrl and mcrfpy.keyboard.shift:
            redo()      # Ctrl+Shift+Z
        elif mcrfpy.keyboard.ctrl:
            undo()      # Ctrl+Z
```

### Run vs Walk

```python
def update_movement():
    speed = 2.0
    if mcrfpy.keyboard.shift:
        speed = 4.0  # Run when shift is held

    move_player(speed)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Key" class="object-link">Key</a>
<a href="InputState" class="object-link">InputState</a>
<a href="Mouse" class="object-link">Mouse</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/input" class="object-link">Input System</a>
</div>
</div>
