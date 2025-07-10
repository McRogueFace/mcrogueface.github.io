# McRogueFace Quick Reference

A handy cheat sheet for common McRogueFace operations.

## Scene Management

```python
# Create and switch scenes
mcrfpy.createScene("menu")
mcrfpy.setScene("menu")
current = mcrfpy.currentScene()

# Get UI elements for current scene
ui = mcrfpy.sceneUI("menu")
ui.append(element)
```

## UI Elements

### Caption (Text)
```python
text = mcrfpy.Caption((x, y), "Hello World")
text.font = mcrfpy.default_font
text.font_size = 24
text.font_color = (255, 255, 255)  # RGB
text.centered = True
text.pos = (new_x, new_y)  # Reposition
```

### Sprite
```python
texture = mcrfpy.Texture("sprites.png", 16, 16)
sprite = mcrfpy.Sprite(x, y)
sprite.texture = texture
sprite.sprite_index = 0
sprite.scale = (2.0, 2.0)
sprite.pos = (new_x, new_y)
```

### Frame (Container)
```python
frame = mcrfpy.Frame(x, y, width, height)
frame.bgcolor = (64, 64, 128)
frame.outline = 2
frame.outline_color = (255, 255, 255)
frame.children.append(caption)  # Add child elements
```

### Grid (Tilemap)
```python
grid = mcrfpy.Grid(x, y, cols, rows, texture, tile_w, tile_h)
grid.set_tile(tile_x, tile_y, sprite_index)
tile_index = grid.get_tile(tile_x, tile_y)
grid.entities.append(entity)  # Add entities
```

### Entity
```python
entity = mcrfpy.Entity(grid_x, grid_y)
entity.texture = texture
entity.sprite_index = 84
entity.pos = (new_x, new_y)  # Move entity
index = entity.index()  # Get position in collection
```

## Collections

```python
# UICollection (for UI elements)
ui = mcrfpy.sceneUI("scene_name")
ui.append(element)
ui.remove(element)
for element in ui:
    print(element)

# EntityCollection (for entities in grids)
entities = grid.entities
entities.append(entity)
entities.extend([e1, e2, e3])  # Add multiple
entities.remove(entity)
```

## Input Handling

```python
def on_key(key):
    if key == "w" or key == "Up":
        player.move_up()
    elif key == "Escape":
        mcrfpy.exit()

mcrfpy.keypressScene(on_key)
```

## Timers

```python
def update(runtime):
    # Called every 100ms
    # runtime is total seconds since start
    player.update(0.1)

# Start timer
mcrfpy.setTimer("game_loop", update, 100)

# Stop timer
mcrfpy.delTimer("game_loop")
```

## Audio

```python
# Sound effects
mcrfpy.createSoundBuffer("explosion.ogg")
mcrfpy.playSound(0)  # Play first loaded sound
mcrfpy.setSoundVolume(80.0)

# Music
mcrfpy.loadMusic("theme.ogg", loop=True)
mcrfpy.setMusicVolume(50)
```

## Common Patterns

### Game Loop
```python
def game_update(runtime):
    # Update logic
    player.update()
    enemies.update()
    check_collisions()

mcrfpy.setTimer("main", game_update, 16)  # ~60 FPS
```

### Scene Transitions
```python
def to_menu():
    mcrfpy.setScene("menu")
    mcrfpy.delTimer("game_loop")
    mcrfpy.setTimer("menu_loop", menu_update, 100)
```

### Entity Movement
```python
# Grid-based movement
entity.pos = (entity.pos[0] + dx, entity.pos[1] + dy)

# Check grid bounds
if 0 <= new_x < grid.grid_x and 0 <= new_y < grid.grid_y:
    entity.pos = (new_x, new_y)
```

### Click Handling
```python
def on_click(x, y, btn, type):
    if btn == "left" and type == "start":
        print(f"Clicked at {x}, {y}")

sprite.click_callable = on_click
```

## Automation API

```python
from mcrfpy import automation

# Screenshots
automation.screenshot("game.png")

# Mouse control
automation.click(x, y)
automation.moveTo(x, y)
automation.dragTo(x, y)

# Keyboard
automation.typewrite("Hello")
automation.keyDown("shift")
automation.keyUp("shift")
automation.hotkey("ctrl", "s")
```

## Color/Vector Helpers

```python
# Colors can be tuples
color = (255, 0, 0)  # Red
frame.bgcolor = color

# Vectors can be tuples or Vector objects
pos = (100, 200)
vec = mcrfpy.Vector(100, 200)
```

## Window Control

```python
# Exit game
mcrfpy.exit()

# Change window scale
mcrfpy.setScale(2.0)  # 2x window size
```

## Tips

1. **Always use timers** for game loops and animations
2. **Check texture paths** - they're relative to the executable
3. **Scene names are global** - use consistent naming
4. **Entities need a grid** - add to grid.entities collection
5. **Use default resources** - mcrfpy.default_font and default_texture
6. **Test with automation** - great for regression testing

## Common Issues

- **No text showing**: Ensure font is loaded (use mcrfpy.default_font)
- **Sprite not visible**: Check texture path and sprite_index bounds
- **Entity not moving**: Ensure it's in a grid's entity collection
- **Timer not firing**: Check scene is active and timer name is unique
- **Click not working**: Assign click_callable to the UI element
