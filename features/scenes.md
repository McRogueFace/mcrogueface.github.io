# Scene Management

Scenes are containers for your game's UI elements and entities. McRogueFace supports both a procedural API and an object-oriented approach with lifecycle callbacks.

## Two Approaches

### Procedural API (Simple)

```python
import mcrfpy

# Create and switch scenes
mcrfpy.createScene("menu")
mcrfpy.createScene("game")

mcrfpy.setScene("menu")

# Access scene UI
ui = mcrfpy.sceneUI("menu")
ui.append(mcrfpy.Caption(pos=(400, 300), text="Main Menu"))

# Set input handler for current scene
mcrfpy.keypressScene(my_handler)
```

### Scene Class (Preferred OOP)

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

    def on_enter(self):
        """Called when scene becomes active."""
        print("Entering game scene")
        self.start_game_timer()

    def on_exit(self):
        """Called when scene deactivates."""
        print("Leaving game scene")
        self.stop_timers()

    def on_keypress(self, key, action):
        """Called for keyboard input while active."""
        if action == "start":
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
2. `on_enter` - Scene activated (setScene or activate)
3. `update` - Every frame while active
4. `on_keypress` - Keyboard events while active
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
    if action == "start":
        print(f"Key pressed: {key}")

scene.on_key = handle_key

# Procedural (only works on current scene)
mcrfpy.keypressScene(handle_key)
```

### Key Handler Signature

```python
def handle_key(key, action):
    """
    key: String like "Up", "Down", "A", "Space", "Escape", "Num1"
    action: "start" (pressed) or "end" (released)
    """
    if action != "start":
        return

    key_lower = key.lower()
    if key_lower == "escape":
        switch_to_menu()
    elif key_lower in ("up", "w"):
        move_player(0, -1)
```

### Common Key Names

| Key | Name |
|-----|------|
| Arrow keys | "Up", "Down", "Left", "Right" |
| Letters | "A" through "Z" |
| Numbers | "0" through "9", "Num0" through "Num9" |
| Special | "Space", "Escape", "Return", "Tab", "Backspace" |
| Function | "F1" through "F12" |

## Scene Transitions

Switch between scenes with optional transition effects:

```python
# Simple switch
mcrfpy.setScene("game")

# With transition effect
mcrfpy.setScene("game", transition="fade", duration=0.5)
mcrfpy.setScene("menu", transition="slide_left", duration=0.3)
```

### Available Transitions

| Transition | Description |
|------------|-------------|
| `"fade"` | Crossfade between scenes |
| `"slide_left"` | New scene slides in from right |
| `"slide_right"` | New scene slides in from left |
| `"slide_up"` | New scene slides in from bottom |
| `"slide_down"` | New scene slides in from top |

## Multi-Scene Architecture

### Common Pattern

```python
class MenuScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("menu")
        self.create_menu()

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

    def on_keypress(self, key, action):
        if action != "start":
            return

        key = key.lower()
        if key in ("up", "w"):
            self.selected = (self.selected - 1) % len(self.options)
            self.update_selection()
        elif key in ("down", "s"):
            self.selected = (self.selected + 1) % len(self.options)
            self.update_selection()
        elif key in ("return", "space"):
            self.select_option()

    def select_option(self):
        option = self.options[self.selected]
        if option == "New Game":
            game_scene.start_new_game()
            mcrfpy.setScene("game", transition="fade", duration=0.5)
        elif option == "Continue":
            game_scene.load_game()
            mcrfpy.setScene("game", transition="fade", duration=0.5)
        elif option == "Quit":
            mcrfpy.exit()


class GameScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("game")
        self.grid = None
        self.player = None

    def on_enter(self):
        print("Starting game...")

    def on_exit(self):
        print("Pausing game...")

    def on_keypress(self, key, action):
        if action != "start":
            return

        key = key.lower()
        if key == "escape":
            mcrfpy.setScene("menu", transition="fade", duration=0.3)
        elif key in ("up", "w"):
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

    def on_keypress(self, key, action):
        if action == "start" and key.lower() == "escape":
            mcrfpy.setScene("game")


# In game scene
def on_keypress(self, key, action):
    if action == "start" and key.lower() == "escape":
        mcrfpy.setScene("pause")
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
# Get current scene name
current = mcrfpy.currentScene()
print(f"Currently in: {current}")

# Conditional logic
if mcrfpy.currentScene() == "game":
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

    def on_keypress(self, key, action):
        if action == "start" and key.lower() == "space":
            mcrfpy.setScene("game", transition="fade", duration=1.0)


class GameScene(mcrfpy.Scene):
    def __init__(self):
        super().__init__("game")
        self.grid = None
        self.player = None
        self.setup_game()

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

    def on_keypress(self, key, action):
        if action != "start":
            return

        key = key.lower()

        if key == "escape":
            mcrfpy.setScene("title", transition="fade", duration=0.5)
            return

        dx, dy = 0, 0
        if key in ("up", "w"): dy = -1
        elif key in ("down", "s"): dy = 1
        elif key in ("left", "a"): dx = -1
        elif key in ("right", "d"): dx = 1

        if dx or dy:
            self.move_player(dx, dy)

    def move_player(self, dx, dy):
        new_x = int(self.player.x) + dx
        new_y = int(self.player.y) + dy

        if self.grid.at(new_x, new_y).walkable:
            self.player.pos = (new_x, new_y)
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
- `on_key` can be set on any scene; `keypressScene()` only affects current scene
- Scene transitions run asynchronously
- UI elements stay in their scene when switching
- Timers continue running across scene changes (stop them in `on_exit` if needed)

## Related Topics

- [Grid System](grid_system.md) - Creating game grids
- [Animation](animation.md) - Scene transition animations
- [Field of View](fov.md) - Scene-specific FOV
