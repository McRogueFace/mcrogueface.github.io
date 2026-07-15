---
layout: default
title: Transition
mcrf:
  objects: [Transition, Scene]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Transition

Scene transition enumeration.

## Overview

The `Transition` IntEnum defines visual effects used when switching between scenes. Transitions make scene changes feel polished and can provide visual continuity in your game.

## Quick Reference

```python
import mcrfpy

# Create scenes
menu = mcrfpy.Scene("menu")
game = mcrfpy.Scene("game")
settings = mcrfpy.Scene("settings")

menu.children.append(mcrfpy.Caption(text="Menu", pos=(10, 10)))
game.children.append(mcrfpy.Caption(text="Game", pos=(10, 10)))
settings.children.append(mcrfpy.Caption(text="Settings", pos=(10, 10)))

# Fade transition (default feel)
game.activate(mcrfpy.Transition.FADE)

# Slide transitions for navigation
settings.activate(mcrfpy.Transition.SLIDE_LEFT)

# Instant switch (no transition)
menu.activate(mcrfpy.Transition.NONE)

# With custom duration (seconds)
game.activate(mcrfpy.Transition.FADE, duration=0.5)
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
# Create menu scenes
main_menu = mcrfpy.Scene("main_menu")
settings = mcrfpy.Scene("settings")

# Going "forward" in menus
def go_to_settings():
    settings.activate(mcrfpy.Transition.SLIDE_LEFT)

# Going "back" in menus
def back_to_main():
    main_menu.activate(mcrfpy.Transition.SLIDE_RIGHT)
```

### Level Transitions

```python
# Create game scenes
level_1 = mcrfpy.Scene("level_1")
level_2 = mcrfpy.Scene("level_2")
inventory = mcrfpy.Scene("inventory")

# Moving between game levels
def next_level():
    level_2.activate(mcrfpy.Transition.FADE, duration=1.0)

# Popup dialogs (instant)
def show_inventory():
    inventory.activate(mcrfpy.Transition.NONE)
```

### Vertical Navigation

```python
# Create scenes
game = mcrfpy.Scene("game")
pause = mcrfpy.Scene("pause")

# Pause menu slides down from top
def pause_game():
    pause.activate(mcrfpy.Transition.SLIDE_DOWN)

# Resume slides it back up
def resume_game():
    game.activate(mcrfpy.Transition.SLIDE_UP)
```

### Scene Subclass with Transitions

```python
import mcrfpy


class GameScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("game")
        self.setup_ui()

    def setup_ui(self):
        self.children.append(mcrfpy.Caption(text="Game", pos=(10, 10)))

    def on_enter(self):
        """Called after transition completes."""
        print("Game scene active!")

    def on_exit(self):
        """Called before transition to another scene."""
        print("Leaving game scene...")


class MenuScene(mcrfpy.Scene):
    def __init__(self, game_scene):
        super().__init__("menu")
        self.game_scene = game_scene
        self.setup_menu()

    def setup_menu(self):
        self.children.append(mcrfpy.Caption(text="Menu", pos=(10, 10)))

    def start_game(self):
        self.game_scene.activate(mcrfpy.Transition.FADE, duration=0.5)


# Usage
game = GameScene()
menu = MenuScene(game)
menu.activate()  # Start at menu
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Scene" class="object-link">Scene</a>
<a href="Easing" class="object-link">Easing</a>
<a href="../systems/scene" class="object-link">Scene System</a>
</div>
</div>
