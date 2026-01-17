---
layout: default
title: Key
---

# Key

Keyboard key constants.

## Overview

`Key` is an IntEnum containing constants for all keyboard keys. These values are passed to keyboard input handlers and can be used with the `Keyboard` singleton to check key states. For backwards compatibility, Key values compare equal to legacy string names.

## Quick Reference

```python
def handle_key(key, state):
    if state == mcrfpy.InputState.PRESSED:
        if key == mcrfpy.Key.ESCAPE:
            print("Escape pressed")
        elif key == mcrfpy.Key.SPACE:
            print("Space pressed")
        elif key == mcrfpy.Key.W:
            print("W pressed")

scene.on_key = handle_key

# Legacy string comparison still works
if key == "Escape":  # Same as Key.ESCAPE
    pass
```

## Values

### Letters

| Value | Legacy String |
|-------|---------------|
| `A` - `Z` | `"A"` - `"Z"` |

### Numbers (Top Row)

| Value | Legacy String |
|-------|---------------|
| `NUM_0` - `NUM_9` | `"Num0"` - `"Num9"` |

### Numpad

| Value | Legacy String |
|-------|---------------|
| `NUMPAD_0` - `NUMPAD_9` | `"Numpad0"` - `"Numpad9"` |

### Function Keys

| Value | Legacy String |
|-------|---------------|
| `F1` - `F15` | `"F1"` - `"F15"` |

### Modifiers

| Value | Legacy String | Description |
|-------|---------------|-------------|
| `LEFT_SHIFT` | `"LShift"` | Left shift key |
| `RIGHT_SHIFT` | `"RShift"` | Right shift key |
| `LEFT_CONTROL` | `"LControl"` | Left control key |
| `RIGHT_CONTROL` | `"RControl"` | Right control key |
| `LEFT_ALT` | `"LAlt"` | Left alt key |
| `RIGHT_ALT` | `"RAlt"` | Right alt key |
| `LEFT_SYSTEM` | `"LSystem"` | Left system key (Win/Cmd) |
| `RIGHT_SYSTEM` | `"RSystem"` | Right system key |

### Navigation

| Value | Legacy String | Description |
|-------|---------------|-------------|
| `LEFT` | `"Left"` | Left arrow |
| `RIGHT` | `"Right"` | Right arrow |
| `UP` | `"Up"` | Up arrow |
| `DOWN` | `"Down"` | Down arrow |
| `HOME` | `"Home"` | Home key |
| `END` | `"End"` | End key |
| `PAGE_UP` | `"PageUp"` | Page up |
| `PAGE_DOWN` | `"PageDown"` | Page down |

### Editing

| Value | Legacy String | Description |
|-------|---------------|-------------|
| `ENTER` | `"Enter"` | Enter/Return key |
| `BACKSPACE` | `"Backspace"` | Backspace key |
| `DELETE` | `"Delete"` | Delete key |
| `INSERT` | `"Insert"` | Insert key |
| `TAB` | `"Tab"` | Tab key |
| `SPACE` | `"Space"` | Spacebar |
| `ESCAPE` | `"Escape"` | Escape key |

### Symbols

| Value | Legacy String | Description |
|-------|---------------|-------------|
| `COMMA` | `"Comma"` | `,` |
| `PERIOD` | `"Period"` | `.` |
| `SLASH` | `"Slash"` | `/` |
| `BACKSLASH` | `"Backslash"` | `\` |
| `SEMICOLON` | `"Semicolon"` | `;` |
| `QUOTE` | `"Quote"` | `'` |
| `LEFT_BRACKET` | `"LBracket"` | `[` |
| `RIGHT_BRACKET` | `"RBracket"` | `]` |
| `MINUS` | `"Hyphen"` | `-` |
| `EQUAL` | `"Equal"` | `=` |
| `GRAVE` | `"Grave"` | `` ` `` |

## Legacy Compatibility

Key values compare equal to their legacy string equivalents:

```python
mcrfpy.Key.ESCAPE == "Escape"    # True
mcrfpy.Key.SPACE == "Space"      # True
mcrfpy.Key.A == "A"              # True
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Keyboard" class="object-link">Keyboard</a>
<a href="InputState" class="object-link">InputState</a>
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/input" class="object-link">Input System</a>
</div>
</div>
