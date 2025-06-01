# API Reference

## mcrfpy Module

The `mcrfpy` module is your interface to the McRogueFace engine. Import it to access all engine functionality:

```python
import mcrfpy
```

## Global Functions

### Scene Management

#### `createScene(name: str) -> None`
Creates a new empty scene.
```python
mcrfpy.createScene("game")
```

#### `setScene(name: str) -> None`
Switches to a different scene. The scene must exist.
```python
mcrfpy.setScene("game")
```

#### `currentScene() -> str`
Returns the name of the currently active scene.
```python
scene_name = mcrfpy.currentScene()
```

#### `sceneUI(name: str) -> UICollection`
Returns the UICollection containing all UI elements in the specified scene.
```python
ui = mcrfpy.sceneUI("game")
```

### Audio System

#### `createSoundBuffer(filename: str) -> int`
Loads a sound file and returns its buffer index.
```python
explosion_sound = mcrfpy.createSoundBuffer("assets/explosion.wav")
```

#### `playSound(buffer_index: int) -> None`
Plays a sound effect by its buffer index.
```python
mcrfpy.playSound(explosion_sound)
```

#### `loadMusic(filename: str) -> None`
Loads and plays background music. Music loops by default.
```python
mcrfpy.loadMusic("assets/dungeon_theme.ogg")
```

#### `setMusicVolume(volume: int) -> None`
Sets music volume (0-100).
```python
mcrfpy.setMusicVolume(75)
```

#### `setSoundVolume(volume: int) -> None`
Sets sound effects volume (0-100).
```python
mcrfpy.setSoundVolume(80)
```

### Input Handling

#### `keypressScene(callback: callable) -> None`
Sets a function to handle keyboard input for the current scene.
```python
def on_key(key_code):
    print(f"Key pressed: {key_code}")
    
mcrfpy.keypressScene(on_key)
```

#### `registerPyAction(action: str, callback: callable) -> None`
Registers a named action that can be triggered by input.
```python
def jump():
    player.pos = (player.pos[0], player.pos[1] - 2)
    
mcrfpy.registerPyAction("jump", jump)
```

#### `registerInputAction(input_code: int, action: str) -> None`
Maps an input code to a named action.
```python
mcrfpy.registerInputAction(32, "jump")  # Spacebar triggers jump
```

### Timers

#### `setTimer(name: str, callback: callable, interval_ms: int) -> None`
Creates a timer that calls a function repeatedly.
```python
def spawn_enemy():
    # Spawn logic here
    pass
    
mcrfpy.setTimer("enemy_spawner", spawn_enemy, 5000)  # Every 5 seconds
```

#### `delTimer(name: str) -> None`
Removes a timer.
```python
mcrfpy.delTimer("enemy_spawner")
```

### System

#### `exit() -> None`
Closes the game window and exits.
```python
mcrfpy.exit()
```

#### `setScale(multiplier: float) -> None`
Resizes the game window. Multiplier must be between 0.2 and 4.0.
```python
mcrfpy.setScale(2.0)  # Double size
```

## Types

### Color

RGBA color representation.

#### Constructor
```python
# From separate values
color = mcrfpy.Color(255, 128, 0)  # Orange
color = mcrfpy.Color(255, 128, 0, 200)  # Semi-transparent orange

# From tuple
color = mcrfpy.Color((255, 128, 0))
color = mcrfpy.Color((255, 128, 0, 200))
```

#### Properties
- `r` (int): Red component (0-255)
- `g` (int): Green component (0-255)
- `b` (int): Blue component (0-255)
- `a` (int): Alpha component (0-255, default 255)

### Vector

2D vector for positions and sizes.

#### Constructor
```python
# From separate values
vec = mcrfpy.Vector(100, 200)

# From tuple
vec = mcrfpy.Vector((100, 200))

# Default (0, 0)
vec = mcrfpy.Vector()
```

#### Properties
- `x` (float): X component
- `y` (float): Y component

### Font

Font for text rendering.

#### Constructor
```python
font = mcrfpy.Font("assets/custom_font.ttf")
```

### Texture

Sprite sheet with fixed-size sprites.

#### Constructor
```python
# Load texture with 16x16 sprites
texture = mcrfpy.Texture("assets/sprites.png", 16, 16)
```

### Grid

Tile-based game world with camera controls.

#### Constructor
```python
grid = mcrfpy.Grid(
    50, 40,                    # Grid dimensions (tiles)
    texture,                   # Texture for rendering
    (0, 0),                   # Screen position
    (800, 600)                # Display size (pixels)
)
```

#### Properties
- `grid_size` (tuple): Grid dimensions as (width, height)
- `position` (Vector): Screen position
- `size` (Vector): Display size in pixels
- `center` (tuple): Camera center position in grid coordinates
- `zoom` (float): Camera zoom level
- `texture` (Texture): Texture used for rendering
- `children` (UIEntityCollection): Entities on this grid
- `click` (callable): Click handler function

#### Methods
- `at(index: int) -> GridPoint`: Get GridPoint at linear index

#### Click Handler
```python
def on_grid_click(x, y, button, action):
    # x, y are grid coordinates (not pixels)
    # button: 0=left, 1=right, 2=middle
    # action: 0=pressed, 1=released
    print(f"Clicked grid at ({x}, {y})")
    
grid.click = on_grid_click
```

### GridPoint

Individual tile in a Grid.

#### Properties
- `color` (Color): Base color tint
- `color_overlay` (Color): Overlay color
- `walkable` (bool): Can entities walk here?
- `transparent` (bool): Can we see through this?
- `tilesprite` (int): Base tile sprite index
- `tile_overlay` (int): Overlay sprite index (-1 for none)
- `uisprite` (int): UI layer sprite index (-1 for none)

### Entity

Game object that exists on a Grid.

#### Constructor
```python
entity = mcrfpy.Entity(grid)  # Must provide parent grid
```

#### Properties
- `pos` (tuple): Grid position as (x, y) integers
- `draw_pos` (tuple): Smooth position for animation as (x, y) floats
- `sprite_number` (int): Sprite index to display
- `gridstate` (list): List of GridPointState objects for FOV

#### Methods
- `at(grid_pos: tuple) -> GridPointState`: Get visibility state at position

### Frame

UI container that can hold other elements.

#### Constructor
```python
frame = mcrfpy.Frame(10, 10, 200, 150)  # x, y, width, height
```

#### Properties
- `x` (float): X position
- `y` (float): Y position
- `w` (float): Width
- `h` (float): Height
- `outline` (int): Border thickness in pixels
- `fill_color` (Color): Background color
- `outline_color` (Color): Border color
- `children` (UICollection): Child UI elements
- `click` (callable): Click handler

### Caption

Text display element.

#### Constructor
```python
# With default font
caption = mcrfpy.Caption("Hello World")

# With custom font
caption = mcrfpy.Caption("Hello World", custom_font)
```

#### Properties
- `text` (str): Text to display
- `x` (float): X position
- `y` (float): Y position
- `pos` (Vector): Position as vector
- `fill_color` (Color): Text color
- `outline_color` (Color): Text outline color
- `click` (callable): Click handler

### Sprite

Single sprite display element.

#### Constructor
```python
sprite = mcrfpy.Sprite(
    texture,           # Texture to use
    sprite_index,      # Which sprite in the texture
    (100, 100),       # Position
    2.0               # Scale (optional, default 1.0)
)
```

#### Properties
- `x` (float): X position
- `y` (float): Y position
- `scale` (float): Size multiplier
- `sprite_number` (int): Sprite index in texture
- `texture` (Texture): Source texture
- `click` (callable): Click handler

### UICollection

Container for UI elements (Frame, Caption, Sprite, Grid).

#### Methods
- `append(element)`: Add a UI element
- `remove(element)`: Remove a UI element

#### Iteration
```python
for element in ui_collection:
    print(element)
```

### UIEntityCollection

Container for Entity objects on a Grid.

#### Methods
- `append(entity)`: Add an entity
- `remove(entity)`: Remove an entity

#### Iteration
```python
for entity in grid.children:
    print(f"Entity at {entity.pos}")
```

## Module Attributes

### `default_font`
The default font (JetbrainsMono.ttf) loaded automatically.
```python
caption = mcrfpy.Caption("Text", mcrfpy.default_font)
```

### `default_texture`
The default texture (kenney_tinydungeon.png) with 16x16 sprites.
```python
grid = mcrfpy.Grid(50, 50, mcrfpy.default_texture, (0, 0), (800, 600))
```

## Common Patterns

### Setting Click Handlers
All visible elements support click handlers:
```python
def handle_click(x, y, button, action):
    # x, y: coordinates (screen for UI, grid for Grid)
    # button: 0=left, 1=right, 2=middle
    # action: 0=pressed, 1=released
    pass

element.click = handle_click
```

### Entity Movement
```python
# Instant movement
entity.pos = (new_x, new_y)

# Smooth movement (interpolate draw_pos)
entity.draw_pos = (float(new_x), float(new_y))
```

### Layering UI Elements
Elements are drawn in the order they appear in collections:
```python
ui.append(background)  # Drawn first
ui.append(midground)   # Drawn second
ui.append(foreground)  # Drawn last (on top)
```