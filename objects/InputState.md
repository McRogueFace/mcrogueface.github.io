---
layout: default
title: InputState
mcrf:
  objects: [InputState]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# InputState

Input event states for key and mouse button events.

## Overview

`InputState` is an IntEnum that represents whether an input event is a press or release. These values are passed to input handlers to indicate the type of event. Some engine functions that accept an `InputState` will also take the equivalent enum-name string (e.g. `"PRESSED"`) or int (`0`/`1`) as an argument, but `InputState` values do **not** compare equal to strings with `==` — always compare against the enum member itself (`mcrfpy.InputState.PRESSED`).

## Quick Reference

```python
import mcrfpy

def handle_input(key, state):
    if state == mcrfpy.InputState.PRESSED:
        print(f"{key} was pressed")
    elif state == mcrfpy.InputState.RELEASED:
        print(f"{key} was released")

scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene
scene.children.append(mcrfpy.Frame(pos=(0, 0), size=(800, 600)))
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
