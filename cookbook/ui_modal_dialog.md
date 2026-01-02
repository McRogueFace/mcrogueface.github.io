# Modal Dialog Widget

Modal dialogs are popup windows that require user interaction before continuing. They're used for confirmations, alerts, and simple forms. This recipe shows how to create centered modal dialogs with buttons.

## The Pattern

A modal dialog consists of:
1. **Overlay Frame** - Semi-transparent backdrop that covers the game
2. **Dialog Frame** - Centered panel containing the message
3. **Title and Message** - Caption elements for content
4. **Action Buttons** - Clickable frames with labels
5. **Focus trap** - Prevents interaction with elements behind the modal

The key technique is using a full-screen semi-transparent overlay to create the modal effect and block clicks to background elements.

## Basic Implementation

```python
import mcrfpy

class ModalDialog:
    """A centered modal dialog with customizable buttons."""

    def __init__(self, title, message, buttons, on_close=None):
        """
        Create a modal dialog.

        Args:
            title: Dialog title
            message: Main message text
            buttons: List of button labels (e.g., ["OK", "Cancel"])
            on_close: Callback function(button_index, button_label)
        """
        self.title = title
        self.message = message
        self.buttons = buttons
        self.on_close = on_close
        self.visible = False
        self.elements = []

        # Calculate dimensions
        self.dialog_width = 400
        self.dialog_height = 180
        self.button_width = 100
        self.button_height = 35

        self._create_elements()

    def _create_elements(self):
        """Create all UI elements for the dialog."""
        # Full-screen overlay
        self.overlay = mcrfpy.Frame(0, 0, 1024, 768)
        self.overlay.fill_color = mcrfpy.Color(0, 0, 0, 150)
        self.overlay.visible = False

        # Prevent clicks from passing through overlay
        self.overlay.click = lambda x, y, b, a: None

        # Center the dialog
        dialog_x = (1024 - self.dialog_width) // 2
        dialog_y = (768 - self.dialog_height) // 2

        # Dialog frame
        self.dialog = mcrfpy.Frame(
            dialog_x, dialog_y,
            self.dialog_width, self.dialog_height
        )
        self.dialog.fill_color = mcrfpy.Color(45, 45, 60)
        self.dialog.outline = 2
        self.dialog.outline_color = mcrfpy.Color(100, 100, 130)
        self.dialog.visible = False

        # Title
        self.title_caption = mcrfpy.Caption(
            self.title,
            mcrfpy.default_font,
            dialog_x + 20,
            dialog_y + 15
        )
        self.title_caption.fill_color = mcrfpy.Color(255, 220, 100)
        self.title_caption.visible = False

        # Message
        self.message_caption = mcrfpy.Caption(
            self.message,
            mcrfpy.default_font,
            dialog_x + 20,
            dialog_y + 50
        )
        self.message_caption.fill_color = mcrfpy.Color(220, 220, 220)
        self.message_caption.visible = False

        # Buttons
        self.button_frames = []
        self.button_labels = []

        total_button_width = len(self.buttons) * self.button_width + (len(self.buttons) - 1) * 15
        start_x = dialog_x + (self.dialog_width - total_button_width) // 2
        button_y = dialog_y + self.dialog_height - self.button_height - 20

        for i, label in enumerate(self.buttons):
            btn_x = start_x + i * (self.button_width + 15)

            btn_frame = mcrfpy.Frame(btn_x, button_y, self.button_width, self.button_height)
            btn_frame.fill_color = mcrfpy.Color(70, 70, 90)
            btn_frame.outline = 1
            btn_frame.outline_color = mcrfpy.Color(100, 100, 120)
            btn_frame.visible = False

            # Click handler
            def make_handler(index, text):
                def handler(x, y, button, action):
                    if action == "start":
                        self._on_button_click(index, text)
                return handler

            btn_frame.click = make_handler(i, label)
            self.button_frames.append(btn_frame)

            # Button label (centered)
            label_x = btn_x + (self.button_width - len(label) * 8) // 2
            label_y = button_y + (self.button_height - 16) // 2

            btn_label = mcrfpy.Caption(label, mcrfpy.default_font, label_x, label_y)
            btn_label.fill_color = mcrfpy.Color(255, 255, 255)
            btn_label.visible = False
            self.button_labels.append(btn_label)

        # Track all elements
        self.elements = [
            self.overlay, self.dialog,
            self.title_caption, self.message_caption
        ]
        self.elements.extend(self.button_frames)
        self.elements.extend(self.button_labels)

    def _on_button_click(self, index, label):
        """Handle button click."""
        self.hide()
        if self.on_close:
            self.on_close(index, label)

    def show(self):
        """Show the dialog."""
        for elem in self.elements:
            elem.visible = True
        self.visible = True

    def hide(self):
        """Hide the dialog."""
        for elem in self.elements:
            elem.visible = False
        self.visible = False

    def add_to_scene(self, ui):
        """Add dialog to scene (call once during setup)."""
        for elem in self.elements:
            ui.append(elem)


# Usage Example
mcrfpy.createScene("modal_demo")
mcrfpy.setScene("modal_demo")
ui = mcrfpy.sceneUI("modal_demo")

# Background content
bg = mcrfpy.Frame(0, 0, 1024, 768)
bg.fill_color = mcrfpy.Color(30, 30, 45)
ui.append(bg)

label = mcrfpy.Caption("Press SPACE to show dialog", mcrfpy.default_font, 350, 350)
label.fill_color = mcrfpy.Color(200, 200, 200)
ui.append(label)

# Create dialog
def on_dialog_close(index, label):
    print(f"Dialog closed with: {label} (index {index})")
    if label == "Yes":
        print("User confirmed!")
    else:
        print("User cancelled.")

dialog = ModalDialog(
    "Confirm Action",
    "Are you sure you want to proceed?",
    ["Yes", "No"],
    on_dialog_close
)
dialog.add_to_scene(ui)

# Show dialog on keypress
def on_key(key, state):
    if state != "start":
        return
    if key == "Space" and not dialog.visible:
        dialog.show()
    elif key == "Escape" and dialog.visible:
        dialog.hide()

mcrfpy.keypressScene(on_key)
```

## Enhanced Dialog with Multiple Styles

A more polished version with different dialog types and animations:

```python
import mcrfpy

class DialogStyle:
    """Predefined dialog styles."""
    INFO = {
        'bg': mcrfpy.Color(45, 55, 75),
        'border': mcrfpy.Color(80, 120, 180),
        'title': mcrfpy.Color(150, 200, 255),
        'btn_bg': mcrfpy.Color(60, 90, 130),
    }
    WARNING = {
        'bg': mcrfpy.Color(75, 65, 45),
        'border': mcrfpy.Color(180, 150, 80),
        'title': mcrfpy.Color(255, 220, 100),
        'btn_bg': mcrfpy.Color(130, 110, 60),
    }
    ERROR = {
        'bg': mcrfpy.Color(75, 45, 45),
        'border': mcrfpy.Color(180, 80, 80),
        'title': mcrfpy.Color(255, 150, 150),
        'btn_bg': mcrfpy.Color(130, 60, 60),
    }
    SUCCESS = {
        'bg': mcrfpy.Color(45, 75, 55),
        'border': mcrfpy.Color(80, 180, 100),
        'title': mcrfpy.Color(150, 255, 180),
        'btn_bg': mcrfpy.Color(60, 130, 80),
    }


class EnhancedDialog:
    """Modal dialog with styles, keyboard navigation, and animations."""

    def __init__(self, title, message, buttons=None, style=None, on_close=None):
        """
        Create an enhanced dialog.

        Args:
            title: Dialog title
            message: Main message (can include newlines)
            buttons: Button labels (default ["OK"])
            style: DialogStyle dict (default INFO)
            on_close: Callback(button_index, button_label)
        """
        self.title = title
        self.message = message
        self.buttons = buttons or ["OK"]
        self.style = style or DialogStyle.INFO
        self.on_close = on_close
        self.visible = False
        self.selected_button = 0

        self.dialog_width = 450
        self.dialog_height = 200

        # Adjust height for multiline messages
        lines = message.count('\n') + 1
        self.dialog_height = 150 + lines * 20

        self._create_elements()

    def _create_elements(self):
        """Build dialog UI."""
        # Overlay
        self.overlay = mcrfpy.Frame(0, 0, 1024, 768)
        self.overlay.fill_color = mcrfpy.Color(0, 0, 0, 180)
        self.overlay.visible = False
        self.overlay.click = lambda x, y, b, a: None

        # Dialog
        dx = (1024 - self.dialog_width) // 2
        dy = (768 - self.dialog_height) // 2

        self.dialog = mcrfpy.Frame(dx, dy, self.dialog_width, self.dialog_height)
        self.dialog.fill_color = self.style['bg']
        self.dialog.outline = 3
        self.dialog.outline_color = self.style['border']
        self.dialog.visible = False

        # Title bar
        self.title_bar = mcrfpy.Frame(dx + 2, dy + 2, self.dialog_width - 4, 35)
        self.title_bar.fill_color = mcrfpy.Color(
            self.style['border'].r,
            self.style['border'].g,
            self.style['border'].b,
            50
        )
        self.title_bar.outline = 0
        self.title_bar.visible = False

        # Title text
        self.title_caption = mcrfpy.Caption(
            self.title,
            mcrfpy.default_font,
            dx + 15,
            dy + 10
        )
        self.title_caption.fill_color = self.style['title']
        self.title_caption.visible = False

        # Message
        self.message_caption = mcrfpy.Caption(
            self.message,
            mcrfpy.default_font,
            dx + 20,
            dy + 50
        )
        self.message_caption.fill_color = mcrfpy.Color(230, 230, 230)
        self.message_caption.visible = False

        # Buttons
        self.button_frames = []
        self.button_labels = []

        btn_width = 110
        btn_height = 38
        total_width = len(self.buttons) * btn_width + (len(self.buttons) - 1) * 15
        start_x = dx + (self.dialog_width - total_width) // 2
        btn_y = dy + self.dialog_height - btn_height - 20

        for i, label in enumerate(self.buttons):
            bx = start_x + i * (btn_width + 15)

            btn = mcrfpy.Frame(bx, btn_y, btn_width, btn_height)
            btn.fill_color = self.style['btn_bg']
            btn.outline = 2
            btn.outline_color = mcrfpy.Color(150, 150, 170)
            btn.visible = False

            def make_handler(idx, txt):
                def handler(x, y, button, action):
                    if action == "start":
                        self._select_button(idx, txt)
                return handler

            btn.click = make_handler(i, label)
            self.button_frames.append(btn)

            # Center label
            lx = bx + (btn_width - len(label) * 8) // 2
            ly = btn_y + (btn_height - 16) // 2

            lbl = mcrfpy.Caption(label, mcrfpy.default_font, lx, ly)
            lbl.fill_color = mcrfpy.Color(255, 255, 255)
            lbl.visible = False
            self.button_labels.append(lbl)

        self._update_button_highlight()

    def _update_button_highlight(self):
        """Update button visual states."""
        for i, btn in enumerate(self.button_frames):
            if i == self.selected_button:
                btn.outline = 2
                btn.outline_color = mcrfpy.Color(255, 255, 100)
                btn.fill_color = mcrfpy.Color(
                    min(255, self.style['btn_bg'].r + 30),
                    min(255, self.style['btn_bg'].g + 30),
                    min(255, self.style['btn_bg'].b + 30)
                )
            else:
                btn.outline = 1
                btn.outline_color = mcrfpy.Color(100, 100, 120)
                btn.fill_color = self.style['btn_bg']

    def _select_button(self, index, label):
        """Handle button selection."""
        self.hide()
        if self.on_close:
            self.on_close(index, label)

    def navigate_left(self):
        """Move selection left."""
        if not self.visible:
            return
        self.selected_button = (self.selected_button - 1) % len(self.buttons)
        self._update_button_highlight()

    def navigate_right(self):
        """Move selection right."""
        if not self.visible:
            return
        self.selected_button = (self.selected_button + 1) % len(self.buttons)
        self._update_button_highlight()

    def confirm(self):
        """Activate selected button."""
        if not self.visible:
            return
        self._select_button(self.selected_button, self.buttons[self.selected_button])

    def show(self):
        """Show the dialog."""
        self.selected_button = 0
        self._update_button_highlight()

        elements = [
            self.overlay, self.dialog, self.title_bar,
            self.title_caption, self.message_caption
        ] + self.button_frames + self.button_labels

        for elem in elements:
            elem.visible = True

        self.visible = True

    def hide(self):
        """Hide the dialog."""
        elements = [
            self.overlay, self.dialog, self.title_bar,
            self.title_caption, self.message_caption
        ] + self.button_frames + self.button_labels

        for elem in elements:
            elem.visible = False

        self.visible = False

    def add_to_scene(self, ui):
        """Add to scene UI."""
        elements = [
            self.overlay, self.dialog, self.title_bar,
            self.title_caption, self.message_caption
        ] + self.button_frames + self.button_labels

        for elem in elements:
            ui.append(elem)

    def handle_key(self, key):
        """Handle keyboard input. Returns True if handled."""
        if not self.visible:
            return False

        if key == "Left" or key == "A":
            self.navigate_left()
            return True
        elif key == "Right" or key == "D":
            self.navigate_right()
            return True
        elif key == "Return" or key == "Space":
            self.confirm()
            return True
        elif key == "Escape":
            # Close with last button (usually Cancel)
            self._select_button(len(self.buttons) - 1, self.buttons[-1])
            return True

        return False


# Usage with different styles
mcrfpy.createScene("styled_dialogs")
mcrfpy.setScene("styled_dialogs")
ui = mcrfpy.sceneUI("styled_dialogs")

bg = mcrfpy.Frame(0, 0, 1024, 768)
bg.fill_color = mcrfpy.Color(35, 35, 45)
ui.append(bg)

# Current dialog reference
current_dialog = None

def show_info():
    global current_dialog
    current_dialog = EnhancedDialog(
        "Information",
        "This is an informational message.\nPress OK to continue.",
        ["OK"],
        DialogStyle.INFO
    )
    current_dialog.add_to_scene(ui)
    current_dialog.show()

def show_warning():
    global current_dialog
    current_dialog = EnhancedDialog(
        "Warning",
        "You are about to delete this item.\nThis action cannot be undone.",
        ["Delete", "Cancel"],
        DialogStyle.WARNING,
        lambda i, l: print(f"Warning response: {l}")
    )
    current_dialog.add_to_scene(ui)
    current_dialog.show()

def show_error():
    global current_dialog
    current_dialog = EnhancedDialog(
        "Error",
        "Failed to save the file.\nPlease check disk space.",
        ["Retry", "Cancel"],
        DialogStyle.ERROR
    )
    current_dialog.add_to_scene(ui)
    current_dialog.show()

def show_success():
    global current_dialog
    current_dialog = EnhancedDialog(
        "Success!",
        "Your progress has been saved.",
        ["Continue"],
        DialogStyle.SUCCESS
    )
    current_dialog.add_to_scene(ui)
    current_dialog.show()

# Help text
help_text = mcrfpy.Caption(
    "Press: 1=Info  2=Warning  3=Error  4=Success",
    mcrfpy.default_font, 280, 700
)
help_text.fill_color = mcrfpy.Color(150, 150, 150)
ui.append(help_text)

def on_key(key, state):
    global current_dialog
    if state != "start":
        return

    # Let dialog handle input first
    if current_dialog and current_dialog.handle_key(key):
        return

    if key == "Num1" or key == "1":
        show_info()
    elif key == "Num2" or key == "2":
        show_warning()
    elif key == "Num3" or key == "3":
        show_error()
    elif key == "Num4" or key == "4":
        show_success()

mcrfpy.keypressScene(on_key)
```

## Dialog Manager for Queued Dialogs

When multiple dialogs might be triggered, use a manager to queue them:

```python
import mcrfpy

class DialogManager:
    """Manages a queue of dialogs."""

    def __init__(self, ui):
        self.ui = ui
        self.queue = []
        self.current = None

    def show(self, title, message, buttons=None, style=None, callback=None):
        """
        Queue a dialog to show.

        If no dialog is active, shows immediately.
        Otherwise, queues for later.
        """
        dialog_data = {
            'title': title,
            'message': message,
            'buttons': buttons or ["OK"],
            'style': style or DialogStyle.INFO,
            'callback': callback
        }

        if self.current is None:
            self._show_dialog(dialog_data)
        else:
            self.queue.append(dialog_data)

    def _show_dialog(self, data):
        """Actually display a dialog."""
        def on_close(index, label):
            if data['callback']:
                data['callback'](index, label)
            self._on_dialog_closed()

        self.current = EnhancedDialog(
            data['title'],
            data['message'],
            data['buttons'],
            data['style'],
            on_close
        )
        self.current.add_to_scene(self.ui)
        self.current.show()

    def _on_dialog_closed(self):
        """Handle dialog close, show next if queued."""
        self.current = None

        if self.queue:
            next_dialog = self.queue.pop(0)
            self._show_dialog(next_dialog)

    def handle_key(self, key):
        """Forward key events to current dialog."""
        if self.current:
            return self.current.handle_key(key)
        return False


# Usage
manager = DialogManager(ui)

# Queue multiple dialogs
manager.show("First", "This is the first message")
manager.show("Second", "This appears after closing the first")
manager.show("Third", "And this is last", ["Done"])
```

## McRogueFace-Specific Considerations

1. **Z-Order**: Add modal elements last to ensure they render on top. The overlay must capture clicks to prevent interaction with background.

2. **Click Blocking**: Setting `overlay.click = lambda x, y, b, a: None` prevents clicks from reaching elements behind the overlay.

3. **Visibility Control**: Use the `visible` property rather than removing/re-adding elements for better performance.

4. **Keyboard Focus**: Modal dialogs should intercept all keyboard input. Return `True` from `handle_key` to indicate the event was consumed.

5. **Screen Coordinates**: All positions are absolute screen coordinates. Calculate dialog center based on screen size (default 1024x768).

6. **No Built-in Modality**: McRogueFace doesn't have native modal support. The overlay-based approach simulates modality by capturing input.

## Complete Example

```python
import mcrfpy

# Scene setup
mcrfpy.createScene("game")
mcrfpy.setScene("game")
ui = mcrfpy.sceneUI("game")

# Game background
bg = mcrfpy.Frame(0, 0, 1024, 768)
bg.fill_color = mcrfpy.Color(25, 35, 45)
ui.append(bg)

title = mcrfpy.Caption("My Game", mcrfpy.default_font, 450, 50)
title.fill_color = mcrfpy.Color(255, 255, 255)
ui.append(title)

# Quit button
quit_btn = mcrfpy.Frame(430, 400, 160, 50)
quit_btn.fill_color = mcrfpy.Color(150, 50, 50)
quit_btn.outline = 2
quit_btn.outline_color = mcrfpy.Color(200, 100, 100)
ui.append(quit_btn)

quit_label = mcrfpy.Caption("Quit Game", mcrfpy.default_font, 460, 415)
quit_label.fill_color = mcrfpy.Color(255, 255, 255)
ui.append(quit_label)

# Confirmation dialog
confirm_dialog = None

def show_quit_confirm():
    global confirm_dialog

    def on_response(index, label):
        if label == "Yes":
            mcrfpy.exit()

    confirm_dialog = EnhancedDialog(
        "Quit Game?",
        "Are you sure you want to quit?\nUnsaved progress will be lost.",
        ["Yes", "No"],
        DialogStyle.WARNING,
        on_response
    )
    confirm_dialog.add_to_scene(ui)
    confirm_dialog.show()

quit_btn.click = lambda x, y, b, a: show_quit_confirm() if a == "start" else None

def on_key(key, state):
    if state != "start":
        return

    if confirm_dialog and confirm_dialog.handle_key(key):
        return

    if key == "Escape":
        show_quit_confirm()

mcrfpy.keypressScene(on_key)
```
