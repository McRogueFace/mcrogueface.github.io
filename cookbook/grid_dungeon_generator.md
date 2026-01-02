---
layout: default
title: Dungeon Generator
parent: Cookbook
nav_order: 2
---

# Room and Corridor Generator

Generate procedural dungeons with rectangular rooms connected by tunnels.

---

## Overview

This recipe creates classic roguelike dungeons with:
- Randomly placed rectangular rooms
- Corridors connecting rooms
- Proper wall/floor tile placement
- Walkable and transparent tile properties set correctly

---

## Quick Start

```python
import mcrfpy
import random

def generate_dungeon(grid, room_count=8):
    """Generate a dungeon with rooms and corridors."""
    rooms = []
    grid_w, grid_h = grid.grid_size

    # Fill with walls first
    for x in range(grid_w):
        for y in range(grid_h):
            point = grid.at(x, y)
            point.tilesprite = 1  # Wall tile
            point.walkable = False
            point.transparent = False

    # Generate rooms
    for _ in range(room_count * 3):  # Try more times than needed
        if len(rooms) >= room_count:
            break

        # Random room dimensions
        w = random.randint(4, 10)
        h = random.randint(4, 10)
        x = random.randint(1, grid_w - w - 1)
        y = random.randint(1, grid_h - h - 1)

        new_room = (x, y, w, h)

        # Check for overlap with existing rooms
        if not any(rooms_overlap(new_room, room) for room in rooms):
            carve_room(grid, x, y, w, h)

            # Connect to previous room
            if rooms:
                connect_rooms(grid, rooms[-1], new_room)

            rooms.append(new_room)

    return rooms
```

---

## Room Class

A helper class for room management:

```python
class Room:
    """Represents a rectangular room in the dungeon."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def center(self):
        """Return the center point of the room."""
        return (
            self.x + self.width // 2,
            self.y + self.height // 2
        )

    @property
    def inner(self):
        """Return the inner area (excluding walls)."""
        return (
            self.x + 1, self.y + 1,
            self.width - 2, self.height - 2
        )

    def intersects(self, other, padding=1):
        """Check if this room overlaps another (with padding)."""
        return (
            self.x - padding < other.x + other.width + padding and
            self.x + self.width + padding > other.x - padding and
            self.y - padding < other.y + other.height + padding and
            self.y + self.height + padding > other.y - padding
        )
```

---

## Complete Generator

```python
import mcrfpy
import random

# Tile indices (adjust for your tileset)
TILE_FLOOR = 0
TILE_WALL = 1
TILE_DOOR = 2
TILE_STAIRS_DOWN = 3
TILE_STAIRS_UP = 4

class DungeonGenerator:
    """Procedural dungeon generator with rooms and corridors."""

    def __init__(self, grid, seed=None):
        self.grid = grid
        self.grid_w, self.grid_h = grid.grid_size
        self.rooms = []

        if seed is not None:
            random.seed(seed)

    def generate(self, room_count=8, min_room=4, max_room=10):
        """Generate a complete dungeon level."""
        self.rooms = []

        # Fill with walls
        self._fill_walls()

        # Place rooms
        attempts = 0
        max_attempts = room_count * 10

        while len(self.rooms) < room_count and attempts < max_attempts:
            attempts += 1

            # Random room size
            w = random.randint(min_room, max_room)
            h = random.randint(min_room, max_room)

            # Random position (leaving border)
            x = random.randint(1, self.grid_w - w - 2)
            y = random.randint(1, self.grid_h - h - 2)

            room = Room(x, y, w, h)

            # Check overlap
            if not any(room.intersects(r) for r in self.rooms):
                self._carve_room(room)

                # Connect to previous room
                if self.rooms:
                    self._dig_corridor(self.rooms[-1].center, room.center)

                self.rooms.append(room)

        # Place stairs
        if len(self.rooms) >= 2:
            self._place_stairs()

        return self.rooms

    def _fill_walls(self):
        """Fill the entire grid with wall tiles."""
        for x in range(self.grid_w):
            for y in range(self.grid_h):
                point = self.grid.at(x, y)
                point.tilesprite = TILE_WALL
                point.walkable = False
                point.transparent = False

    def _carve_room(self, room):
        """Carve out a room, making it walkable."""
        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                self._set_floor(x, y)

    def _set_floor(self, x, y):
        """Set a single tile as floor."""
        if 0 <= x < self.grid_w and 0 <= y < self.grid_h:
            point = self.grid.at(x, y)
            point.tilesprite = TILE_FLOOR
            point.walkable = True
            point.transparent = True

    def _dig_corridor(self, start, end):
        """Dig an L-shaped corridor between two points."""
        x1, y1 = start
        x2, y2 = end

        # Randomly choose horizontal-first or vertical-first
        if random.random() < 0.5:
            # Horizontal then vertical
            self._dig_horizontal(x1, x2, y1)
            self._dig_vertical(y1, y2, x2)
        else:
            # Vertical then horizontal
            self._dig_vertical(y1, y2, x1)
            self._dig_horizontal(x1, x2, y2)

    def _dig_horizontal(self, x1, x2, y):
        """Dig a horizontal tunnel."""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self._set_floor(x, y)

    def _dig_vertical(self, y1, y2, x):
        """Dig a vertical tunnel."""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self._set_floor(x, y)

    def _place_stairs(self):
        """Place stairs in first and last rooms."""
        # Stairs up in first room
        start_room = self.rooms[0]
        sx, sy = start_room.center
        point = self.grid.at(sx, sy)
        point.tilesprite = TILE_STAIRS_UP

        # Stairs down in last room
        end_room = self.rooms[-1]
        ex, ey = end_room.center
        point = self.grid.at(ex, ey)
        point.tilesprite = TILE_STAIRS_DOWN

        return (sx, sy), (ex, ey)

    def get_spawn_point(self):
        """Get a good spawn point for the player."""
        if self.rooms:
            return self.rooms[0].center
        return (self.grid_w // 2, self.grid_h // 2)

    def get_random_floor(self):
        """Get a random walkable floor tile."""
        floors = []
        for x in range(self.grid_w):
            for y in range(self.grid_h):
                if self.grid.at(x, y).walkable:
                    floors.append((x, y))
        return random.choice(floors) if floors else None
```

---

## Usage Example

```python
import mcrfpy

# Setup
mcrfpy.createScene("dungeon")
mcrfpy.setScene("dungeon")
ui = mcrfpy.sceneUI("dungeon")

texture = mcrfpy.Texture("assets/dungeon.png", 16, 16)
grid = mcrfpy.Grid(60, 40, texture, 0, 0, 960, 640)
ui.append(grid)

# Generate dungeon
generator = DungeonGenerator(grid, seed=42)
rooms = generator.generate(room_count=10)

# Place player at spawn
spawn = generator.get_spawn_point()
player = mcrfpy.Entity(spawn, texture, 64)
grid.entities.append(player)

# Place some enemies in random rooms
for i in range(5):
    pos = generator.get_random_floor()
    if pos and pos != spawn:
        enemy = mcrfpy.Entity(pos, texture, 80)
        grid.entities.append(enemy)

# Center camera
grid.center = spawn

print(f"Generated dungeon with {len(rooms)} rooms")
```

---

## Advanced: BSP Dungeon

Binary Space Partitioning creates more structured layouts:

```python
class BSPNode:
    """Node in a BSP tree for dungeon generation."""

    MIN_SIZE = 6

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.left = None
        self.right = None
        self.room = None

    def split(self):
        """Recursively split this node."""
        if self.left or self.right:
            return False

        # Choose split direction
        if self.w > self.h and self.w / self.h >= 1.25:
            horizontal = False
        elif self.h > self.w and self.h / self.w >= 1.25:
            horizontal = True
        else:
            horizontal = random.random() < 0.5

        max_size = (self.h if horizontal else self.w) - self.MIN_SIZE
        if max_size <= self.MIN_SIZE:
            return False

        split = random.randint(self.MIN_SIZE, max_size)

        if horizontal:
            self.left = BSPNode(self.x, self.y, self.w, split)
            self.right = BSPNode(self.x, self.y + split, self.w, self.h - split)
        else:
            self.left = BSPNode(self.x, self.y, split, self.h)
            self.right = BSPNode(self.x + split, self.y, self.w - split, self.h)

        return True

    def create_rooms(self, grid):
        """Create rooms in leaf nodes and connect siblings."""
        if self.left or self.right:
            if self.left:
                self.left.create_rooms(grid)
            if self.right:
                self.right.create_rooms(grid)

            # Connect children
            if self.left and self.right:
                left_room = self.left.get_room()
                right_room = self.right.get_room()
                if left_room and right_room:
                    connect_points(grid, left_room.center, right_room.center)
        else:
            # Leaf node - create room
            w = random.randint(3, self.w - 2)
            h = random.randint(3, self.h - 2)
            x = self.x + random.randint(1, self.w - w - 1)
            y = self.y + random.randint(1, self.h - h - 1)
            self.room = Room(x, y, w, h)
            carve_room(grid, self.room)

    def get_room(self):
        """Get a room from this node or its children."""
        if self.room:
            return self.room

        left_room = self.left.get_room() if self.left else None
        right_room = self.right.get_room() if self.right else None

        if left_room and right_room:
            return random.choice([left_room, right_room])
        return left_room or right_room


def generate_bsp_dungeon(grid, iterations=4):
    """Generate a BSP-based dungeon."""
    grid_w, grid_h = grid.grid_size

    # Fill with walls
    for x in range(grid_w):
        for y in range(grid_h):
            point = grid.at(x, y)
            point.tilesprite = TILE_WALL
            point.walkable = False
            point.transparent = False

    # Build BSP tree
    root = BSPNode(0, 0, grid_w, grid_h)
    nodes = [root]

    for _ in range(iterations):
        new_nodes = []
        for node in nodes:
            if node.split():
                new_nodes.extend([node.left, node.right])
        nodes = new_nodes or nodes

    # Create rooms and corridors
    root.create_rooms(grid)

    # Collect all rooms
    rooms = []
    def collect_rooms(node):
        if node.room:
            rooms.append(node.room)
        if node.left:
            collect_rooms(node.left)
        if node.right:
            collect_rooms(node.right)

    collect_rooms(root)
    return rooms
```

---

## Tips

1. **Seed for reproducibility**: Pass a seed to recreate the same dungeon
2. **Room padding**: Add padding when checking overlaps to ensure corridors
3. **Validate connectivity**: Consider flood-fill to ensure all rooms connect
4. **Tile variety**: Add random floor variations for visual interest
5. **Special rooms**: Mark rooms for specific purposes (treasure, boss, etc.)

---

## Related Recipes

- [Fog of War](grid_fog_of_war.md) - Add visibility to your dungeon
- [Dijkstra Maps](grid_dijkstra.md) - Pathfinding in generated dungeons
- [Multi-Layer Tiles](grid_multi_layer.md) - Decorations and overlays
