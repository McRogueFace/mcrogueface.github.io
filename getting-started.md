# Getting Started with McRogueFace

## Installation

McRogueFace requires:
- C++ compiler with C++17 support
- CMake 3.10+
- SFML 2.5+
- Python 3.12
- libtcod (included)

### Building from Source

```bash
git clone https://github.com/user/McRogueFace.git
cd McRogueFace
cmake .
make
./mcrogueface
```

## Your First Game {#first-game}

Let's create a simple roguelike with a player that can move around a dungeon.

### Step 1: Create the Game Script

Create a file `scripts/game.py`:

```python
import mcrfpy

# Create main game scene
mcrfpy.createScene("game")
mcrfpy.setScene("game")
ui = mcrfpy.sceneUI("game")

# Create a 40x30 grid (standard roguelike size)
grid = mcrfpy.Grid(
    40, 30,                          # Grid dimensions
    mcrfpy.default_texture,          # Texture with 16x16 tiles
    (0, 0),                          # Position on screen
    (640, 480)                       # Display size
)
ui.append(grid)

# Initialize the dungeon tiles
for x in range(40):
    for y in range(30):
        pt = grid.at(x + y * 40)
        if x == 0 or x == 39 or y == 0 or y == 29:
            # Walls around the edge
            pt.tilesprite = 35  # Wall tile
            pt.walkable = False
            pt.transparent = False
        else:
            # Floor tiles
            pt.tilesprite = 46  # Floor tile
            pt.walkable = True
            pt.transparent = True

# Create the player
player = mcrfpy.Entity(grid)
player.pos = (20, 15)  # Start in center
player.sprite_number = 5  # Player sprite
grid.children.append(player)

# Center camera on player
grid.center = player.pos
```

### Step 2: Add Movement

Add keyboard controls to move the player:

```python
def handle_keys(key):
    # Get current position
    x, y = player.pos
    
    # WASD movement
    if key == 119 and y > 0:  # W - up
        new_pos = (x, y - 1)
    elif key == 115 and y < 29:  # S - down
        new_pos = (x, y + 1)
    elif key == 97 and x > 0:  # A - left
        new_pos = (x - 1, y)
    elif key == 100 and x < 39:  # D - right
        new_pos = (x + 1, y)
    else:
        return
    
    # Check if we can walk there
    tile = grid.at(new_pos[0] + new_pos[1] * 40)
    if tile.walkable:
        player.pos = new_pos
        grid.center = new_pos  # Camera follows player

mcrfpy.keypressScene(handle_keys)
```

### Step 3: Add Enemies

Let's add some enemies to make it interesting:

```python
import random

# Create enemies
enemies = []
for i in range(5):
    enemy = mcrfpy.Entity(grid)
    # Place randomly on walkable tiles
    while True:
        x = random.randint(1, 38)
        y = random.randint(1, 28)
        if grid.at(x + y * 40).walkable:
            enemy.pos = (x, y)
            break
    enemy.sprite_number = 16  # Enemy sprite
    grid.children.append(enemy)
    enemies.append(enemy)
```

### Step 4: Add a HUD

Display player information with UI elements:

```python
# Create HUD frame
hud = mcrfpy.Frame(0, 480, 640, 40)
hud.fill_color = mcrfpy.Color(20, 20, 20)
ui.append(hud)

# Add health display
health_label = mcrfpy.Caption("Health: 100", mcrfpy.default_font)
health_label.pos = (10, 490)
health_label.fill_color = mcrfpy.Color(255, 0, 0)
hud.children.append(health_label)

# Add position display
pos_label = mcrfpy.Caption("Position: (20, 15)", mcrfpy.default_font)
pos_label.pos = (200, 490)
pos_label.fill_color = mcrfpy.Color(255, 255, 255)
hud.children.append(pos_label)

# Update position label when moving
def update_hud():
    pos_label.text = f"Position: {player.pos}"
```

## Understanding the Coordinate System

McRogueFace uses several coordinate systems:

1. **Grid Coordinates**: Integer positions on the grid (0,0) to (width-1, height-1)
2. **Screen Coordinates**: Pixel positions for UI elements
3. **Sprite Indices**: Sprites are numbered left-to-right, top-to-bottom in the texture

## Working with Textures

Textures are sprite sheets with fixed-size tiles:

```python
# Load a custom texture with 32x32 sprites
texture = mcrfpy.Texture("assets/my_sprites.png", 32, 32)

# Create a grid using this texture
grid = mcrfpy.Grid(50, 50, texture, (0, 0), (800, 600))
```

## Scene Management

Organize your game into scenes:

```python
# Create multiple scenes
mcrfpy.createScene("menu")
mcrfpy.createScene("game")
mcrfpy.createScene("gameover")

# Switch between them
mcrfpy.setScene("menu")  # Show menu

# Later...
mcrfpy.setScene("game")  # Start game
```

## Next Steps

- Read the [API Reference](api-reference.html) for detailed documentation
- Check out [Tutorials](tutorials.html) for advanced techniques
- Study the example game "Crypt of Sokoban" in `scripts/`