# The Entity System

*How Entities, Grids, and spatial indexing work together.*

## Core Relationship: Entity and Grid

An Entity is a "discrete, moveable object" that lives on a Grid. This relationship is bidirectional:

- Entities reference their grid via `entity.grid`
- Grids track entities via `grid.entities` (an EntityCollection)

**Key constraint:** An entity can only exist on 0 or 1 grids at a time. Adding an entity to a new grid automatically removes it from the old one.

This isn't a limitation—it's a design choice that enables automatic spatial indexing and clean ownership semantics.

## Why Tight Coupling?

EntityCollection is intentionally coupled to Grid. The benefits:

1. **Automatic SpatialHash updates**: When an entity moves, the spatial index updates automatically
2. **Efficient C++ iteration**: The collection lives in C++, avoiding Python overhead for bulk operations
3. **Clean subclassing**: Python users subclass Entity; render-relevant properties stay in C++

If you need entities that aren't on a grid, you probably want UI elements (Sprites, Captions) instead.

## Spatial Indexing: SpatialHash

For games with many entities, linear scanning becomes a bottleneck. McRogueFace uses SpatialHash for O(k) spatial queries where k is nearby entity count, not total entities.

**Performance gains are dramatic:**

| Entity Count | Linear Scan | SpatialHash | Speedup |
|--------------|-------------|-------------|---------|
| 1,000 | 2.1ms | 0.08ms | 26x |
| 5,000 | 10.5ms | 0.28ms | 37x |

**Key operations:**
- `grid.entities_at(x, y)` — entities at exact position
- `grid.entities_in_radius(x, y, r)` — entities within radius (ideal for AI)

The spatial index updates automatically when entity positions change.

## Visibility System

Entities track what they can see through the `gridstate` system:

- **Visible cells**: Currently in line-of-sight
- **Discovered cells**: Previously seen (for fog-of-war)

Call `entity.update_visibility()` to recompute FOV. This:
1. Runs libtcod's FOV algorithm from entity position
2. Updates the entity's gridstate
3. Auto-updates any bound ColorLayers

**Why bind layers?** ColorLayers can visualize FOV without Python iteration. The binding happens in C++, so updating thousands of cells is fast.

## Movement and Collision

Entity movement is straightforward:

```python
entity.x, entity.y = new_x, new_y
```

Check walkability before moving:

```python
if grid.at(new_x, new_y).walkable:
    entity.x, entity.y = new_x, new_y
```

For animated movement, use the Animation system instead of direct position changes.

## Entity Lifecycle

- **Creation**: `entity = mcrfpy.Entity((x, y), texture=tex, sprite_index=idx)`
- **Adding to grid**: `grid.entities.append(entity)`
- **Removal**: `entity.die()` removes from grid and spatial index
- **Cleanup**: Python garbage collection handles the rest
