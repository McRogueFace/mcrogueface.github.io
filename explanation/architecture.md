# McRogueFace Architecture

*Understanding why McRogueFace is designed the way it is.*

## Design Philosophy: Foundation First

McRogueFace follows a "Foundation First" philosophy: stable fundamentals before feature expansion. This means prioritizing:

- **Performance foundations** over new capabilities
- **API consistency** over rapid feature additions
- **Beginner accessibility** over power-user flexibility

The goal is a beginner-friendly roguelike engine that "just works" for the common cases while remaining extensible for advanced users.

## The Grid: A Unified World View

The Grid is McRogueFace's central abstraction. But what *is* a Grid?

It's not just a tilemap renderer with algorithms attached. It's not just an algorithm engine with rendering bolted on. **Grid is a unified roguelike "world view" abstraction**—the container for your game's level data that handles rendering, pathfinding, and visibility as integrated concerns.

A Grid represents "something mostly everywhere"—the visible tiles that make up terrain. Its partner class, Entity, represents "discrete, moveable objects" that interact with the grid through:

- **Display**: Entities render via FOV calculations
- **Movement**: Entities check the `walkable` flag on tiles
- **Interaction**: Entities query other entities in the Grid's collection

## Entity-Grid Coupling: Intentional Design

EntityCollection is tightly coupled to Grid by design. An entity can exist on zero or one grids—adding to a new grid automatically removes from the old one.

This isn't a limitation; it's a feature. The tight coupling enables:

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

## Algorithm Integration: libtcod vs Grid Methods

McRogueFace exposes libtcod algorithms through two interfaces:

- **`mcrfpy.libtcod`**: Dijkstra pathfinding, lower-level algorithm access
- **Grid methods**: A* via `find_path()`, integrated with Grid's walkable data

The distinction exists for libtcod familiarity, but the practical guidance is:
- Use Grid methods when working with a specific Grid's terrain
- Use `mcrfpy.libtcod` for standalone algorithm calls

## Three Target Audiences

McRogueFace serves three user types with different needs:

1. **Beginners**: Learning game development, need simple APIs and clear tutorials
2. **Game Jammers**: Building quickly under time pressure, need things that "just work"
3. **Researchers**: Exploring procedural generation or AI, need headless mode and automation

Design decisions prioritize the first two audiences, with the third supported through features like headless mode.
