---
mcrf:
  objects: [Grid, Entity, DijkstraMap, AStarPath, Behavior]
  diataxis: howto
  disposition: current
  verified: "0.3.0-dev"
  verified_commit: 73acab0
---

# Pathfinding

McRogueFace provides built-in pathfinding algorithms for AI movement, player auto-travel, and tactical analysis. The engine supports A* pathfinding for point-to-point routes and Dijkstra maps for distance calculations.

## A* Pathfinding

A* finds the shortest path between two points, respecting walkability.

### Entity.path_to()

The simplest way to pathfind - ask an entity for a path to a destination. `path_to(x, y)`
takes **grid/tile coordinates** and returns a plain `list` of `(x, y)` tuples (not an
`AStarPath` object):

```python
import mcrfpy

# Create an entity on a grid (grid must already exist)
entity = mcrfpy.Entity(grid_pos=(5, 5), texture=mcrfpy.default_texture, sprite_index=64)
grid.entities.append(entity)

# Find path to destination (grid coordinates)
path = entity.path_to(20, 15)

if path:
    print(f"Path found! {len(path)} steps")
    for x, y in path:
        print(f"  -> ({x}, {y})")
else:
    print("No path available")
```

The returned path is a list of `(x, y)` tuples representing each step from the current
position to the destination.

There is also `entity.find_path(target, diagonal_cost=1.41, collide=None)`, which returns
an `AStarPath` object (consumed step-by-step with `.walk()`/`.peek()`) instead of a plain
list — useful when you want to keep the path around and consume it turn by turn.

### Grid.find_path()

For pathfinding without an entity, use the grid directly. `Grid.find_path()` takes
`start`/`end` positions (tuples, `Vector`s, or `Entity`s) and returns an `AStarPath`
object, or `None` if no path exists:

```python
# Find path between any two points
start = (5, 5)
end = (20, 15)
path = grid.find_path(start, end)

if path:
    print(f"Found path with {len(path)} steps")
```

### Walkability

Pathfinding respects the `walkable` property of each GridPoint:

```python
# Set up a simple map
for y in range(30):
    for x in range(40):
        point = grid.at(x, y)
        point.walkable = True

# Add some walls
for x in range(10, 25):
    point = grid.at(x, 15)
    point.walkable = False

# Path will go around the wall
path = entity.path_to(20, 20)  # Will route around the obstacle
```

After changing any cell's `walkable` state, call `grid.clear_dijkstra_maps()` to
invalidate cached Dijkstra maps (A* via `find_path`/`path_to` always recomputes fresh,
but Dijkstra maps are cached by root position).

### Error Handling

```python
# Invalid target coordinates
try:
    path = entity.path_to(100, 100)  # Outside grid bounds
except ValueError as e:
    print(f"Invalid target: {e}")

# Unreachable destination
path = entity.path_to(25, 25)
if path is None or len(path) == 0:
    print("Cannot reach destination")
```

## Dijkstra Distance Maps

Dijkstra maps calculate distances from a source point to all reachable tiles. This is useful for:
- AI that needs to know distances to multiple targets
- Heat maps showing "danger zones"
- Multi-agent pathfinding
- Flee behavior (move away from player)

### Computing a Dijkstra Map

`Grid.get_dijkstra_map(root)` returns a `DijkstraMap` object. Grids cache these by root
position, so calling it again with the same root is cheap:

```python
# Compute distances from a source point
source = (25, 15)
dijkstra = grid.get_dijkstra_map(source)

# Now query distances from any point
distance = dijkstra.distance((10, 10))
if distance is not None:
    print(f"Distance from (10,10) to source: {distance}")
else:
    print("Position is unreachable")
```

### Getting Paths from Dijkstra

Once computed, you can get the shortest path from any point back to the root, or take a
single step toward it:

```python
# Compute from player's grid position
dijkstra = grid.get_dijkstra_map(player.grid_pos)

# Full path from enemy to the root (player), in walking order:
# path.walk() yields the first step first
path = dijkstra.path_from(enemy.grid_pos)
if path:
    next_pos = path.walk()
    enemy.grid_pos = next_pos

# Or just take one step toward the root (an adjacent cell) without building a full path
step = dijkstra.step_from(enemy.grid_pos)
if step is not None:
    enemy.grid_pos = step
```

### Multi-Target Dijkstra

For enemies chasing multiple possible targets (like multiple party members):

You can also let `get_dijkstra_map` compute a single map from multiple roots at once via
its `roots` argument (multi-source maps are not cached, unlike single-root maps):

```python
def compute_player_distances(grid, players):
    """
    Compute minimum distance to the nearest player, for every walkable cell.
    Returns dict mapping (x,y) -> distance to nearest player.
    """
    roots = [player.grid_pos for player in players]
    dijkstra = grid.get_dijkstra_map(roots=roots)

    distances = {}
    for y in range(grid.grid_size[1]):
        for x in range(grid.grid_size[0]):
            dist = dijkstra.distance((x, y))
            if dist is not None:
                distances[(x, y)] = dist

    return distances
```

### Flee Behavior with Dijkstra

To make an entity flee (move away from a threat):

A `DijkstraMap` also has `.invert()`, which flips the distance field into a "safety"
field — descending it moves away from the root, which is a shortcut for the same flee
logic below:

```python
def flee_from(grid, entity, threat_pos):
    """Move entity away from threat."""
    dijkstra = grid.get_dijkstra_map(threat_pos)

    ex, ey = entity.grid_x, entity.grid_y
    current_dist = dijkstra.distance((ex, ey))
    if current_dist is None:
        return  # Can't calculate

    # Check all adjacent tiles, pick the one farthest from threat
    best_pos = None
    best_dist = current_dist

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = ex + dx, ey + dy

        if not grid.at(nx, ny).walkable:
            continue

        dist = dijkstra.distance((nx, ny))
        if dist is not None and dist > best_dist:
            best_dist = dist
            best_pos = (nx, ny)

    if best_pos:
        entity.grid_pos = best_pos
```

## Line of Sight

There is no `libtcod` submodule — Bresenham line tracing is exposed directly as
`mcrfpy.bresenham(start, end, include_start=True, include_end=True)`, returning a list of
`(x, y)` grid coordinates:

```python
import mcrfpy

# Get all cells along a line
line = mcrfpy.bresenham((x1, y1), (x2, y2))

# Check for obstacles
def has_line_of_sight(grid, start, end):
    """Check if there's a clear line of sight between two points."""
    line = mcrfpy.bresenham(start, end)

    for x, y in line:
        if not grid.at(x, y).transparent:
            return False

    return True

# Example usage
if has_line_of_sight(grid, player.grid_pos, enemy.grid_pos):
    print("Enemy has clear shot at player!")
```

### Line for Projectiles

```python
def get_projectile_path(grid, start, end):
    """Get the path a projectile would travel."""
    line = mcrfpy.bresenham(start, end)
    path = []

    for x, y in line:
        path.append((x, y))

        # Stop at walls
        if not grid.at(x, y).transparent:
            break

        # Stop at entities (hit detection)
        if len(grid.at(x, y).entities) > 0:
            break

    return path
```

## AI Movement Patterns

### Simple Chase AI

```python
def chase_player(enemy, player):
    """Move enemy one step toward player using A*."""
    path = enemy.path_to(player.grid_x, player.grid_y)

    if path and len(path) > 0:
        # Move to first step in path
        next_x, next_y = path[0]
        enemy.grid_pos = (next_x, next_y)
```

### Smart Chase with Dijkstra

For multiple enemies sharing pathfinding calculation:

```python
def update_all_enemies(grid, enemies, player):
    """Efficient multi-enemy chase using shared Dijkstra map."""
    # Compute once from player (cached by root position)
    dijkstra = grid.get_dijkstra_map(player.grid_pos)

    for enemy in enemies:
        step = dijkstra.step_from(enemy.grid_pos)
        if step is not None:
            next_x, next_y = int(step.x), int(step.y)

            # Don't walk into player (would be attack in real game)
            if (next_x, next_y) == (player.grid_x, player.grid_y):
                continue

            # Check if another enemy is there
            occupied = False
            for other in enemies:
                if other != enemy and other.grid_x == next_x and other.grid_y == next_y:
                    occupied = True
                    break

            if not occupied:
                enemy.grid_pos = (next_x, next_y)
```

### Wander Behavior

```python
import random

def wander(grid, entity):
    """Move entity in a random valid direction."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx = entity.grid_x + dx
        ny = entity.grid_y + dy

        if grid.at(nx, ny).walkable:
            entity.grid_pos = (nx, ny)
            return True

    return False  # Stuck
```

## Complete Pathfinding Example

```python
import mcrfpy
import random

# Setup
scene = mcrfpy.Scene("game")
mcrfpy.current_scene = scene

# Create grid
grid = mcrfpy.Grid(
    grid_size=(40, 30),
    texture=mcrfpy.default_texture,
    pos=(0, 0),
    size=(800, 600)
)
scene.children.append(grid)

# Initialize map
for y in range(30):
    for x in range(40):
        point = grid.at(x, y)
        if x == 0 or x == 39 or y == 0 or y == 29:
            point.tilesprite = 1
            point.walkable = False
        else:
            point.tilesprite = 0
            point.walkable = True

# Add some obstacles
for _ in range(50):
    x = random.randint(2, 37)
    y = random.randint(2, 27)
    point = grid.at(x, y)
    point.tilesprite = 1
    point.walkable = False

# Create player
player = mcrfpy.Entity(grid_pos=(5, 5), texture=mcrfpy.default_texture, sprite_index=64)
grid.entities.append(player)

# Create enemies
enemies = []
for _ in range(5):
    while True:
        x = random.randint(20, 35)
        y = random.randint(5, 25)
        if grid.at(x, y).walkable:
            break

    enemy = mcrfpy.Entity(grid_pos=(x, y), texture=mcrfpy.default_texture, sprite_index=111)
    grid.entities.append(enemy)
    enemies.append(enemy)

# Enemy AI
def update_enemies():
    """Move all enemies toward player."""
    # Use Dijkstra for efficiency with multiple enemies; cached by root position
    dijkstra = grid.get_dijkstra_map(player.grid_pos)

    for enemy in enemies:
        dist = dijkstra.distance(enemy.grid_pos)

        if dist is not None and dist <= 15:  # Only chase if close enough
            step = dijkstra.step_from(enemy.grid_pos)

            if step is not None:
                next_x, next_y = int(step.x), int(step.y)

                # Don't walk into player (would be attack in real game)
                if next_x == player.grid_x and next_y == player.grid_y:
                    continue

                # Don't walk into other enemies
                blocked = False
                for other in enemies:
                    if other != enemy:
                        if other.grid_x == next_x and other.grid_y == next_y:
                            blocked = True
                            break

                if not blocked:
                    enemy.grid_pos = (next_x, next_y)

# Player movement
def on_key(key, action):
    if action != mcrfpy.InputState.PRESSED:
        return

    dx, dy = 0, 0

    if key == mcrfpy.Key.UP or key == mcrfpy.Key.W: dy = -1
    elif key == mcrfpy.Key.DOWN or key == mcrfpy.Key.S: dy = 1
    elif key == mcrfpy.Key.LEFT or key == mcrfpy.Key.A: dx = -1
    elif key == mcrfpy.Key.RIGHT or key == mcrfpy.Key.D: dx = 1
    else:
        return

    new_x = player.grid_x + dx
    new_y = player.grid_y + dy

    if grid.at(new_x, new_y).walkable:
        player.grid_pos = (new_x, new_y)
        grid.center = player.pos

        # Enemy turn after player moves. get_dijkstra_map() is cached by root
        # position, so a moved root simply produces a fresh map on next call.
        update_enemies()

scene.on_key = on_key

# Initialize camera
grid.center = player.pos
```

## Performance Tips

- **A* vs Dijkstra**: Use A* (`entity.path_to`, `entity.find_path`, `grid.find_path`) for
  single paths. Use Dijkstra (`grid.get_dijkstra_map`) when multiple entities need paths
  to the same target, since the map is computed once and reused.
- **Caching**: Single-root Dijkstra maps are cached by root position — calling
  `get_dijkstra_map()` again with the same root is cheap. Call
  `grid.clear_dijkstra_maps()` after changing any cell's `walkable` state to invalidate
  stale cached maps. Multi-source maps (`roots=[...]`) are never cached.
- **Path Length**: Very long paths are expensive. Consider limiting search distance for AI.
- **Grid Size**: Pathfinding on large grids (100x100+) may need optimization strategies.

## Notes and Caveats

- Pathfinding only considers the `walkable` property, not other entities, unless you pass
  a `collide` label to `find_path`/`get_dijkstra_map` to make entities with that label
  block the search.
- `entity.path_to()` returns an empty list (not `None`) if no path exists.
  `entity.find_path()` / `grid.find_path()` return `None` if no path exists.
- Dijkstra distances are in tile units (diagonal moves cost 1.41 by default, matching
  `diagonal_cost`).
- Paths returned by `path_to()` do not include the starting position; `AStarPath.walk()`
  likewise only yields steps ahead of the current position.
- `mcrfpy.bresenham()` uses Bresenham's line algorithm.

## Related Topics

- [Grid System](grid_system.md) - Setting up walkable tiles
- [Field of View](fov.md) - Visibility calculations
- [Animation](animation.md) - Smooth movement along paths
