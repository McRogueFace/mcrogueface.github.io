---
layout: default
title: Cookbook
---

# Cookbook

Visual gallery and example library for common game development patterns.

## Ready-to-use Code Recipes

Practical code snippets you can copy and paste into your games.

### Text Input Box

A simple text input field that captures keyboard input. Perfect for player names, chat messages, or console commands.

#### Basic Example

```python
import mcrfpy

# Create scene
scene = mcrfpy.Scene("text_demo")
scene.activate()

# Background frame for the input field
input_frame = mcrfpy.Frame(50, 100, 300, 30)
input_frame.fill_color = (255, 255, 255, 255)
input_frame.outline_color = (100, 100, 100, 255)
input_frame.outline = 2
scene.children.append(input_frame)

# Text display
text_display = mcrfpy.Caption("", 55, 107)
text_display.fill_color = (0, 0, 0, 255)
scene.children.append(text_display)

# Cursor (blinking underscore)
cursor = mcrfpy.Caption("_", 55, 107)
cursor.fill_color = (0, 0, 0, 255)
scene.children.append(cursor)

# Input state
text_content = ""
cursor_visible = True

def update_display():
    """Update the text display and cursor position"""
    text_display.text = text_content
    # Simple cursor positioning (works for monospace fonts)
    cursor_x = 55 + len(text_content) * 8
    cursor.x = cursor_x

def toggle_cursor():
    """Blink the cursor"""
    global cursor_visible
    cursor_visible = not cursor_visible
    cursor.visible = cursor_visible

# Set up cursor blinking
cursor_timer = mcrfpy.Timer("cursor_blink", lambda t, rt: toggle_cursor(), 0.5)

def handle_input(key, state):
    """Handle keyboard input"""
    global text_content
    
    if state != "start":  # Only handle key press, not release
        return
    
    # Handle special keys
    if key == "Backspace" and len(text_content) > 0:
        text_content = text_content[:-1]
        update_display()
    elif key == "Return":
        print(f"Submitted: {text_content}")
        text_content = ""
        update_display()
    # Handle alphanumeric input
    elif len(key) == 1 and key.isprintable():
        text_content += key
        update_display()
    # Handle space
    elif key == "Space":
        text_content += " "
        update_display()

# Register keyboard handler
scene.on_key = handle_input

# Initial display update
update_display()
```

#### Advanced Text Input Widget

For multiple text fields with focus management, use this reusable widget class:

```python
import mcrfpy

class TextInput:
    """Reusable text input widget"""
    def __init__(self, x, y, width, height=30, placeholder="", on_submit=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.placeholder = placeholder
        self.on_submit = on_submit
        self.text = ""
        self.focused = False
        self.cursor_pos = 0
        
        # Create UI elements
        self.frame = mcrfpy.Frame(x, y, width, height)
        self.frame.fill_color = (255, 255, 255, 255)
        self.frame.outline_color = (128, 128, 128, 255)
        self.frame.outline = 2
        
        self.text_display = mcrfpy.Caption("", x + 5, y + 7)
        self.text_display.fill_color = (0, 0, 0, 255)
        
        self.placeholder_display = mcrfpy.Caption(placeholder, x + 5, y + 7)
        self.placeholder_display.fill_color = (180, 180, 180, 255)
        
        self.cursor = mcrfpy.Caption("|", x + 5, y + 7)
        self.cursor.fill_color = (0, 0, 0, 255)
        self.cursor.visible = False
        
        # Set click handler
        def on_click():
            self.focus()
        self.frame.click = on_click
    
    def add_to_scene(self, ui):
        """Add widget to scene UI"""
        scene.children.append(self.frame)
        scene.children.append(self.placeholder_display)
        scene.children.append(self.text_display)
        scene.children.append(self.cursor)
    
    def focus(self):
        """Give focus to this input"""
        self.focused = True
        self.frame.outline_color = (0, 120, 215, 255)  # Blue when focused
        self.cursor.visible = True
        self._update_display()
    
    def blur(self):
        """Remove focus from this input"""
        self.focused = False
        self.frame.outline_color = (128, 128, 128, 255)
        self.cursor.visible = False
    
    def _update_display(self):
        """Update text and cursor display"""
        if self.text:
            self.text_display.text = self.text
            self.placeholder_display.visible = False
            # Update cursor position (assumes ~8 pixels per character)
            self.cursor.x = self.x + 5 + len(self.text) * 8
        else:
            self.text_display.text = ""
            self.placeholder_display.visible = True
            self.cursor.x = self.x + 5
    
    def handle_key(self, key):
        """Process keyboard input"""
        if not self.focused:
            return False
        
        if key == "Backspace" and self.cursor_pos > 0:
            self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1
        elif key == "Return":
            if self.on_submit:
                self.on_submit(self.text)
            self.text = ""
            self.cursor_pos = 0
        elif len(key) == 1 and key.isprintable():
            self.text = self.text[:self.cursor_pos] + key + self.text[self.cursor_pos:]
            self.cursor_pos += 1
        elif key == "Space":
            self.text = self.text[:self.cursor_pos] + " " + self.text[self.cursor_pos:]
            self.cursor_pos += 1
        elif key == "Left" and self.cursor_pos > 0:
            self.cursor_pos -= 1
        elif key == "Right" and self.cursor_pos < len(self.text):
            self.cursor_pos += 1
        else:
            return False
        
        self._update_display()
        return True

# Example usage
scene = mcrfpy.Scene("form_demo")
scene.activate()

# Create multiple input fields
name_input = TextInput(50, 50, 300, placeholder="Enter your name",
                      on_submit=lambda text: print(f"Name: {text}"))
email_input = TextInput(50, 100, 300, placeholder="Enter your email",
                       on_submit=lambda text: print(f"Email: {text}"))

name_input.add_to_scene(scene.children)
email_input.add_to_scene(scene.children)

# Track focused input
current_input = None

def handle_keys(key, state):
    """Global keyboard handler"""
    global current_input
    
    if state != "start":
        return
    
    # Tab to switch between inputs
    if key == "Tab":
        if current_input == name_input:
            name_input.blur()
            email_input.focus()
            current_input = email_input
        else:
            email_input.blur()
            name_input.focus()
            current_input = name_input
    elif current_input:
        current_input.handle_key(key)

# Register keyboard handler
scene.on_key = handle_keys

# Focus first input by default
name_input.focus()
current_input = name_input
```

#### Tips and Tricks

1. **Keyboard Input**: McRogueFace sends key names like "A", "Space", "Return", "Backspace", etc. to your handler function.

2. **Focus Management**: Only one input should be focused at a time. Use visual indicators like outline color to show which input is active.

3. **Cursor Positioning**: For precise cursor positioning with proportional fonts, you'll need to measure text width. The examples above assume monospace fonts.

4. **Special Characters**: To handle shift states and special characters properly, track whether shift is pressed:

```python
shift_pressed = False

def handle_keys(key, state):
    global shift_pressed
    
    if key in ["LShift", "RShift"]:
        shift_pressed = (state == "start")
        return
    
    if state == "start" and len(key) == 1:
        char = key.upper() if shift_pressed else key.lower()
        # Add char to input...
```

5. **Input Validation**: Add validation in your handle_key method:

```python
# Numeric only input
if key.isdigit():
    self.text += key

# Max length
if len(self.text) < self.max_length:
    self.text += key
```

6. **Password Fields**: Replace displayed text with asterisks:

```python
self.text_display.text = "*" * len(self.text)
```

### Next Recipe: Coming Soon

More recipes will be added here for common game development patterns like:
- Animated sprites
- Particle effects  
- Dialog boxes
- Inventory systems
- Save/load game state