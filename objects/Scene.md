---
layout: default
title: Scene
mcrf:
  objects: [Scene, Transition, Key, InputState]
  diataxis: reference
  disposition: rewrite-pending
---

# Scene

Object-oriented scene management with lifecycle callbacks.

## Overview

A `Scene` is a container that holds UI elements and manages input handling. Only one scene is active at a time. Scenes provide lifecycle callbacks for initialization, cleanup, and per-frame updates. Switch between scenes for menus, gameplay, inventory screens, and other game states.

## Quick Reference

```python
import mcrfpy

# Create a scene
scene = mcrfpy.Scene("game")

# Add UI elements
scene.children.append(mcrfpy.Frame(pos=(0, 0), size=(800, 600)))
scene.children.append(mcrfpy.Caption(text="Hello", pos=(100, 100)))

# Handle input
def on_key(key, action):
    if key == mcrfpy.Key.ESCAPE and action == mcrfpy.InputState.PRESSED:
        menu_scene.activate()

scene.on_key = on_key

# Activate with optional transition
scene.activate()
scene.activate(mcrfpy.Transition.FADE, duration=0.5)

# Subclass for lifecycle callbacks
class GameScene(mcrfpy.Scene):
    def on_enter(self):
        print("Entering game scene")

    def on_exit(self):
        print("Leaving game scene")

    def on_key(self, key, action):
        if key == mcrfpy.Key.Q and action == mcrfpy.InputState.PRESSED:
            self.handle_quit()

    def update(self, dt):
        # Called every frame with delta time
        self.update_entities(dt)

    def on_resize(self, new_size):
        # Window resize handling - new_size is a Vector(width, height)
        self.realign()
```

## Constructor

```python
mcrfpy.Scene(name: str)
```

Creates a new scene with the given name. If a scene with that name already exists, returns the existing scene.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier for the scene |

## Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `name` | str | read-only | Scene identifier |
| `active` | bool | read-only | True if this is the current scene |
| `registered` | bool | read-only | Scene registration state |
| `children` | UICollection | read-only | UI elements in this scene |
| `on_key` | callable | read/write | Keyboard input callback |
| `pos` | tuple | read/write | Scene offset position (x, y) |
| `visible` | bool | read/write | Whether scene renders |
| `opacity` | float | read/write | Scene transparency (0.0-1.0) |

## Methods

| Method | Description |
|--------|-------------|
| `activate(transition=None, duration=None)` | Make this scene active |
| `realign()` | Recompute layout for all child elements |
| `register()` | Register the scene |
| `unregister()` | Unregister the scene |

### activate()

```python
scene.activate(transition=None, duration=None)
```

Activates this scene, making it the current scene. Optionally applies a visual transition effect.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `transition` | Transition | None | Transition type: `mcrfpy.Transition.NONE`, `FADE`, `SLIDE_LEFT`, `SLIDE_RIGHT`, `SLIDE_UP`, `SLIDE_DOWN` |
| `duration` | float | None | Transition duration in seconds |

Defaults for `transition` and `duration` come from `mcrfpy.default_transition` and `mcrfpy.default_transition_duration` when not specified.

## Lifecycle Callbacks

When subclassing Scene, override these methods for custom behavior:

| Callback | Signature | Description |
|----------|-----------|-------------|
| `on_enter()` | `def on_enter(self)` | Called when scene becomes active |
| `on_exit()` | `def on_exit(self)` | Called when scene is deactivated |
| `on_key(key, action)` | `def on_key(self, key, action)` | Called on keyboard events |
| `update(dt)` | `def update(self, dt)` | Called every frame with delta time |
| `on_resize(new_size)` | `def on_resize(self, new_size)` | Called when window resizes (new_size is Vector) |

### Key Handler Arguments

The `on_key` callback receives:
- `key`: a `mcrfpy.Key` enum member (e.g. `mcrfpy.Key.A`, `mcrfpy.Key.ESCAPE`, `mcrfpy.Key.SPACE`, `mcrfpy.Key.Num1`)
- `action`: `mcrfpy.InputState.PRESSED` or `mcrfpy.InputState.RELEASED`

## Examples

### Basic Scene Setup

```python
import mcrfpy

# Create and populate a scene
menu = mcrfpy.Scene("menu")
menu.children.append(mcrfpy.Caption(
    text="Press ENTER to start",
    pos=(400, 300)
))

def menu_keys(key, action):
    if key == mcrfpy.Key.ENTER and action == mcrfpy.InputState.PRESSED:
        mcrfpy.Scene("game").activate()

menu.on_key = menu_keys
menu.activate()
```

### Scene Subclass

```python
class InventoryScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("inventory")
        self.setup_ui()

    def setup_ui(self):
        self.children.append(mcrfpy.Frame(
            pos=(100, 100), size=(600, 400)
        ))

    def on_enter(self):
        self.refresh_items()

    def on_key(self, key, action):
        if key == mcrfpy.Key.ESCAPE and action == mcrfpy.InputState.PRESSED:
            mcrfpy.Scene("game").activate()
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Frame" class="object-link">Frame</a>
<a href="Caption" class="object-link">Caption</a>
<a href="Sprite" class="object-link">Sprite</a>
<a href="Grid" class="object-link">Grid</a>
<a href="Window" class="object-link">Window</a>
<a href="Transition" class="object-link">Transition</a>
</div>
</div>
