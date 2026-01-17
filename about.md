---
layout: default
title: About McRogueFace
---

# About McRogueFace

**A Python game engine for roguelikes and tile-based games** - C++ performance, Python simplicity.

## Why McRogueFace?

McRogueFace is designed specifically for roguelikes and tile-based games. Write your game logic in Python while the C++ engine handles rendering, pathfinding, and field-of-view calculations. No game loop to manage, no low-level graphics code - just import `mcrfpy` and start building your dungeon.

### vs Pygame

Pygame gives you a blank canvas and event loop. McRogueFace gives you Grid, Entity, and FOV systems purpose-built for roguelikes. No need to implement your own tile rendering, camera systems, or pathfinding.

### vs libtcod/python-tcod

libtcod is console-based with character cells. McRogueFace is sprite-based with full graphical rendering, while providing the same FOV and pathfinding algorithms under the hood.

### vs Godot/Unity

Full engines require learning editors, scene formats, and scripting integration. McRogueFace is a single executable - your entire game is Python scripts. No project files, no asset pipeline, no compile step.

## Core Philosophy

1. **Python First**: Your entire game logic lives in Python scripts. No C++ required (unless you want to extend the engine).

2. **Batteries Included**: Grid systems, pathfinding, FOV, animations, and UI components are all built-in. Focus on your game, not infrastructure.

3. **Roguelike-Native**: Tile-based rendering, turn-based input handling, and procedural generation tools are first-class features.

4. **Simple Deployment**: One executable, your Python scripts, and your assets. That's it.

## Target Audience

- **Game Jam Participants**: Get a roguelike up and running in hours, not days
- **Python Developers**: Use the language you know without learning a new engine
- **Roguelike Enthusiasts**: Purpose-built tools for the genre you love

## License

McRogueFace is open source under the MIT license. Created for [7DRL 2025](https://7drl.com/).
