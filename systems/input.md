---
layout: default
title: Input & Callbacks
mcrf:
  objects: [Scene, Timer, Key, InputState, MouseButton, Keyboard, Mouse]
  diataxis: explanation
  disposition: current
  verified: "0.2.9-dev"
  verified_commit: b6720f6
---

# Input & Callbacks

The Input & Callback System handles all user interaction and timed events in McRogueFace. It provides keyboard input through scene callbacks, mouse input through per-element callbacks, and scheduled execution through timers.

## Overview

McRogueFace uses a callback-based input model. Instead of polling for input in a game loop, you register callback functions that are invoked when events occur. Callbacks receive enum values ([Key](../objects/Key), [InputState](../objects/InputState), [MouseButton](../objects/MouseButton)) rather than strings, so typos fail loudly instead of silently never matching.

```python
def on_key(key, state):
    if key == mcrfpy.Key.W and state == mcrfpy.InputState.PRESSED:
        move_player(0, -1)

scene.on_key = on_key
```

Keyboard input belongs to the [Scene](../objects/Scene); mouse input belongs to individual UI elements. A click is delivered to the topmost element under the cursor that has a handler, so there is no manual hit-testing in your code.

## Objects

| Object | Purpose |
|--------|---------|
| [Scene](../objects/Scene) | Keyboard input via `on_key`, lifecycle callbacks |
| [Key](../objects/Key) | Keyboard key enum |
| [InputState](../objects/InputState) | `PRESSED` / `RELEASED` enum |
| [MouseButton](../objects/MouseButton) | Mouse button and scroll wheel enum |
| [Keyboard](../objects/Keyboard) | Modifier key state singleton (`mcrfpy.keyboard`) |
| [Mouse](../objects/Mouse) | Mouse position/button state singleton (`mcrfpy.mouse`) |
| [Timer](../objects/Timer) | Scheduled callbacks at intervals |

---

## Keyboard Input {#keyboard}

Keyboard input is handled through the scene's `on_key` callback.

### Key Callback Signature

```python
def on_key(key: mcrfpy.Key, state: mcrfpy.InputState) -> None:
    pass

scene.on_key = on_key   # set to None to remove the handler
```

- `key`: A [Key](../objects/Key) enum value (e.g., `mcrfpy.Key.W`, `mcrfpy.Key.SPACE`, `mcrfpy.Key.ESCAPE`)
- `state`: An [InputState](../objects/InputState) enum value: `PRESSED` or `RELEASED`

A handler can be set on *any* scene, not just the active one - only the active scene's handler receives events. Holding a key down delivers repeated `PRESSED` events (OS key repeat); `RELEASED` fires exactly once when the key comes up.

### Example: Movement

```python
import mcrfpy

scene = mcrfpy.Scene("game")
grid = mcrfpy.Grid(grid_size=(20, 15), pos=(50, 50), size=(320, 240))
scene.children.append(grid)

player = mcrfpy.Entity(grid_pos=(10, 7), sprite_index=84)
grid.entities.append(player)

# Cells default to walkable=False; open up the floor
for y in range(15):
    for x in range(20):
        grid.at(x, y).walkable = True

MOVES = {
    mcrfpy.Key.W: (0, -1), mcrfpy.Key.UP: (0, -1),
    mcrfpy.Key.S: (0, 1),  mcrfpy.Key.DOWN: (0, 1),
    mcrfpy.Key.A: (-1, 0), mcrfpy.Key.LEFT: (-1, 0),
    mcrfpy.Key.D: (1, 0),  mcrfpy.Key.RIGHT: (1, 0),
}

def on_key(key, state):
    if state != mcrfpy.InputState.PRESSED:
        return
    if key in MOVES:
        dx, dy = MOVES[key]
        nx, ny = player.grid_x + dx, player.grid_y + dy
        if 0 <= nx < 20 and 0 <= ny < 15 and grid.at(nx, ny).walkable:
            player.grid_pos = (nx, ny)

scene.on_key = on_key
scene.activate()
```

### Example: PRESSED vs RELEASED

`InputState` distinguishes key-down from key-up, which enables hold-and-release mechanics. This is a complete runnable script:

```python
import mcrfpy

scene = mcrfpy.Scene("charge_demo")
status = mcrfpy.Caption(text="Hold SPACE to charge, release to fire", pos=(20, 20))
scene.children.append(status)

charging = False

def on_key(key, state):
    global charging
    if key == mcrfpy.Key.SPACE:
        if state == mcrfpy.InputState.PRESSED and not charging:
            # Guard with a flag: key repeat delivers PRESSED again while held
            charging = True
            status.text = "Charging..."
        elif state == mcrfpy.InputState.RELEASED:
            charging = False
            status.text = "Fired! Hold SPACE to charge again"
    elif key == mcrfpy.Key.ESCAPE and state == mcrfpy.InputState.PRESSED:
        mcrfpy.exit()

scene.on_key = on_key
scene.activate()
```

### Modifier Keys

Modifier keys arrive as their own `Key` events (`LEFT_SHIFT`, `RIGHT_CONTROL`, ...), but for "is Shift held right now?" checks it is easier to poll the `mcrfpy.keyboard` singleton:

```python
def on_key(key, state):
    if key == mcrfpy.Key.UP and state == mcrfpy.InputState.PRESSED:
        step = 10 if mcrfpy.keyboard.shift else 1
        move_cursor(0, -step)
```

`mcrfpy.keyboard` exposes `shift`, `ctrl`, `alt`, and `system` (all read-only booleans, true if either the left or right key is held).

### Key Names

`mcrfpy.Key` covers the full keyboard. Commonly used values:
- Letters: `Key.A` through `Key.Z`
- Numbers: `Key.NUM_0` through `Key.NUM_9` (numpad: `Key.NUMPAD_0`...)
- Arrows: `Key.UP`, `Key.DOWN`, `Key.LEFT`, `Key.RIGHT`
- Modifiers: `Key.LEFT_SHIFT`, `Key.RIGHT_SHIFT`, `Key.LEFT_CONTROL`, `Key.LEFT_ALT`, ...
- Special: `Key.SPACE`, `Key.ENTER`, `Key.ESCAPE`, `Key.TAB`, `Key.BACKSPACE`
- Function keys: `Key.F1` through `Key.F15`

For debugging, `key.name` gives the string name of any key that arrives in your handler.

---

## Mouse Input {#mouse}

Mouse input is delivered to UI elements, not to the scene. Every drawable (Frame, Caption, Sprite, Grid, ...) supports click and hover callbacks. Events go to the topmost element under the cursor; the first element that handles a click stops propagation.

### Click Callback Signature

```python
def on_click(pos: mcrfpy.Vector, button: mcrfpy.MouseButton, action: mcrfpy.InputState) -> None:
    pass

element.on_click = on_click
```

- `pos`: A [Vector](../objects/Vector) with the click position in scene coordinates
- `button`: A [MouseButton](../objects/MouseButton) enum value: `LEFT`, `RIGHT`, `MIDDLE`, `X1`, `X2` - or `SCROLL_UP` / `SCROLL_DOWN` for the wheel
- `action`: `InputState.PRESSED` or `InputState.RELEASED`

`on_click` fires for **both** press and release, so filter on `action`:

```python
button_frame = mcrfpy.Frame(pos=(100, 100), size=(120, 40))

def on_button(pos, button, action):
    if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
        print(f"Clicked at {pos.x}, {pos.y}")

button_frame.on_click = on_button
```

Scroll wheel events arrive through the same callback with `button` set to `SCROLL_UP` or `SCROLL_DOWN`.

### Hover Callbacks

Hover callbacks receive only the position:

```python
def on_enter(pos):
    panel.fill_color = mcrfpy.Color(80, 80, 120)  # highlight

def on_exit(pos):
    panel.fill_color = mcrfpy.Color(50, 50, 50)   # restore

panel.on_enter = on_enter
panel.on_exit = on_exit
```

- `on_enter`: mouse entered the element's bounds - called with `(pos)`
- `on_exit`: mouse left the element's bounds - called with `(pos)`
- `on_move`: mouse moved while inside - called with `(pos)` on every movement, so keep it cheap

### Polling Mouse State

The `mcrfpy.mouse` singleton offers read-only state for polling instead of callbacks: `pos` (Vector), `x`, `y`, and `left`/`middle`/`right` booleans. It also controls the cursor via `visible` and `grabbed`.

---

## Grid Cell Input {#grid-cells}

[Grid](../objects/Grid) adds cell-level callbacks that report positions in **tile coordinates** rather than pixels, accounting for the grid's camera (`center` and `zoom`) automatically.

### Cell Callback Signatures

```python
def on_cell_click(cell_pos: mcrfpy.Vector, button: mcrfpy.MouseButton, action: mcrfpy.InputState) -> None:
    pass

def on_cell_enter(cell_pos: mcrfpy.Vector) -> None:
    pass

grid.on_cell_click = on_cell_click
grid.on_cell_enter = on_cell_enter
grid.on_cell_exit = lambda cell_pos: None
```

### Example: Tile Inspection

```python
def inspect_cell(cell_pos, button, action):
    if button != mcrfpy.MouseButton.LEFT or action != mcrfpy.InputState.PRESSED:
        return
    x, y = int(cell_pos.x), int(cell_pos.y)
    point = grid.at(x, y)
    print(f"Cell ({x}, {y}): walkable={point.walkable}, entities={len(point.entities)}")

grid.on_cell_click = inspect_cell
```

The currently hovered cell is also available as `grid.hovered_cell` - an `(x, y)` tuple, or `None` when the mouse is outside the grid.

A grid also supports the standard `on_click` (pixel position) alongside `on_cell_click` (tile position); use the cell variant whenever you care about tiles rather than screen geometry.

---

## Timers {#timers}

[Timers](../objects/Timer) execute callbacks at specified intervals. The callback receives the timer object and the total elapsed runtime in milliseconds.

### Creating Timers

```python
def update(timer, runtime):
    print(f"{timer.name} tick at {runtime} ms")

t = mcrfpy.Timer("update_timer", update, 500)   # every 500 ms, starts immediately
```

### One-Shot Timers

Pass `once=True` for single execution; pass `start=False` to create a timer without starting it:

```python
def delayed_action(timer, runtime):
    print("Delayed!")

t = mcrfpy.Timer("delay_timer", delayed_action, 1000, once=True)
```

One-shot timers stop themselves after firing and can be restarted with `t.restart()`.

### Timer Control

Timers are controlled through methods on the object:

```python
t.pause()     # preserve remaining time
t.resume()    # continue from where it paused
t.stop()      # remove from the tick loop (callback preserved)
t.start()     # start a stopped timer
t.restart()   # reset to the full interval and ensure running
```

State is inspectable via `t.active`, `t.paused`, `t.stopped`, and `t.remaining` (milliseconds until the next fire). `t.interval` can be changed while running.

### Sprite Animation with a Timer

```python
frames = [84, 85, 86, 87]

def animate(timer, runtime):
    sprite.sprite_index = frames[(runtime // 100) % len(frames)]

mcrfpy.Timer("walk_cycle", animate, 100)  # 10 FPS animation
```

For property transitions (position, color, opacity), prefer the [Animation System](animation) over hand-rolled timer loops.

---

## Scene Lifecycle {#lifecycle}

Scenes have lifecycle callbacks for initialization and cleanup. Unlike `on_key`, these are **subclass methods**, not assignable properties - define them by subclassing [Scene](../objects/Scene):

```python
class GameScene(mcrfpy.Scene):
    def on_enter(self):
        # Scene became active (via activate())
        print("Game started!")

    def on_exit(self):
        # Another scene activated; clean up timers, save state
        print("Leaving scene")

    def update(self, dt):
        # Called every frame with delta time in seconds
        pass

    def on_resize(self, new_size):
        # Window was resized; realign responsive layouts
        self.realign()

scene = GameScene("game")
scene.activate()
```

`scene.activate()` deactivates the current scene (firing its `on_exit`) and activates this one (firing `on_enter`). Keyboard handlers can also be defined as a subclass `on_key(self, key, state)` method instead of assigning the property.

---

## Related Objects

<div class="related-objects">
<div class="object-links">
<a href="../objects/Scene" class="object-link">Scene</a>
<a href="../objects/Key" class="object-link">Key</a>
<a href="../objects/InputState" class="object-link">InputState</a>
<a href="../objects/MouseButton" class="object-link">MouseButton</a>
<a href="../objects/Keyboard" class="object-link">Keyboard</a>
<a href="../objects/Mouse" class="object-link">Mouse</a>
<a href="../objects/Timer" class="object-link">Timer</a>
<a href="../objects/Vector" class="object-link">Vector</a>
<a href="../objects/Grid" class="object-link">Grid</a>
</div>
</div>
