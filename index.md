---
layout: home
title: Home
---

## Quick Example

A complete, runnable example - create a scene, add a grid, place a player, and move with WASD:

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

## Get Involved

McRogueFace is open source under the MIT license.

- [GitHub Repository](https://github.com/jmccardle/McRogueFace) - Source code, issues, and releases
- [Tutorials](tutorials) - Step-by-step guide from basics to complete games

Created for [7DRL 2025](https://7drl.com/). Contributions welcome.
