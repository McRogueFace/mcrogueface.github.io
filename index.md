# McRogueFace Game Engine

McRogueFace is a powerful roguelike game engine that combines C++ performance with Python flexibility. Create tile-based games with procedural generation, UI systems, and full audio support - all scriptable in Python.

## Key Features

- **Grid-based World System** - Efficient tile-based rendering with camera controls
- **Entity Management** - Spawn and control game objects on your grid
- **UI Framework** - Frames, captions, sprites, and nested layouts
- **Audio System** - Background music and sound effects
- **Input Handling** - Flexible keyboard and mouse input mapping
- **Scene Management** - Organize your game into multiple scenes

## Quick Example

```python
import mcrfpy

# Create a game scene
mcrfpy.createScene("game")
mcrfpy.setScene("game")

# Create a 50x50 grid world
grid = mcrfpy.Grid(50, 50, mcrfpy.default_texture, (0, 0), (800, 600))
ui = mcrfpy.sceneUI("game")
ui.append(grid)

# Add a player entity
player = mcrfpy.Entity(grid)
player.pos = (25, 25)  # Center of the grid
player.sprite_number = 5  # Use sprite index 5
grid.children.append(player)

# Set up keyboard controls
def on_keypress(key):
    if key == 119:  # 'w' key
        player.pos = (player.pos[0], player.pos[1] - 1)
    elif key == 115:  # 's' key
        player.pos = (player.pos[0], player.pos[1] + 1)
    # ... more controls

mcrfpy.keypressScene(on_keypress)
```

## Primary Types

McRogueFace provides five primary types for building games:

### 1. **Grid** - Your Game World
The Grid is the foundation of your roguelike - a tile-based world that efficiently renders terrain, handles camera movement, and manages entities.

### 2. **Entity** - Game Objects
Entities are objects that exist on your Grid - players, enemies, items, and interactive elements. Each entity has a position and sprite.

### 3. **Frame** - UI Containers
Frames are rectangular UI panels that can contain other UI elements. Use them for menus, HUDs, and dialog boxes.

### 4. **Sprite** - Image Display
Sprites display single images from texture atlases. Perfect for UI icons, decorations, and non-grid visuals.

### 5. **Caption** - Text Display
Captions render text with customizable fonts and colors. Use them for labels, dialog, and game messages.

## Getting Started

1. [Installation Guide](getting-started.html#installation)
2. [Your First Game](getting-started.html#first-game)
3. [API Reference](api-reference.html)
4. [Tutorials](tutorials.html)

## Architecture

McRogueFace uses a hybrid architecture:
- **C++ Core**: High-performance rendering, audio, and input handling
- **Python Scripts**: Game logic, AI, procedural generation
- **mcrfpy Module**: Bridge between C++ engine and Python code

This design gives you the best of both worlds - the performance of C++ with the rapid development of Python.

## Community

- [GitHub Repository](https://github.com/user/McRogueFace)
- [7DRL Entry](https://7drl.com/) - Created for 7DRL 2025