# McRogueFace Stdlib Extraction from Test Suite

**Status:** Foundation Research Document
**Date:** 2025-12-29
**Source:** /home/john/Development/McRogueFace/tests/ (>96% passing tests)

---

## Executive Summary

The McRogueFace test suite provides authoritative examples of the actual API in action. This document extracts patterns and proposes stdlib modules that can serve as "batteries included" for the 13-part roguelike tutorial.

**Key Finding:** The Scene object pattern (`mcrfpy.Scene`) is the preferred approach over the procedural `createScene()`/`keypressScene()` pattern, enabling cleaner OOP-style game organization.

---

## 1. Scene Object Pattern (NEW Preferred Approach)

**Source:** `/home/john/Development/McRogueFace/tests/unit/test_scene_object_api.py`

### Old Approach (Procedural)
```python
import mcrfpy

mcrfpy.createScene("game")
mcrfpy.setScene("game")
ui = mcrfpy.sceneUI("game")
ui.append(mcrfpy.Frame(...))
mcrfpy.keypressScene(handler)  # ONLY works on current scene!
```

### New Approach (OOP - Preferred)
```python
import mcrfpy

scene = mcrfpy.Scene("game")
scene.children.append(mcrfpy.Frame(...))
scene.on_key = handler  # Works on ANY scene!
scene.activate()
```

### Key Benefits
1. `scene.on_key` can be set on non-active scenes
2. Subclassing enables lifecycle callbacks (`on_enter`, `on_exit`, `update`)
3. Object reference makes code more readable
4. `scene.children` is clearer than `sceneUI(name)`

### Scene Subclass Pattern (Lifecycle Hooks)
```python
class GameScene(mcrfpy.Scene):
    def __init__(self, name):
        super().__init__(name)
        self.setup_ui()

    def on_enter(self):
        """Called when scene becomes active"""
        print("Entering game scene")

    def on_exit(self):
        """Called when scene deactivates"""
        print("Leaving game scene")

    def on_keypress(self, key, action):
        """Alternative to setting on_key property"""
        if action == "start":
            self.handle_input(key)

    def update(self, dt):
        """Called every frame (use sparingly)"""
        pass
```

### Scene Properties
- `scene.name` - Scene name (read-only after creation)
- `scene.active` - Whether scene is currently active
- `scene.children` - UICollection of UI elements
- `scene.on_key` - Keyboard handler callback
- `scene.pos` - Scene offset position
- `scene.visible` - Scene visibility
- `scene.opacity` - Scene opacity (0.0 to 1.0)

---

## 2. Verified Constructor Patterns

**Source:** `/home/john/Development/McRogueFace/tests/unit/test_constructor_comprehensive.py`

### Frame
```python
# All valid patterns:
mcrfpy.Frame()  # Empty, pos=(0,0), size=(0,0)
mcrfpy.Frame((10, 20), (100, 200))  # Positional: pos, size
mcrfpy.Frame(pos=(5, 5), size=(50, 50), fill_color=(255, 0, 0), name="red")
mcrfpy.Frame(x=15, y=25, w=150, h=250, outline=2.0, visible=True, opacity=0.5)
```

### Grid
```python
# All valid patterns:
mcrfpy.Grid()  # Defaults to 2x2
mcrfpy.Grid((0, 0), (320, 320), (10, 10))  # pos, size, grid_size
mcrfpy.Grid(pos=(50, 50), grid_x=20, grid_y=15, zoom=2.0, name="main_grid")
mcrfpy.Grid(grid_size=(40, 25), pos=(0, 0), size=(640, 400))
```

### Caption
```python
# All valid patterns:
mcrfpy.Caption()  # Empty text at (0,0)
mcrfpy.Caption((50, 100), None, "Hello World")  # pos, font, text
mcrfpy.Caption(text="Test", font_size=24, fill_color=(0, 255, 0), name="label")
mcrfpy.Caption(pos=(10, 10), text="Mixed", outline=1.0, opacity=0.8)
```

### Sprite
```python
# All valid patterns:
mcrfpy.Sprite()  # At (0,0), sprite_index=0
mcrfpy.Sprite((100, 150), None, 5)  # pos, texture, sprite_index
mcrfpy.Sprite(x=200, y=250, sprite_index=10, scale=2.0, name="icon")
mcrfpy.Sprite(scale_x=2.0, scale_y=3.0)  # Asymmetric scaling
```

### Entity
```python
# All valid patterns:
mcrfpy.Entity()  # At grid (0,0)
mcrfpy.Entity((5, 10), None, 3)  # grid_pos, texture, sprite_index
mcrfpy.Entity(x=15, y=20, sprite_index=7, name="player", visible=True)
mcrfpy.Entity((5, 5), grid=some_grid)  # Auto-add to grid's entities
```

---

## 3. Grid and FOV Patterns

**Sources:**
- `/home/john/Development/McRogueFace/tests/unit/test_tcod_fov.py`
- `/home/john/Development/McRogueFace/tests/unit/test_tcod_fov_entities.py`
- `/home/john/Development/McRogueFace/tests/unit/test_visibility.py`

### Basic Grid Setup with Color Layer
```python
# Create grid
grid = mcrfpy.Grid(grid_x=20, grid_y=15)
grid.fill_color = mcrfpy.Color(20, 20, 30)

# Add a color layer for cell coloring (z_index=-1 = below entities)
color_layer = grid.add_layer("color", z_index=-1)

# Initialize all cells
for y in range(15):
    for x in range(20):
        cell = grid.at(x, y)
        cell.walkable = True
        cell.transparent = True
        color_layer.set(x, y, mcrfpy.Color(100, 100, 120))
```

### Wall Creation Pattern
```python
# Create walls
walls = [(3, 3), (3, 4), (3, 5), (4, 3), (5, 3)]
for x, y in walls:
    cell = grid.at(x, y)
    cell.walkable = False
    cell.transparent = False
    color_layer.set(x, y, mcrfpy.Color(40, 20, 20))  # Wall color
```

### FOV Computation
```python
# FOV enum values
mcrfpy.FOV.BASIC
mcrfpy.FOV.SHADOW  # Most commonly used

# Compute FOV from position
grid.compute_fov(player_x, player_y, radius=15, algorithm=mcrfpy.FOV.SHADOW)

# Check if position is visible
if grid.is_in_fov(x, y):
    # Cell is visible
    pass
```

### Per-Entity Visibility (Knowledge System)
```python
# Create entity
entity = mcrfpy.Entity((5, 5), grid=grid)

# Update entity's personal visibility
entity.update_visibility()

# Access entity's gridstate (per-cell visibility info)
for state in entity.gridstate:
    if state.visible:
        # Cell is currently visible to this entity
        pass
    if state.discovered:
        # Cell has been seen before by this entity
        pass
```

### Perspective Rendering
```python
# Set grid to render from specific entity's perspective
grid.perspective = 0  # First entity's view
grid.perspective = 1  # Second entity's view
grid.perspective = -1  # Omniscient (show everything)
```

### FOV Color Layer Visualization
```python
fov_layer = grid.add_layer('color', z_index=-1)
fov_layer.fill((0, 0, 0, 255))  # Start with black (unknown)

# Draw FOV-based colors
fov_layer.draw_fov(
    source=(player_x, player_y),
    radius=10,
    fov=mcrfpy.FOV.SHADOW,
    visible=(255, 255, 200, 64),      # Yellow tint for visible
    discovered=(100, 100, 100, 128),  # Gray for discovered
    unknown=(0, 0, 0, 255)            # Black for unknown
)

# Or apply entity perspective
fov_layer.apply_perspective(
    entity=player_entity,
    visible=mcrfpy.Color(0, 0, 0, 0),       # Transparent = show tile
    discovered=mcrfpy.Color(40, 40, 60, 180),  # Dim overlay
    unknown=mcrfpy.Color(0, 0, 0, 255)      # Black = hide
)
```

---

## 4. Pathfinding Patterns

**Sources:**
- `/home/john/Development/McRogueFace/tests/unit/test_entity_path_to.py`
- `/home/john/Development/McRogueFace/tests/unit/test_dijkstra_pathfinding.py`
- `/home/john/Development/McRogueFace/tests/unit/test_astar.py`

### Entity.path_to() - A* Pathfinding
```python
# Simple path finding
entity = mcrfpy.Entity((2, 2), grid=grid)
path = entity.path_to(6, 6)  # Returns list of (x, y) tuples
print(f"Path length: {len(path)} steps")

# Keyword arguments also work
path = entity.path_to(target_x=7, target_y=7)

# Error handling for out of bounds
try:
    path = entity.path_to(100, 100)
except ValueError as e:
    print(f"Invalid target: {e}")
```

### Grid-Level Pathfinding
```python
# A* via grid
path = grid.find_path(start_x, start_y, end_x, end_y)
```

### Dijkstra Distance Maps
```python
from mcrfpy import libtcod

# Compute Dijkstra map from root position
grid.compute_dijkstra(5, 5)

# Get distance to any position
distance = grid.get_dijkstra_distance(15, 15)
if distance is None:
    print("Position unreachable")

# Get path from any position to root
path = grid.get_dijkstra_path(15, 15)

# Alternative via libtcod module
dijkstra = libtcod.dijkstra_new(grid)
libtcod.dijkstra_compute(grid, 10, 2)
distance = libtcod.dijkstra_get_distance(grid, 10, 17)
path = libtcod.dijkstra_path_to(grid, 10, 17)
```

### Line of Sight
```python
from mcrfpy import libtcod

# Get cells in a line
line = libtcod.line(start_x, start_y, end_x, end_y)
# Returns list of (x, y) tuples
```

---

## 5. Timer Patterns

**Sources:**
- `/home/john/Development/McRogueFace/tests/unit/test_timer_object.py`
- `/home/john/Development/McRogueFace/tests/unit/test_timer_legacy.py`

### Legacy Timer API (Still Works)
```python
def my_callback(runtime):
    """runtime = milliseconds since timer started"""
    print(f"Timer fired at {runtime}ms")

# Create recurring timer
mcrfpy.setTimer("update", my_callback, 100)  # Every 100ms

# Delete timer
mcrfpy.delTimer("update")
```

### Timer Object API (Preferred)
```python
def my_callback(timer, runtime):
    """timer = the Timer object, runtime = milliseconds"""
    print(f"Timer fired! Runtime: {runtime}ms")

# Create timer
timer = mcrfpy.Timer("my_timer", my_callback, 500)

# Timer properties
print(f"Interval: {timer.interval}ms")
print(f"Active: {timer.active}")
print(f"Paused: {timer.paused}")
print(f"Remaining: {timer.remaining}ms")

# Control timer
timer.pause()
timer.resume()
timer.restart()
timer.cancel()

# Modify interval
timer.interval = 1000
```

### One-Shot Timer
```python
# Timer that fires once then auto-cancels
timer = mcrfpy.Timer("one_shot", callback, 500, once=True)
```

---

## 6. Animation Patterns

**Sources:**
- `/home/john/Development/McRogueFace/tests/unit/test_animation_chaining.py`
- `/home/john/Development/McRogueFace/tests/unit/test_entity_animation.py`
- `/home/john/Development/McRogueFace/tests/demo/screens/animation_demo.py`

### Basic Animation
```python
# Animation(property, target_value, duration_seconds, easing)
anim = mcrfpy.Animation("x", 500.0, 2.0, "easeInOut")
anim.start(frame)  # Animate frame.x to 500 over 2 seconds
```

### Available Easing Functions
- `"linear"` - Constant speed
- `"easeIn"` - Slow start
- `"easeOut"` - Slow end
- `"easeInOut"` - Slow start and end

### Animatable Properties
- Position: `x`, `y`
- Size: `w`, `h`
- Color components: `r`, `g`, `b`, `a`
- Scale: `scale`, `scale_x`, `scale_y`
- Opacity: `opacity`

### Animation with Callback
```python
def on_complete(anim, target):
    print("Animation finished!")

anim = mcrfpy.Animation("x", 100.0, 1.0, "linear", callback=on_complete)
anim.start(entity)
```

### Path Animation Pattern (Step-by-Step)
```python
class PathAnimator:
    """Handles step-by-step path animation with proper chaining"""

    def __init__(self, entity, path, step_duration=0.3, on_complete=None):
        self.entity = entity
        self.path = path
        self.current_index = 0
        self.step_duration = step_duration
        self.on_complete = on_complete
        self.animating = False

    def start(self):
        """Start animating along the path"""
        if not self.path or self.animating:
            return
        self.current_index = 0
        self.animating = True
        self._animate_next_step()

    def _animate_next_step(self):
        """Animate to the next position in the path"""
        if self.current_index >= len(self.path):
            self.animating = False
            if self.on_complete:
                self.on_complete()
            return

        target_x, target_y = self.path[self.current_index]

        # Create animations
        anim_x = mcrfpy.Animation("x", float(target_x), self.step_duration, "easeInOut")
        anim_y = mcrfpy.Animation("y", float(target_y), self.step_duration, "easeInOut")

        # Start animations
        anim_x.start(self.entity)
        anim_y.start(self.entity)

        # Schedule next step
        duration_ms = int(self.step_duration * 1000 + 50)
        mcrfpy.setTimer(f"path_{id(self)}",
                       lambda dt: self._on_step_complete(), duration_ms)

    def _on_step_complete(self):
        mcrfpy.delTimer(f"path_{id(self)}")
        self.current_index += 1
        self._animate_next_step()
```

---

## 7. Input Handling Patterns

**Sources:**
- `/home/john/Development/McRogueFace/tests/unit/keypress_scene_validation_test.py`
- `/home/john/Development/McRogueFace/tests/unit/test_headless_click.py`
- `/home/john/Development/McRogueFace/tests/unit/test_mouse_enter_exit.py`
- `/home/john/Development/McRogueFace/tests/unit/test_grid_cell_events.py`

### Keyboard Handler
```python
def handle_key(key, action):
    """
    key: String like "Up", "Down", "A", "Space", "Escape", "Num1", etc.
    action: "start" (key pressed) or "end" (key released)
    """
    if action != "start":
        return

    key = key.lower()
    if key == "q":
        sys.exit(0)
    elif key == "up":
        move_player(0, -1)

# Set handler on scene
mcrfpy.keypressScene(handle_key)

# Or with Scene object
scene.on_key = handle_key
```

### Callable Class as Handler
```python
class KeyHandler:
    def __call__(self, key, action):
        print(f"Key: {key}, action: {action}")

handler = KeyHandler()
mcrfpy.keypressScene(handler)
```

### Click Handler (Frame, Sprite, Caption)
```python
def on_click(x, y, button, action):
    """
    x, y: Click coordinates
    button: "left", "right", "middle"
    action: "start" (press) or "end" (release)
    """
    if action == "start":
        print(f"Clicked at ({x}, {y})")

frame.on_click = on_click
```

### Mouse Enter/Exit Events
```python
def on_enter(x, y, button, action):
    print(f"Mouse entered at ({x}, {y})")

def on_exit(x, y, button, action):
    print(f"Mouse exited at ({x}, {y})")

frame.on_enter = on_enter
frame.on_exit = on_exit

# Check if currently hovered (read-only)
if frame.hovered:
    print("Frame is being hovered")
```

### Grid Cell Events
```python
def on_cell_enter(x, y):
    """Called when mouse enters a grid cell"""
    print(f"Entered cell ({x}, {y})")

def on_cell_exit(x, y):
    """Called when mouse exits a grid cell"""
    print(f"Exited cell ({x}, {y})")

def on_cell_click(x, y):
    """Called when a grid cell is clicked"""
    print(f"Clicked cell ({x}, {y})")

grid.on_cell_enter = on_cell_enter
grid.on_cell_exit = on_cell_exit
grid.on_cell_click = on_cell_click

# Get currently hovered cell
cell = grid.hovered_cell  # Returns (x, y) tuple or None
```

---

## 8. Collection Patterns

**Source:** `/home/john/Development/McRogueFace/tests/unit/collection_list_methods_test.py`

### UICollection (scene.children, frame.children)
```python
ui = scene.children

# List-like operations
ui.append(frame)
ui.insert(0, header_frame)  # Insert at beginning
popped = ui.pop()  # Remove and return last
popped = ui.pop(0)  # Remove and return first
ui.remove(frame)  # Remove specific element (by value, not index!)

# Query operations
idx = ui.index(frame)  # Find position
cnt = ui.count(frame)  # Count occurrences (always 0 or 1)
length = len(ui)

# Iteration
for element in ui:
    print(element)

# Indexing
first = ui[0]
last = ui[-1]
```

### EntityCollection (grid.entities)
```python
entities = grid.entities

# Same list-like operations
entities.append(entity)
entities.insert(0, player)
removed = entities.pop()
entities.remove(entity)

# GridPoint.entities - entities at a specific cell
cell = grid.at(5, 5)
entities_here = cell.entities  # List of entities at (5, 5)
```

---

## 9. Color Utilities

**Source:** `/home/john/Development/McRogueFace/tests/unit/test_color_helpers.py`

### Color Creation
```python
# From RGBA values
color = mcrfpy.Color(255, 128, 64)       # RGB, alpha defaults to 255
color = mcrfpy.Color(255, 128, 64, 127)  # RGBA

# From hex string
color = mcrfpy.Color.from_hex("#FF0000")     # Red
color = mcrfpy.Color.from_hex("00FF00")      # Green (# optional)
color = mcrfpy.Color.from_hex("#0000FF80")   # Blue with 50% alpha
```

### Color Properties
```python
print(color.r, color.g, color.b, color.a)  # 0-255 each
```

### Color Operations
```python
# Convert to hex
hex_str = color.to_hex()  # "#FF8040" or "#FF80407F" with alpha

# Linear interpolation
red = mcrfpy.Color(255, 0, 0)
blue = mcrfpy.Color(0, 0, 255)
purple = red.lerp(blue, 0.5)  # Mix 50% of each

# Gradient generation
steps = []
for i in range(5):
    t = i / 4.0
    color = start.lerp(end, t)
    steps.append(color)
```

---

## 10. Proposed Stdlib Modules

Based on the patterns extracted, here are proposed stdlib modules:

### 10.1 MessageLog Widget

**Purpose:** Scrolling message display for game events

```python
# Proposed API
from mcrfpy_stdlib.widgets import MessageLog

log = MessageLog(
    pos=(0, 400),
    size=(800, 200),
    max_messages=100,
    font_size=14
)
scene.children.append(log)

log.add("Welcome to the dungeon!", color=mcrfpy.Color(255, 255, 100))
log.add("You see a goblin.", color=mcrfpy.Color(200, 200, 200))
log.add("The goblin attacks! [5 damage]", color=mcrfpy.Color(255, 100, 100))
```

**Implementation Pattern (from tests):**
```python
class MessageLog:
    def __init__(self, pos, size, max_messages=100, font_size=14):
        self.frame = mcrfpy.Frame(pos=pos, size=size)
        self.frame.fill_color = mcrfpy.Color(20, 20, 30)
        self.messages = []
        self.max_messages = max_messages
        self.font_size = font_size
        self._rebuild_display()

    def add(self, text, color=None):
        if color is None:
            color = mcrfpy.Color(200, 200, 200)
        self.messages.append((text, color))
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        self._rebuild_display()

    def _rebuild_display(self):
        # Clear old captions
        while len(self.frame.children) > 0:
            self.frame.children.pop()

        # Calculate visible messages based on size
        line_height = self.font_size + 4
        visible_count = int(self.frame.h / line_height)

        # Show most recent messages
        for i, (text, color) in enumerate(self.messages[-visible_count:]):
            cap = mcrfpy.Caption(
                pos=(5, 5 + i * line_height),
                text=text,
                font_size=self.font_size
            )
            cap.fill_color = color
            self.frame.children.append(cap)
```

### 10.2 HealthBar Widget

**Purpose:** Visual health/stat bar

```python
# Proposed API
from mcrfpy_stdlib.widgets import HealthBar

hp_bar = HealthBar(
    pos=(10, 10),
    size=(200, 20),
    current=75,
    maximum=100,
    fg_color=mcrfpy.Color(255, 0, 0),
    bg_color=mcrfpy.Color(50, 0, 0),
    show_text=True
)
scene.children.append(hp_bar)

# Update
hp_bar.current = 50
hp_bar.maximum = 120
```

**Implementation Pattern:**
```python
class HealthBar:
    def __init__(self, pos, size, current, maximum,
                 fg_color=None, bg_color=None, show_text=True):
        self.frame = mcrfpy.Frame(pos=pos, size=size)
        self._current = current
        self._maximum = maximum
        self.fg_color = fg_color or mcrfpy.Color(255, 0, 0)
        self.bg_color = bg_color or mcrfpy.Color(50, 0, 0)
        self.show_text = show_text
        self._create_elements()

    def _create_elements(self):
        # Background
        self.frame.fill_color = self.bg_color

        # Foreground bar
        self.bar = mcrfpy.Frame(pos=(0, 0), size=(0, self.frame.h))
        self.bar.fill_color = self.fg_color
        self.frame.children.append(self.bar)

        # Text label
        if self.show_text:
            self.label = mcrfpy.Caption(pos=(5, 2), text="")
            self.label.fill_color = mcrfpy.Color(255, 255, 255)
            self.frame.children.append(self.label)

        self._update_display()

    def _update_display(self):
        ratio = self._current / self._maximum if self._maximum > 0 else 0
        self.bar.w = int(self.frame.w * ratio)
        if self.show_text:
            self.label.text = f"{self._current}/{self._maximum}"

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = max(0, min(value, self._maximum))
        self._update_display()

    @property
    def maximum(self):
        return self._maximum

    @maximum.setter
    def maximum(self, value):
        self._maximum = max(1, value)
        self._update_display()
```

### 10.3 Menu Widget

**Purpose:** Keyboard-navigable selection menu

```python
# Proposed API
from mcrfpy_stdlib.widgets import Menu

def on_select(index, option):
    print(f"Selected: {option}")

menu = Menu(
    pos=(200, 100),
    options=["New Game", "Continue", "Options", "Quit"],
    on_select=on_select,
    selected_color=mcrfpy.Color(255, 255, 100),
    normal_color=mcrfpy.Color(200, 200, 200)
)
scene.children.append(menu)

# Navigation (call from key handler)
menu.move_up()
menu.move_down()
menu.select()  # Triggers on_select callback
```

**Implementation Pattern:**
```python
class Menu:
    def __init__(self, pos, options, on_select=None,
                 selected_color=None, normal_color=None):
        self.frame = mcrfpy.Frame(pos=pos, size=(300, len(options) * 30 + 20))
        self.options = options
        self.on_select = on_select
        self.selected_index = 0
        self.selected_color = selected_color or mcrfpy.Color(255, 255, 100)
        self.normal_color = normal_color or mcrfpy.Color(200, 200, 200)
        self._create_options()

    def _create_options(self):
        self.labels = []
        for i, option in enumerate(self.options):
            label = mcrfpy.Caption(
                pos=(20, 10 + i * 30),
                text=option
            )
            self.frame.children.append(label)
            self.labels.append(label)
        self._update_display()

    def _update_display(self):
        for i, label in enumerate(self.labels):
            if i == self.selected_index:
                label.fill_color = self.selected_color
                label.text = f"> {self.options[i]}"
            else:
                label.fill_color = self.normal_color
                label.text = f"  {self.options[i]}"

    def move_up(self):
        self.selected_index = (self.selected_index - 1) % len(self.options)
        self._update_display()

    def move_down(self):
        self.selected_index = (self.selected_index + 1) % len(self.options)
        self._update_display()

    def select(self):
        if self.on_select:
            self.on_select(self.selected_index, self.options[self.selected_index])
```

### 10.4 InputModeDispatcher

**Purpose:** Mode-based input handling for different game states

```python
# Proposed API
from mcrfpy_stdlib.input import InputModeDispatcher, InputMode

class GameMode(InputMode):
    def handle_key(self, key, action):
        if key == "Up": return ("move", 0, -1)
        if key == "I": return ("open_inventory",)
        return None

class InventoryMode(InputMode):
    def handle_key(self, key, action):
        if key == "Escape": return ("close_inventory",)
        if key == "Up": return ("inv_cursor_up",)
        return None

dispatcher = InputModeDispatcher()
dispatcher.register("game", GameMode())
dispatcher.register("inventory", InventoryMode())
dispatcher.set_mode("game")

# In your key handler
def on_key(key, action):
    if action != "start":
        return
    result = dispatcher.handle(key, action)
    if result:
        execute_action(result)

scene.on_key = on_key
```

**Implementation Pattern:**
```python
class InputMode:
    """Base class for input modes"""
    def handle_key(self, key, action):
        """Return action tuple or None"""
        raise NotImplementedError

class InputModeDispatcher:
    def __init__(self):
        self.modes = {}
        self.current_mode = None

    def register(self, name, mode):
        self.modes[name] = mode

    def set_mode(self, name):
        if name not in self.modes:
            raise ValueError(f"Unknown mode: {name}")
        self.current_mode = name

    def handle(self, key, action):
        if self.current_mode is None:
            return None
        mode = self.modes[self.current_mode]
        return mode.handle_key(key, action)
```

### 10.5 TurnManager

**Purpose:** Turn-based game flow management

```python
# Proposed API
from mcrfpy_stdlib.turns import TurnManager

class Actor:
    def __init__(self, entity, speed=100):
        self.entity = entity
        self.speed = speed
        self.energy = 0

manager = TurnManager()
manager.add_actor(player, speed=100)
manager.add_actor(goblin, speed=80)  # Slower than player

# Game loop integration
def process_turn():
    actor = manager.current_actor()
    if actor == player:
        # Wait for player input
        pass
    else:
        # AI takes turn
        ai_action(actor)
        manager.end_turn()
```

**Implementation Pattern (from vllm_demo turn_orchestrator.py):**
```python
class TurnManager:
    def __init__(self):
        self.actors = []
        self.turn_number = 0
        self.current_index = 0

    def add_actor(self, actor, speed=100):
        self.actors.append({"actor": actor, "speed": speed, "energy": 0})

    def remove_actor(self, actor):
        self.actors = [a for a in self.actors if a["actor"] != actor]

    def current_actor(self):
        if not self.actors:
            return None
        return self.actors[self.current_index]["actor"]

    def end_turn(self):
        """End current actor's turn, advance to next"""
        if not self.actors:
            return

        self.current_index = (self.current_index + 1) % len(self.actors)
        if self.current_index == 0:
            self.turn_number += 1

    def all_acted_this_round(self):
        """Check if all actors have acted this round"""
        return self.current_index == 0
```

### 10.6 ActionExecutor

**Purpose:** Game action execution with validation

```python
# Proposed API (based on vllm_demo/action_executor.py)
from mcrfpy_stdlib.actions import ActionExecutor, ActionResult

executor = ActionExecutor(grid)

# Execute movement
result = executor.move(entity, dx=1, dy=0)
if result.success:
    print(result.message)  # "Moved east to (5, 3)"
else:
    print(result.message)  # "Cannot move - path blocked"

# Execute attack
result = executor.attack(attacker, target)
```

**Implementation Pattern:**
```python
@dataclass
class ActionResult:
    success: bool
    message: str
    data: dict = None  # Optional extra data

class ActionExecutor:
    def __init__(self, grid):
        self.grid = grid

    def move(self, entity, dx, dy):
        """Attempt to move entity by (dx, dy)"""
        current_x, current_y = int(entity.x), int(entity.y)
        new_x, new_y = current_x + dx, current_y + dy

        # Check bounds
        if not (0 <= new_x < self.grid.grid_x and 0 <= new_y < self.grid.grid_y):
            return ActionResult(False, "Cannot move - edge of map")

        # Check walkability
        cell = self.grid.at(new_x, new_y)
        if not cell.walkable:
            return ActionResult(False, "Cannot move - path blocked")

        # Check entity collision
        for other in cell.entities:
            if other != entity:
                return ActionResult(False, "Cannot move - someone is there")

        # Execute movement
        entity.x = new_x
        entity.y = new_y

        direction = self._get_direction_name(dx, dy)
        return ActionResult(True, f"Moved {direction} to ({new_x}, {new_y})")

    def _get_direction_name(self, dx, dy):
        dirs = {(0, -1): "north", (0, 1): "south",
                (1, 0): "east", (-1, 0): "west"}
        return dirs.get((dx, dy), "somewhere")
```

---

## 11. API Corrections (Updates to F1)

Based on test analysis, these corrections should be noted:

### Confirmed Working Patterns

1. **Grid cell access:** `grid.at(x, y)` returns GridPoint with:
   - `.walkable` (bool)
   - `.transparent` (bool)
   - `.tilesprite` (int)
   - `.entities` (list of entities at this position)

2. **Entity position:** Both work:
   - `entity.pos` - tuple `(x, y)`
   - `entity.x`, `entity.y` - individual float properties

3. **Click handler signature:** `(x, y, button, action)` confirmed

4. **Key handler signature:** `(key, action)` where:
   - `key` is a string like "Up", "Down", "A", "Space", "Escape", "Num1"
   - `action` is "start" or "end"

5. **Timer callback signatures:**
   - Legacy: `callback(runtime)`
   - Timer object: `callback(timer, runtime)`

6. **Scene lifecycle methods:** `on_enter()`, `on_exit()`, `update(dt)`, `on_keypress(key, action)`

### Missing from F1

1. `grid.add_layer("color", z_index=-1)` - Returns ColorLayer for cell coloring
2. `color_layer.set(x, y, color)` - Set individual cell color
3. `color_layer.fill(color)` - Fill all cells
4. `color_layer.draw_fov(...)` - FOV-based coloring
5. `color_layer.apply_perspective(entity, ...)` - Entity-based FOV coloring
6. `grid.perspective` property - Set rendering perspective (-1 for omniscient)
7. `entity.gridstate` - Per-entity visibility data
8. `entity.update_visibility()` - Refresh entity's FOV
9. `gridpoint.entities` - List entities at grid position
10. `mcrfpy.libtcod` module - Direct access to libtcod functions
11. `frame.hovered` - Read-only hover state
12. `frame.on_enter`, `frame.on_exit` - Mouse enter/exit events
13. `grid.on_cell_enter`, `grid.on_cell_exit`, `grid.on_cell_click` - Cell events
14. `grid.hovered_cell` - Currently hovered cell coordinates

---

## 12. Tutorial Part Mapping

| Part | Key Patterns Needed | Source Tests |
|------|---------------------|--------------|
| 0-1 Basic Setup | Scene object, Grid, Entity, keypressScene | test_scene_object_api.py, test_constructor_comprehensive.py |
| 2-3 Dungeon | grid.at(), walkable, ColorLayer | test_tcod_fov.py, test_visibility.py |
| 4 FOV | compute_fov, is_in_fov, perspective | test_tcod_fov_entities.py, test_visibility.py |
| 5 Enemies | EntityCollection, grid.entities | test_gridpoint_entities.py, test_entity_collection_remove.py |
| 6 Combat | Action pattern, collision detection | action_executor.py, test_animation_chaining.py |
| 7 UI | Frame.children, Caption, MessageLog | demo screens, test_frame_clipping.py |
| 8 Items | Cell inspection, entity data | test_gridpoint_entities.py |
| 9 Inventory | Menu pattern, input modes | demo_main.py (menu creation) |
| 10 Save/Load | Python serialization (no engine support) | N/A - pure Python |
| 11 Stairs | Scene transitions, multiple grids | test_scene_object_api.py |
| 12 Range | Dijkstra, line drawing | test_dijkstra_pathfinding.py |
| 13 Equipment | Data modeling patterns | action_executor.py dataclasses |

---

## Appendix: Key Test Files Reference

| Test File | Key Patterns Demonstrated |
|-----------|---------------------------|
| `test_scene_object_api.py` | Scene OOP pattern, lifecycle, on_key |
| `test_constructor_comprehensive.py` | All constructor signatures |
| `test_tcod_fov.py` | FOV computation basics |
| `test_tcod_fov_entities.py` | Entity FOV, color layers |
| `test_visibility.py` | Per-entity visibility, perspective |
| `test_dijkstra_pathfinding.py` | Distance maps, multi-target |
| `test_entity_path_to.py` | A* pathfinding |
| `test_timer_object.py` | Timer object API |
| `test_animation_chaining.py` | Path animation pattern |
| `test_headless_click.py` | Click handler signature |
| `test_mouse_enter_exit.py` | Hover events |
| `test_grid_cell_events.py` | Grid cell interaction |
| `test_color_helpers.py` | Color utilities |
| `collection_list_methods_test.py` | Collection operations |
| `test_gridpoint_entities.py` | Entities at grid positions |
| `vllm_demo/action_executor.py` | Action execution pattern |
| `vllm_demo/turn_orchestrator.py` | Turn management |
| `demo/demo_main.py` | Menu/scene navigation |
