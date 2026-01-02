# McRogueFace Complete Roguelike Template

A fully playable mini-roguelike demonstrating all major McRogueFace features. Use this as a starting point for your own roguelike game!

## Features

- **Procedural Dungeon Generation** - Random rooms connected by corridors
- **Turn-Based Gameplay** - Classic roguelike mechanics
- **Multiple Enemy Types** - Goblins, Orcs, and Trolls with different stats
- **Combat System** - Attack, defense, and damage calculations
- **Enemy AI** - Chase player when visible, wander otherwise
- **Field of View** - TCOD-powered visibility with fog of war
- **Health Bar** - Visual HP display with color warnings
- **Message Log** - Scrolling combat messages
- **Multi-Level Dungeons** - Stairs to descend deeper

## Quick Start

1. Copy all `.py` files to your McRogueFace `scripts/` directory
2. Rename or replace `game.py` to be your main script
3. Run McRogueFace!

```bash
# From your McRogueFace directory
./mcrogueface
```

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move |
| Numpad 1-9 | Move (including diagonals) |
| . / Numpad 5 | Wait (skip turn) |
| > / Space | Descend stairs |
| R | Restart (when dead) |
| Escape | Quit |

## File Structure

```
complete/
├── game.py          # Main entry point - ties everything together
├── constants.py     # All configuration values
├── dungeon.py       # Procedural dungeon generation
├── entities.py      # Player and enemy definitions
├── combat.py        # Attack and damage calculations
├── ai.py            # Enemy AI behaviors
├── turns.py         # Turn management system
├── ui.py            # Health bar and message log
└── README.md        # This file
```

## Architecture Overview

### Game Loop Flow

```
1. Player presses key
   └─> game.py: handle_keypress()

2. If movement key:
   └─> turns.py: TurnManager.handle_player_action()
       ├─> Check for attack target
       │   └─> combat.py: try_attack()
       └─> Or move player

3. After player action:
   └─> ai.py: process_enemy_turns()
       └─> Each enemy: chase/attack/wander

4. Update display:
   ├─> Update FOV (entity.update_visibility())
   ├─> Center camera
   └─> Update UI (health bar, messages)
```

### Key Classes

**Dungeon** (`dungeon.py`)
- Generates rooms and corridors
- Tracks tile properties (walkable, transparent)
- Places stairs for level progression

**Player / Enemy** (`entities.py`)
- Wraps McRogueFace Entity objects
- Contains Fighter component for combat stats
- Handles movement and position

**TurnManager** (`turns.py`)
- Controls game flow
- Processes player actions
- Triggers enemy turns
- Tracks game state (player turn, game over, etc.)

**GameUI** (`ui.py`)
- HealthBar: Visual HP display
- MessageLog: Scrolling combat messages
- LevelDisplay: Current dungeon depth

## Customization Guide

### Adding New Enemy Types

1. Add sprite constant in `constants.py`:
```python
SPRITE_SKELETON = 113
```

2. Add stats in `constants.py`:
```python
ENEMY_STATS = {
    ...
    'skeleton': {
        'hp': 12,
        'attack': 4,
        'defense': 1,
        'xp': 45,
        'sprite': SPRITE_SKELETON,
        'name': 'Skeleton'
    }
}
```

3. Add to spawn weights:
```python
ENEMY_SPAWN_WEIGHTS = {
    3: [('goblin', 50), ('skeleton', 30), ('orc', 20)],
    ...
}
```

### Modifying Dungeon Generation

In `constants.py`:
```python
# Larger rooms
ROOM_MIN_SIZE = 8
ROOM_MAX_SIZE = 16

# More rooms
MAX_ROOMS = 20

# Bigger dungeon
DUNGEON_WIDTH = 100
DUNGEON_HEIGHT = 60
```

### Adding Items

1. Create item classes in a new `items.py`:
```python
@dataclass
class Item:
    name: str
    sprite: int

class HealthPotion(Item):
    def __init__(self):
        super().__init__("Health Potion", SPRITE_POTION)
        self.heal_amount = 10

    def use(self, player):
        healed = player.fighter.heal(self.heal_amount)
        return f"You heal for {healed} HP!"
```

2. Add inventory to Player in `entities.py`
3. Add pickup logic in `game.py`
4. Add use item key handler

### Custom AI Behaviors

Extend `AIBehavior` in `ai.py`:
```python
class FleeingAI(AIBehavior):
    """Runs away when HP is low."""

    def take_turn(self, enemy, player, dungeon, enemies):
        # Run when below 25% HP
        if enemy.fighter.hp_percent < 0.25:
            # Move away from player
            ...
        else:
            # Normal chase behavior
            return super().take_turn(enemy, player, dungeon, enemies)
```

## API Patterns Used

### Entity Creation
```python
# Create entity with position, texture, sprite index
entity = mcrfpy.Entity((x, y), texture, sprite_index)
grid.entities.append(entity)
```

### Grid Access
```python
# Get tile at position
point = grid.at(x, y)
point.tilesprite = 10
point.walkable = True
point.transparent = True
point.color_overlay = mcrfpy.Color(0, 0, 0, 128)
```

### FOV Calculation
```python
# Update entity's visibility data
entity.update_visibility()

# Check visibility at position
state = entity.at(x, y)
if state.visible:
    # Currently visible
elif state.discovered:
    # Seen before but not now
```

### Pathfinding
```python
# Get path from entity to target
path = entity.path_to(target_x, target_y)
# Returns list of (x, y) tuples
```

### Input Handling
```python
def handle_keypress(key, state):
    if state != "start":  # Only handle key down
        return
    if key == "W":
        # Move up

mcrfpy.keypressScene(handle_keypress)
```

### UI Building
```python
# Frame with children
frame = mcrfpy.Frame(x, y, width, height)
frame.fill_color = mcrfpy.Color(50, 50, 50, 200)
frame.outline = 2
frame.outline_color = mcrfpy.Color(255, 255, 255)

# Caption for text
caption = mcrfpy.Caption("Text", font, x, y)
caption.fill_color = mcrfpy.Color(255, 255, 255)

# Add to scene
ui = mcrfpy.sceneUI("game")
ui.append(frame)
ui.append(caption)
```

## Troubleshooting

### "No module named 'constants'"
Make sure all `.py` files are in the same directory and that directory is in Python's path. McRogueFace should handle this automatically when files are in `scripts/`.

### Enemies not appearing
Check that `MAX_ENEMIES_PER_ROOM` in constants.py is greater than 0, and that your spawn weights include the current level.

### FOV not working
Ensure you call `entity.update_visibility()` after moving the player, and that tiles have correct `transparent` values set.

### Performance issues
- Reduce `DUNGEON_WIDTH` and `DUNGEON_HEIGHT`
- Reduce `MAX_ROOMS`
- Limit number of enemies with `MAX_ENEMIES_PER_ROOM`

## Credits

- McRogueFace game engine by jmccardle
- Default tileset: Kenney's Tiny Dungeon (CC0)
- Font: JetBrains Mono

## License

This template is provided as-is for use with McRogueFace. Modify freely for your own projects!
