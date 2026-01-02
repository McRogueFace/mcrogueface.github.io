# McRogueFace Minimal Template

A barebones starting point for roguelike prototypes using McRogueFace.

## What This Template Demonstrates

- **Scene Object Pattern**: Uses `mcrfpy.Scene()` (the preferred OOP approach)
- **Grid-Based Movement**: Player moves on a tile grid with boundary checking
- **Keyboard Input**: Arrow keys and WASD for movement, Escape to exit
- **Entity System**: Player represented as an `mcrfpy.Entity` on a `Grid`
- **Type Hints**: Python type annotations for clarity and IDE support
- **Constants**: Named constants for sprite indices and configuration

## Files

```
minimal/
└── game.py    # Complete game in ~150 lines
```

## How to Run

1. Copy `game.py` to your McRogueFace `scripts/` directory
2. Rename it to `game.py` (or update McRogueFace's startup script path)
3. Run McRogueFace:

```bash
# Linux
./mcrogueface

# Windows
mcrogueface.exe
```

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move player |
| Escape | Exit game |

## Suggested Modifications

### Add Walls

```python
# After creating the grid, add some walls:
def add_wall(grid, x, y):
    point = grid.at(x, y)
    point.tilesprite = 35  # '#' in CP437
    point.walkable = False

# Create a border
for x in range(GRID_WIDTH):
    add_wall(grid, x, 0)
    add_wall(grid, x, GRID_HEIGHT - 1)
for y in range(GRID_HEIGHT):
    add_wall(grid, 0, y)
    add_wall(grid, GRID_WIDTH - 1, y)
```

### Check Walkability Before Moving

```python
def try_move(dx: int, dy: int) -> bool:
    global player_x, player_y
    new_x = player_x + dx
    new_y = player_y + dy

    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
        # Check if the target tile is walkable
        if grid.at(new_x, new_y).walkable:
            player_x = new_x
            player_y = new_y
            player_entity.x = player_x
            player_entity.y = player_y
            return True
    return False
```

### Add a Second Entity (NPC or Item)

```python
# Create an NPC
npc = mcrfpy.Entity(
    pos=(5, 5),
    texture=texture,
    sprite_index=111  # 'o' in CP437 - common for orcs
)
grid.entities.append(npc)
```

### Display a Status Message

```python
# Load a font and add a caption
font = mcrfpy.Font("assets/JetbrainsMono.ttf")
status = mcrfpy.Caption(
    pos=(32, 10),
    text="Use arrow keys to move",
    font=font
)
status.fill_color = mcrfpy.Color(200, 200, 200)
scene.children.append(status)
```

### Add Animation

```python
# Animate the player with a smooth transition
from mcrfpy import Animation

def try_move_animated(dx: int, dy: int) -> bool:
    global player_x, player_y
    new_x = player_x + dx
    new_y = player_y + dy

    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
        player_x = new_x
        player_y = new_y

        # Animate position change over 0.1 seconds
        Animation(player_entity, "x", float(new_x), 0.1).start()
        Animation(player_entity, "y", float(new_y), 0.1).start()
        return True
    return False
```

## CP437 Sprite Reference

Common sprite indices for CP437-based tilesets:

| Character | Index | Typical Use |
|-----------|-------|-------------|
| `@` | 64 | Player |
| `.` | 46 | Floor |
| `#` | 35 | Wall |
| `+` | 43 | Door (closed) |
| `/` | 47 | Door (open) / Weapon |
| `>` | 62 | Stairs down |
| `<` | 60 | Stairs up |
| `!` | 33 | Potion |
| `?` | 63 | Scroll |
| `%` | 37 | Corpse / Food |
| `o` | 111 | Orc |
| `T` | 84 | Troll |
| `g` | 103 | Goblin |

## Next Steps

1. **Add collision detection** with walls using `grid.at(x, y).walkable`
2. **Implement FOV** using `entity.update_visibility()` and color layers
3. **Create multiple scenes** for menu, gameplay, and game over states
4. **Follow the full tutorial** at [McRogueFace Tutorials](https://mcrogueface.github.io/tutorials)

## Resources

- [McRogueFace Quickstart](https://mcrogueface.github.io/quickstart) - Get running in 5 minutes
- [API Reference](https://mcrogueface.github.io/api-reference) - Complete documentation
- [Cookbook](https://mcrogueface.github.io/cookbook) - Copy-paste solutions
- [Full Tutorial](https://mcrogueface.github.io/tutorials) - Build a complete roguelike
