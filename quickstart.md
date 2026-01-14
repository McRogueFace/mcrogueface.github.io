# McRogueFace Quickstart Guide

**Make 2D games with Python** - No C++ required!

---

[**Source Code**](https://github.com/jmccardle/McRogueFace) • [**Downloads**](https://github.com/jmccardle/McRogueFace/releases) • **[Quickstart](https://mcrogueface.github.io/quickstart)** • [**Tutorials**](https://mcrogueface.github.io/tutorials) • [**API Reference**](https://mcrogueface.github.io/api-reference) • [**Cookbook**](https://mcrogueface.github.io/cookbook) • [**C++ Extensions**](https://mcrogueface.github.io/extending-cpp)

---

## Get Started in 5 Minutes

This guide will have you running games and making changes in just a few minutes. No compilation needed!

**⚠️ Caution:** McRogueFace is in *Alpha Pre-Release* - the API may change, hopefully for the better. Download the source code or clone the repository to review the complete documentation in the `/docs` directory, and check back frequently for updates.

### 1. Download McRogueFace


1. Go to the [latest release](https://github.com/jmccardle/McRogueFace/releases/latest)
2. Download the right version for your system:
   - **Windows**: [McRogueFace-0.1.0-prerelease2-Win.zip](https://github.com/jmccardle/McRogueFace/releases/download/v0.1.0-prerelease2/McRogueFace-0.1.0-prerelease2-Win.zip)
   - **Linux**: [McRogueFace-0.1.0-prerelease2-Linux.tar.bz2](https://github.com/jmccardle/McRogueFace/releases/download/v0.1.0-prerelease2/McRogueFace-0.1.0-prerelease2-Linux.tar.bz2)
3. Extract the archive to a folder (e.g., `C:\Games\McRogueFace` or `~/McRogueFace`)

### 2. Run the Demo Game

Open a terminal/command prompt in the McRogueFace folder and run:

**Windows:**
```cmd
mcrogueface.exe
```

**Linux:**
```bash
./mcrogueface
```

You should see the demo game start up! Use arrow keys to move around, click buttons, and explore what's possible.

### 3. Switch to a Different Game

McRogueFace automatically runs `scripts/game.py` on startup. The demo game is already running when you start McRogueFace - it includes the full "Crypt of Sokoban" game with the main menu.

To see a simpler example, you can replace `scripts/game.py` with:

```python
import mcrfpy

# Create a scene
scene = mcrfpy.Scene("test")

# Load a texture (sprite sheet)
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create a grid for tile-based graphics
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture,
                   pos=(10, 10), size=(800, 600))

# Add the grid to the scene
scene.children.append(grid)

# Add keyboard controls
def move_around(key, state):
    if state == "start":
        print(f"You pressed {key}")

scene.on_key = move_around

# Activate the scene
scene.activate()
```

Save and run McRogueFace again to see your simple scene!

### 4. Make Your First Change

Let's create a custom main menu with buttons. Open `scripts/game.py` and replace it with:

```python
import mcrfpy

# Create a scene
scene = mcrfpy.Scene("main_menu")

# Load resources
font = mcrfpy.Font("assets/JetbrainsMono.ttf")

# Add a background
bg = mcrfpy.Frame(pos=(0, 0), size=(1024, 768),
                  fill_color=mcrfpy.Color(20, 20, 40))
scene.children.append(bg)

# Add a title
title = mcrfpy.Caption(pos=(312, 100), text="My Awesome Game",
                       fill_color=mcrfpy.Color(255, 255, 100))
title.font_size = 48
title.outline = 2
title.outline_color = mcrfpy.Color(0, 0, 0)
scene.children.append(title)

# Create a button using Frame + Caption + click handler
button_frame = mcrfpy.Frame(pos=(362, 300), size=(300, 80),
                            fill_color=mcrfpy.Color(50, 150, 50))
button_caption = mcrfpy.Caption(pos=(90, 25), text="Start Game",
                                fill_color=mcrfpy.Color(255, 255, 255))
button_caption.font_size = 24
button_frame.children.append(button_caption)

# Add click handler (3 arguments: x, y, button)
def start_game(x, y, button):
    print("Starting the game!")
    game_scene = mcrfpy.Scene("game")
    game_scene.activate()

button_frame.on_click = start_game
scene.children.append(button_frame)

# Activate the menu scene
scene.activate()
```

Save and run - you now have a custom main menu with a working button!

### 5. Add a Game Entity

Let's create a custom entity for a game. Entities in McRogueFace can be NPCs, enemies, or interactive objects. Here's an example:

```python
import mcrfpy

# Create a scene and load resources
scene = mcrfpy.Scene("game")
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create a grid
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture,
                   pos=(10, 10), size=(640, 480))
scene.children.append(grid)

# Add the player entity
player = mcrfpy.Entity(grid_pos=(10, 7), texture=texture, sprite_index=85)
grid.entities.append(player)

# Add an NPC entity
npc = mcrfpy.Entity(grid_pos=(5, 5), texture=texture, sprite_index=109)
grid.entities.append(npc)

# Add a treasure chest
treasure = mcrfpy.Entity(grid_pos=(15, 10), texture=texture, sprite_index=89)
grid.entities.append(treasure)

# Basic movement with keyboard
def handle_keys(key, state):
    if state == "start":
        x, y = player.pos[0], player.pos[1]
        if key == "W": player.pos = (x, y - 1)
        elif key == "S": player.pos = (x, y + 1)
        elif key == "A": player.pos = (x - 1, y)
        elif key == "D": player.pos = (x + 1, y)

scene.on_key = handle_keys
scene.activate()
```

For more complex entity behavior, look at the Crypt of Sokoban source in `src/scripts/cos_entities.py`!

### 6. Load a Custom Sprite Sheet

Want to use your own graphics? Here's how:

```python
import mcrfpy

# Create a scene
scene = mcrfpy.Scene("game")

# Load your sprite sheet (tile width, tile height)
my_texture = mcrfpy.Texture("assets/my_sprites.png", 32, 32)

# Create a grid using your texture
grid = mcrfpy.Grid(grid_size=(20, 15), texture=my_texture,
                   pos=(10, 10), size=(640, 480))

# Set specific tiles - grid.at() returns a grid point
grid.at((5, 5)).tilesprite = 10  # Tree sprite at index 10
grid.at((6, 5)).tilesprite = 11  # Rock sprite at index 11

# You can also set walkability
grid.at((6, 5)).walkable = False  # Make the rock solid

# Add the grid to the scene
scene.children.append(grid)

# Activate the scene
scene.activate()
```

Tips for sprite sheets:
- Use consistent tile sizes (16x16, 32x32, etc.)
- Sprites are indexed left-to-right, top-to-bottom starting at 0
- PNG format with transparency works best

## What's Next?

### Learn by Doing
- **[McRogueFace Does The Entire Roguelike Tutorial](https://mcrogueface.github.io/tutorials)** - Build a complete game step-by-step
- **[Cookbook](https://mcrogueface.github.io/cookbook)** - Copy/paste solutions for common tasks

### Reference Material  
- **[Complete API Reference](https://mcrogueface.github.io/api-reference)** - Every function and class documented
- **[Example Games](https://github.com/jmccardle/McRogueFace/tree/main/examples)** - Full source code to learn from

### Advanced Topics
- **[C++ Extension Guide](https://mcrogueface.github.io/extending-cpp)** - Add new engine features (requires compilation)

## Troubleshooting

### "mcrogueface: command not found"
You need to be in the McRogueFace directory, or add it to your PATH.

### "No module named mcrfpy"
Make sure you're running `mcrogueface`, not `python`. McRogueFace is a complete Python environment.

### Black screen on startup
Check that the `assets/` and `scripts/` folders are in the same directory as the mcrogueface executable.

### Can't load my sprites
- Ensure your sprite sheet uses 32x32 pixel tiles (or adjust the size in loadTexture)
- Use PNG format with transparency
- Check the file path is relative to the mcrogueface executable

## Get Help

- **Documentation**: Check the [API Reference](/api-reference) and [Examples](/examples)
- **Source Code**: Browse the [GitHub repository](https://github.com/jmccardle/McRogueFace) for implementation details

---

