# McRogueFace Architecture

I built McRogueFace with the intention of writing games entirely in Python, and without accepting the shortcomings like difficult installation, performance impacts, or the boilerplate that games call for. The McRogueFace philosophy is "C++ every frame, Python every tick": once you define your objects, McRogueFace handles rendering them, and your animations play while Python doesn't run at all. When user input occurs, your code modifies your objects. I imagine that means moving sprites around to play a game, but really it's just a Python environment: I hope you'll be enticed by the fun, but stay for the full-blown powers of programming in the same language used by web developers, AI researchers, and system administrators worldwide.

## Design Philosophy: Foundation First

McRogueFace follows a "Foundation First" philosophy: stable fundamentals before feature expansion. This means prioritizing:

- **Performance foundations** over new capabilities
- **API consistency** over rapid feature additions
- **Beginner accessibility** over power-user flexibility

The goal is a beginner-friendly roguelike engine that "just works" for the common cases while remaining extensible for advanced users.

## The Grid: A Unified World View

The Grid is McRogueFace's central abstraction. But what *is* a Grid?

A Grid is both a **`Drawable`**, a McRogueFace object with a position and size that can be drawn on screen, and a container for map data, with flexible presentation. Grids can be much larger on the inside, and will be rendered to screen centered on its camera position.

A Grid represents a fixed array of tiles that make up a game world or level. Its partner class, Entity, represents discrete, moveable objects that interact with the grid through:

- **Display**: Entities render via FOV calculations
- **Movement**: Entities check the `walkable` flag on tiles
- **Interaction**: Entities query other entities in the Grid's collection

Grids can be used to pan and zoom on different points of interest, visualize terrain, place user interface elements adjacent to entities, and draw partially transparent overlays on top of the tiles. The 2D array of tiles inside a Grid is like a classic roguelike's console output, but you can place many of them on-screen at once, or not render it at all to simply use it as a container for pathfinding and visibility data.

## Entity-Grid Coupling: Intentional Design

EntityCollection is a C++ class exposed via Python for entity management. An entity can exist on zero or one grids — adding to a new grid automatically removes from the old one, i.e. the entity is "moved" between grids. This makes the Entity a natural container for characters even as they move between multiple screens or areas of the world.

The tight coupling enables:

- **Automatic spatial indexing** via SpatialHash (37x speedup for radius queries)
- **Efficient FOV updates** that stay on the C++ side
- **Clean Python subclassing** where render properties remain in C++

## The Layer System

Layers are central to any *visible* Grid. While a Grid could theoretically be a pure data store with zero layers, that's rarely useful—you need something to look at.

**Layer types serve different purposes:**

- **TileLayer**: Shows ground/terrain using sprite indices
- **ColorLayer**: Debug visualization or placeholder graphics before assets exist
- **Overlay layers**: Cursors, highlights, selection indicators above entities

Layers also support **C++ data binding** for FOV updates—when `entity.update_visibility()` is called, bound ColorLayers update automatically with minimal Python/C++ boundary crossing.

## Algorithm Integration: libtcod under the hood

McRogueFace exposes libtcod algorithms through its own objects:

- **Grid Path Finding methods**: A* and Djikstra maps integrated with Grid's walkable data
- **Grid + Entity Field of View methods**: Entity perspectives integrated with Grid's transparency data and GridLayer for rendering
- **mcrfpy.HeightMap**: libtcod's heightmap class is a first-class McRogueFace object for handling terrain, path, walkability data
- **mcrfpy.BSP**: libtcod's binary space partitioning tree is a first-class McRogueFace object
- **mcrfpy.NoiseSource**: libtcod's noise generator is a first-class McRogueFace object
- **`mcrfpy.libtcod`**: For utilities that don't directly relate to McRogueFace's objects

*What's a "First Class" McRogueFace object?* Things that relate to what your game renders follow McRogueFace's data model: manipulation of arrays of values stays in C++, and Python requests manipulations to take place. You shouldn't set the visible/discovered/unknown value of every cell for an Entity's perspective, you manage their FOV. You shouldn't copy individual tile values from Grids or Layers or HeightMaps, you call a method to copy a region. Just a few Python commands can instruct libtcod to copy, combine, modify, and generate tens of thousands of tiles for your maps. This is fundamentally what libtcod always enabled, and rendered via its console view - McRogueFace makes the same algorithms and data structures available in a way that supports arbitrary on-screen positioning, scaling, and animation.

## Three Target Audiences

McRogueFace serves three user types with different needs:

1. **Beginners**: Learning game development, need simple APIs and clear tutorials
2. **Game Jammers**: Building quickly under time pressure, need things that "just work"
3. **Researchers**: Exploring procedural generation or AI, need headless mode and automation

Design decisions prioritize the first two audiences, with the third supported through features like headless mode.
