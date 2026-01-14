# McRogueFace

**A Python game engine for roguelikes and tile-based games** - C++ performance, Python simplicity.

---

[**Quickstart**](quickstart) | [**Tutorials**](tutorials) | [**API Reference**](api-reference) | [**Cookbook**](cookbook) | [**Source Code**](https://github.com/jmccardle/McRogueFace)

---

## Build Roguelikes Without the Boilerplate

McRogueFace is a game engine designed specifically for roguelikes and tile-based games. Write your game logic in Python while the C++ engine handles rendering, pathfinding, and field-of-view calculations. No game loop to manage, no low-level graphics code - just import `mcrfpy` and start building your dungeon.

<div style="text-align: center; margin: 2em 0;">
<a href="quickstart" style="background: #4a9; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin-right: 12px; font-weight: bold;">Get Started</a>
<a href="https://github.com/jmccardle/McRogueFace" style="background: #333; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">View on GitHub</a>
</div>

---

## Core Features

| Feature | Description | Learn More |
|---------|-------------|------------|
| **Grid System** | Tile-based world with automatic camera and zoom | [Grid Guide](features/grid_system) |
| **Field of View** | libtcod-powered visibility and fog of war | [FOV Guide](features/fov) |
| **Pathfinding** | A* and Dijkstra algorithms built-in | [Pathfinding Guide](features/pathfinding) |
| **Animation** | Smooth transitions with easing and callbacks | [Animation Guide](features/animation) |
| **Scene Management** | Organize menus, gameplay, and UI screens | [Scenes Guide](features/scenes) |

---

## Quick Example

A complete, runnable example - create a scene, place tiles, add a player, and move with WASD:

```python
import mcrfpy

# Create and activate a game scene
scene = mcrfpy.Scene("game")
scene.activate()

# Load a sprite sheet (16x16 pixel tiles)
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create a 20x15 tile grid at 2x zoom
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture, pos=(112, 84), size=(800, 600))
grid.zoom = 2.0

# Fill with floor tiles, add walls around edges
for y in range(15):
    for x in range(20):
        cell = grid.at(x, y)
        if x == 0 or x == 19 or y == 0 or y == 14:
            cell.tilesprite = 3   # wall
            cell.walkable = False
        else:
            cell.tilesprite = 0   # floor
            cell.walkable = True

# Add grid to scene
scene.children.append(grid)

# Create player entity at tile (10, 7)
player = mcrfpy.Entity(pos=(10, 7), texture=texture, sprite_index=84)
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

    if grid.at(x, y).walkable:
        player.x, player.y = x, y

scene.on_key = on_key
```

Save as `game.py`, run `mcrogueface game.py`, and you have a movable character in a walled room.

---

## Documentation

### Learning Path
- [**Quickstart**](quickstart) - Download and run in 5 minutes
- [**Tutorials**](tutorials) - 14-part series from basics to complete games
- [**Cookbook**](cookbook) - Copy-paste recipes for common patterns

### Reference
- [**API Reference**](api-reference) - Complete `mcrfpy` module documentation
- [**Quick Reference**](quick-reference) - Cheat sheet for common operations
- [**C++ Extensions**](extending-cpp) - Extend the engine with custom C++

### Understanding McRogueFace
- [**Architecture**](explanation/architecture) - Design philosophy and system overview
- [**Entity System**](explanation/entity-system) - How Grid and Entity work together
- [**Procgen Algorithms**](explanation/procgen-algorithms) - When to use BSP vs WFC vs noise

### Project
- [**Roadmap**](roadmap) - Planned features and direction
- [**Extras & Fun**](extras) - Game showcase, asset packs, community tools

---

## Why McRogueFace?

### vs Pygame
Pygame gives you a blank canvas and event loop. McRogueFace gives you Grid, Entity, and FOV systems purpose-built for roguelikes.

### vs libtcod/python-tcod
libtcod is console-based with character cells. McRogueFace is sprite-based with full graphical rendering, while providing the same FOV and pathfinding algorithms.

### vs Godot/Unity
Full engines require learning editors, scene formats, and scripting integration. McRogueFace is a single executable - your entire game is Python scripts. No project files, no asset pipeline, no compile step.

---

## Get Involved

McRogueFace is open source under the MIT license.

- [GitHub Repository](https://github.com/jmccardle/McRogueFace) - Source code, issues, and releases
- [Quickstart Guide](quickstart) - Download and run in 5 minutes
- [Tutorials](tutorials) - Step-by-step guide from basics to complete games

Created for [7DRL 2025](https://7drl.com/). Contributions welcome.
