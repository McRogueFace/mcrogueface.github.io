---
layout: default
title: InputState
mcrf:
  objects: [InputState]
  diataxis: reference
  disposition: needs-review
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
```

## Values

| Value | Description |
|-------|-------------|
| `PRESSED` | Key or button was pressed down |
| `RELEASED` | Key or button was released |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Key" class="object-link">Key</a>
<a href="MouseButton" class="object-link">MouseButton</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/input" class="object-link">Input System</a>
</div>
</div>
