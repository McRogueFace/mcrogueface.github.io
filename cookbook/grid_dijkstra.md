---
layout: default
title: Dijkstra Maps
parent: Cookbook
nav_order: 4
---

# Dijkstra Distance Maps

Use Dijkstra maps for AI movement, area effects, and tactical analysis.

---

## Overview

Dijkstra maps (also called "distance fields") provide:
- Distance from any cell to a goal
- Optimal pathfinding to goals
- AI flee/chase behavior
- Area-of-influence calculations

---

## Quick Start

```python
import mcrfpy

# Compute distances from player position
grid.compute_dijkstra(player_x, player_y)

# Get distance to any cell
distance = grid.get_dijkstra_distance(target_x, target_y)

# Get path from any cell to the goal
path = grid.get_dijkstra_path(start_x, start_y)
```

---

## Basic Pathfinding

Use Dijkstra for enemy movement:

```python
def move_enemy_toward_player(enemy, player):
    """Move enemy one step toward the player."""
    px, py = player.pos
    ex, ey = enemy.pos

    # Compute distance map from player
    grid.compute_dijkstra(px, py)

    # Get path from enemy to player
    path = grid.get_dijkstra_path(ex, ey)

    if path and len(path) > 1:
        # Move to next cell in path (skip current position)
        next_x, next_y = path[1]
        enemy.pos = (next_x, next_y)
```

---

## AI Behaviors

### Chase Behavior

Move toward lowest distance values:

```python
def ai_chase(entity, target_x, target_y):
    """Move entity toward target using Dijkstra map."""
    grid.compute_dijkstra(target_x, target_y)

    ex, ey = entity.pos
    current_dist = grid.get_dijkstra_distance(ex, ey)

    # Find neighbor with lowest distance
    best_move = None
    best_dist = current_dist

    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = ex + dx, ey + dy

        if grid.at(nx, ny).walkable:
            dist = grid.get_dijkstra_distance(nx, ny)
            if dist < best_dist:
                best_dist = dist
                best_move = (nx, ny)

    if best_move:
        entity.pos = best_move
```

### Flee Behavior

Move toward highest distance values:

```python
def ai_flee(entity, threat_x, threat_y):
    """Move entity away from threat using Dijkstra map."""
    grid.compute_dijkstra(threat_x, threat_y)

    ex, ey = entity.pos
    current_dist = grid.get_dijkstra_distance(ex, ey)

    # Find neighbor with highest distance
    best_move = None
    best_dist = current_dist

    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = ex + dx, ey + dy

        if grid.at(nx, ny).walkable:
            dist = grid.get_dijkstra_distance(nx, ny)
            if dist > best_dist:
                best_dist = dist
                best_move = (nx, ny)

    if best_move:
        entity.pos = best_move
```

---

## Multiple Goals

Combine Dijkstra maps for complex behaviors:

```python
class DijkstraManager:
    """Manage multiple Dijkstra maps for AI decisions."""

    def __init__(self, grid):
        self.grid = grid
        self.maps = {}  # name -> distance array

    def compute_map(self, name, sources):
        """Compute Dijkstra map from multiple sources."""
        # For multiple sources, compute from each and take minimum
        grid_w, grid_h = self.grid.grid_size
        combined = [[float('inf')] * grid_h for _ in range(grid_w)]

        for sx, sy in sources:
            self.grid.compute_dijkstra(sx, sy)

            for x in range(grid_w):
                for y in range(grid_h):
                    dist = self.grid.get_dijkstra_distance(x, y)
                    combined[x][y] = min(combined[x][y], dist)

        self.maps[name] = combined

    def get_distance(self, name, x, y):
        """Get distance in a named map."""
        if name in self.maps:
            return self.maps[name][x][y]
        return float('inf')

    def get_combined_value(self, x, y, weights):
        """Get weighted combination of multiple maps."""
        value = 0
        for name, weight in weights.items():
            if name in self.maps:
                value += self.maps[name][x][y] * weight
        return value


# Usage: Enemy AI with multiple factors
dijkstra = DijkstraManager(grid)

def update_ai_maps():
    """Recompute AI decision maps."""
    # Map to player (for chasing)
    dijkstra.compute_map('player', [player.pos])

    # Map to all exits (for fleeing)
    exits = find_exits()
    dijkstra.compute_map('exits', exits)

    # Map to healing potions
    potions = find_items('potion')
    dijkstra.compute_map('potions', potions)

def ai_decision(enemy):
    """Make AI decision based on multiple factors."""
    ex, ey = enemy.pos

    if enemy.hp < enemy.max_hp * 0.3:
        # Low health - prioritize potions, avoid player
        weights = {
            'potions': -1.0,  # Move toward potions
            'player': 0.5,    # Move away from player
        }
    else:
        # Healthy - chase player
        weights = {
            'player': -1.0,   # Move toward player
        }

    # Find best adjacent cell
    best_move = None
    best_value = float('inf')

    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = ex + dx, ey + dy

        if grid.at(nx, ny).walkable:
            value = dijkstra.get_combined_value(nx, ny, weights)
            if value < best_value:
                best_value = value
                best_move = (nx, ny)

    if best_move:
        enemy.pos = best_move
```

---

## Movement Range Calculation

Use Dijkstra for tactical movement:

```python
def get_reachable_cells(start_x, start_y, max_cost):
    """Get all cells reachable within a movement budget."""
    grid.compute_dijkstra(start_x, start_y)

    reachable = []
    grid_w, grid_h = grid.grid_size

    for x in range(grid_w):
        for y in range(grid_h):
            dist = grid.get_dijkstra_distance(x, y)
            if dist <= max_cost and dist != float('inf'):
                reachable.append((x, y, dist))

    return reachable

def show_movement_range(entity, movement_points):
    """Highlight reachable cells with distance coloring."""
    ex, ey = entity.pos
    reachable = get_reachable_cells(ex, ey, movement_points)

    highlight_layer.clear()

    for x, y, dist in reachable:
        # Color intensity based on remaining movement
        remaining = movement_points - dist
        intensity = int(200 * remaining / movement_points)
        color = mcrfpy.Color(50, 50 + intensity, 255, 100)
        highlight_layer.set(x, y, color)
```

---

## Influence Mapping

Visualize tactical influence:

```python
def compute_influence_map():
    """Show which team controls which areas."""
    grid_w, grid_h = grid.grid_size
    influence = [[0.0] * grid_h for _ in range(grid_w)]

    # Compute player team influence
    for ally in player_team:
        grid.compute_dijkstra(ally.pos[0], ally.pos[1])
        for x in range(grid_w):
            for y in range(grid_h):
                dist = grid.get_dijkstra_distance(x, y)
                if dist != float('inf'):
                    influence[x][y] += 1.0 / (1.0 + dist)

    # Subtract enemy team influence
    for enemy in enemy_team:
        grid.compute_dijkstra(enemy.pos[0], enemy.pos[1])
        for x in range(grid_w):
            for y in range(grid_h):
                dist = grid.get_dijkstra_distance(x, y)
                if dist != float('inf'):
                    influence[x][y] -= 1.0 / (1.0 + dist)

    # Visualize
    for x in range(grid_w):
        for y in range(grid_h):
            val = influence[x][y]
            if val > 0:
                # Player controlled - blue
                alpha = min(150, int(abs(val) * 50))
                influence_layer.set(x, y, mcrfpy.Color(50, 50, 200, alpha))
            elif val < 0:
                # Enemy controlled - red
                alpha = min(150, int(abs(val) * 50))
                influence_layer.set(x, y, mcrfpy.Color(200, 50, 50, alpha))
```

---

## Terrain Costs

Factor in terrain when pathfinding:

```python
# Set terrain costs before computing
def set_terrain_costs(grid):
    """Configure terrain movement costs."""
    grid_w, grid_h = grid.grid_size

    for x in range(grid_w):
        for y in range(grid_h):
            point = grid.at(x, y)

            # Different terrain types have different costs
            if point.tilesprite == TILE_WATER:
                point.cost = 3  # Slow through water
            elif point.tilesprite == TILE_MUD:
                point.cost = 2  # Slower through mud
            elif point.tilesprite == TILE_ROAD:
                point.cost = 0.5  # Faster on roads
            else:
                point.cost = 1  # Normal cost

# Compute with costs enabled
grid.compute_dijkstra(px, py, use_costs=True)
```

---

## Visibility-Aware Pathfinding

Only path through discovered areas:

```python
def compute_safe_dijkstra(player, goal_x, goal_y):
    """Compute path only through discovered tiles."""
    # Temporarily mark undiscovered tiles as unwalkable
    grid_w, grid_h = grid.grid_size
    original_walkable = {}

    for x in range(grid_w):
        for y in range(grid_h):
            state = player.at(x, y)
            if not state.discovered:
                point = grid.at(x, y)
                original_walkable[(x, y)] = point.walkable
                point.walkable = False

    # Compute Dijkstra
    grid.compute_dijkstra(goal_x, goal_y)

    # Restore walkability
    for (x, y), walkable in original_walkable.items():
        grid.at(x, y).walkable = walkable

    # Now get_dijkstra_path will avoid unknown areas
```

---

## Performance Tips

```python
# Cache Dijkstra maps when possible
class CachedDijkstra:
    """Cache Dijkstra computations."""

    def __init__(self, grid):
        self.grid = grid
        self.cache = {}
        self.cache_valid = False

    def invalidate(self):
        """Call when map changes."""
        self.cache = {}
        self.cache_valid = False

    def get_distance(self, from_x, from_y, to_x, to_y):
        """Get cached distance or compute."""
        key = (to_x, to_y)  # Cache by destination

        if key not in self.cache:
            self.grid.compute_dijkstra(to_x, to_y)
            # Store all distances from this computation
            self.cache[key] = self._snapshot_distances()

        return self.cache[key].get((from_x, from_y), float('inf'))

    def _snapshot_distances(self):
        """Capture current distance values."""
        grid_w, grid_h = self.grid.grid_size
        distances = {}
        for x in range(grid_w):
            for y in range(grid_h):
                dist = self.grid.get_dijkstra_distance(x, y)
                if dist != float('inf'):
                    distances[(x, y)] = dist
        return distances
```

---

## Tips

1. **Recompute when needed**: Dijkstra maps become stale when the map changes
2. **Multiple sources**: Compute once per source, then combine
3. **Performance**: Large maps benefit from caching
4. **Blocked paths**: Distance is infinity for unreachable cells
5. **Direction**: Paths go FROM cell TO goal (follow decreasing distance)

---

## Related Recipes

- [Fog of War](grid_fog_of_war.md) - Combine with visibility
- [Dungeon Generator](grid_dungeon_generator.md) - Generate maps to pathfind
- [Cell Highlighting](grid_cell_highlighting.md) - Visualize distances
