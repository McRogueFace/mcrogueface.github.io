# Part 0: Setting Up McRogueFace

Welcome to the McRogueFace roguelike tutorial! In this 13-part series, you will build a complete roguelike game from scratch using Python and the McRogueFace game engine.

## What is McRogueFace?

McRogueFace is a Python game engine designed for creating 2D games, particularly roguelikes. Unlike traditional Python game libraries, McRogueFace:

- **Runs your scripts in an embedded Python interpreter** - you do not call a `run()` function
- **Provides a built-in game loop** - the engine handles rendering and timing
- **Uses Scenes to organize game states** - menus, gameplay, and UI are separate scenes
- **Includes roguelike-specific features** - FOV, pathfinding, and grid-based maps

## Prerequisites

Before you begin, ensure you have:

- A working McRogueFace installation (see the [GitHub repository](https://github.com/jmccardle/McRogueFace) for build instructions)
- Basic Python knowledge (variables, functions, classes)
- A text editor or IDE

## Your First Script: Hello Roguelike

Create a new file called `hello_roguelike.py`:

```python
"""McRogueFace Tutorial - Part 0: Hello Roguelike

This script demonstrates the basic structure of a McRogueFace program.
"""
import mcrfpy

# Create a Scene object - this is the preferred approach
scene = mcrfpy.Scene("hello")

# Create a caption to display text
title = mcrfpy.Caption(
    pos=(512, 300),
    text="Hello, Roguelike!"
)
title.fill_color = mcrfpy.Color(255, 255, 255)
title.font_size = 32

# Add the caption to the scene's UI collection
scene.children.append(title)

# Activate the scene to display it
scene.activate()

# Note: There is no run() function!
# The engine is already running - your script is imported by it.
```

## Running Your Script

Place your script in the appropriate location for your McRogueFace installation and run the engine:

```bash
./mcrogueface hello_roguelike.py
```

You should see a window with "Hello, Roguelike!" displayed in white text.

## Understanding the Code

Let us examine each part of the script:

### 1. Importing McRogueFace

```python
import mcrfpy
```

The `mcrfpy` module is McRogueFace's Python API. It provides all the classes and functions you need to create games.

### 2. Creating a Scene

```python
scene = mcrfpy.Scene("hello")
```

A `Scene` is a container for your game's visual elements. You can have multiple scenes (menu, game, inventory) and switch between them. The Scene object pattern is preferred because:

- You can set `scene.on_key` for keyboard handling on ANY scene, not just the active one
- `scene.children` provides direct access to UI elements
- Subclassing Scene enables lifecycle callbacks (`on_enter`, `on_exit`)

### 3. Creating a Caption

```python
title = mcrfpy.Caption(
    pos=(512, 300),
    text="Hello, Roguelike!"
)
title.fill_color = mcrfpy.Color(255, 255, 255)
title.font_size = 32
```

A `Caption` displays text. The default window is 1024x768 pixels, so (512, 300) places the text near the center. Colors use RGBA format via `mcrfpy.Color`.

### 4. Adding to the Scene

```python
scene.children.append(title)
```

UI elements must be added to a scene's `children` collection to be displayed.

### 5. Activating the Scene

```python
scene.activate()
```

Only one scene can be active at a time. Activating a scene makes it visible and enables its input handlers.

## Key Concept: No Game Loop Required

Unlike many game frameworks, McRogueFace does not require you to write a game loop or call a `run()` function. The engine:

1. Starts up and initializes the window
2. Imports your Python script
3. Runs the game loop automatically
4. Your script sets up scenes and handlers; the engine does the rest

This design means your script is more declarative - you describe what should exist, and the engine handles when to draw it.

## Try This

1. Change the text color to yellow: `mcrfpy.Color(255, 255, 0)`
2. Add a second Caption below the first one
3. Change the window position by adjusting the `pos` tuple
4. Try different font sizes to see how text scales

## What is Next

In Part 1, we will create a Grid and place a player Entity that responds to keyboard input. You will learn:

- How to create a tile-based game world
- How to use textures for sprite graphics
- How to handle keyboard input
- The difference between grid coordinates and pixel coordinates

[Continue to Part 1: The '@' and the Dungeon Grid](part_01_grid_movement.md)
