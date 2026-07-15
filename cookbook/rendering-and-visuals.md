---
title: Rendering and Visuals
mcrf:
  objects: [Frame, Caption, Sprite, Grid, TileLayer, Color, Texture, Easing, Timer, Scene]
  diataxis: howto
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Rendering and Visuals

How to create and display visual elements in McRogueFace.

## Quick Reference

**Systems:** UI Component Hierarchy, Grid System, Animation System

**Key Types:**
- `Frame` - Rectangles and containers
- `Caption` - Text rendering
- `Sprite` - Images and sprite sheets
- `Grid` - Tilemaps with layers
- `Entity` - Grid-based sprites

---

## Basic Rendering

### Creating UI Elements

```python
import mcrfpy

# Create scene
scene = mcrfpy.Scene("game")
ui = scene.children

# Rectangle/Frame
frame = mcrfpy.Frame(pos=(100, 100), size=(200, 150),
                      fill_color=mcrfpy.Color(50, 50, 50))
frame.outline_color = mcrfpy.Color(255, 255, 255)
frame.outline = 2
ui.append(frame)

# Text
label = mcrfpy.Caption(text="Hello World!", pos=(10, 10))
label.font_size = 24
label.fill_color = mcrfpy.Color(255, 255, 255)
ui.append(label)

# Sprite
sprite = mcrfpy.Sprite(x=50, y=50, sprite_index=0)
ui.append(sprite)

mcrfpy.current_scene = scene
```

---

## Textures and Sprite Sheets

### Loading Textures

```python
# Load a sprite sheet with tile dimensions
texture = mcrfpy.Texture("assets/sprites/tileset.png", 16, 16)

# Use with sprite
sprite = mcrfpy.Sprite(x=100, y=100)
sprite.texture = texture
sprite.sprite_index = 5  # Use 6th sprite (0-indexed)
```

### Sprite Sheets with Grids

```python
# Load tileset for grid layers
texture = mcrfpy.Texture("assets/sprites/tileset.png", 16, 16)
terrain = mcrfpy.TileLayer(name="terrain", z_index=-1, texture=texture)

grid = mcrfpy.Grid(grid_size=(50, 50), pos=(100, 100), size=(400, 400),
                    layers=[terrain])

# Set tiles using the TileLayer
for x in range(50):
    for y in range(50):
        terrain.set((x, y), 0)  # Floor tile index
```

---

## Z-Order Layering

Control render order with `z_index` (higher = front):

```python
scene = mcrfpy.Scene("game")
ui = scene.children

# Background layer (z=0)
background = mcrfpy.Frame(pos=(0, 0), size=(800, 600),
                           fill_color=mcrfpy.Color(20, 20, 20))
background.z_index = 0
ui.append(background)

# Game layer (z=10)
grid = mcrfpy.Grid(grid_size=(50, 50), pos=(50, 50), size=(700, 500))
grid.z_index = 10
ui.append(grid)

# UI layer (z=100)
hud = mcrfpy.Frame(pos=(0, 0), size=(800, 50),
                    fill_color=mcrfpy.Color(30, 30, 30, 200))
hud.z_index = 100
ui.append(hud)

# Renders: background -> grid -> hud
mcrfpy.current_scene = scene
```

**Implementation:** Automatic sorting by z_index in `src/Scene.cpp::render()`

---

## Colors

### Color Creation

```python
# RGB
red = mcrfpy.Color(255, 0, 0)

# RGBA (with alpha/transparency)
semi_transparent = mcrfpy.Color(255, 255, 255, 128)

# Access components
color = mcrfpy.Color(100, 150, 200, 255)
# color.r, color.g, color.b, color.a
```

### Color Application

```python
# Frame colors
frame.fill_color = mcrfpy.Color(50, 50, 50)
frame.outline_color = mcrfpy.Color(255, 255, 255)

# Text color
caption.fill_color = mcrfpy.Color(255, 255, 0)  # Yellow text

# Opacity
sprite.opacity = 0.5  # 50% transparent
```

---

## Visual Effects

### Animations

See the Animation System documentation for complete animation details.

```python
# Fade in
frame.animate("opacity", 1.0, 1.0, mcrfpy.Easing.EASE_IN_QUAD)

# Color transition
frame.animate("fill_color", (255, 0, 0, 255), 0.5, mcrfpy.Easing.LINEAR)

# Movement
frame.animate("x", 500.0, 0.3, mcrfpy.Easing.EASE_OUT_CUBIC)
frame.animate("y", 300.0, 0.3, mcrfpy.Easing.EASE_OUT_CUBIC)

# With completion callback
def on_done(target, prop, value):
    print(f"{prop} reached {value}")
frame.animate("x", 500.0, 0.3, mcrfpy.Easing.EASE_OUT_CUBIC, callback=on_done)
```

### Visibility

```python
# Show/hide elements
sprite.visible = False  # Hidden
sprite.visible = True   # Visible

# Opacity
sprite.opacity = 0.0   # Invisible
sprite.opacity = 0.5   # Semi-transparent
sprite.opacity = 1.0   # Opaque
```

---

## Common Patterns

### HUD/UI Overlay

```python
def create_hud(scene):
    ui = scene.children

    hud = mcrfpy.Frame(pos=(0, 0), size=(800, 60),
                        fill_color=mcrfpy.Color(30, 30, 30, 200))
    hud.z_index = 100
    ui.append(hud)

    health_label = mcrfpy.Caption(text="HP: 100/100", pos=(10, 10))
    health_label.font_size = 18
    health_label.fill_color = mcrfpy.Color(255, 255, 255)
    hud.children.append(health_label)

    return health_label

def update_hud(health_label, current_hp, max_hp):
    health_label.text = f"HP: {current_hp}/{max_hp}"

    if current_hp < max_hp * 0.3:
        health_label.fill_color = mcrfpy.Color(255, 0, 0)    # Red
    elif current_hp < max_hp * 0.6:
        health_label.fill_color = mcrfpy.Color(255, 255, 0)  # Yellow
    else:
        health_label.fill_color = mcrfpy.Color(0, 255, 0)    # Green
```

### Particle-Like Effects

```python
def create_explosion(scene, x, y):
    """Create explosion effect using animated frames."""
    import random
    ui = scene.children
    particles = []

    for i in range(10):
        p = mcrfpy.Frame(pos=(x, y), size=(4, 4),
                          fill_color=mcrfpy.Color(255, 200, 50))
        p.z_index = 50

        target_x = x + random.randint(-50, 50)
        target_y = y + random.randint(-50, 50)

        p.animate("x", float(target_x), 0.5, mcrfpy.Easing.EASE_OUT_QUAD)
        p.animate("y", float(target_y), 0.5, mcrfpy.Easing.EASE_OUT_QUAD)
        p.animate("opacity", 0.0, 0.5, mcrfpy.Easing.LINEAR)

        particles.append(p)
        ui.append(p)

    # Cleanup after animation
    # Timer callbacks receive (timer, runtime_ms), not just runtime
    def cleanup(timer, runtime):
        for p in particles:
            ui.remove(p)
    timer = mcrfpy.Timer("explosion_cleanup", cleanup, 600)
```

### Health Bars

```python
class HealthBar:
    def __init__(self, parent, pos, width, height, max_hp):
        self.max_hp = max_hp
        self.width = width

        # Background (red)
        self.bg = mcrfpy.Frame(pos=pos, size=(width, height),
                                fill_color=mcrfpy.Color(255, 0, 0))
        self.bg.z_index = 90
        parent.children.append(self.bg)

        # Foreground (green)
        self.fg = mcrfpy.Frame(pos=pos, size=(width, height),
                                fill_color=mcrfpy.Color(0, 255, 0))
        self.fg.z_index = 91
        parent.children.append(self.fg)

    def set_hp(self, current):
        current = max(0, min(current, self.max_hp))
        ratio = current / self.max_hp
        target_width = int(self.width * ratio)

        self.fg.animate("w", float(target_width), 0.2,
                         mcrfpy.Easing.EASE_OUT_QUAD)

        if ratio < 0.3:
            self.fg.fill_color = mcrfpy.Color(255, 0, 0)
        elif ratio < 0.6:
            self.fg.fill_color = mcrfpy.Color(255, 255, 0)
```

---

## Grid Rendering

See the Grid System documentation for complete grid details.

### Basic Grid

```python
# Load tileset
texture = mcrfpy.Texture("assets/sprites/tileset.png", 16, 16)
terrain = mcrfpy.TileLayer(name="terrain", z_index=-1, texture=texture)

# Create grid with layer
grid = mcrfpy.Grid(grid_size=(50, 50), pos=(100, 100), size=(400, 400),
                    layers=[terrain])

# Set tiles via the TileLayer
for x in range(50):
    for y in range(50):
        if x == 0 or x == 49 or y == 0 or y == 49:
            terrain.set((x, y), 1)  # Wall
        else:
            terrain.set((x, y), 0)  # Floor
```

### Grid Viewport

```python
# Zoom
grid.zoom = 2.0

# Center camera on tile coordinates
grid.center_camera((25, 25))

# Animate viewport
grid.animate("zoom", 1.5, 1.0, mcrfpy.Easing.EASE_IN_OUT)
grid.animate("center_x", 100.0, 1.0, mcrfpy.Easing.EASE_IN_OUT)
```

---

## Performance Tips

### Minimize Draw Calls

```python
# Good: Group related UI in Frames
hud_frame = mcrfpy.Frame(pos=(0, 0), size=(800, 600))
hud_frame.children.append(label1)
hud_frame.children.append(label2)
hud_frame.children.append(label3)

# Avoid: Many top-level UI elements
# (Each top-level element is a separate draw call)
```

### Use Visibility

```python
# Hide off-screen elements
for element in all_elements:
    if not in_viewport(element):
        element.visible = False
```

### Reuse Textures

```python
# Good: One texture, many sprites
texture = mcrfpy.Texture("assets/sprites/all_sprites.png", 16, 16)
for i in range(100):
    sprite = mcrfpy.Sprite(x=i * 20, y=0)
    sprite.texture = texture
    sprite.sprite_index = i
```

---

## Related Documentation

- UI Component Hierarchy - UI element details
- Grid System - Grid rendering details
- Animation System - Animating visual properties
- Performance and Profiling - Rendering performance

---

*Last updated: 2026-02-07*
