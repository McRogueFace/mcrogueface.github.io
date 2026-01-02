# Roguelike Starter Template

A minimal but complete roguelike template for McRogueFace that demonstrates the core systems needed for a traditional roguelike game.

## Features

- **Procedural Dungeon Generation**: Classic "rooms and corridors" algorithm
- **Player Movement**: WASD/Arrow key movement with collision detection
- **Field of View**: TCOD-powered FOV with explored/unexplored areas
- **Enemy Entities**: Static enemies placed throughout the dungeon
- **Camera System**: Follows the player through the dungeon

## Quick Start

1. Copy this template folder to your McRogueFace `scripts/` directory
2. Run McRogueFace - it automatically loads `scripts/game.py`

```bash
# From McRogueFace directory
cp -r templates/roguelike/* scripts/
./mcrogueface
```

## Controls

| Key | Action |
|-----|--------|
| W / Up Arrow | Move North |
| S / Down Arrow | Move South |
| A / Left Arrow | Move West |
| D / Right Arrow | Move East |
| Numpad 7,9,1,3 | Diagonal Movement |
| Escape | Quit Game |

## File Structure

```
roguelike/
├── game.py          # Main entry point - scene setup, game loop, input
├── dungeon.py       # Dungeon generation algorithm
├── entities.py      # Entity creation and management helpers
├── constants.py     # Sprite indices, colors, configuration
└── README.md        # This file
```

### constants.py

Defines all the magic numbers in one place:

- **Sprite Indices**: CP437 character codes for tiles and entities
- **Colors**: FOV overlay colors, tile colors, entity colors
- **Configuration**: Map size, room parameters, FOV radius

### dungeon.py

Procedural dungeon generation with:

- `RectangularRoom`: Room geometry class with center/intersection helpers
- `generate_dungeon()`: Creates list of non-overlapping rooms
- `tunnel_between()`: Generates L-shaped corridors
- `populate_grid()`: Applies layout to McRogueFace Grid

### entities.py

Entity management utilities:

- `create_player()`: Factory for player entity
- `create_enemy()`: Factory for enemy entities with stats
- `move_entity()`: Movement with collision checking
- `EntityStats`: Dataclass for HP, power, defense (for combat systems)

### game.py

Main game logic:

- Scene and grid initialization
- FOV system using `Entity.update_visibility()`
- Input handling for movement
- Camera that follows the player

## Extending the Template

### Adding Combat

The `EntityStats` dataclass in `entities.py` is ready for combat:

```python
from entities import EntityStats, get_blocking_entity_at

# In your input handler, check for enemies at destination
target = get_blocking_entity_at(enemies, dest_x, dest_y)
if target:
    # Found an enemy - attack instead of move
    enemy_stats = enemy_stats_dict[target]  # Look up stats
    damage = player_stats.power - enemy_stats.defense
    enemy_stats.take_damage(damage)
```

### Adding Enemy AI

Create an update function that runs each turn:

```python
def enemy_turn():
    for entity, stats in game.enemies:
        if not stats.is_alive:
            continue

        # Simple chase AI: move toward player if visible
        player_state = game.player.at(entity.pos[0], entity.pos[1])
        if player_state.visible:
            # Calculate direction to player
            dx = sign(game.player.pos[0] - entity.pos[0])
            dy = sign(game.player.pos[1] - entity.pos[1])
            move_entity(entity, game.grid, dx, dy)
```

### Adding Items

Create item sprites and pickup logic:

```python
# In constants.py
SPRITE_POTION = 33  # '!'

# In entities.py
def create_item(grid, texture, x, y, item_type):
    item = mcrfpy.Entity((x, y), texture, SPRITE_POTION)
    grid.entities.append(item)
    return item

# In game.py - check for items at player position
def check_items():
    px, py = game.player.pos
    for item in game.items:
        if item.pos == (px, py):
            pickup_item(item)
```

### Multiple Levels

Add stairs and level transitions:

```python
# After dungeon generation, place stairs
last_room = game.rooms[-1]
stairs_x, stairs_y = last_room.center
game.grid.at(stairs_x, stairs_y).tilesprite = SPRITE_STAIRS_DOWN

# Check for stairs in movement
if game.grid.at(new_x, new_y).tilesprite == SPRITE_STAIRS_DOWN:
    generate_new_level()
```

## Technical Notes

### FOV System

McRogueFace uses TCOD (The Complete Roguelike Developer) for field of view calculations. The system works as follows:

1. Set `walkable` and `transparent` on grid tiles during generation
2. Call `entity.update_visibility()` after the entity moves
3. Query visibility with `entity.at(x, y).visible` and `.discovered`
4. Apply color overlays to tiles based on visibility state

### Coordinate System

- Origin (0, 0) is top-left
- X increases to the right
- Y increases downward
- Grid uses integer tile coordinates
- Entity positions are (x, y) tuples

### Performance Tips

- Only update FOV when the player moves
- Use `entity.at(x, y)` for visibility checks (cached per entity)
- Avoid iterating all tiles every frame - only update changed tiles

## License

This template is provided as part of McRogueFace documentation.
Use it freely in your own projects.

## Resources

- [McRogueFace Documentation](https://mcrogueface.github.io)
- [API Reference](https://mcrogueface.github.io/api-reference)
- [Roguelike Tutorial](https://mcrogueface.github.io/tutorials)
- [TCOD Documentation](https://python-tcod.readthedocs.io/)
