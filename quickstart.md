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

# Create a simple test scene
mcrfpy.createScene("test")

# Load a texture (sprite sheet) and font
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)
font = mcrfpy.Font("assets/JetbrainsMono.ttf")

# Create a grid for tile-based graphics
grid = mcrfpy.Grid(20, 15, texture, (10, 10), (800, 600))

# Add it to the scene's UI
ui = mcrfpy.sceneUI("test")
ui.append(grid)

# Switch to our scene
mcrfpy.setScene("test")

# Add keyboard controls
def move_around(key, state):
    if state == "start":
        print(f"You pressed {key}")

mcrfpy.keypressScene(move_around)
```

Save and run McRogueFace again to see your simple scene!

### 4. Make Your First Change

Let's create a custom main menu with buttons. Open `scripts/game.py` and replace it with:

```python
import mcrfpy

# Create a scene
mcrfpy.createScene("main_menu")

# Load resources
font = mcrfpy.Font("assets/JetbrainsMono.ttf")
btn_tex = mcrfpy.Texture("assets/48px_ui_icons-KenneyNL.png", 48, 48)

# Get the scene's UI collection
ui = mcrfpy.sceneUI("main_menu")

# Add a background
bg = mcrfpy.Frame(0, 0, 1024, 768, fill_color=(20, 20, 40))
ui.append(bg)

# Add a title
title = mcrfpy.Caption((312, 100), "My Awesome Game", font, fill_color=(255, 255, 100))
title.font_size = 48
title.outline = 2
title.outline_color = (0, 0, 0)
ui.append(title)

# Create a button using Frame + Caption + click handler
button_frame = mcrfpy.Frame(362, 300, 300, 80, fill_color=(50, 150, 50))
button_caption = mcrfpy.Caption((150, 25), "Start Game", font, fill_color=(255, 255, 255))
button_caption.font_size = 24
button_frame.children.append(button_caption)

# Add click handler
def start_game(x, y, button, event):
    if event == "end":  # Mouse button release
        print("Starting the game!")
        # Create and switch to game scene
        mcrfpy.createScene("game")
        mcrfpy.setScene("game")

button_frame.click = start_game
ui.append(button_frame)

# Switch to our menu scene
mcrfpy.setScene("main_menu")
```

Save and run - you now have a custom main menu with a working button!

### 5. Add a Game Entity

Let's create a custom entity for a game. Entities in McRogueFace can be NPCs, enemies, or interactive objects. Here's an example:

```python
import mcrfpy

# Create a scene and load resources
mcrfpy.createScene("game")
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)
font = mcrfpy.Font("assets/JetbrainsMono.ttf")

# Create a grid
grid = mcrfpy.Grid(20, 15, texture, (10, 10), (640, 480))
ui = mcrfpy.sceneUI("game")
ui.append(grid)

# Add the player entity
player = mcrfpy.Entity((10, 7), texture, 85)  # Sprite 85 is a character
grid.entities.append(player)

# Add an NPC entity
npc = mcrfpy.Entity((5, 5), texture, 109)  # Sprite 109 is a monster
grid.entities.append(npc)

# Add a treasure chest
treasure = mcrfpy.Entity((15, 10), texture, 89)  # Sprite 89 is a chest
grid.entities.append(treasure)

# Basic movement with keyboard
def handle_keys(key, state):
    if state == "start":
        if key == "W": player.pos = (player.pos.x, player.pos.y - 1)
        elif key == "S": player.pos = (player.pos.x, player.pos.y + 1)
        elif key == "A": player.pos = (player.pos.x - 1, player.pos.y)
        elif key == "D": player.pos = (player.pos.x + 1, player.pos.y)

mcrfpy.keypressScene(handle_keys)
mcrfpy.setScene("game")
```

For more complex entity behavior, look at the Crypt of Sokoban source in `src/scripts/cos_entities.py`!

### 6. Load a Custom Sprite Sheet

Want to use your own graphics? Here's how:

```python
import mcrfpy

# Create a scene
mcrfpy.createScene("game")

# Load your sprite sheet (tile width, tile height)
my_texture = mcrfpy.Texture("assets/my_sprites.png", 32, 32)

# Create a grid using your texture
grid = mcrfpy.Grid(20, 15, my_texture, (10, 10), (640, 480))

# Set specific tiles - grid.at() returns a grid point
grid.at(5, 5).sprite = 10  # Tree sprite at index 10
grid.at(6, 5).sprite = 11  # Rock sprite at index 11

# You can also set walkability
grid.at(6, 5).walkable = False  # Make the rock solid

# Add the grid to the scene
ui = mcrfpy.sceneUI("game")
ui.append(grid)

# Switch to the scene
mcrfpy.setScene("game")
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

