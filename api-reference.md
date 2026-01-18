---
layout: default
title: API Reference
---

# API Reference

Complete reference for the `mcrfpy` Python module.

```python
import mcrfpy
```

## Module Attributes

### Scene Management

| Attribute | Type | Description |
|-----------|------|-------------|
| `current_scene` | Scene | Get or set the active scene |
| `scenes` | list | Read-only list of all scene names |

```python
# Get current scene
scene = mcrfpy.current_scene

# Switch scenes
mcrfpy.current_scene = mcrfpy.Scene("gameplay")

# List all scenes
for name in mcrfpy.scenes:
    print(name)
```

### Default Resources

| Attribute | Type | Description |
|-----------|------|-------------|
| `default_font` | Font | JetBrains Mono font, always available |
| `default_texture` | Texture | Kenney Tiny Dungeon tileset (16x16 sprites) |

```python
# Use default resources
caption = mcrfpy.Caption(text="Hello", font=mcrfpy.default_font)
sprite = mcrfpy.Sprite(texture=mcrfpy.default_texture, sprite_index=0)
```

## Module Functions

### Application Control

#### `exit()`

Cleanly shut down the engine and exit the application.

```python
def on_quit():
    mcrfpy.exit()
```

#### `step(dt=None) -> float`

Advance simulation time (headless mode only).

| Parameter | Type | Description |
|-----------|------|-------------|
| `dt` | float | Time to advance in seconds. If None, advances to next scheduled event. |

**Returns:** Actual time advanced in seconds. Returns 0.0 in windowed mode.

```python
# Headless testing
mcrfpy.step(0.016)  # Advance 16ms
mcrfpy.step()       # Advance to next timer/animation
```

#### `setScale(multiplier)`

Scale the game window size (deprecated - use Window.resolution instead).

#### `setDevConsole(enabled)`

Enable or disable the developer console overlay.

```python
mcrfpy.setDevConsole(False)  # Disable for release builds
```

### Element Finding

#### `find(name, scene=None) -> UIDrawable | None`

Find the first UI element with the specified name.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Exact name to search for |
| `scene` | str | Scene to search (default: current scene) |

```python
health_bar = mcrfpy.find("health_bar")
if health_bar:
    health_bar.w = player.hp * 2
```

#### `findAll(pattern, scene=None) -> list`

Find all UI elements matching a name pattern.

| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | str | Name pattern with wildcards (* matches any) |
| `scene` | str | Scene to search (default: current scene) |

```python
# Find all enemies
enemies = mcrfpy.findAll("enemy_*")

# Find all UI elements
ui_elements = mcrfpy.findAll("ui_*")
```

### Performance Monitoring

#### `getMetrics() -> dict`

Get current performance metrics.

**Returns:** Dictionary with keys:
- `frame_time` - Last frame duration in seconds
- `avg_frame_time` - Average frame time
- `fps` - Frames per second
- `draw_calls` - Number of draw calls
- `ui_elements` - Total UI element count
- `visible_elements` - Visible element count
- `current_frame` - Frame counter
- `runtime` - Total runtime in seconds

```python
metrics = mcrfpy.getMetrics()
print(f"FPS: {metrics['fps']:.1f}")
```

#### `start_benchmark()`

Start capturing benchmark data to a JSON file.

#### `end_benchmark() -> str`

Stop benchmark capture and return the filename.

#### `log_benchmark(message)`

Add a log message to the current benchmark frame.

## Classes

For detailed class documentation, see the [Reference](reference) page or individual object pages:

### Core Objects

| Class | Description |
|-------|-------------|
| [Scene](objects/Scene) | Scene container with lifecycle callbacks |
| [Window](objects/Window) | Application window singleton |
| [Timer](objects/Timer) | Scheduled callback execution |

### Drawable Objects

| Class | Description |
|-------|-------------|
| [Frame](objects/Frame) | Rectangular container with children |
| [Caption](objects/Caption) | Text rendering |
| [Sprite](objects/Sprite) | Single sprite display |
| [Grid](objects/Grid) | Tile-based game world |
| [Entity](objects/Entity) | Grid-based game object |
| [Arc](objects/Arc) | Arc/pie shape |
| [Circle](objects/Circle) | Circle shape |
| [Line](objects/Line) | Line shape |

### Grid Layers

| Class | Description |
|-------|-------------|
| [TileLayer](objects/TileLayer) | Tile sprite layer |
| [ColorLayer](objects/ColorLayer) | Color overlay layer |
| [GridPoint](objects/GridPoint) | Tile properties (walkable, transparent) |
| [GridPointState](objects/GridPointState) | Entity visibility state |

### Pathfinding

| Class | Description |
|-------|-------------|
| [AStarPath](objects/AStarPath) | A* pathfinding result |
| [DijkstraMap](objects/DijkstraMap) | Distance field |

### Animation

| Class | Description |
|-------|-------------|
| [Animation](objects/Animation) | Property interpolation |
| [Easing](objects/Easing) | Easing function enum |
| [Transition](objects/Transition) | Scene transition enum |

### Assets

| Class | Description |
|-------|-------------|
| [Font](objects/Font) | Font resource |
| [Texture](objects/Texture) | Sprite sheet |
| [Color](objects/Color) | RGBA color |
| [Vector](objects/Vector) | 2D vector |

### Input

| Class | Description |
|-------|-------------|
| [Key](objects/Key) | Keyboard key enum |
| [Keyboard](objects/Keyboard) | Keyboard state |
| [Mouse](objects/Mouse) | Mouse state |
| [MouseButton](objects/MouseButton) | Mouse button enum |
| [InputState](objects/InputState) | Press/release state |

### Procedural Generation

| Class | Description |
|-------|-------------|
| [NoiseSource](objects/NoiseSource) | Coherent noise generator |
| [HeightMap](objects/HeightMap) | 2D height field |
| [BSP](objects/BSP) | Binary space partitioning |
| [Traversal](objects/Traversal) | BSP traversal order |
| [FOV](objects/FOV) | Field of view algorithm |

### Audio

| Class | Description |
|-------|-------------|
| [Music](objects/Music) | Background music |
| [Sound](objects/Sound) | Sound effects |

### Enums

| Enum | Description |
|------|-------------|
| [Alignment](objects/Alignment) | UI element alignment |
| [Easing](objects/Easing) | Animation easing functions |
| [Transition](objects/Transition) | Scene transitions |
| [Key](objects/Key) | Keyboard keys |
| [MouseButton](objects/MouseButton) | Mouse buttons |
| [InputState](objects/InputState) | Input event states |
| [FOV](objects/FOV) | FOV algorithms |
| [Traversal](objects/Traversal) | BSP traversal orders |

## Automation Module

The `mcrfpy.automation` submodule provides programmatic input control for testing.

```python
from mcrfpy import automation

# Screenshots
automation.screenshot("test.png")

# Mouse control
automation.click(100, 200)
automation.moveTo(300, 400)

# Keyboard
automation.typewrite("hello")
automation.hotkey('ctrl', 's')
```

See individual function documentation in the automation module for details.
