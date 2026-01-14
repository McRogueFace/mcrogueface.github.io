# Pathfinding

McRogueFace provides built-in pathfinding algorithms for AI movement, player auto-travel, and tactical analysis. The engine supports A* pathfinding for point-to-point routes and Dijkstra maps for distance calculations.

## A* Pathfinding

A* finds the shortest path between two points, respecting walkability.

### Entity.path_to()

The simplest way to pathfind - ask an entity for a path to a destination:

```python
import mcrfpy

# Create an entity on a grid
entity = mcrfpy.Entity(grid_pos=(5, 5), texture=texture, sprite_index=64)
grid.entities.append(entity)

# Find path to destination
path = entity.path_to(20, 15)

if path:
    print(f"Path found! {len(path)} steps")
    for x, y in path:
        print(f"  -> ({x}, {y})")
else:
    print("No path available")
```

The returned path is a list of `(x, y)` tuples representing each step from the current position to the destination.

### Grid.find_path()

For pathfinding without an entity, use the grid directly:

```python
# Find path between any two points
start = (5, 5)
end = (20, 15)
path = grid.find_path(start[0], start[1], end[0], end[1])

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

```python
# Compute distances from a source point
source_x, source_y = 25, 15
grid.compute_dijkstra(source_x, source_y)

# Now query distances from any point
distance = grid.get_dijkstra_distance(10, 10)
if distance is not None:
    print(f"Distance from (10,10) to source: {distance}")
else:
    print("Position is unreachable")
```

### Getting Paths from Dijkstra

Once computed, you can get the shortest path from any point back to the source:

```python
# Compute from player position
grid.compute_dijkstra(player.x, player.y)

# Get path from enemy to player
path = grid.get_dijkstra_path(enemy.x, enemy.y)

if path:
    # Move enemy along path
    next_x, next_y = path[0]
    enemy.pos = (next_x, next_y)
```

### Multi-Target Dijkstra

For enemies chasing multiple possible targets (like multiple party members):

```python
def compute_player_distances(players):
    """
    Compute minimum distances to any player.
    Returns dict mapping (x,y) -> distance to nearest player.
    """
    distances = {}

    for player in players:
        grid.compute_dijkstra(player.x, player.y)

        for y in range(grid.grid_size[1]):
            for x in range(grid.grid_size[0]):
                dist = grid.get_dijkstra_distance(x, y)
                if dist is not None:
                    key = (x, y)
                    if key not in distances or dist < distances[key]:
                        distances[key] = dist

    return distances
```

### Flee Behavior with Dijkstra

To make an entity flee (move away from a threat):

```python
def flee_from(entity, threat_x, threat_y):
    """Move entity away from threat."""
    grid.compute_dijkstra(threat_x, threat_y)

    current_dist = grid.get_dijkstra_distance(entity.x, entity.y)
    if current_dist is None:
        return  # Can't calculate

    # Check all adjacent tiles, pick the one farthest from threat
    best_pos = None
    best_dist = current_dist

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = int(entity.x) + dx, int(entity.y) + dy

        if not grid.at(nx, ny).walkable:
            continue

        dist = grid.get_dijkstra_distance(nx, ny)
        if dist is not None and dist > best_dist:
            best_dist = dist
            best_pos = (nx, ny)

    if best_pos:
        entity.pos = best_pos
```

## Line of Sight

For checking if two points have an unobstructed line between them:

```python
from mcrfpy import libtcod

# Get all cells along a line
line = libtcod.line(x1, y1, x2, y2)

# Check for obstacles
def has_line_of_sight(grid, x1, y1, x2, y2):
    """Check if there's a clear line of sight between two points."""
    line = libtcod.line(x1, y1, x2, y2)

    for x, y in line:
        if not grid.at(x, y).transparent:
            return False

    return True

# Example usage
if has_line_of_sight(grid, player.x, player.y, enemy.x, enemy.y):
    print("Enemy has clear shot at player!")
```

### Line for Projectiles

```python
def get_projectile_path(start_x, start_y, end_x, end_y):
    """Get the path a projectile would travel."""
    line = libtcod.line(start_x, start_y, end_x, end_y)
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
    path = enemy.path_to(player.x, player.y)

    if path and len(path) > 0:
        # Move to first step in path
        next_x, next_y = path[0]
        enemy.pos = (next_x, next_y)
```

### Smart Chase with Dijkstra

For multiple enemies sharing pathfinding calculation:

```python
def update_all_enemies(enemies, player):
    """Efficient multi-enemy chase using shared Dijkstra map."""
    # Compute once from player
    grid.compute_dijkstra(player.x, player.y)

    for enemy in enemies:
        path = grid.get_dijkstra_path(enemy.x, enemy.y)
        if path and len(path) > 0:
            next_x, next_y = path[0]

            # Check if another enemy is there
            occupied = False
            for other in enemies:
                if other != enemy and int(other.x) == next_x and int(other.y) == next_y:
                    occupied = True
                    break

            if not occupied:
                enemy.pos = (next_x, next_y)
```

### Wander Behavior

```python
import random

def wander(entity):
    """Move entity in a random valid direction."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx = int(entity.x) + dx
        ny = int(entity.y) + dy

        if grid.at(nx, ny).walkable:
            entity.pos = (nx, ny)
            return True

    return False  # Stuck
```

## Complete Pathfinding Example

```python
import mcrfpy
import random

# Setup
scene = mcrfpy.Scene("game")
scene.activate()

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

# Player movement
def on_key(key, action):
    if action != "start":
        return

    dx, dy = 0, 0
    key = key.lower()

    if key in ("up", "w"): dy = -1
    elif key in ("down", "s"): dy = 1
    elif key in ("left", "a"): dx = -1
    elif key in ("right", "d"): dx = 1
    else:
        return

    new_x = int(player.x) + dx
    new_y = int(player.y) + dy

    if grid.at(new_x, new_y).walkable:
        player.pos = (new_x, new_y)
        grid.center = player.pos

        # Enemy turn after player moves
        update_enemies()

scene.on_key = on_key

# Enemy AI
def update_enemies():
    """Move all enemies toward player."""
    # Use Dijkstra for efficiency with multiple enemies
    grid.compute_dijkstra(player.x, player.y)

    for enemy in enemies:
        dist = grid.get_dijkstra_distance(enemy.x, enemy.y)

        if dist is not None and dist <= 15:  # Only chase if close enough
            path = grid.get_dijkstra_path(enemy.x, enemy.y)

            if path and len(path) > 0:
                next_x, next_y = path[0]

                # Don't walk into player (would be attack in real game)
                if next_x == int(player.x) and next_y == int(player.y):
                    continue

                # Don't walk into other enemies
                blocked = False
                for other in enemies:
                    if other != enemy:
                        if int(other.x) == next_x and int(other.y) == next_y:
                            blocked = True
                            break

                if not blocked:
                    enemy.pos = (next_x, next_y)

# Initialize camera
grid.center = player.pos
```

## Performance Tips

- **A* vs Dijkstra**: Use A* (`path_to`, `find_path`) for single paths. Use Dijkstra when multiple entities need paths to the same target.
- **Caching**: Dijkstra results are valid until the map changes. Recompute only when walls change or the target moves.
- **Path Length**: Very long paths are expensive. Consider limiting search distance for AI.
- **Grid Size**: Pathfinding on large grids (100x100+) may need optimization strategies.

## Notes and Caveats

- Pathfinding only considers `walkable` property, not other entities
- `path_to()` returns `None` or empty list if no path exists
- Dijkstra distances are in tile units (diagonal moves count as 1.4 if supported)
- Paths do not include the starting position
- The `libtcod.line()` function uses Bresenham's algorithm

## Related Topics

- [Grid System](grid_system.md) - Setting up walkable tiles
- [Field of View](fov.md) - Visibility calculations
- [Animation](animation.md) - Smooth movement along paths
