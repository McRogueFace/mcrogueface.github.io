---
layout: default
title: Cookbook
mcrf:
  objects: [Frame, Caption, Timer, Scene]
  diataxis: howto
  disposition: current
  verified: "0.2.9-dev"
  verified_commit: b6720f6
---

# Cookbook

Ready-to-use code recipes for common game development patterns. Every snippet on this page runs against the current `mcrfpy` API.

## Recipe Library

The full recipe collection lives in the [Cookbook Recipes library](cookbook/), organized by category:

| Category | Recipes |
|----------|---------|
| [Combat Systems](cookbook/#combat-systems) | Turn systems, enemy AI, melee, status effects, animated movement |
| [Visual Effects](cookbook/#visual-effects) | Screen shake, damage flash, floating text, color pulses, scene transitions |
| [Grid Utilities](cookbook/#grid-utilities) | Fog of war, Dijkstra maps, dungeon generation, cell highlighting, layers |
| [Procedural Generation](cookbook/#procedural-generation) | Cellular caves, Wave Function Collapse |
| [UI Patterns](cookbook/#ui-patterns) | Menus, health bars, message logs, modal dialogs, tooltips |

The rest of this page is a worked recipe that demonstrates the core UI building blocks — `Scene`, `Frame`, `Caption`, and `Timer` — together with keyboard and mouse input.

## Text Input Box

A text input field that captures keyboard input. Perfect for player names, chat messages, or console commands.

Keyboard events arrive as `mcrfpy.Key` and `mcrfpy.InputState` enum values, not strings, so the recipe builds a small dictionary mapping the keys you care about to the characters they produce.

### Basic Example

```python
import mcrfpy

# Create and activate a scene
scene = mcrfpy.Scene("text_demo")
scene.activate()

# Background frame for the input field
input_frame = mcrfpy.Frame(pos=(50, 100), size=(300, 30))
input_frame.fill_color = mcrfpy.Color(255, 255, 255)
input_frame.outline_color = mcrfpy.Color(100, 100, 100)
input_frame.outline = 2
scene.children.append(input_frame)

# Text display
text_display = mcrfpy.Caption(text="", pos=(55, 105))
text_display.fill_color = mcrfpy.Color(0, 0, 0)
text_display.font_size = 16
scene.children.append(text_display)

# Cursor (blinking underscore)
cursor = mcrfpy.Caption(text="_", pos=(55, 105))
cursor.fill_color = mcrfpy.Color(0, 0, 0)
cursor.font_size = 16
scene.children.append(cursor)

text_content = ""

# Map Key enum members to the characters they produce
CHAR_KEYS = {getattr(mcrfpy.Key, letter): letter.lower()
             for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
for digit in "0123456789":
    CHAR_KEYS[getattr(mcrfpy.Key, "NUM_" + digit)] = digit
CHAR_KEYS[mcrfpy.Key.SPACE] = " "

def update_display():
    text_display.text = text_content
    # Caption.w reports the rendered text width in pixels
    cursor.x = text_display.x + text_display.w

def blink_cursor(timer, runtime_ms):
    cursor.visible = not cursor.visible

# Timer intervals are integer milliseconds
cursor_timer = mcrfpy.Timer("cursor_blink", blink_cursor, 500)

def handle_input(key, state):
    global text_content
    if state != mcrfpy.InputState.PRESSED:
        return  # ignore key releases
    if key == mcrfpy.Key.BACKSPACE:
        text_content = text_content[:-1]
    elif key == mcrfpy.Key.ENTER:
        print("Submitted: " + text_content)
        text_content = ""
    elif key in CHAR_KEYS:
        char = CHAR_KEYS[key]
        if mcrfpy.keyboard.shift:
            char = char.upper()
        text_content += char
    else:
        return
    update_display()

scene.on_key = handle_input
update_display()
```

### Advanced Text Input Widget

For multiple text fields with focus management, wrap the pattern in a reusable class. Each widget owns a `Frame`, and its captions are appended to `frame.children`, so they position relative to the frame and move with it. Clicking a field focuses it via the frame's `on_click` handler, which receives `(pos, button, action)`.

```python
import mcrfpy

# Shared key-to-character mapping
CHAR_KEYS = {getattr(mcrfpy.Key, letter): letter.lower()
             for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
for digit in "0123456789":
    CHAR_KEYS[getattr(mcrfpy.Key, "NUM_" + digit)] = digit
CHAR_KEYS[mcrfpy.Key.SPACE] = " "

class TextInput:
    """Reusable text input widget with click-to-focus."""

    def __init__(self, pos, width, placeholder="", on_submit=None):
        self.on_submit = on_submit
        self.text = ""
        self.focused = False

        # Container frame; child captions position relative to it
        self.frame = mcrfpy.Frame(pos=pos, size=(width, 30))
        self.frame.fill_color = mcrfpy.Color(255, 255, 255)
        self.frame.outline_color = mcrfpy.Color(128, 128, 128)
        self.frame.outline = 2

        self.text_display = mcrfpy.Caption(text="", pos=(5, 5))
        self.text_display.fill_color = mcrfpy.Color(0, 0, 0)
        self.text_display.font_size = 16
        self.frame.children.append(self.text_display)

        self.placeholder = mcrfpy.Caption(text=placeholder, pos=(5, 5))
        self.placeholder.fill_color = mcrfpy.Color(180, 180, 180)
        self.placeholder.font_size = 16
        self.frame.children.append(self.placeholder)

        self.cursor = mcrfpy.Caption(text="|", pos=(5, 5))
        self.cursor.fill_color = mcrfpy.Color(0, 0, 0)
        self.cursor.font_size = 16
        self.cursor.visible = False
        self.frame.children.append(self.cursor)

        # Click to focus: handler receives (pos, button, action)
        def clicked(pos, button, action):
            if (button == mcrfpy.MouseButton.LEFT
                    and action == mcrfpy.InputState.PRESSED):
                focus_input(self)
        self.frame.on_click = clicked

    def add_to(self, ui):
        """Add the widget to a scene's children collection."""
        ui.append(self.frame)

    def focus(self):
        self.focused = True
        self.frame.outline_color = mcrfpy.Color(0, 120, 215)  # blue
        self.cursor.visible = True
        self._update_display()

    def blur(self):
        self.focused = False
        self.frame.outline_color = mcrfpy.Color(128, 128, 128)
        self.cursor.visible = False

    def _update_display(self):
        self.text_display.text = self.text
        self.placeholder.visible = (self.text == "")
        # Position the cursor after the rendered text
        self.cursor.x = self.text_display.x + self.text_display.w

    def handle_key(self, key):
        """Process one key press. Returns True if consumed."""
        if not self.focused:
            return False
        if key == mcrfpy.Key.BACKSPACE:
            self.text = self.text[:-1]
        elif key == mcrfpy.Key.ENTER:
            if self.on_submit:
                self.on_submit(self.text)
            self.text = ""
        elif key in CHAR_KEYS:
            char = CHAR_KEYS[key]
            if mcrfpy.keyboard.shift:
                char = char.upper()
            self.text += char
        else:
            return False
        self._update_display()
        return True

# --- Example usage ---
scene = mcrfpy.Scene("form_demo")
scene.activate()

name_input = TextInput((50, 50), 300, placeholder="Enter your name",
                       on_submit=lambda text: print("Name: " + text))
email_input = TextInput((50, 100), 300, placeholder="Enter your email",
                        on_submit=lambda text: print("Email: " + text))
name_input.add_to(scene.children)
email_input.add_to(scene.children)

inputs = [name_input, email_input]
focused_input = None

def focus_input(widget):
    global focused_input
    for inp in inputs:
        inp.blur()
    widget.focus()
    focused_input = widget

def handle_keys(key, state):
    if state != mcrfpy.InputState.PRESSED:
        return
    if key == mcrfpy.Key.TAB:
        # Cycle focus through the inputs
        index = inputs.index(focused_input) if focused_input else -1
        focus_input(inputs[(index + 1) % len(inputs)])
    elif focused_input:
        focused_input.handle_key(key)

scene.on_key = handle_keys
focus_input(name_input)
```

### Tips and Tricks

1. **Keys are enums, not strings.** `scene.on_key` handlers receive `(key: mcrfpy.Key, state: mcrfpy.InputState)`. Compare against enum members like `mcrfpy.Key.BACKSPACE` and `mcrfpy.InputState.PRESSED` — string comparisons will never match.

2. **Modifier keys.** The `mcrfpy.keyboard` singleton reports live modifier state — `keyboard.shift`, `keyboard.ctrl`, `keyboard.alt`, and `keyboard.system` — so you don't need to track shift presses yourself.

3. **Measuring text.** `Caption.w` and `Caption.h` are the rendered pixel dimensions (read-only). Use them for cursor placement instead of assuming a fixed character width; it works with proportional fonts too.

4. **Timer intervals are milliseconds.** `mcrfpy.Timer(name, callback, interval)` takes an integer millisecond interval, and the callback receives `(timer, runtime_ms)`. Timers also support `pause()`, `resume()`, `stop()`, and `restart()`.

5. **Punctuation keys.** Extend the mapping with any additional keys you need:

   ```python
   CHAR_KEYS[mcrfpy.Key.PERIOD] = "."
   CHAR_KEYS[mcrfpy.Key.COMMA] = ","
   CHAR_KEYS[mcrfpy.Key.HYPHEN] = "-"
   CHAR_KEYS[mcrfpy.Key.SEMICOLON] = ";"
   CHAR_KEYS[mcrfpy.Key.APOSTROPHE] = "'"
   CHAR_KEYS[mcrfpy.Key.SLASH] = "/"
   ```

6. **Input validation.** Filter characters before appending:

   ```python
   # Numeric-only input
   if char.isdigit():
       self.text += char

   # Maximum length
   if len(self.text) < self.max_length:
       self.text += char
   ```

7. **Password fields.** Store the real text but display asterisks:

   ```python
   self.text_display.text = "*" * len(self.text)
   ```

8. **Frames swallow clicks for their children.** A plain `Caption` child without its own `on_click` handler passes clicks through to the parent frame, which is why the widget above sets the handler on the frame. Avoid setting `on_click` on captions inside a clickable frame — the caption will consume the click.

## Related Pages

- [Quick Reference](quick-reference) — cheat sheet for common operations
- [Tutorials](tutorials) — step-by-step introduction to scenes, grids, and entities
- [Cookbook Recipes library](cookbook/) — the full recipe collection by category
