# McRogueFace

**A Python game engine for roguelikes and tile-based games** - C++ performance, Python simplicity.

---

[**Source Code**](https://github.com/jmccardle/McRogueFace) | [**Downloads**](https://github.com/jmccardle/McRogueFace/releases) | [**Quickstart**](https://mcrogueface.github.io/quickstart) | [**Tutorials**](https://mcrogueface.github.io/tutorials) | [**API Reference**](https://mcrogueface.github.io/api-reference) | [**Cookbook**](https://mcrogueface.github.io/cookbook) | [**C++ Extensions**](https://mcrogueface.github.io/extending-cpp)

---

## Build Roguelikes Without the Boilerplate

McRogueFace is a game engine designed specifically for roguelikes and tile-based games. Write your game logic in Python while the C++ engine handles rendering, pathfinding, and field-of-view calculations. No game loop to manage, no low-level graphics code - just import `mcrfpy` and start building your dungeon.

<div style="text-align: center; margin: 2em 0;">
<a href="https://mcrogueface.github.io/quickstart" style="background: #4a9; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin-right: 12px; font-weight: bold;">Get Started</a>
<a href="https://github.com/jmccardle/McRogueFace" style="background: #333; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">View on GitHub</a>
</div>

---

## Feature Highlights

### Grid and Entity System
The Grid is the foundation of your game world. Place tiles, spawn entities, and let the engine handle efficient rendering with automatic camera controls and zoom. Entity positions are in tile coordinates - no pixel math required.

### Built-in FOV and Pathfinding
Field-of-view uses libtcod algorithms out of the box. Set `walkable` and `transparent` on your tiles, call `update_visibility()` on your entities, and you get accurate line-of-sight. A* and Dijkstra pathfinding work the same way - define your terrain, get paths back.

### Animation System
Smooth movement, color transitions, and property interpolation through a declarative animation API. Chain animations with callbacks, queue moves for responsive controls, choose from multiple easing functions.

### Scene Management
Organize your game into scenes - menus, gameplay, inventory screens. Each scene has its own UI collection and can be switched instantly. The engine preserves scene state, so switching back picks up right where you left off.

### Sprite-Based Rendering
Load sprite sheets with `mcrfpy.Texture()`, specify tile dimensions, and reference sprites by index. The same texture works for Grid tiles, Entities, and UI Sprites. Supports transparency, color tinting, and overlay layers.

### Audio and Input
Background music, sound effects, and volume control built in. Keyboard input comes through a simple callback with key name and state. Click handlers attach directly to UI elements and Grid tiles.

---

## Quick Example

Here is a complete, runnable example that creates a scene with a grid, places some walls and floors, adds a player entity, and lets you move with WASD:

```python
import mcrfpy

# Create and switch to a game scene
mcrfpy.createScene("game")
mcrfpy.setScene("game")

# Load a sprite sheet (16x16 pixel tiles)
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create a 20x15 tile grid, displayed at 2x zoom
grid = mcrfpy.Grid(
    grid_size=(20, 15),
    texture=texture,
    pos=(112, 84),
    size=(800, 600)
)
grid.zoom = 2.0

# Fill with floor tiles, add walls around edges
for y in range(15):
    for x in range(20):
        point = grid.at(x, y)
        if x == 0 or x == 19 or y == 0 or y == 14:
            point.tilesprite = 3   # wall
            point.walkable = False
        else:
            point.tilesprite = 0   # floor
            point.walkable = True

# Add the grid to the scene
mcrfpy.sceneUI("game").append(grid)

# Create a player entity at tile (10, 7)
player = mcrfpy.Entity((10, 7), texture=texture, sprite_index=84)
grid.entities.append(player)

# Handle keyboard input
def on_key(key, state):
    if state != "start":
        return
    x, y = int(player.x), int(player.y)
    if key == "W": y -= 1
    elif key == "S": y += 1
    elif key == "A": x -= 1
    elif key == "D": x += 1

    # Only move if destination is walkable
    if grid.at(x, y).walkable:
        player.x, player.y = x, y

mcrfpy.keypressScene(on_key)
```

Save this as `scripts/game.py`, run `mcrogueface`, and you have a movable character in a walled room. The grid handles rendering, the entity tracks position in tile coordinates, and the keyboard callback updates state on each keypress.

---

## Why McRogueFace?

### Compared to Pygame
Pygame gives you a blank canvas and event loop. McRogueFace gives you a Grid, Entity, and FOV system purpose-built for roguelikes. You write game logic instead of rendering code.

### Compared to libtcod/python-tcod
libtcod is console-based with character cells. McRogueFace is sprite-based with full graphical rendering, while still providing the same FOV and pathfinding algorithms you expect.

### Compared to Godot/Unity
Full game engines require learning their editor, scene format, and scripting integration. McRogueFace is a single executable - your entire game is Python scripts that run when the engine starts. No project files, no asset pipeline, no compile step.

### The Roguelike-First Design
Most engines treat tile-based games as one use case among many. McRogueFace treats it as the primary use case. Grid coordinates, turn-based input, visibility state, pathfinding costs - these are first-class concepts, not things you build on top of a general-purpose renderer.

---

## Get Involved

McRogueFace is open source under the MIT license.

- [GitHub Repository](https://github.com/jmccardle/McRogueFace) - Source code, issues, and releases
- [Quickstart Guide](https://mcrogueface.github.io/quickstart) - Download and run in 5 minutes
- [Tutorials](https://mcrogueface.github.io/tutorials) - Step-by-step guide from basics to complete games
- [API Reference](https://mcrogueface.github.io/api-reference) - Complete documentation of the `mcrfpy` module

Created for [7DRL 2025](https://7drl.com/). Contributions welcome.
