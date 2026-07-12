---
layout: default
title: About McRogueFace
mcrf:
  objects: []
  diataxis: meta
  disposition: current
  verified: "0.2.9-dev"
  verified_commit: b6720f6
---

# About McRogueFace

**A Python game engine for roguelikes and tile-based games** - C++ performance, Python simplicity.

## Why McRogueFace?

McRogueFace is designed specifically for roguelikes and tile-based games. Write your game logic in Python while the C++ engine handles rendering, pathfinding, and field-of-view calculations. No game loop to manage, no low-level graphics code - just import `mcrfpy` and start building your dungeon.

### vs Pygame

Pygame gives you a blank canvas and event loop. McRogueFace gives you Grid, Entity, and FOV systems purpose-built for roguelikes - plus a turn manager, A* and Dijkstra pathfinding, and procedural generation tools (HeightMap, BSP, noise). No need to implement your own tile rendering, camera system, or pathfinding.

### vs libtcod/python-tcod

libtcod is console-based with character cells. McRogueFace is sprite-based with full graphical rendering, while providing the same FOV and pathfinding algorithms under the hood - it embeds libtcod itself.

### vs Godot/Unity

Full engines require learning editors, scene formats, and scripting integration. McRogueFace is a single executable - your entire game is Python scripts. No project files, no asset pipeline, no compile step.

## Core Philosophy

1. **C++ every frame, Python every tick**: Rendering, animation interpolation, and pathfinding run in native code. Your Python sets up the scene and responds to events; the engine draws it without touching the interpreter.

2. **Batteries Included**: Grid systems, pathfinding, FOV, animations, procedural generation, audio, and UI components are all built-in. Focus on your game, not infrastructure.

3. **Roguelike-Native**: Tile-based rendering, a turn-based entity manager (`grid.step()`), entity behaviors, and dungeon generation are first-class features.

4. **Zip and Ship**: One executable, your Python scripts, and your assets. The runtime is a full Python environment - distribute your game by zipping a folder.

## The Story So Far

McRogueFace began in February 2023 as an experiment: could SFML graphics, an embedded Python interpreter, and libtcod's roguelike algorithms live in one binary? The 7-Day Roguelike Challenge turned that experiment into an engine - McRogueFace has been developed through four consecutive 7DRLs (2023-2026), each jam stress-testing the engine against a real deadline.

**Crypt of Sokoban**, a boulder-pushing dungeon crawler built in a single 7DRL week, became the engine's proving ground - and still ships as the demo game you see when you first run McRogueFace.

Since then the project has shifted from jam-driven features to foundation-first engineering:

- **Alpha 0.1** (2024) delivered the first complete release with all core datatypes stable.
- **The 0.2 series** (2026) added multi-layer grids, the Behavior/Trigger turn manager, procedural generation (HeightMap, BSP, noise), Tiled and LDtk import, animation callbacks, Windows cross-compilation, and WebAssembly builds - the same engine that powers the in-browser [Playground](playground/).
- **The road to 1.0** (current, version 0.2.8): the public API is being audited and frozen, locked behind a snapshot regression test, while a fuzzing campaign sweeps the engine for memory-safety bugs. The 1.0 criteria are performance, stability, and documentation - not feature count.

For the blow-by-blow, see the [Project History](history) page and the [development roadmap](roadmap).

## Target Audience

- **Game Jam Participants**: Get a roguelike up and running in hours, not days
- **Python Developers**: Use the language you know without learning a new engine
- **Roguelike Enthusiasts**: Purpose-built tools for the genre you love

## License

McRogueFace is open source under the MIT license.

## Credits

- Created by John McCardle. (Blame his wife for the name.)
- Built with [SFML](https://www.sfml-dev.org/), [libtcod](https://github.com/libtcod/libtcod), and [Python](https://www.python.org/)
- Inspired by David Churchill's COMP4300 game engine lectures
- Demo assets include [Kenney's](https://kenney.nl/) Tiny Dungeon tileset

Contributions are welcome - see the [GitHub repository](https://github.com/jmccardle/McRogueFace) for source, issues, and releases.
