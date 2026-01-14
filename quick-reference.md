# McRogueFace Quick Reference

A handy cheat sheet for common McRogueFace operations.

## Scene Management

```python
# Create and activate scenes (modern API)
scene = mcrfpy.Scene("menu")
scene.activate()
current = mcrfpy.currentScene()

# Access scene UI elements
scene.children.append(element)

# Set input handler on scene
scene.on_key = on_key
```

## UI Elements

### Caption (Text)
```python
caption = mcrfpy.Caption(text="Hello World", pos=(x, y))
caption.font = mcrfpy.default_font
caption.font_size = 24
caption.fill_color = mcrfpy.Color(255, 255, 255)
caption.pos = (new_x, new_y)  # Reposition
```

### Sprite
```python
texture = mcrfpy.Texture("sprites.png", 16, 16)
sprite = mcrfpy.Sprite(pos=(x, y), texture=texture, sprite_index=0)
sprite.scale = (2.0, 2.0)
sprite.pos = (new_x, new_y)
```

### Frame (Container)
```python
frame = mcrfpy.Frame(pos=(x, y), size=(width, height))
frame.fill_color = mcrfpy.Color(64, 64, 128)
frame.outline = 2
frame.outline_color = mcrfpy.Color(255, 255, 255)
frame.children.append(caption)  # Add child elements

# Alignment (NEW!)
frame.align = mcrfpy.Alignment.CENTER  # Auto-position in parent
frame.margin = 10.0  # Offset from edge
```

### Grid (Tilemap)
```python
grid = mcrfpy.Grid(grid_size=(cols, rows), texture=texture, pos=(x, y), size=(w, h))
cell = grid.at(tile_x, tile_y)
cell.tilesprite = sprite_index
cell.walkable = True
cell.transparent = True
grid.entities.append(entity)  # Add entities
```

### Entity
```python
entity = mcrfpy.Entity(pos=(grid_x, grid_y), texture=texture, sprite_index=84)
entity.x, entity.y = new_x, new_y  # Move entity
grid.entities.append(entity)
```

## Collections

```python
# Scene children (modern API)
scene = mcrfpy.Scene("game")
scene.children.append(element)
scene.children.remove(element)
for element in scene.children:
    print(element)

# EntityCollection (for entities in grids)
entities = grid.entities
entities.append(entity)
entities.remove(entity)
```

## Input Handling

```python
def on_key(key, state):
    if state != "start":  # Ignore key release
        return
    if key == "W" or key == "Up":
        move_player(0, -1)
    elif key == "Escape":
        mcrfpy.exit()

scene.on_key = on_key
```

## Timers

```python
def update(timer, runtime):
    # timer: the Timer object
    # runtime: total seconds since start
    player.update()

# Create timer (interval in seconds)
timer = mcrfpy.Timer("game_loop", update, 0.1)  # 100ms = 0.1s

# Cancel timer
timer.cancel()
```

## Headless Mode & Testing

```python
# Advance simulation time (for testing)
mcrfpy.step(0.1)  # Advance by 0.1 seconds

# Screenshots (synchronous in headless)
from mcrfpy import automation
automation.screenshot("game.png")
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
scene = mcrfpy.Scene("game")
scene.activate()

def game_update(timer, runtime):
    update_player()
    update_enemies()
    check_collisions()

timer = mcrfpy.Timer("main", game_update, 0.016)  # ~60 FPS
```

### Scene Transitions
```python
menu_scene = mcrfpy.Scene("menu")
game_scene = mcrfpy.Scene("game")

def start_game():
    game_scene.activate()

def return_to_menu():
    menu_scene.activate()
```

### Grid Movement with Collision
```python
def move_player(dx, dy):
    new_x = int(player.x) + dx
    new_y = int(player.y) + dy

    if grid.at(new_x, new_y).walkable:
        player.x, player.y = new_x, new_y
        grid.center = (player.x, player.y)
```

### Click Handling
```python
def on_click(x, y, btn, action):
    if btn == "left" and action == "start":
        print(f"Clicked at {x}, {y}")

frame.click = on_click
```

## Pathfinding & FOV

```python
# Field of View
grid.compute_fov(player.x, player.y, radius=10)
if grid.is_in_fov(enemy.x, enemy.y):
    print("Enemy visible!")

# A* Pathfinding
path = grid.compute_astar(start_x, start_y, end_x, end_y)

# Dijkstra Maps (NEW!)
dijkstra = grid.get_dijkstra_map((source_x, source_y))
distance = dijkstra.distance((target_x, target_y))
heightmap = dijkstra.to_heightmap()  # For procgen!
```

## Animation

```python
# Animate any property
anim = mcrfpy.Animation("x", target=200.0, duration=1.0, easing="easeInOut")
anim.start(frame)

# With callback
def on_complete(anim, target):
    print("Animation done!")

anim = mcrfpy.Animation("opacity", 0.0, 0.5, "easeOut", callback=on_complete)
anim.start(element)
```

## Alignment System (NEW!)

```python
# Auto-position elements in their parent
child.align = mcrfpy.Alignment.CENTER      # Centered
child.align = mcrfpy.Alignment.TOP_LEFT    # Corner with margin
child.align = mcrfpy.Alignment.BOTTOM_RIGHT
child.margin = 10.0  # Offset from edge

# Alignment values: TOP_LEFT, TOP_CENTER, TOP_RIGHT,
#                   CENTER_LEFT, CENTER, CENTER_RIGHT,
#                   BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT
```

## Color Helper

```python
# Use mcrfpy.Color for colors
red = mcrfpy.Color(255, 0, 0)
transparent_blue = mcrfpy.Color(0, 0, 255, 128)  # RGBA

frame.fill_color = red
caption.fill_color = mcrfpy.Color(255, 255, 255)
```

## Tips

1. **Use `mcrfpy.Scene()`** - modern API with `scene.children` and `scene.on_key`
2. **Timer callbacks take `(timer, runtime)`** - not just runtime
3. **Use `mcrfpy.step()`** for testing - advances simulation time instantly
4. **Alignment auto-updates** - child repositions when parent resizes
5. **Grid.at() returns a cell** - set `tilesprite`, `walkable`, `transparent`
6. **Dijkstra.to_heightmap()** - great for procgen and visualization

## Common Issues

- **Scene not showing**: Call `scene.activate()` after creating
- **Timer not firing**: Check callback signature is `(timer, runtime)`
- **Alignment not working**: Element must be added to parent's `children`
- **Key handler not working**: Use `scene.on_key = handler`, not old API
- **Colors look wrong**: Use `mcrfpy.Color()`, not tuples
