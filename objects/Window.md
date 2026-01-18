---
layout: default
title: Window
---

# Window

Singleton for game window properties and control.

## Overview

`Window` is a singleton that provides access to the game window's properties. Use it to control resolution, fullscreen mode, VSync, frame rate, and take screenshots. Access the window instance via the `get()` class method or through `mcrfpy.Window`.

## Quick Reference

```python
import mcrfpy

# Get window instance
window = mcrfpy.Window.get()

# Configure window
window.title = "My Roguelike"
window.resolution = (1280, 720)
window.fullscreen = False
window.vsync = True
window.framerate_limit = 60

# Scaling modes for different resolutions
window.game_resolution = (320, 240)  # Internal game resolution
window.scaling_mode = "fit"          # Scale to fit window

# Take a screenshot
window.screenshot("screenshot.png")

# Center window on screen
window.center()
```

## Class Methods

| Method | Description |
|--------|-------------|
| `Window.get()` | Returns the Window singleton instance |

## Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `resolution` | tuple | read/write | Window size in pixels (width, height) |
| `game_resolution` | tuple | read/write | Internal render resolution (width, height) |
| `fullscreen` | bool | read/write | Fullscreen mode toggle |
| `vsync` | bool | read/write | Vertical sync toggle |
| `framerate_limit` | int | read/write | Maximum frames per second (0 = unlimited) |
| `title` | str | read/write | Window title bar text |
| `visible` | bool | read/write | Window visibility |
| `scaling_mode` | str | read/write | How game renders to window |

### Scaling Modes

The `scaling_mode` property controls how the game resolution scales to the window:

| Mode | Description |
|------|-------------|
| `"center"` | No scaling, game centered in window |
| `"stretch"` | Stretch to fill window (may distort) |
| `"fit"` | Scale to fit while maintaining aspect ratio |

## Methods

| Method | Description |
|--------|-------------|
| `center()` | Center window on the screen |
| `screenshot(filename=None)` | Capture window to PNG file |

### screenshot()

```python
window.screenshot(filename=None)
```

Captures the current window contents to a PNG file.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filename` | str | None | Output filename (auto-generated if None) |

If no filename is provided, generates one with timestamp: `screenshot_YYYYMMDD_HHMMSS.png`

## Examples

### Basic Window Setup

```python
import mcrfpy

window = mcrfpy.Window.get()
window.title = "Dungeon Crawler"
window.resolution = (1024, 768)
window.vsync = True
```

### Pixel Art Scaling

```python
# For pixel art games, use low internal resolution
# and scale up to window size
window = mcrfpy.Window.get()
window.game_resolution = (320, 180)  # 16:9 at low res
window.resolution = (1280, 720)       # Scale 4x
window.scaling_mode = "fit"           # Maintain aspect ratio
```

### Fullscreen Toggle

```python
def toggle_fullscreen():
    window = mcrfpy.Window.get()
    window.fullscreen = not window.fullscreen

# In key handler
def on_key(key, action):
    if key == "F11" and action == "start":
        toggle_fullscreen()
```

### Screenshot on Key Press

```python
def on_key(key, action):
    if key == "F12" and action == "start":
        window = mcrfpy.Window.get()
        window.screenshot()  # Auto-named with timestamp
```

### Named Screenshot

```python
def save_game_state():
    window = mcrfpy.Window.get()
    window.screenshot("savegame_preview.png")
```

### Frame Rate Control

```python
window = mcrfpy.Window.get()

# Cap at 60 FPS
window.framerate_limit = 60

# Uncapped (use VSync instead)
window.framerate_limit = 0
window.vsync = True
```

### Resolution Management

```python
class Settings:
    resolutions = [
        (640, 480),
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1920, 1080)
    ]
    current_index = 2

    @classmethod
    def cycle_resolution(cls):
        cls.current_index = (cls.current_index + 1) % len(cls.resolutions)
        window = mcrfpy.Window.get()
        window.resolution = cls.resolutions[cls.current_index]
        window.center()
```

### Responsive UI

```python
class GameScene(mcrfpy.Scene):
    def on_resize(self, new_size):
        # new_size is a Vector with .x and .y properties
        # Reposition UI elements based on new size
        panel_width = 400
        panel_x = (new_size.x - panel_width) // 2
        self.panel.x = panel_x
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Scene" class="object-link">Scene</a>
</div>
</div>
