---
layout: default
title: Quickstart
mcrf:
  objects: [Scene, Texture, Grid, TileLayer, Entity, Frame, Caption, Color, Font, Key, InputState, MouseButton, Behavior]
  diataxis: tutorial
  disposition: current
  verified: "0.2.9-dev"
  verified_commit: b6720f6
---

# Quickstart Guide

Get McRogueFace running and make your first changes in minutes.

## Get Started in 5 Minutes

This guide will have you running games and making changes in just a few minutes. No compilation needed!

**⚠️ Caution:** McRogueFace is in *Alpha Pre-Release* - the API may change, hopefully for the better. Download the source code or clone the repository to review the complete documentation in the `/docs` directory, and check back frequently for updates.

### 1. Download McRogueFace

1. Go to the [releases page](https://github.com/jmccardle/McRogueFace/releases)
2. Download the right version for your system. The newest published build is **0.2.7-prerelease-7drl2026**:
   - **Windows**: [McRogueFace-0.2.7-prerelease-7drl2026-Windows-full.zip](https://github.com/jmccardle/McRogueFace/releases/download/0.2.7-prerelease-7drl2026/McRogueFace-0.2.7-prerelease-7drl2026-Windows-full.zip)
   - **Linux**: [McRogueFace-0.2.7-prerelease-7drl2026-Linux-full.tar.gz](https://github.com/jmccardle/McRogueFace/releases/download/0.2.7-prerelease-7drl2026/McRogueFace-0.2.7-prerelease-7drl2026-Linux-full.tar.gz)
   - **Browser (WebAssembly)**: [McRogueFace-0.2.7-prerelease-7drl2026-WASM.zip](https://github.com/jmccardle/McRogueFace/releases/download/0.2.7-prerelease-7drl2026/McRogueFace-0.2.7-prerelease-7drl2026-WASM.zip) - host the extracted files with any static web server
3. Extract the archive to a folder (e.g., `C:\Games\McRogueFace` or `~/McRogueFace`)

Newer builds may appear on the releases page after this guide was written - grab the most recent one. The code on this page tracks the current engine API.

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

McRogueFace automatically runs `scripts/game.py` on startup. The demo game is already running when you start McRogueFace.

To see a simpler example, you can replace `scripts/game.py` with:

```python
import mcrfpy

# Create a scene
scene = mcrfpy.Scene("test")

# Load a texture (sprite sheet of 16x16 tiles)
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create a grid for tile-based graphics
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture,
                   pos=(10, 10), size=(800, 600))

# Add a tile layer and fill it with floor tiles (sprite index 0)
terrain = mcrfpy.TileLayer(name="terrain", z_index=-1, texture=texture)
grid.add_layer(terrain)
terrain.fill(0)

# Add the grid to the scene
scene.children.append(grid)

# Add keyboard controls
def move_around(key, state):
    if state == mcrfpy.InputState.PRESSED:
        print(f"You pressed {key.name}")

scene.on_key = move_around

# Activate the scene
scene.activate()
```

Save and run McRogueFace again to see your simple scene!

A few things to notice:

- **Scenes** are containers for your game states. Create one with `mcrfpy.Scene("name")` and make it visible with `scene.activate()`.
- **Keyboard handlers** receive two enums: a `mcrfpy.Key` (like `Key.W` or `Key.ESCAPE`) and a `mcrfpy.InputState` (`PRESSED` or `RELEASED`).
- **Tile graphics live on layers.** A `TileLayer` stores a sprite index per cell; a negative `z_index` draws it underneath entities.

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
title = mcrfpy.Caption(pos=(312, 100), font=font, text="My Awesome Game",
                       fill_color=mcrfpy.Color(255, 255, 100))
title.font_size = 48
title.outline = 2
title.outline_color = mcrfpy.Color(0, 0, 0)
scene.children.append(title)

# Create a button using Frame + Caption + click handler
button_frame = mcrfpy.Frame(pos=(362, 300), size=(300, 80),
                            fill_color=mcrfpy.Color(50, 150, 50))
button_caption = mcrfpy.Caption(pos=(90, 25), font=font, text="Start Game",
                                fill_color=mcrfpy.Color(255, 255, 255))
button_caption.font_size = 24
button_frame.children.append(button_caption)

# Click handler: receives (pos: Vector, button: MouseButton, action: InputState)
def start_game(pos, button, action):
    if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
        print("Starting the game!")
        game_scene = mcrfpy.Scene("game")
        game_scene.activate()

button_frame.on_click = start_game
scene.children.append(button_frame)

# Activate the menu scene
scene.activate()
```

Save and run - you now have a custom main menu with a working button!

### 5. Add Game Entities

Entities in McRogueFace can be NPCs, enemies, or interactive objects. They live on a grid and have a logical cell position (`grid_pos`), separate from the pixel position used for drawing:

```python
import mcrfpy

# Create a scene and load resources
scene = mcrfpy.Scene("game")
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create a grid
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture,
                   pos=(10, 10), size=(640, 480))
grid.zoom = 2.0
scene.children.append(grid)

# Terrain: floor everywhere, walls around the edges
FLOOR, WALL = 0, 3
terrain = mcrfpy.TileLayer(name="terrain", z_index=-1, texture=texture)
grid.add_layer(terrain)
for y in range(15):
    for x in range(20):
        if x == 0 or x == 19 or y == 0 or y == 14:
            terrain.set((x, y), WALL)
            grid.at(x, y).walkable = False
        else:
            terrain.set((x, y), FLOOR)
            grid.at(x, y).walkable = True

# Add the player entity
player = mcrfpy.Entity(grid_pos=(10, 7), texture=texture, sprite_index=85)
grid.entities.append(player)

# Add an NPC entity
npc = mcrfpy.Entity(grid_pos=(5, 5), texture=texture, sprite_index=109)
grid.entities.append(npc)

# Add a treasure chest
treasure = mcrfpy.Entity(grid_pos=(15, 10), texture=texture, sprite_index=89)
grid.entities.append(treasure)

# Basic movement with keyboard and collision checking
def handle_keys(key, state):
    if state != mcrfpy.InputState.PRESSED:
        return
    x, y = player.grid_x, player.grid_y
    if key == mcrfpy.Key.W or key == mcrfpy.Key.UP:
        y -= 1
    elif key == mcrfpy.Key.S or key == mcrfpy.Key.DOWN:
        y += 1
    elif key == mcrfpy.Key.A or key == mcrfpy.Key.LEFT:
        x -= 1
    elif key == mcrfpy.Key.D or key == mcrfpy.Key.RIGHT:
        x += 1
    if grid.at(x, y).walkable:
        player.grid_pos = (x, y)

scene.on_key = handle_keys
scene.activate()
```

**Note:** grid cells start with `walkable = False`. Set walkability yourself when you build your map - it's what both your collision checks and the engine's pathfinding use.

### 6. Let the World Take Turns

McRogueFace has a built-in turn manager: give entities a behavior with `set_behavior()`, then call `grid.step()` to advance the whole world one turn. Here the guard patrols one cell per player move:

```python
import mcrfpy

scene = mcrfpy.Scene("game")
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture,
                   pos=(10, 10), size=(640, 480))
scene.children.append(grid)

# Open floor so everyone can move (cells start walkable=False!)
terrain = mcrfpy.TileLayer(name="terrain", z_index=-1, texture=texture)
grid.add_layer(terrain)
terrain.fill(0)
for y in range(15):
    for x in range(20):
        grid.at(x, y).walkable = True

player = mcrfpy.Entity(grid_pos=(10, 7), texture=texture, sprite_index=85)
grid.entities.append(player)

# A guard that patrols between waypoints, one cell per turn
guard = mcrfpy.Entity(grid_pos=(3, 3), texture=texture, sprite_index=109)
grid.entities.append(guard)
guard.set_behavior(mcrfpy.Behavior.PATROL,
                   waypoints=[(3, 3), (16, 3), (16, 11), (3, 11)])

def handle_keys(key, state):
    if state != mcrfpy.InputState.PRESSED:
        return
    x, y = player.grid_x, player.grid_y
    if key == mcrfpy.Key.W:
        y -= 1
    elif key == mcrfpy.Key.S:
        y += 1
    elif key == mcrfpy.Key.A:
        x -= 1
    elif key == mcrfpy.Key.D:
        x += 1
    else:
        return
    player.grid_pos = (x, y)
    grid.step()  # the world takes a turn every time the player moves

scene.on_key = handle_keys
scene.activate()
```

Other built-in behaviors include `Behavior.SEEK` (chase a target with pathfinding), `Behavior.FLEE`, `Behavior.PATH`, and random wandering with `Behavior.NOISE4`/`NOISE8`. Set `entity.step` to a callback receiving `(trigger, data)` to react when a behavior finishes, gets blocked, or spots a target - see the [API Reference](https://mcrogueface.github.io/reference/generated/Trigger) for the `Trigger` enum.

### 7. Load a Custom Sprite Sheet

Want to use your own graphics? Here's how:

```python
import mcrfpy

# Create a scene
scene = mcrfpy.Scene("game")

# Load your sprite sheet (tile width, tile height)
my_texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create a grid using your texture
grid = mcrfpy.Grid(grid_size=(20, 15), texture=my_texture,
                   pos=(10, 10), size=(640, 480))

# Add a tile layer for terrain graphics
terrain = mcrfpy.TileLayer(name="terrain", z_index=-1, texture=my_texture)
grid.add_layer(terrain)

# Set specific tiles by sprite index
terrain.fill(0)             # floor everywhere
terrain.set((5, 5), 10)     # tree sprite at index 10
terrain.set((6, 5), 11)     # rock sprite at index 11

# Walkability lives on the grid cells, separate from the graphics
grid.at(6, 5).walkable = False  # make the rock solid

# Add the grid to the scene
scene.children.append(grid)

# Activate the scene
scene.activate()
```

Tips for sprite sheets:
- Use consistent tile sizes (16x16, 32x32, etc.)
- Sprites are indexed left-to-right, top-to-bottom starting at 0
- PNG format with transparency works best
- Use `terrain.set((x, y), -1)` to make a cell transparent, and `fill_rect()` for rectangular regions
- For fast bulk edits (e.g., with NumPy), `TileLayer.edit()` yields a writable buffer view - see the [API Reference](https://mcrogueface.github.io/reference)

## Building From Source

Most users don't need this - the pre-built releases above cover Windows, Linux, and WebAssembly. Build from source if you're on an unsupported platform, want the latest unreleased code, or plan to extend the C++ engine itself.

**Prerequisites:** CMake 3.14+, a C++17 compiler (GCC/Clang/MSVC), and SFML 2.6 development libraries. The build vendors its own Python runtime (no separate Python install needed).

```bash
git clone https://github.com/jmccardle/McRogueFace.git
cd McRogueFace
make            # from the project root - never from build/
```

The executable is `build/mcrogueface`; run it from that directory (`./mcrogueface`) so it finds `assets/` and `scripts/` alongside it. See the repository's `CLAUDE.md` and `BUILD_FROM_SOURCE.md` for platform-specific dependency lists (including Windows cross-compilation) and troubleshooting.

## What's Next?

### Learn by Doing
- **[McRogueFace Does The Entire Roguelike Tutorial](https://mcrogueface.github.io/tutorials)** - Build a complete game step-by-step
- **[Cookbook](https://mcrogueface.github.io/cookbook)** - Copy/paste solutions for common tasks

### Reference Material
- **[Complete API Reference](https://mcrogueface.github.io/reference)** - Every function and class documented

### Advanced Topics
- **[C++ Extension Guide](https://mcrogueface.github.io/extending-cpp)** - Add new engine features (requires compilation)

## Troubleshooting

### "mcrogueface: command not found"
You need to be in the McRogueFace directory, or add it to your PATH.

### "No module named mcrfpy"
Make sure you're running `mcrogueface`, not `python`. McRogueFace is a complete Python environment.

### Black screen on startup
Check that the `assets/` and `scripts/` folders are in the same directory as the mcrogueface executable.

### Entities won't move / pathfinding does nothing
Grid cells start with `walkable = False`. Set `grid.at(x, y).walkable = True` for every cell that should be passable when you build your map.

### No tiles are drawn
Tile graphics come from a `TileLayer` - create one, `grid.add_layer()` it, and set sprite indices with `fill()` or `set()`. A grid with no layers only draws its entities.

### Can't load my sprites
- Pass your actual tile size to `mcrfpy.Texture(path, tile_width, tile_height)`
- Use PNG format with transparency
- Check the file path is relative to the mcrogueface executable

## Get Help

- **Documentation**: Check the [API Reference](https://mcrogueface.github.io/reference) and [Cookbook](https://mcrogueface.github.io/cookbook)
- **Source Code**: Browse the [GitHub repository](https://github.com/jmccardle/McRogueFace) for implementation details

---
