# Dijkstra to HeightMap Conversion

![Dijkstra to HeightMap Recipe](/images/cookbook/grid_dijkstra_heightmap.png)

Convert pathfinding distance data into heightmaps for procedural generation, visualization, and gameplay mechanics.

## Overview

A Dijkstra map stores the distance from every cell to a target point. Converting it to a HeightMap lets you use distance data for:
- Distance-based enemy difficulty scaling
- Fog/lighting intensity gradients
- Terrain generation based on paths
- Heat maps and influence visualization

## Quick Start

```python
import mcrfpy

# Create a grid with walkable cells
grid = mcrfpy.Grid(grid_size=(20, 20))
for y in range(20):
    for x in range(20):
        grid.at((x, y)).walkable = True

# Get dijkstra map from player position
dijkstra = grid.get_dijkstra_map((10, 10))

# Convert to heightmap
hmap = dijkstra.to_heightmap()

# Use the heights
player_distance = hmap[(5, 5)]  # Distance from (5,5) to (10,10)
```

## API Reference

### Getting a Dijkstra Map

```python
# From a grid, compute distances from a source point
dijkstra = grid.get_dijkstra_map((source_x, source_y))

# Query individual distances
distance = dijkstra.distance((x, y))
```

### Converting to HeightMap

```python
# Basic conversion - same size as dijkstra map
hmap = dijkstra.to_heightmap()

# Custom unreachable value (default is -1.0)
hmap = dijkstra.to_heightmap(unreachable=0.0)
hmap = dijkstra.to_heightmap(unreachable=999.0)

# Custom output size
hmap = dijkstra.to_heightmap(size=(width, height))
```

### HeightMap Access

```python
# Get height at position
height = hmap[(x, y)]

# HeightMaps also support standard operations
# (see HeightMap documentation for full API)
```

## Common Patterns

### Distance-Based Enemy Difficulty

Spawn harder enemies farther from the player's starting position:

```python
def spawn_enemies(grid, player_start, enemy_count):
    """Spawn enemies with difficulty based on distance from start."""
    dijkstra = grid.get_dijkstra_map(player_start)
    hmap = dijkstra.to_heightmap(unreachable=0.0)

    enemies = []
    spawn_points = find_valid_spawns(grid)

    for point in spawn_points[:enemy_count]:
        distance = hmap[point]

        if distance < 5:
            enemy_type = "rat"      # Easy enemies near spawn
        elif distance < 10:
            enemy_type = "goblin"   # Medium difficulty
        elif distance < 15:
            enemy_type = "orc"      # Hard enemies
        else:
            enemy_type = "troll"    # Boss-tier far from spawn

        enemies.append(create_enemy(enemy_type, point))

    return enemies
```

### Distance-Based Fog Intensity

Create fog that's thicker farther from the player:

```python
def update_fog(grid, fog_layer, player_pos):
    """Update fog intensity based on distance from player."""
    dijkstra = grid.get_dijkstra_map(player_pos)
    hmap = dijkstra.to_heightmap(unreachable=20.0)

    width, height = int(grid.grid_size[0]), int(grid.grid_size[1])

    for y in range(height):
        for x in range(width):
            distance = hmap[(x, y)]

            # Calculate fog alpha based on distance
            if distance <= 3:
                alpha = 0        # Clear near player
            elif distance <= 8:
                alpha = int((distance - 3) * 30)  # Gradual fade
            else:
                alpha = 200      # Dense fog far away

            fog_layer.set((x, y), mcrfpy.Color(20, 20, 40, alpha))
```

### Visualizing Dijkstra as Color Gradient

Debug pathfinding by visualizing distances as colors:

```python
def visualize_dijkstra(grid, color_layer, source):
    """Render dijkstra distances as a color gradient."""
    dijkstra = grid.get_dijkstra_map(source)
    hmap = dijkstra.to_heightmap(unreachable=-1.0)

    width, height = int(grid.grid_size[0]), int(grid.grid_size[1])

    # Find max distance for normalization
    max_dist = 0
    for y in range(height):
        for x in range(width):
            d = hmap[(x, y)]
            if d > max_dist and d != -1.0:
                max_dist = d

    # Color each cell
    for y in range(height):
        for x in range(width):
            dist = hmap[(x, y)]

            if dist == -1.0:
                # Unreachable - dark red
                color = mcrfpy.Color(60, 0, 0)
            elif dist == 0:
                # Source - bright yellow
                color = mcrfpy.Color(255, 255, 0)
            else:
                # Gradient from green (near) to blue (far)
                t = dist / max_dist
                r = 0
                g = int(255 * (1 - t))
                b = int(255 * t)
                color = mcrfpy.Color(r, g, b)

            color_layer.set((x, y), color)
```

### River/Path Carving with Distance Fields

Use distance from multiple points to carve natural-looking paths:

```python
def carve_river(grid, source, destination):
    """Carve a river-like path between two points."""
    # Get distance from destination
    dijkstra = grid.get_dijkstra_map(destination)
    hmap = dijkstra.to_heightmap(unreachable=999.0)

    # Start at source, follow decreasing distance
    current = source
    path = [current]

    while current != destination:
        x, y = current
        best_neighbor = None
        best_dist = hmap[current]

        # Check all neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid.grid_size[0] and 0 <= ny < grid.grid_size[1]:
                neighbor_dist = hmap[(nx, ny)]
                if neighbor_dist < best_dist:
                    best_dist = neighbor_dist
                    best_neighbor = (nx, ny)

        if best_neighbor is None:
            break  # No path found

        current = best_neighbor
        path.append(current)

        # Carve the path (make it water/floor)
        grid.at(current).tilesprite = WATER_TILE
        grid.at(current).walkable = True

    return path
```

### Influence Map for AI

Create an influence map showing areas controlled by different factions:

```python
def create_influence_map(grid, player_pos, enemy_positions):
    """Create influence map for AI decision-making."""
    width, height = int(grid.grid_size[0]), int(grid.grid_size[1])

    # Player influence
    player_dijkstra = grid.get_dijkstra_map(player_pos)
    player_hmap = player_dijkstra.to_heightmap(unreachable=100.0)

    # Combined enemy influence (take minimum distance to any enemy)
    influence = {}

    for y in range(height):
        for x in range(width):
            player_dist = player_hmap[(x, y)]

            # Find closest enemy
            min_enemy_dist = 100.0
            for enemy_pos in enemy_positions:
                enemy_dijkstra = grid.get_dijkstra_map(enemy_pos)
                enemy_hmap = enemy_dijkstra.to_heightmap(unreachable=100.0)
                enemy_dist = enemy_hmap[(x, y)]
                min_enemy_dist = min(min_enemy_dist, enemy_dist)

            # Influence: positive = player controlled, negative = enemy
            influence[(x, y)] = min_enemy_dist - player_dist

    return influence
```

## Performance Tips

1. **Cache dijkstra maps** - Don't recompute every frame if the grid hasn't changed
2. **Use appropriate unreachable values** - Choose values that make sense for your use case
3. **Consider size parameter** - If you only need a portion, use custom size
4. **Batch operations** - Convert once, query many times

## Use Cases

| Use Case | Technique |
|----------|-----------|
| Enemy difficulty scaling | Distance from spawn → enemy tier |
| Fog of war intensity | Distance from player → alpha value |
| Safe zone detection | Distance from hazards → safety score |
| Pathfinding visualization | Distance → color gradient |
| Terrain generation | Distance from features → elevation |
| AI influence maps | Compare distances from factions |

## See Also

- [Dijkstra Pathfinding](grid_dijkstra.md) - Basic dijkstra usage
- [Fog of War](grid_fog_of_war.md) - Visibility systems
- [Dungeon Generator](grid_dungeon_generator.md) - Procedural generation
