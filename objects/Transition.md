---
layout: default
title: Transition
---

# Transition

Scene transition enumeration.

## Overview

The `Transition` IntEnum defines visual effects used when switching between scenes. Transitions make scene changes feel polished and can provide visual continuity in your game.

## Quick Reference

```python
# Fade transition (default feel)
mcrfpy.setScene("game", mcrfpy.Transition.FADE)

# Slide transitions for navigation
mcrfpy.setScene("next_level", mcrfpy.Transition.SLIDE_LEFT)
mcrfpy.setScene("previous_menu", mcrfpy.Transition.SLIDE_RIGHT)

# Instant switch (no transition)
mcrfpy.setScene("dialog", mcrfpy.Transition.NONE)

# Using Scene.activate() method
game_scene = mcrfpy.Scene("game")
game_scene.activate(mcrfpy.Transition.SLIDE_UP)
```

## Values

| Value | Description |
|-------|-------------|
| `NONE` | Instant switch, no visual transition |
| `FADE` | Cross-fade between scenes |
| `SLIDE_LEFT` | New scene slides in from the right |
| `SLIDE_RIGHT` | New scene slides in from the left |
| `SLIDE_UP` | New scene slides in from the bottom |
| `SLIDE_DOWN` | New scene slides in from the top |

## Usage Patterns

### Menu Navigation

```python
# Going "forward" in menus
def go_to_settings():
    mcrfpy.setScene("settings", mcrfpy.Transition.SLIDE_LEFT)

# Going "back" in menus
def back_to_main():
    mcrfpy.setScene("main_menu", mcrfpy.Transition.SLIDE_RIGHT)
```

### Level Transitions

```python
# Moving between game levels
def next_level():
    mcrfpy.setScene("level_2", mcrfpy.Transition.FADE)

# Popup dialogs (instant)
def show_inventory():
    mcrfpy.setScene("inventory", mcrfpy.Transition.NONE)
```

### Vertical Navigation

```python
# Pause menu slides down from top
def pause_game():
    mcrfpy.setScene("pause", mcrfpy.Transition.SLIDE_DOWN)

# Resume slides it back up
def resume_game():
    mcrfpy.setScene("game", mcrfpy.Transition.SLIDE_UP)
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Scene" class="object-link">Scene</a>
</div>
</div>
