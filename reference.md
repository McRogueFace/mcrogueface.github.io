---
layout: default
title: Reference
---

# Reference

Complete documentation for McRogueFace systems and objects.

## Systems

High-level guides explaining how McRogueFace's major systems work together.

| System | Description |
|--------|-------------|
| [Scene System](systems/scene) | Windows, scenes, frames, and UI rendering |
| [Grid System](systems/grid) | Tile-based worlds, layers, FOV, and pathfinding |
| [Input & Callbacks](systems/input) | Keyboard, mouse, and timer events |
| [Animation](systems/animation) | Smooth transitions with easing functions |
| [Procedural Generation](systems/procgen) | HeightMaps, BSP, and noise generation |

## Objects

Detailed reference for every McRogueFace object.

### Scene System Objects
- [Window](objects/Window) - The application window
- [Scene](objects/Scene) - Container for UI elements and game state
- [Frame](objects/Frame) - Rectangular container with background
- [Caption](objects/Caption) - Text rendering
- [Font](objects/Font) - Font loading and management
- [Sprite](objects/Sprite) - Single sprite rendering
- [Texture](objects/Texture) - Sprite sheet loading

### Grid System Objects
- [Grid](objects/Grid) - Tile-based game world
- [GridPoint](objects/GridPoint) - Individual tile in a grid
- [GridPointState](objects/GridPointState) - Tile appearance state
- [Entity](objects/Entity) - Game objects that exist on grids

### Input & Timer Objects
- [Timer](objects/Timer) - Scheduled callbacks

### Animation Objects
- [Animation](objects/Animation) - Property animation system

### Procedural Generation Objects
- [Perlin](objects/Perlin) - Perlin noise generation

## Quick Reference

For a condensed cheat sheet of common operations, see the [Quick Reference](quick-reference).

## Full API

For the complete `mcrfpy` module documentation with all methods and parameters, see the [API Reference](api-reference).
