---
layout: default
title: Scene System
---

# Scene System

The Scene System is McRogueFace's core rendering and UI architecture. It manages the application window, organizes content into scenes, and provides UI components for building game interfaces.

## Overview

```
Window
  └── Scene (active)
        └── children (UICollection)
              ├── Frame
              ├── Caption
              ├── Sprite
              └── Grid
```

Every McRogueFace application has one [Window](../objects/Window). The window displays one active [Scene](../objects/Scene) at a time. Scenes contain a collection of UI elements (their `children`), which are rendered in order from back to front.

## Objects

| Object | Purpose |
|--------|---------|
| [Window](../objects/Window) | Application window, display settings |
| [Scene](../objects/Scene) | Container for UI elements, input handling |
| [Frame](../objects/Frame) | Rectangular container with background and border |
| [Caption](../objects/Caption) | Text rendering with font and color |
| [Font](../objects/Font) | Font loading and text measurement |
| [Sprite](../objects/Sprite) | Single image/sprite rendering |
| [Texture](../objects/Texture) | Sprite sheet loading and management |

---

## Text Subsystem {#text}

The text subsystem handles all text rendering through [Caption](../objects/Caption) and [Font](../objects/Font) objects.

### Font Loading

Fonts are loaded from TTF files:

```python
font = mcrfpy.Font("assets/fonts/DejaVuSans.ttf")
```

### Creating Captions

Captions render text at a position:

```python
caption = mcrfpy.Caption(pos=(100, 50), text="Hello, World!")
caption.font = font
caption.size = 24
caption.color = mcrfpy.Color(255, 255, 255)
scene.children.append(caption)
```

### Text Measurement

Use Font's `measure()` method to get text dimensions for layout:

```python
width, height = font.measure("Hello", size=24)
```

---

## Image Subsystem {#image}

The image subsystem handles sprite rendering through [Texture](../objects/Texture) and [Sprite](../objects/Sprite) objects.

### Loading Textures

Textures load sprite sheets with a specified tile size:

```python
# Load a 16x16 tile sprite sheet
texture = mcrfpy.Texture("assets/sprites.png", 16, 16)
```

### Creating Sprites

Sprites display a single tile from a texture:

```python
sprite = mcrfpy.Sprite(pos=(200, 100), texture=texture, sprite_index=42)
sprite.scale = 2.0  # Double size
scene.children.append(sprite)
```

### Texture Usage

Textures are shared across multiple objects:
- [Sprite](../objects/Sprite) - Single sprite display
- [Grid](../objects/Grid) - Tile-based world rendering
- [Entity](../objects/Entity) - Game objects on grids

---

## Children Collection Subsystem {#children}

Every Scene and Frame has a `children` property - a [UICollection](../objects/UICollection) that holds UI elements.

### Adding Elements

```python
scene.children.append(frame)
scene.children.append(caption)
scene.children.append(grid)
```

### Render Order

Elements render in order - first added is furthest back:

```python
# Background frame (renders first, behind everything)
scene.children.append(background_frame)

# Game grid (renders on top of background)
scene.children.append(grid)

# UI overlay (renders on top of grid)
scene.children.append(ui_frame)
```

### Nested Frames

Frames can contain their own children for hierarchical UI:

```python
panel = mcrfpy.Frame(pos=(10, 10), size=(200, 300))
panel.children.append(title_caption)
panel.children.append(content_caption)
scene.children.append(panel)
```

---

## Related Objects

<div class="related-objects">
<div class="object-links">
<a href="../objects/Window" class="object-link">Window</a>
<a href="../objects/Scene" class="object-link">Scene</a>
<a href="../objects/Frame" class="object-link">Frame</a>
<a href="../objects/Caption" class="object-link">Caption</a>
<a href="../objects/Font" class="object-link">Font</a>
<a href="../objects/Sprite" class="object-link">Sprite</a>
<a href="../objects/Texture" class="object-link">Texture</a>
</div>
</div>
