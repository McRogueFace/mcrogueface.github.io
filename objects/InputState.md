---
layout: default
title: InputState
---

# InputState

Input event states for key and mouse button events.

## Overview

`InputState` is an IntEnum that represents whether an input event is a press or release. These values are passed to input handlers to indicate the type of event. For backwards compatibility, InputState values compare equal to legacy string names.

## Quick Reference

```python
def handle_input(key, state):
    if state == mcrfpy.InputState.PRESSED:
        print(f"{key} was pressed")
    elif state == mcrfpy.InputState.RELEASED:
        print(f"{key} was released")

scene.on_key = handle_input

# Legacy string comparison still works
if state == "start":   # Same as InputState.PRESSED
    pass
if state == "end":     # Same as InputState.RELEASED
    pass
```

## Values

| Value | Legacy String | Description |
|-------|---------------|-------------|
| `PRESSED` | `"start"` | Key or button was pressed down |
| `RELEASED` | `"end"` | Key or button was released |

## Legacy Compatibility

For backwards compatibility with older McRogueFace code, InputState values compare equal to their legacy string equivalents:

```python
# These are equivalent
mcrfpy.InputState.PRESSED == "start"   # True
mcrfpy.InputState.RELEASED == "end"    # True

# Both styles work in handlers
def on_key(key, state):
    # Modern style
    if state == mcrfpy.InputState.PRESSED:
        pass

    # Legacy style (still supported)
    if state == "start":
        pass
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Key" class="object-link">Key</a>
<a href="MouseButton" class="object-link">MouseButton</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/input" class="object-link">Input System</a>
</div>
</div>
