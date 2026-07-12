---
layout: home
title: Home
mcrf:
  objects: [Scene, Texture, Grid, TileLayer, Entity, Key, InputState]
  diataxis: meta
  disposition: current
  verified: "0.2.9-dev"
  verified_commit: b6720f6
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

# Create a 20x15 tile grid, drawn at 2x zoom
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture, pos=(112, 84), size=(800, 600))
grid.zoom = 2.0
scene.children.append(grid)

# Tiles live on layers: add one, then fill it with floor and walls
tiles = mcrfpy.TileLayer(name="terrain", z_index=-1, texture=texture)
grid.add_layer(tiles)

WALL, FLOOR = 3, 0
for y in range(15):
    for x in range(20):
        edge = x in (0, 19) or y in (0, 14)
        tiles.set((x, y), WALL if edge else FLOOR)
        grid.at(x, y).walkable = not edge

# Create a player entity at cell (10, 7)
player = mcrfpy.Entity(grid_pos=(10, 7), texture=texture, sprite_index=84)
grid.entities.append(player)

# Move with WASD; walls block movement
MOVES = {mcrfpy.Key.W: (0, -1), mcrfpy.Key.S: (0, 1),
         mcrfpy.Key.A: (-1, 0), mcrfpy.Key.D: (1, 0)}

def on_key(key, state):
    if state != mcrfpy.InputState.PRESSED or key not in MOVES:
        return
    dx, dy = MOVES[key]
    x, y = player.cell_x + dx, player.cell_y + dy
    if grid.at(x, y).walkable:
        player.grid_pos = (x, y)

scene.on_key = on_key
```

Save it as `scripts/game.py` next to the McRogueFace executable, run `mcrogueface`, and you have a movable character in a walled room. No install, no compile step - the engine *is* the Python runtime.

## Where Next

- [Quickstart](quickstart) - download, run, and modify your first game in minutes
- [Tutorial](tutorial/part_00_setup) - build a complete roguelike, step by step
- [Cookbook](cookbook/) - copy-paste recipes for common patterns
- [Reference](reference) - every object, method, and system in detail
- [Playground](playground/) - try McRogueFace in your browser, nothing to install

---

## Get Involved

McRogueFace is open source under the MIT license. The current release is **0.2.8**, and the API is being finalized for a 1.0 freeze.

- [GitHub Repository](https://github.com/jmccardle/McRogueFace) - source code, issues, and [releases](https://github.com/jmccardle/McRogueFace/releases/latest)
- [About](about) - the engine's story, from 7DRL experiment to 1.0 candidate

Forged across four 7-Day Roguelike challenges (2023-2026) and still in active development. Contributions welcome.
