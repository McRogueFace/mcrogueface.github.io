---
layout: default
title: Reference
mcrf:
  objects: []
  diataxis: reference
  disposition: needs-review
  verified: "0.3.0-dev"
  verified_commit: 73acab0
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

| Object | Description |
|--------|-------------|
| [Window](objects/Window) | The application window singleton |
| [Scene](objects/Scene) | Container for UI elements and game state |
| [Frame](objects/Frame) | Rectangular container with background |
| [Caption](objects/Caption) | Text rendering |
| [Sprite](objects/Sprite) | Single sprite rendering |
| [Arc](objects/Arc) | Arc/pie shape drawing |
| [Circle](objects/Circle) | Circle shape drawing |
| [Line](objects/Line) | Line drawing |
| [Drawable](objects/Drawable) | Base class for all drawable elements |

### Asset Objects

| Object | Description |
|--------|-------------|
| [Font](objects/Font) | Font loading and management |
| [Texture](objects/Texture) | Sprite sheet loading |
| [Color](objects/Color) | RGBA color representation |
| [Vector](objects/Vector) | 2D vector for positions and sizes |

### Grid System Objects

| Object | Description |
|--------|-------------|
| [Grid](objects/Grid) | Tile-based game world: `GridData` (the map) and `GridView` (the drawable camera); `Grid` is an alias of `GridView` ([GridData](reference/generated/GridData), [GridView](reference/generated/GridView)) |
| [GridPoint](objects/GridPoint) | Individual tile data (walkable, transparent) |
| [Entity](objects/Entity) | Game objects that exist on grids (per-entity FOV memory via `perspective_map`) |
| [TileLayer](objects/TileLayer) | Tile sprite layer for grids |
| [ColorLayer](objects/ColorLayer) | Color overlay layer for grids |

### Pathfinding Objects

| Object | Description |
|--------|-------------|
| [AStarPath](objects/AStarPath) | A* pathfinding result |
| [DijkstraMap](objects/DijkstraMap) | Distance field from a root position |
| [FOV](objects/FOV) | Field of view algorithm enum |

### Input Objects

| Object | Description |
|--------|-------------|
| [Timer](objects/Timer) | Scheduled callbacks |
| [Key](objects/Key) | Keyboard key enum |
| [Keyboard](objects/Keyboard) | Keyboard state queries |
| [Mouse](objects/Mouse) | Mouse state and position |
| [MouseButton](objects/MouseButton) | Mouse button enum |
| [InputState](objects/InputState) | Input event state enum (pressed/released) |

### Animation Objects

| Object | Description |
|--------|-------------|
| [Animation](objects/Animation) | Animation handle returned by drawable.animate() (mcrfpy.Animation is not directly constructible) |
| [Easing](objects/Easing) | Easing function enum |
| [Transition](objects/Transition) | Scene transition enum |
| [Alignment](objects/Alignment) | UI element alignment enum |

### Procedural Generation Objects

| Object | Description |
|--------|-------------|
| [NoiseSource](objects/NoiseSource) | Coherent noise generation (Perlin, Simplex, etc.) |
| [HeightMap](objects/HeightMap) | 2D height field for terrain generation |
| [BSP](objects/BSP) | Binary space partitioning for dungeon generation |
| [Traversal](objects/Traversal) | BSP tree traversal order enum |

### Audio Objects

| Object | Description |
|--------|-------------|
| [Music](objects/Music) | Background music playback |
| [Sound](objects/Sound) | Sound effect playback |

## Module Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| [`current_scene`](reference/generated/functions) | Scene | Get or set the active scene: `mcrfpy.current_scene = mcrfpy.Scene("gameplay")` |
| `scenes` | tuple[str] | Read-only tuple of all scene names |
| `default_font` | Font | JetBrains Mono font, always available |
| `default_texture` | Texture | Kenney Tiny Dungeon tileset (16x16 sprites) |

## Module Functions

For every top-level `mcrfpy` function (`step`, `advance`, `lock`, `find`, `find_all`, `get_metrics`, `bresenham`, the benchmark API, ...), see the auto-generated [Module Functions](reference/generated/functions) reference, extracted directly from the C++ docstrings.

## Quick Reference

For a condensed cheat sheet of common operations, see the [Quick Reference](quick-reference).

## Full API

For the complete generated `mcrfpy` object reference (every class, method, and property, with lifecycle badges), see [Generated Reference](reference/generated/functions).
