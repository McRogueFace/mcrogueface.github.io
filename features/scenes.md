---
mcrf:
  objects: [Scene, Key, InputState, Caption, Frame]
  diataxis: howto
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Scene Management

Scenes are containers for your game's UI elements and entities. McRogueFace provides an object-oriented Scene class with lifecycle callbacks.

## Scene Class API

```python
import mcrfpy

# Create scene with object reference
scene = mcrfpy.Scene("game")

# Access children directly
scene.children.append(mcrfpy.Frame(pos=(0, 0), size=(800, 600)))

# Set input handler on any scene (not just active)
scene.on_key = my_handler

# Activate the scene
scene.activate()
```

## Scene Class

The `Scene` class provides an object-oriented interface with several advantages:

- Set `on_key` handler on non-active scenes
- Subclass for lifecycle callbacks
- Direct `children` access
- Object reference for cleaner code

### Constructor

```python
scene = mcrfpy.Scene(name)
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | str | Scene name (read-only after creation) |
| `active` | bool | Whether this scene is currently displayed |
| `children` | UICollection | UI elements in this scene |
| `on_key` | callable | Keyboard input handler |

### Methods

| Method | Description |
|--------|-------------|
| `activate()` | Make this scene active |

## Lifecycle Callbacks

Subclass `Scene` to receive lifecycle events:

```python
class GameScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("game")
        self.setup_ui()
        self.on_key = self.handle_key

    def on_enter(self):
        """Called when scene becomes active."""
        print("Entering game scene")
        self.start_game_timer()

    def on_exit(self):
        """Called when scene deactivates."""
        print("Leaving game scene")
        self.stop_timers()

    def handle_key(self, key, action):
        """Called for keyboard input while active."""
        if action == mcrfpy.InputState.PRESSED:
            self.handle_input(key)

    def update(self, dt):
        """Called every frame while active (use sparingly)."""
        self.update_animations(dt)

    def setup_ui(self):
        """Set up the scene's UI elements."""
        self.children.append(mcrfpy.Grid(...))
        self.children.append(mcrfpy.Frame(...))
```

### Lifecycle Order

1. `__init__` - Scene creation
2. `on_enter` - Scene activated (via activate())
3. `update` - Every frame while active
4. `on_key` handler - Keyboard events (assign your handler in `__init__`, e.g. `self.on_key = self.handle_key`)
5. `on_exit` - Another scene becomes active

## Scene Children

The `children` property provides a `UICollection` of all UI elements:

```python
scene = mcrfpy.Scene("ui_demo")

# Add elements
frame = mcrfpy.Frame(pos=(100, 100), size=(200, 150))
scene.children.append(frame)

grid = mcrfpy.Grid(grid_size=(20, 15), texture=mcrfpy.default_texture)
scene.children.append(grid)

# List operations
count = len(scene.children)
first = scene.children[0]
last = scene.children[-1]

# Iteration
for element in scene.children:
    print(element)

# Remove
scene.children.remove(frame)
popped = scene.children.pop()
```

## Input Handling

### Setting Key Handlers

```python
# On Scene object (preferred - works on any scene)
def handle_key(key, action):
    if action == mcrfpy.InputState.PRESSED:
        print(f"Key pressed: {key}")

scene.on_key = handle_key
```

### Key Handler Signature

```python
def handle_key(key, action):
    """
    key: mcrfpy.Key enum member, e.g. mcrfpy.Key.UP, mcrfpy.Key.A, mcrfpy.Key.SPACE
    action: mcrfpy.InputState.PRESSED or mcrfpy.InputState.RELEASED
    """
    if action != mcrfpy.InputState.PRESSED:
        return

    if key == mcrfpy.Key.ESCAPE:
        switch_to_menu()
    elif key in (mcrfpy.Key.UP, mcrfpy.Key.W):
        move_player(0, -1)
```

### Common Key Names

| Key | Enum member |
|-----|------|
| Arrow keys | `Key.UP`, `Key.DOWN`, `Key.LEFT`, `Key.RIGHT` |
| Letters | `Key.A` through `Key.Z` |
| Numbers | `Key.NUM_0` through `Key.NUM_9` (top row) |
| Special | `Key.SPACE`, `Key.ESCAPE`, `Key.ENTER`, `Key.TAB`, `Key.BACKSPACE` |
| Function | `Key.F1` through `Key.F15` |

## Scene Transitions

Switch between scenes:

```python
# Simple switch - use scene.activate()
game_scene.activate()

# If you have a scene reference, activate it directly
menu_scene.activate()
```

## Multi-Scene Architecture

### Common Pattern

```python
class MenuScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("menu")
        self.create_menu()
        self.on_key = self.handle_key

    def create_menu(self):
        title = mcrfpy.Caption(pos=(400, 100), text="My Roguelike")
        title.fill_color = mcrfpy.Color(255, 255, 0)
        self.children.append(title)

        # Menu options
        self.options = ["New Game", "Continue", "Quit"]
        self.selected = 0
        self.option_labels = []

        for i, option in enumerate(self.options):
            label = mcrfpy.Caption(pos=(400, 200 + i * 50), text=option)
            label.fill_color = mcrfpy.Color(200, 200, 200)
            self.children.append(label)
            self.option_labels.append(label)

        self.update_selection()

    def update_selection(self):
        for i, label in enumerate(self.option_labels):
            if i == self.selected:
                label.fill_color = mcrfpy.Color(255, 255, 100)
                label.text = f"> {self.options[i]}"
            else:
                label.fill_color = mcrfpy.Color(200, 200, 200)
                label.text = f"  {self.options[i]}"

    def handle_key(self, key, action):
        if action != mcrfpy.InputState.PRESSED:
            return

        if key in (mcrfpy.Key.UP, mcrfpy.Key.W):
            self.selected = (self.selected - 1) % len(self.options)
            self.update_selection()
        elif key in (mcrfpy.Key.DOWN, mcrfpy.Key.S):
            self.selected = (self.selected + 1) % len(self.options)
            self.update_selection()
        elif key in (mcrfpy.Key.ENTER, mcrfpy.Key.SPACE):
            self.select_option()

    def select_option(self):
        option = self.options[self.selected]
        if option == "New Game":
            game_scene.start_new_game()
            game_scene.activate()
        elif option == "Continue":
            game_scene.load_game()
            game_scene.activate()
        elif option == "Quit":
            mcrfpy.exit()


class GameScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("game")
        self.grid = None
        self.player = None
        self.on_key = self.handle_key

    def on_enter(self):
        print("Starting game...")

    def on_exit(self):
        print("Pausing game...")

    def handle_key(self, key, action):
        if action != mcrfpy.InputState.PRESSED:
            return

        if key == mcrfpy.Key.ESCAPE:
            menu_scene.activate()
        elif key in (mcrfpy.Key.UP, mcrfpy.Key.W):
            self.move_player(0, -1)
        # ... more controls

    def start_new_game(self):
        self.setup_grid()
        self.spawn_player()

    def load_game(self):
        # Load saved state
        pass


# Create scenes
menu_scene = MenuScene()
game_scene = GameScene()

# Start with menu
menu_scene.activate()
```

### Pause Menu Pattern

```python
class PauseScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("pause")

        # Semi-transparent overlay
        overlay = mcrfpy.Frame(pos=(0, 0), size=(800, 600))
        overlay.fill_color = mcrfpy.Color(0, 0, 0, 180)
        self.children.append(overlay)

        # Pause text
        pause_text = mcrfpy.Caption(pos=(400, 250), text="PAUSED")
        pause_text.fill_color = mcrfpy.Color(255, 255, 255)
        self.children.append(pause_text)

        resume_text = mcrfpy.Caption(pos=(400, 320), text="Press ESC to resume")
        resume_text.fill_color = mcrfpy.Color(180, 180, 180)
        self.children.append(resume_text)

        self.on_key = self.handle_key

    def handle_key(self, key, action):
        if action == mcrfpy.InputState.PRESSED and key == mcrfpy.Key.ESCAPE:
            game_scene.activate()


# In game scene, switch to pause
def handle_key(self, key, action):
    if action == mcrfpy.InputState.PRESSED and key == mcrfpy.Key.ESCAPE:
        pause_scene.activate()
```

## Scene State Management

### Preserving State

Scenes maintain their state when not active:

```python
class InventoryScene(mcrfpy.Scene):
    def __init__(self, game_scene):
        super().__init__("inventory")
        self.game = game_scene
        self.selected_slot = 0

    def on_enter(self):
        # Refresh inventory display from game state
        self.refresh_display()

    def refresh_display(self):
        # Clear old items
        while len(self.children) > 0:
            self.children.pop()

        # Display current inventory
        for i, item in enumerate(self.game.player.inventory):
            label = mcrfpy.Caption(
                pos=(100, 50 + i * 30),
                text=item.name if item else "Empty"
            )
            self.children.append(label)
```

### Querying Current Scene

```python
# Get current scene (returns Scene object)
current = mcrfpy.current_scene
print(f"Currently in: {current.name}")

# Conditional logic
if mcrfpy.current_scene.name == "game":
    # Game-specific logic
    pass
```

## Complete Example

```python
import mcrfpy

class TitleScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("title")

        # Background
        bg = mcrfpy.Frame(pos=(0, 0), size=(800, 600))
        bg.fill_color = mcrfpy.Color(20, 20, 40)
        self.children.append(bg)

        # Title
        title = mcrfpy.Caption(pos=(400, 150), text="DUNGEON EXPLORER")
        title.fill_color = mcrfpy.Color(255, 215, 0)
        self.children.append(title)

        # Subtitle
        subtitle = mcrfpy.Caption(pos=(400, 220), text="A McRogueFace Demo")
        subtitle.fill_color = mcrfpy.Color(180, 180, 180)
        self.children.append(subtitle)

        # Instructions
        start_text = mcrfpy.Caption(pos=(400, 400), text="Press SPACE to start")
        start_text.fill_color = mcrfpy.Color(100, 255, 100)
        self.children.append(start_text)

        self.on_key = self.handle_key

    def handle_key(self, key, action):
        if action == mcrfpy.InputState.PRESSED and key == mcrfpy.Key.SPACE:
            game.activate()


class GameScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("game")
        self.grid = None
        self.player = None
        self.setup_game()
        self.on_key = self.handle_key

    def setup_game(self):
        # Create grid
        self.grid = mcrfpy.Grid(
            grid_size=(40, 30),
            texture=mcrfpy.default_texture,
            pos=(0, 0),
            size=(800, 600)
        )
        self.children.append(self.grid)

        # Initialize map
        for y in range(30):
            for x in range(40):
                point = self.grid.at(x, y)
                if x == 0 or x == 39 or y == 0 or y == 29:
                    point.tilesprite = 1
                    point.walkable = False
                else:
                    point.tilesprite = 0
                    point.walkable = True

        # Create player
        self.player = mcrfpy.Entity(
            grid_pos=(20, 15),
            texture=mcrfpy.default_texture,
            sprite_index=64
        )
        self.grid.entities.append(self.player)
        self.grid.center = self.player.pos

    def on_enter(self):
        print("Game started!")

    def on_exit(self):
        print("Game paused")

    def handle_key(self, key, action):
        if action != mcrfpy.InputState.PRESSED:
            return

        if key == mcrfpy.Key.ESCAPE:
            title.activate()
            return

        dx, dy = 0, 0
        if key in (mcrfpy.Key.UP, mcrfpy.Key.W): dy = -1
        elif key in (mcrfpy.Key.DOWN, mcrfpy.Key.S): dy = 1
        elif key in (mcrfpy.Key.LEFT, mcrfpy.Key.A): dx = -1
        elif key in (mcrfpy.Key.RIGHT, mcrfpy.Key.D): dx = 1

        if dx or dy:
            self.move_player(dx, dy)

    def move_player(self, dx, dy):
        new_x = self.player.grid_x + dx
        new_y = self.player.grid_y + dy

        if self.grid.at(new_x, new_y).walkable:
            self.player.grid_pos = (new_x, new_y)
            self.grid.center = self.player.pos


# Create and activate scenes
title = TitleScene()
game = GameScene()

title.activate()
```

## Notes and Caveats

- Scene names must be unique
- Scenes persist in memory when not active
- Only one scene can be active at a time
- `on_key` can be set on any scene, not just the active one
- `activate()` deactivates the current scene and activates the new one immediately; pass `transition`/`duration` for an animated visual crossfade/slide that plays over `duration` seconds
- UI elements stay in their scene when switching
- Timers continue running across scene changes (stop them in `on_exit` if needed)

## Related Topics

- [Grid System](grid_system.md) - Creating game grids
- [Animation](animation.md) - Scene transition animations
- [Field of View](fov.md) - Scene-specific FOV
