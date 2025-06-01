# Quick Reference

## Essential Imports
```python
import mcrfpy
```

## Scene Setup
```python
mcrfpy.createScene("game")
mcrfpy.setScene("game")
ui = mcrfpy.sceneUI("game")
```

## Creating a Grid World
```python
grid = mcrfpy.Grid(
    50, 40,                      # Grid size (tiles)
    mcrfpy.default_texture,      # Texture
    (0, 0),                      # Position
    (800, 600)                   # Display size
)
ui.append(grid)
```

## Working with Tiles
```python
# Get a tile
tile = grid.at(x + y * grid_width)

# Set tile properties
tile.tilesprite = 46        # Sprite index
tile.walkable = True        # Can walk on it
tile.transparent = True     # Can see through it
tile.color = mcrfpy.Color(255, 255, 255)
```

## Creating Entities
```python
player = mcrfpy.Entity(grid)
player.pos = (10, 10)
player.sprite_number = 5
grid.children.append(player)
```

## Keyboard Input
```python
def on_key(key):
    # WASD: 119, 97, 115, 100
    # Arrow keys: 273, 274, 275, 276
    # Space: 32, Escape: 27
    if key == 119:  # W
        player.pos = (player.pos[0], player.pos[1] - 1)

mcrfpy.keypressScene(on_key)
```

## UI Elements

### Frame (Container)
```python
frame = mcrfpy.Frame(x, y, width, height)
frame.fill_color = mcrfpy.Color(50, 50, 50)
frame.outline = 2
frame.outline_color = mcrfpy.Color(255, 255, 255)
ui.append(frame)
```

### Caption (Text)
```python
text = mcrfpy.Caption("Hello World", mcrfpy.default_font)
text.pos = (100, 100)
text.fill_color = mcrfpy.Color(255, 255, 255)
frame.children.append(text)
```

### Sprite (Image)
```python
sprite = mcrfpy.Sprite(texture, sprite_index, (x, y), scale)
ui.append(sprite)
```

## Click Handlers
```python
def on_click(x, y, button, action):
    # x, y: coordinates
    # button: 0=left, 1=right, 2=middle
    # action: 0=pressed, 1=released
    print(f"Clicked at {x},{y}")

element.click = on_click
```

## Audio
```python
# Sound effects
boom = mcrfpy.createSoundBuffer("boom.wav")
mcrfpy.playSound(boom)
mcrfpy.setSoundVolume(80)

# Music
mcrfpy.loadMusic("theme.ogg")
mcrfpy.setMusicVolume(60)
```

## Timers
```python
def update():
    # Called every 100ms
    pass

mcrfpy.setTimer("update", update, 100)
mcrfpy.delTimer("update")  # Stop it
```

## Common Key Codes
```
W: 119    A: 97     S: 115    D: 100
↑: 273    ←: 276    ↓: 274    →: 275
Space: 32           Enter: 13
Escape: 27          Tab: 9
0-9: 48-57          a-z: 97-122
```

## Grid Coordinate Conversion
```python
# Convert (x,y) to index
index = x + y * grid_width

# Convert index to (x,y)
x = index % grid_width
y = index // grid_width
```

## Camera Control
```python
# Center camera on position
grid.center = (x, y)

# Zoom in/out
grid.zoom = 2.0  # 2x zoom
```

## Color Presets
```python
BLACK = mcrfpy.Color(0, 0, 0)
WHITE = mcrfpy.Color(255, 255, 255)
RED = mcrfpy.Color(255, 0, 0)
GREEN = mcrfpy.Color(0, 255, 0)
BLUE = mcrfpy.Color(0, 0, 255)
GRAY = mcrfpy.Color(128, 128, 128)
```

## Performance Tips
- Keep entities under 100 for smooth performance
- Update multiple tiles in one loop
- Use timers sparingly (< 10 active)
- Entities on same Grid are automatically batched