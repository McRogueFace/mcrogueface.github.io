# Getting Started with McRogueFace

Welcome to McRogueFace! This guide will help you get up and running with your first game.

## Installation

### Prerequisites

Before installing McRogueFace, ensure you have:

- **C++ Compiler**: GCC 7+, Clang 5+, or MSVC 2017+
- **CMake**: Version 3.14 or higher
- **Python**: Version 3.12 or higher
- **Git**: For cloning the repository
- **SFML**: Version 2.5+ (usually installed automatically)

### Linux Installation

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install build-essential cmake git libsfml-dev python3.12-dev

# Clone the repository
git clone https://github.com/jmcb/McRogueFace.git
cd McRogueFace

# Build the project
make

# Run the example game
cd build
./mcrogueface
```

### Windows Installation

```powershell
# Clone the repository
git clone https://github.com/jmcb/McRogueFace.git
cd McRogueFace

# Build with CMake
mkdir build
cd build
cmake ..
cmake --build .

# Run the example game
mcrogueface.exe
```

## Your First Game

Let's create a simple "Hello World" game to understand the basics.

### Step 1: Create the Game Script

Create a new file `scripts/hello_game.py` in your build directory:

```python
import mcrfpy

# Create a new scene
mcrfpy.createScene("main")

# Create a title
title = mcrfpy.Caption(400, 100, "Hello McRogueFace!")
title.font = mcrfpy.default_font
title.font_size = 32
title.font_color = (255, 255, 255)  # White
title.centered = True

# Create instructions
instructions = mcrfpy.Caption(400, 200, "Press ESC to exit")
instructions.font = mcrfpy.default_font
instructions.font_size = 18
instructions.font_color = (200, 200, 200)  # Light gray
instructions.centered = True

# Add a background frame
background = mcrfpy.Frame(200, 50, 400, 200)
background.bgcolor = (64, 64, 128)  # Blue-gray
background.outline = 2

# Add elements to the scene
ui = mcrfpy.sceneUI("main")
ui.append(background)
ui.append(title)
ui.append(instructions)

# Handle keyboard input
def handle_keys(key):
    if key == "Escape":
        mcrfpy.exit()
    print(f"Key pressed: {key}")

# Register the keyboard handler
mcrfpy.keypressScene(handle_keys)

# Switch to our scene
mcrfpy.setScene("main")
```

### Step 2: Run Your Game

```bash
./mcrogueface
```

Your game should display a window with a blue-gray background, white title text, and respond to the ESC key.

## Understanding the Basics

### Scenes

Scenes are containers for your game states (menu, gameplay, game over, etc.):

```python
# Create scenes
mcrfpy.createScene("menu")
mcrfpy.createScene("game")
mcrfpy.createScene("gameover")

# Switch between scenes
mcrfpy.setScene("menu")  # Show the menu
```

### UI Elements

McRogueFace provides several UI element types:

#### Captions (Text)
```python
text = mcrfpy.Caption(x, y, "Your text here")
text.font = mcrfpy.default_font
text.font_size = 24
text.font_color = (255, 255, 255)  # RGB
text.centered = True  # Center on x,y position
```

#### Sprites
```python
# Load a texture (sprite sheet)
texture = mcrfpy.Texture("assets/sprites.png", 16, 16)  # 16x16 tiles

# Create a sprite
sprite = mcrfpy.Sprite(x, y)
sprite.texture = texture
sprite.sprite_index = 0  # Which tile to show
sprite.scale = (2.0, 2.0)  # Make it bigger
```

#### Frames (Containers)
```python
frame = mcrfpy.Frame(x, y, width, height)
frame.bgcolor = (50, 50, 50)  # Dark gray
frame.outline = 2  # 2-pixel border
frame.outline_color = (255, 255, 255)  # White border
```

#### Grids (Tilemaps)
```python
# Create a 20x15 grid of 32x32 pixel tiles
grid = mcrfpy.Grid(x, y, 20, 15, texture, 32, 32)

# Set individual tiles
grid.set_tile(tile_x, tile_y, sprite_index)
```

### Input Handling

Handle keyboard input with callback functions:

```python
def on_keypress(key):
    if key == "w" or key == "Up":
        # Move up
        pass
    elif key == "s" or key == "Down":
        # Move down
        pass
    elif key == "Space":
        # Action
        pass

mcrfpy.keypressScene(on_keypress)
```

### Game Loop with Timers

Create game loops using timers:

```python
def game_update(runtime):
    # This runs every 100ms
    # Update game logic here
    player.move()
    check_collisions()
    
# Set a timer to call game_update every 100ms
mcrfpy.setTimer("gameloop", game_update, 100)

# Stop the timer
mcrfpy.delTimer("gameloop")
```

## Next Steps

Now that you understand the basics:

1. **Explore the Examples**: Look at the Crypt of Sokoban source in `src/scripts/`
2. **Read the API Reference**: [Full API Documentation](api-reference.md)
3. **Try the Tutorials**: [Advanced tutorials](tutorials.md) for specific features
4. **Study the Source**: Examine the [implementation](https://github.com/jmccardle/McRogueFace) for deeper understanding

## Common Issues

### "Module 'mcrfpy' not found"
- Make sure you're running from the `build` directory
- Check that Python 3.12 is installed

### Graphics not showing
- Verify your texture paths are correct (relative to the executable)
- Check that sprite indices are within texture bounds

### Game crashes on start
- Look for Python errors in the console
- Ensure all required assets are in the `assets/` directory

### Performance issues
- Use timers instead of tight loops
- Limit the number of entities on screen
- Consider using RenderTexture for static content

## Tips for Success

1. **Start Small**: Build simple games before attempting complex projects
2. **Use Timers**: They're essential for animations and game logic
3. **Organize Scenes**: Keep menu, gameplay, and UI in separate scenes
4. **Test Often**: Use the automation API to create repeatable tests
5. **Read the Source**: The engine source code is well-documented

Happy game development with McRogueFace!