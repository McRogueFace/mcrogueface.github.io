---
layout: default
title: Tutorials
mcrf:
  objects: [Scene, Texture, Grid, Entity, Caption, Timer, Color]
  diataxis: tutorial
  disposition: current
  verified: "0.2.9-dev"
  verified_commit: b6720f6
---

# Tutorials

Build a complete roguelike game from scratch with the McRogueFace tutorial series. Across 14 parts you will go from a blank window to a finished game with procedural dungeons, field of view, combat, items, saving, and character progression - all in Python, with no compilation required.

Each part builds on the previous one and ends with a working game you can run. If you are brand new to McRogueFace, the [Quickstart](/quickstart) will get the engine installed and running in a few minutes; the series below assumes you can launch a script.

> **Note:** This page previously hosted a standalone three-part tutorial written against a much older version of the engine. It has been replaced by the full series below, which tracks the current API.

## The Roguelike Tutorial Series

| Part | Topic | What you build |
|------|-------|----------------|
| [Part 0: Setting Up McRogueFace](/tutorial/part_00_setup) | Engine basics | Your first script - and an understanding of the embedded interpreter, the built-in game loop, and Scenes |
| [Part 1: The '@' and the Dungeon Grid](/tutorial/part_01_grid_movement) | Grid, Entity, input | A tile-based world with a player character you move using the keyboard |
| [Part 2: Walls, Floors, and Collision](/tutorial/part_02_tiles_collision) | Tiles, walkability | A hand-made map with walls that actually block movement |
| [Part 3: Procedural Dungeon Generation](/tutorial/part_03_dungeon_generation) | Procgen | Rooms and corridors generated fresh every run |
| [Part 4: Field of View](/tutorial/part_04_fov) | FOV | Classic fog of war - unexplored areas hidden, explored areas fading into memory |
| [Part 5: Placing Enemies](/tutorial/part_05_enemies) | Spawning, visibility | Goblins, orcs, and trolls that appear only when your hero can see them |
| [Part 6: Combat System](/tutorial/part_06_combat) | Bump combat | HP, attack, defense, and death - for the player and the monsters |
| [Part 7: User Interface](/tutorial/part_07_ui) | Frames, Captions | A visual health bar, scrolling message log, and dungeon info panel |
| [Part 8: Items and Inventory](/tutorial/part_08_items) | Items | Health potions on the floor, a pickup command, and an inventory screen |
| [Part 9: Ranged Combat and Targeting](/tutorial/part_09_ranged) | Targeting mode | Attack spells with a cursor-driven targeting system |
| [Part 10: Saving and Loading](/tutorial/part_10_save_load) | Serialization | Persistent progress between play sessions |
| [Part 11: Multiple Dungeon Levels](/tutorial/part_11_levels) | Level transitions | Stairs descending into progressively deadlier floors |
| [Part 12: Experience and Leveling](/tutorial/part_12_experience) | Progression | XP rewards and level-up stat gains |
| [Part 13: Equipment System](/tutorial/part_13_equipment) | Equipment | Weapons and armor with stat bonuses - and a finished roguelike |

## McRogueFace at a Glance

If you want a feel for the engine before committing to Part 0, this short script shows the objects the series is built around. Save it as `scripts/game.py` in your McRogueFace folder and run the executable:

```python
"""McRogueFace at a glance - the core objects the tutorial series teaches."""
import mcrfpy

# A Scene holds a tree of UI elements; one scene is active at a time
scene = mcrfpy.Scene("hub_demo")

# A Texture is a sprite atlas - this sheet uses 16x16 pixel tiles
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# A Grid is a tile-based world; entities live in its cells
grid = mcrfpy.Grid(grid_size=(20, 12), texture=texture,
                   pos=(112, 120), size=(800, 480))
grid.zoom = 2.0
grid.center_camera()  # camera helpers take tile coordinates
scene.children.append(grid)

# An Entity occupies a logical cell on the grid
player = mcrfpy.Entity(grid_pos=(10, 6), texture=texture, sprite_index=84)
grid.entities.append(player)

# Captions draw text; Color is RGBA
status = mcrfpy.Caption(text="Arrow keys to move", pos=(112, 60))
status.fill_color = mcrfpy.Color(255, 255, 255)
scene.children.append(status)

# Animations start from the object itself - no Animation class to construct
grid.animate("zoom", 2.5, 1.5, mcrfpy.Easing.EASE_IN_OUT)

# Keyboard input arrives as Key and InputState enums
def on_key(key, state):
    if state != mcrfpy.InputState.PRESSED:
        return
    dx, dy = 0, 0
    if key == mcrfpy.Key.LEFT:
        dx = -1
    elif key == mcrfpy.Key.RIGHT:
        dx = 1
    elif key == mcrfpy.Key.UP:
        dy = -1
    elif key == mcrfpy.Key.DOWN:
        dy = 1
    if dx or dy:
        x, y = player.cell_x + dx, player.cell_y + dy
        player.grid_pos = (x, y)
        status.text = f"Player at ({x}, {y})"

scene.on_key = on_key

# Timers fire callbacks on an interval, measured in milliseconds
def tick(timer, runtime_ms):
    print(f"Engine has been running for {runtime_ms / 1000:.1f} s")

heartbeat = mcrfpy.Timer("heartbeat", tick, 1000)

scene.activate()
```

A few things worth noticing - the tutorial series explains each in depth:

- **There is no `run()` call.** The engine is already running; it imports your script and takes over from there.
- **Entities track a logical cell** (`grid_pos` / `cell_x` / `cell_y`), which is separate from the pixel position used for drawing. Grid coordinates are tiles; screen coordinates are pixels.
- **Animations are started from the object** with `obj.animate(property, target, duration, easing)`, using the `mcrfpy.Easing` enum. Older documentation showed a constructible `Animation` class - that idiom is gone.
- **Input handlers receive enums**, not strings: `mcrfpy.Key` and `mcrfpy.InputState` for the keyboard, `mcrfpy.MouseButton` for the mouse.
- **Timer intervals are milliseconds**, and callbacks receive `(timer, runtime_ms)`.

## Where to Go Next

- [Quickstart](/quickstart) - download, install, and run the engine
- [Cookbook](/cookbook) - copy-paste recipes for common patterns
- [API Reference](/reference) - every class, method, and property
- [Quick Reference](/quick-reference) - a condensed cheat sheet
