---
layout: default
title: Quick Reference
mcrf:
  objects: [Scene, Caption, Sprite, Frame, Grid, Entity, Timer, Color, Alignment, DijkstraMap]
  diataxis: reference
  disposition: current
  verified: "0.2.9-dev"
  verified_commit: b6720f6
---

# McRogueFace Quick Reference

A handy cheat sheet for common McRogueFace operations. Every snippet on this page runs against the current engine.

## Scene Management

```python
# Create and activate scenes
scene = mcrfpy.Scene("menu")
scene.activate()
current = mcrfpy.current_scene  # property, not a function

# Access scene UI elements
scene.children.append(element)

# Set input handler on scene
scene.on_key = on_key
```

## UI Elements

### Caption (Text)
```python
caption = mcrfpy.Caption(text="Hello World", pos=(100, 100))
caption.font_size = 24
caption.fill_color = mcrfpy.Color(255, 255, 255)
caption.pos = (120, 140)  # Reposition

# font is read-only after construction - pass it up front
styled = mcrfpy.Caption(text="Styled", pos=(10, 10), font=mcrfpy.default_font)
```

### Sprite
```python
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)
sprite = mcrfpy.Sprite(pos=(50, 50), texture=texture, sprite_index=0)
sprite.scale = 2.0  # single float, applies to both axes
sprite.pos = (60, 70)
# scale_x / scale_y exist for non-uniform scaling
```

### Frame (Container)
```python
frame = mcrfpy.Frame(pos=(10, 10), size=(200, 150))
frame.fill_color = mcrfpy.Color(64, 64, 128)
frame.outline = 2
frame.outline_color = mcrfpy.Color(255, 255, 255)
frame.children.append(caption)  # Add child elements

# Alignment: add to parent first, then align
label = mcrfpy.Caption(text="Centered")
frame.children.append(label)
label.align = mcrfpy.Alignment.CENTER  # Auto-position in parent
```

### Grid (Tilemap)
```python
grid = mcrfpy.Grid(grid_size=(20, 15), texture=texture, pos=(0, 0), size=(400, 300))
cell = grid.at(3, 4)      # GridPoint at tile coordinates
cell.walkable = True
cell.transparent = True
grid.entities.append(entity)  # Add entities
```

Tile and color visuals live on **layers**, not on cells:

```python
# Construct a layer standalone, then attach it
ground = mcrfpy.TileLayer(name="ground", z_index=-1, texture=texture)
grid.add_layer(ground)
ground.fill(48)          # every cell -> tile index 48
ground.set((3, 4), 12)   # one cell -> tile index 12
ground.set((5, 5), -1)   # -1 = no tile (transparent)

# ColorLayer for tints, fog, highlights
overlay = mcrfpy.ColorLayer(name="overlay", z_index=1)
grid.add_layer(overlay)
overlay.fill(mcrfpy.Color(0, 0, 0, 0))

# Look layers up later
grid.layers            # tuple sorted by z_index
grid.layer("ground")   # by name

# Or pass layers at construction
grid2 = mcrfpy.Grid(grid_size=(10, 10), texture=texture,
                    layers=[mcrfpy.TileLayer(name="floor", z_index=-1, texture=texture)])
```

Bulk edits go through `layer.edit()` - a context manager yielding a zero-copy
writable memoryview (TileLayer: shape `(height, width)`, int32; ColorLayer:
`(height, width, 4)`, uint8). The layer re-renders when the block exits:

```python
with ground.edit() as view:
    view[4, 3] = 12   # row-major: view[y, x]
    # with numpy installed: np.asarray(view)[...] = 48
```

### Camera

```python
grid.center = (160, 120)        # PIXEL coordinates
grid.center_camera((10.5, 7.5)) # tile coordinates (+0.5 = middle of tile)
grid.zoom = 2.0                 # float magnification
```

### Entity
```python
entity = mcrfpy.Entity(grid_pos=(10, 7), texture=texture, sprite_index=84)
grid.entities.append(entity)
entity.grid_pos = (11, 7)     # logical cell position (also: entity.cell_pos)
entity.labels = {"player"}    # frozenset of str, for collision/targeting
# entity.draw_pos is the fractional render position - animate it for smooth movement
```

## Collections

```python
# Scene children
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

Keyboard handlers receive `Key` and `InputState` **enums**, not strings:

```python
def on_key(key, state):
    if state != mcrfpy.InputState.PRESSED:
        return  # ignore key release
    if key == mcrfpy.Key.W or key == mcrfpy.Key.UP:
        move_player(0, -1)
    elif key == mcrfpy.Key.ESCAPE:
        mcrfpy.exit()

scene.on_key = on_key
```

Mouse handlers attach to drawables via `on_click` (not `click`):

```python
def on_click(pos, button, action):
    # pos: Vector, button: MouseButton, action: InputState
    if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
        print(f"Clicked at {pos.x}, {pos.y}")

frame.on_click = on_click

# Hover callbacks receive only (pos)
frame.on_enter = lambda pos: print("entered")
frame.on_exit = lambda pos: print("left")
frame.on_move = lambda pos: None  # fires every movement - keep it cheap

# Grids get cell-level callbacks in tile coordinates
grid.on_cell_click = lambda cell_pos, button, action: print(cell_pos)
grid.on_cell_enter = lambda cell_pos: None
grid.on_cell_exit = lambda cell_pos: None
```

## Timers

```python
def update(timer, runtime):
    # timer: the Timer object
    # runtime: total elapsed time in MILLISECONDS
    player.update()

# Interval is in milliseconds
timer = mcrfpy.Timer("game_loop", update, 100)   # fires every 100 ms

# One-shot timer
one_shot = mcrfpy.Timer("delayed", update, 500, once=True)

# Control (there is no cancel())
timer.pause()
timer.resume()
timer.stop()      # remove from tick loop, callback preserved
timer.restart()   # start over from the beginning
```

## Animation

There is no `mcrfpy.Animation` constructor - call `.animate()` on the object itself:

```python
# animate(property, target, duration_seconds, easing, ...)
frame.animate("x", 500.0, 2.0, mcrfpy.Easing.EASE_IN_OUT)
frame.animate("opacity", 0.0, 0.5, mcrfpy.Easing.EASE_OUT)

# Completion callback receives (target, property, final_value)
def on_complete(target, prop, value):
    print(f"{type(target).__name__}.{prop} reached {value}")

handle = frame.animate("x", 500.0, 2.0, mcrfpy.Easing.EASE_IN_OUT,
                       callback=on_complete)
```

## Turn Manager

The engine runs turn-based entity behavior natively via `grid.step()`:

```python
# Give an enemy a behavior
to_player = grid.get_dijkstra_map(root=(11, 7))
enemy.set_behavior(mcrfpy.Behavior.SEEK, pathfinder=to_player)

# Waypoint patrol: visit each point, waiting n turns at each
patrol.set_behavior(mcrfpy.Behavior.WAYPOINT, waypoints=[(5, 5), (10, 10)], turns=3)

# Turn order: lower goes first, 0 = skip this entity
enemy.turn_order = 2

# React to behavior events with a step callback
def on_trigger(trigger, data):
    if trigger == mcrfpy.Trigger.DONE:
        print("behavior finished")
    elif trigger == mcrfpy.Trigger.BLOCKED:
        print("path blocked")

enemy.step = on_trigger

# Advance the world
grid.step()     # one round: every entity acts in turn_order
grid.step(n=3)  # three rounds
```

Behaviors include `IDLE`, `SEEK`, `FLEE`, `WAYPOINT`, `PATROL`, `PATH`, `LOOP`,
`NOISE4`, `NOISE8`, `SLEEP`, and `CUSTOM`. Triggers include `DONE`, `BLOCKED`,
and `TARGET`.

## Pathfinding & FOV

```python
# Field of View: position tuple + radius keyword
grid.compute_fov((11, 7), radius=10)
if grid.is_in_fov(int(enemy.cell_x), int(enemy.cell_y)):
    print("Enemy visible!")

# A* pathfinding (returns AStarPath or None)
path = grid.find_path((2, 2), (11, 7))
if path:
    nxt = path.peek()     # look without consuming
    step = path.walk()    # consume one step
    left = path.remaining

# Dijkstra maps (cached per root; cleared with grid.clear_dijkstra_maps())
dijkstra = grid.get_dijkstra_map(root=(11, 7))
dist = dijkstra.distance((2, 2))
next_cell = dijkstra.step_from((2, 2))   # one step toward the root
full_path = dijkstra.path_from((2, 2))   # AStarPath to the root
heightmap = dijkstra.to_heightmap()      # for procgen and visualization
```

## Audio

Audio is class-based - `SoundBuffer`, `Sound`, and `Music` objects:

```python
# Sound effects (short clips)
buf = mcrfpy.SoundBuffer("assets/sfx/splat1.ogg")
sound = mcrfpy.Sound(buf)       # or mcrfpy.Sound("assets/sfx/splat2.ogg")
sound.volume = 80               # 0-100
sound.play()
sound.play_varied()             # randomized pitch/volume for natural variation

# Music (streamed, for longer tracks)
music = mcrfpy.Music("assets/sfx/splat1.ogg")  # use your own track here
music.loop = True
music.volume = 50
music.play()
```

## Headless Mode & Testing

```python
# Advance simulation time (seconds); timers fire at most ONCE per step call
mcrfpy.step(0.1)
mcrfpy.step(0.1)  # call repeatedly for repeated timer fires

# Screenshots (synchronous in headless)
from mcrfpy import automation
automation.screenshot("game.png")
```

## Common Patterns

### Grid Movement with Collision
```python
def move_player(dx, dy):
    nx = player.cell_x + dx
    ny = player.cell_y + dy
    if grid.at(nx, ny).walkable:
        player.grid_pos = (nx, ny)
        grid.center_camera((nx + 0.5, ny + 0.5))  # tile coords, +0.5 = tile center
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

## Alignment System

```python
# Add to parent FIRST, then set alignment
frame.children.append(child)
child.align = mcrfpy.Alignment.CENTER      # Centered
child.align = mcrfpy.Alignment.TOP_LEFT    # Corner with margin
child.margin = 10.0  # Offset from edge (invalid for CENTER)

# Alignment values: TOP_LEFT, TOP_CENTER, TOP_RIGHT,
#                   CENTER_LEFT, CENTER, CENTER_RIGHT,
#                   BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT
```

## Color Helper

```python
red = mcrfpy.Color(255, 0, 0)
transparent_blue = mcrfpy.Color(0, 0, 255, 128)  # RGBA

frame.fill_color = red
caption.fill_color = mcrfpy.Color(255, 255, 255)
```

## Tips

1. **Enums everywhere** - compare against `mcrfpy.Key`, `mcrfpy.InputState`, `mcrfpy.MouseButton`, never strings
2. **Timer intervals and runtimes are milliseconds** - callback signature is `(timer, runtime_ms)`
3. **Sprite.scale is a single float** - use `scale_x`/`scale_y` for non-uniform scaling
4. **Animate via the object** - `obj.animate(...)`, there is no `mcrfpy.Animation` constructor
5. **Cell visuals live on layers** - `GridPoint` has `walkable`/`transparent`/`entities`; colors go on a `ColorLayer`
6. **`grid.center` is pixels; `grid.center_camera()` is tiles** - don't mix them up
7. **Let the engine run turns** - `grid.step()` + behaviors replaces hand-rolled turn loops

## Common Issues

- **Scene not showing**: Call `scene.activate()` after creating
- **Timer firing too rarely**: Interval is milliseconds - `0.1` means 0.1 ms rounds to nothing useful; use `100` for 100 ms
- **Alignment not working**: Element must be in the parent's `children` before setting `align`
- **Click handler never fires**: The property is `on_click` (signature `(pos, button, action)`), not `click`
- **Caption font won't change**: `font` is read-only after construction - pass `font=` to the constructor
- **Pathfinding stale after digging**: Call `grid.clear_dijkstra_maps()` after changing walkability
