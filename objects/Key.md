---
layout: default
title: Key
mcrf:
  objects: [Key]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Key

Keyboard key constants.

## Overview

`Key` is an IntEnum containing constants for all keyboard keys. These values are passed to keyboard input handlers and can be used with the `Keyboard` singleton to check key states. For backwards compatibility, Key values compare equal to legacy string names.

## Quick Reference

```python
import mcrfpy

scene = mcrfpy.Scene("key_demo")

def handle_key(key, state):
    if state == mcrfpy.InputState.PRESSED:
        if key == mcrfpy.Key.ESCAPE:
            print("Escape pressed")
        elif key == mcrfpy.Key.SPACE:
            print("Space pressed")
        elif key == mcrfpy.Key.W:
            print("W pressed")

scene.on_key = handle_key
scene.children.append(mcrfpy.Caption(text="Press a key", pos=(10, 10)))
mcrfpy.current_scene = scene
```

## Values

### Letters

| Value |
|-------|
| `A` - `Z` |

### Numbers (Top Row)

| Value |
|-------|
| `NUM_0` - `NUM_9` |

### Numpad

| Value |
|-------|
| `NUMPAD_0` - `NUMPAD_9` |
| `ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE` |

### Function Keys

| Value |
|-------|
| `F1` - `F15` |

### Modifiers

| Value | Description |
|-------|-------------|
| `LEFT_SHIFT` | Left shift key |
| `RIGHT_SHIFT` | Right shift key |
| `LEFT_CONTROL` | Left control key |
| `RIGHT_CONTROL` | Right control key |
| `LEFT_ALT` | Left alt key |
| `RIGHT_ALT` | Right alt key |
| `LEFT_SYSTEM` | Left system key (Win/Cmd) |
| `RIGHT_SYSTEM` | Right system key |

### Navigation

| Value | Description |
|-------|-------------|
| `LEFT` | Left arrow |
| `RIGHT` | Right arrow |
| `UP` | Up arrow |
| `DOWN` | Down arrow |
| `HOME` | Home key |
| `END` | End key |
| `PAGE_UP` | Page up |
| `PAGE_DOWN` | Page down |

### Editing

| Value | Description |
|-------|-------------|
| `ENTER` | Enter/Return key |
| `BACKSPACE` | Backspace key |
| `DELETE` | Delete key |
| `INSERT` | Insert key |
| `TAB` | Tab key |
| `SPACE` | Spacebar |
| `ESCAPE` | Escape key |

### Symbols

| Value | Description |
|-------|-------------|
| `COMMA` | `,` |
| `PERIOD` | `.` |
| `SLASH` | `/` |
| `BACKSLASH` | `\` |
| `SEMICOLON` | `;` |
| `APOSTROPHE` | `'` |
| `LEFT_BRACKET` | `[` |
| `RIGHT_BRACKET` | `]` |
| `HYPHEN` | `-` |
| `EQUAL` | `=` |
| `GRAVE` | `` ` `` |

### Other

| Value | Description |
|-------|-------------|
| `MENU` | Menu key |
| `PAUSE` | Pause key |
| `UNKNOWN` | Unknown/unrecognized key |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Keyboard" class="object-link">Keyboard</a>
<a href="InputState" class="object-link">InputState</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/input" class="object-link">Input System</a>
</div>
</div>
