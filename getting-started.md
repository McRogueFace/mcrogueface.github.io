# Getting Started with McRogueFace

**Make 2D games with Python** - No C++ required!

---

[**Source Code**](https://github.com/jmccardle/McRogueFace) | [**Downloads**](https://github.com/jmccardle/McRogueFace/releases) | **[Getting Started](https://mcrogueface.github.io/getting-started)** | [**Tutorials**](https://mcrogueface.github.io/tutorials) | [**API Reference**](https://mcrogueface.github.io/api-reference) | [**Cookbook**](https://mcrogueface.github.io/cookbook) | [**C++ Extensions**](https://mcrogueface.github.io/extending-cpp)

---

This guide will help you get McRogueFace installed and running your first game script.

## Prerequisites

Before building McRogueFace, ensure you have the following installed:

### Required Software

- **C++17 Compiler**: GCC 7+, Clang 5+, or MSVC 2017+
- **CMake**: Version 3.14 or higher
- **Python**: Version 3.12 development headers
- **SFML**: Version 2.5+ (multimedia library)
- **Git**: For cloning the repository

### Linux (Ubuntu/Debian)

```bash
# Install all dependencies
sudo apt-get update
sudo apt-get install build-essential cmake git libsfml-dev python3.12-dev
```

### Linux (Fedora)

```bash
sudo dnf install gcc-c++ cmake git SFML-devel python3.12-devel
```

### Windows

1. Install [Visual Studio 2019+](https://visualstudio.microsoft.com/) with C++ workload
2. Install [CMake](https://cmake.org/download/)
3. Install [Python 3.12](https://www.python.org/downloads/)
4. SFML will be downloaded automatically during build

## Building McRogueFace

### Option 1: Download Pre-built Release (Recommended)

1. Go to the [latest release](https://github.com/jmccardle/McRogueFace/releases/latest)
2. Download the appropriate version:
   - **Windows**: `McRogueFace-*-Win.zip`
   - **Linux**: `McRogueFace-*-Linux.tar.bz2`
3. Extract to a folder (e.g., `~/McRogueFace` or `C:\Games\McRogueFace`)

### Option 2: Build from Source

#### Linux

```bash
# Clone the repository
git clone https://github.com/jmccardle/McRogueFace.git
cd McRogueFace

# Build the project
make

# The executable will be in build/
cd build
./mcrogueface
```

#### Windows

```powershell
# Clone the repository
git clone https://github.com/jmccardle/McRogueFace.git
cd McRogueFace

# Build with CMake
mkdir build
cd build
cmake ..
cmake --build . --config Release

# Run the executable
Release\mcrogueface.exe
```

### Verify Installation

After building or extracting, verify your installation:

```bash
# Linux
./mcrogueface --version

# Windows
mcrogueface.exe --version
```

You should see the demo game start up when running without arguments.

## Your First Game

McRogueFace runs Python scripts automatically. The engine looks for `scripts/game.py` on startup.

Create a new file `scripts/game.py` with the following content:

```python
import mcrfpy

# Create a scene - scenes are containers for all UI elements
scene = mcrfpy.Scene("hello")

# Add a caption (text display)
caption = mcrfpy.Caption(
    pos=(400, 300),
    text="Hello Roguelike!"
)
caption.fill_color = mcrfpy.Color(255, 255, 100)  # Yellow text
caption.font_size = 32

# Add the caption to the scene's children collection
scene.children.append(caption)

# Add instructions
instructions = mcrfpy.Caption(
    pos=(350, 350),
    text="Press ESC to exit, or any key to see it printed"
)
instructions.fill_color = mcrfpy.Color(200, 200, 200)
instructions.font_size = 16
scene.children.append(instructions)

# Input handler - receives (key, action) where action is "start" or "end"
def on_key(key, action):
    if action != "start":  # Only respond to key press, not release
        return
    if key == "Escape":
        mcrfpy.exit()
    print(f"Key pressed: {key}")

# Register the keyboard handler for this scene
scene.on_key = on_key

# Activate the scene (make it visible)
scene.activate()
```

Run McRogueFace to see your game:

```bash
./mcrogueface  # Linux
mcrogueface.exe  # Windows
```

You should see yellow text that says "Hello Roguelike!" and pressing keys will print to the console.

## Understanding the Basics

### How McRogueFace Works

McRogueFace is different from traditional Python game frameworks:

1. **No game loop needed** - The engine handles the render loop internally
2. **Scripts are imported** - Your Python script runs once at startup to set up the game
3. **Event-driven** - Use callbacks for input handling and timers for updates

### Scenes

Scenes are containers for your game states (menu, gameplay, inventory, etc.):

```python
# Create scenes
menu = mcrfpy.Scene("menu")
game = mcrfpy.Scene("game")
game_over = mcrfpy.Scene("game_over")

# Activate a scene
menu.activate()
```

### UI Elements

McRogueFace provides several UI element types. All use keyword arguments:

#### Caption (Text)

```python
text = mcrfpy.Caption(
    pos=(100, 100),
    text="Your text here"
)
text.fill_color = mcrfpy.Color(255, 255, 255)
text.font_size = 24
```

#### Frame (Container)

```python
panel = mcrfpy.Frame(
    pos=(50, 50),
    size=(400, 300),
    fill_color=mcrfpy.Color(50, 50, 80)
)
panel.outline = 2
panel.outline_color = mcrfpy.Color(255, 255, 255)
```

#### Grid (Tilemap)

```python
# Load a sprite sheet texture (16x16 pixel tiles)
texture = mcrfpy.Texture("assets/tiles.png", 16, 16)

# Create a 20x15 tile grid
grid = mcrfpy.Grid(
    pos=(10, 10),
    grid_size=(20, 15),
    texture=texture,
    size=(640, 480)  # Display size in pixels
)

# Set individual tiles using grid.at()
grid.at(5, 5).tilesprite = 10  # Set tile at (5,5) to sprite index 10
grid.at(5, 5).walkable = True
```

#### Entity (Grid Object)

```python
# Create an entity on the grid
player = mcrfpy.Entity(
    grid_pos=(10, 7),
    texture=texture,
    sprite_index=64  # Character sprite
)

# Add to grid's entity collection
grid.entities.append(player)

# Move the entity
player.x = 11
player.y = 7
```

### Input Handling

Keyboard input uses a callback that receives the key name and action:

```python
def on_key(key, action):
    if action != "start":  # Filter out key release events
        return

    if key == "W" or key == "Up":
        player.y -= 1
    elif key == "S" or key == "Down":
        player.y += 1
    elif key == "A" or key == "Left":
        player.x -= 1
    elif key == "D" or key == "Right":
        player.x += 1

scene.on_key = on_key
```

### Timers

For animations and game updates, use timers:

```python
def game_update(timer, runtime):
    # This runs every 100ms
    update_enemies()
    check_collisions()

# Create a recurring timer (duration in seconds)
game_timer = mcrfpy.Timer("gameloop", game_update, 0.1)

# Stop the timer when done
game_timer.cancel()
```

## A More Complete Example

Here is a working example with a movable character on a grid:

```python
import mcrfpy

# Create and set up the scene
scene = mcrfpy.Scene("game")

# Load the tileset texture
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create a grid
grid = mcrfpy.Grid(
    pos=(32, 32),
    grid_size=(20, 15),
    texture=texture,
    size=(640, 480)
)
grid.zoom = 2.0  # Scale up for visibility

# Fill the grid with floor tiles, walls on edges
FLOOR = 0
WALL = 3

for y in range(15):
    for x in range(20):
        point = grid.at(x, y)
        if x == 0 or x == 19 or y == 0 or y == 14:
            point.tilesprite = WALL
            point.walkable = False
        else:
            point.tilesprite = FLOOR
            point.walkable = True

# Add the grid to the scene
scene.children.append(grid)

# Create the player entity
player = mcrfpy.Entity(
    grid_pos=(10, 7),
    texture=texture,
    sprite_index=85  # Character sprite
)
grid.entities.append(player)

# Add a title
title = mcrfpy.Caption(
    pos=(250, 5),
    text="Use WASD or Arrow Keys to Move"
)
title.fill_color = mcrfpy.Color(255, 255, 255)
scene.children.append(title)

# Input handler with collision detection
def on_key(key, action):
    if action != "start":
        return

    # Calculate new position
    new_x, new_y = int(player.x), int(player.y)

    if key == "W" or key == "Up":
        new_y -= 1
    elif key == "S" or key == "Down":
        new_y += 1
    elif key == "A" or key == "Left":
        new_x -= 1
    elif key == "D" or key == "Right":
        new_x += 1
    elif key == "Escape":
        mcrfpy.exit()
        return

    # Check if the new position is walkable
    point = grid.at(new_x, new_y)
    if point and point.walkable:
        player.x = new_x
        player.y = new_y

scene.on_key = on_key
scene.activate()

print("Game started! Use WASD or arrow keys to move.")
```

## Next Steps

Now that you have a working game foundation:

1. **Follow the Tutorials** - Start with [Part 0: Scene, Texture, and Grid](/tutorials#part-0-scene-texture-and-grid) for a complete walkthrough
2. **Browse the API Reference** - See [API Reference](/api-reference) for all available functions and classes
3. **Check the Cookbook** - Find [copy-paste solutions](/cookbook) for common tasks
4. **Study the Demo Game** - Look at `src/scripts/` in the repository for the full "Crypt of Sokoban" source code

## Troubleshooting

### "Module 'mcrfpy' not found"

You are running `python scripts/game.py` directly. McRogueFace embeds Python - run the `mcrogueface` executable instead, which will import your script automatically.

### Black screen on startup

- Check that the `assets/` and `scripts/` folders are in the same directory as the `mcrogueface` executable
- Ensure `scripts/game.py` exists and has no Python syntax errors
- Check the console for error messages

### Graphics not showing

- Verify your texture paths are correct (relative to the executable)
- Check that sprite indices are within the texture bounds
- Make sure you called `scene.children.append()` to add elements to the scene
- Confirm you called `scene.activate()` to activate the scene

### Game crashes on start

- Look for Python errors in the console output
- Ensure all required asset files exist in `assets/`
- Check for typos in file paths (they are case-sensitive on Linux)

### Performance issues

- Use timers instead of tight loops
- Limit the number of entities on screen
- Use appropriate timer intervals (16ms for 60 FPS, 33ms for 30 FPS)

### Python errors not showing

Run McRogueFace from a terminal/command prompt to see Python error messages and print() output.

## Getting Help

- **Documentation**: [API Reference](/api-reference), [Tutorials](/tutorials), [Cookbook](/cookbook)
- **Source Code**: [GitHub Repository](https://github.com/jmccardle/McRogueFace)
- **Issues**: Report bugs on the [GitHub Issues](https://github.com/jmccardle/McRogueFace/issues) page

---

Happy game development with McRogueFace!
