---
title: UI Widget Patterns
mcrf:
  objects: [Frame, Caption, Color, Key, MouseButton, InputState, Scene, Vector]
  diataxis: howto
  disposition: migrated-from-wiki-needs-review
---

# UI Widget Patterns

Reusable patterns for building menus, dialogs, and HUD elements using Frame, Caption, and Sprite components. These patterns work independently of Grids.

**Related Pages:**
- UI Component Hierarchy - Base UI components
- Input and Events - Event handler reference
- Animation System - Animating widget transitions

---

## Setup Template

Most widget patterns fit into this basic structure:

```python
import mcrfpy

# Create scene and get UI collection
scene = mcrfpy.Scene("menu")
ui = scene.children

# Create root container for the menu/HUD
root = mcrfpy.Frame(pos=(50, 50), size=(300, 400),
                     fill_color=mcrfpy.Color(30, 30, 40))
root.outline_color = mcrfpy.Color(80, 80, 100)
root.outline = 2
ui.append(root)

# Add widgets to root.children...

mcrfpy.current_scene = scene
```

---

## Button

A clickable frame with label and hover feedback.

```python
def make_button(parent, pos, text, on_click):
    """Create a button with hover effects."""
    btn = mcrfpy.Frame(pos=pos, size=(120, 32),
                        fill_color=mcrfpy.Color(60, 60, 80))
    btn.outline_color = mcrfpy.Color(100, 100, 140)
    btn.outline = 1

    label = mcrfpy.Caption(text=text, pos=(10, 6))
    label.fill_color = mcrfpy.Color(220, 220, 220)
    btn.children.append(label)

    # Hover effects - on_enter/on_exit receive (pos: Vector)
    btn.on_enter = lambda pos: setattr(btn, 'fill_color',
                                        mcrfpy.Color(80, 80, 110))
    btn.on_exit = lambda pos: setattr(btn, 'fill_color',
                                       mcrfpy.Color(60, 60, 80))

    # Click handler receives (pos: Vector, button: MouseButton, action: InputState)
    def handle_click(pos, button, action):
        if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
            on_click()
    btn.on_click = handle_click

    parent.children.append(btn)
    return btn

# Usage
make_button(root, (20, 20), "New Game", lambda: start_new_game())
make_button(root, (20, 60), "Options", lambda: show_options())
make_button(root, (20, 100), "Quit", lambda: sys.exit(0))
```

---

## Toggle / Checkbox

A button that toggles state and updates its appearance.

```python
def make_toggle(parent, pos, label_text, initial=False, on_change=None):
    """Create a toggle with visual state indicator."""
    state = {"checked": initial}

    frame = mcrfpy.Frame(pos=pos, size=(160, 28),
                          fill_color=mcrfpy.Color(40, 40, 50))

    # Checkbox indicator
    indicator = mcrfpy.Frame(pos=(6, 6), size=(16, 16))
    indicator.outline = 1
    indicator.outline_color = mcrfpy.Color(120, 120, 140)
    frame.children.append(indicator)

    # Label
    label = mcrfpy.Caption(text=label_text, pos=(30, 5))
    label.fill_color = mcrfpy.Color(200, 200, 200)
    frame.children.append(label)

    def update_visual():
        if state["checked"]:
            indicator.fill_color = mcrfpy.Color(100, 180, 100)
        else:
            indicator.fill_color = mcrfpy.Color(50, 50, 60)

    def toggle(pos, button, action):
        if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
            state["checked"] = not state["checked"]
            update_visual()
            if on_change:
                on_change(state["checked"])

    frame.on_click = toggle
    update_visual()

    parent.children.append(frame)
    return state  # Return state dict for external access

# Usage
music_toggle = make_toggle(root, (20, 20), "Music", initial=True,
                           on_change=lambda on: set_music_volume(1.0 if on else 0.0))
```

---

## Vertical Menu

A list of selectable options with keyboard navigation support.

```python
class VerticalMenu:
    def __init__(self, parent, pos, options, on_select):
        """
        options: list of (label, value) tuples
        on_select: callback(value) when option chosen
        """
        self.options = options
        self.on_select = on_select
        self.selected = 0

        self.frame = mcrfpy.Frame(pos=pos,
                                   size=(180, len(options) * 28 + 8),
                                   fill_color=mcrfpy.Color(35, 35, 45))
        parent.children.append(self.frame)

        self.items = []
        for i, (label, value) in enumerate(options):
            item = mcrfpy.Caption(text=label, pos=(12, 4 + i * 28))
            item.fill_color = mcrfpy.Color(180, 180, 180)
            self.frame.children.append(item)
            self.items.append(item)

        self._update_highlight()

    def _update_highlight(self):
        for i, item in enumerate(self.items):
            if i == self.selected:
                item.fill_color = mcrfpy.Color(255, 220, 100)
            else:
                item.fill_color = mcrfpy.Color(180, 180, 180)

    def move_up(self):
        self.selected = (self.selected - 1) % len(self.options)
        self._update_highlight()

    def move_down(self):
        self.selected = (self.selected + 1) % len(self.options)
        self._update_highlight()

    def confirm(self):
        _, value = self.options[self.selected]
        self.on_select(value)

# Usage
menu = VerticalMenu(root, (20, 20), [
    ("Continue", "continue"),
    ("New Game", "new"),
    ("Options", "options"),
    ("Quit", "quit")
], on_select=handle_menu_choice)

# Keyboard navigation via scene.on_key
def handle_key(key, action):
    if action != mcrfpy.InputState.PRESSED:
        return
    if key == mcrfpy.Key.UP:
        menu.move_up()
    elif key == mcrfpy.Key.DOWN:
        menu.move_down()
    elif key == mcrfpy.Key.ENTER:
        menu.confirm()

scene.on_key = handle_key
```

---

## Modal Dialog

A dialog that captures all input until dismissed.

```python
class ModalDialog:
    def __init__(self, scene, message, on_dismiss=None):
        self.scene = scene
        self.on_dismiss = on_dismiss
        ui = scene.children

        # Semi-transparent backdrop
        self.backdrop = mcrfpy.Frame(pos=(0, 0), size=(1024, 768),
                                      fill_color=mcrfpy.Color(0, 0, 0, 160))
        self.backdrop.z_index = 900
        self.backdrop.on_click = lambda pos, btn, action: None  # Block clicks
        ui.append(self.backdrop)

        # Dialog box
        self.dialog = mcrfpy.Frame(pos=(312, 284), size=(400, 200),
                                    fill_color=mcrfpy.Color(50, 50, 65))
        self.dialog.outline_color = mcrfpy.Color(120, 120, 150)
        self.dialog.outline = 2
        self.dialog.z_index = 901
        ui.append(self.dialog)

        # Message
        msg = mcrfpy.Caption(text=message, pos=(20, 20))
        msg.fill_color = mcrfpy.Color(220, 220, 220)
        self.dialog.children.append(msg)

        # OK button
        ok_btn = mcrfpy.Frame(pos=(150, 140), size=(100, 36),
                               fill_color=mcrfpy.Color(70, 100, 70))
        ok_btn.outline = 1
        ok_btn.outline_color = mcrfpy.Color(100, 150, 100)
        ok_btn.on_click = lambda pos, btn, action: self.close()
        self.dialog.children.append(ok_btn)

        ok_label = mcrfpy.Caption(text="OK", pos=(35, 8))
        ok_label.fill_color = mcrfpy.Color(220, 255, 220)
        ok_btn.children.append(ok_label)

        # Capture keyboard
        self._prev_handler = scene.on_key

        def modal_keys(key, action):
            if action == mcrfpy.InputState.PRESSED:
                if key == mcrfpy.Key.ENTER or key == mcrfpy.Key.ESCAPE:
                    self.close()
        scene.on_key = modal_keys

    def close(self):
        ui = self.scene.children
        ui.remove(self.backdrop)
        ui.remove(self.dialog)
        if self._prev_handler:
            self.scene.on_key = self._prev_handler
        if self.on_dismiss:
            self.on_dismiss()

# Usage
dialog = ModalDialog(scene, "Game saved successfully!")
```

---

## Hotbar / Quick Slots

Number keys (1-9) mapped to inventory slots.

```python
class Hotbar:
    def __init__(self, parent, pos, slot_count=9):
        self.slots = []
        self.items = [None] * slot_count
        self.selected = 0

        self.frame = mcrfpy.Frame(pos=pos,
                                   size=(slot_count * 36 + 8, 44),
                                   fill_color=mcrfpy.Color(30, 30, 40, 200))
        parent.children.append(self.frame)

        for i in range(slot_count):
            slot = mcrfpy.Frame(pos=(4 + i * 36, 4), size=(32, 32),
                                 fill_color=mcrfpy.Color(50, 50, 60))
            slot.outline = 1
            slot.outline_color = mcrfpy.Color(80, 80, 100)
            self.frame.children.append(slot)
            self.slots.append(slot)

            num = mcrfpy.Caption(text=str((i + 1) % 10), pos=(2, 2))
            num.fill_color = mcrfpy.Color(100, 100, 120)
            slot.children.append(num)

        self._update_selection()

    def _update_selection(self):
        for i, slot in enumerate(self.slots):
            if i == self.selected:
                slot.outline_color = mcrfpy.Color(200, 180, 80)
                slot.outline = 2
            else:
                slot.outline_color = mcrfpy.Color(80, 80, 100)
                slot.outline = 1

    def select(self, index):
        if 0 <= index < len(self.slots):
            self.selected = index
            self._update_selection()

# Usage
hotbar = Hotbar(root, (200, 700))

# Key mapping for number keys
num_keys = {
    mcrfpy.Key.NUM_1: 0, mcrfpy.Key.NUM_2: 1, mcrfpy.Key.NUM_3: 2,
    mcrfpy.Key.NUM_4: 3, mcrfpy.Key.NUM_5: 4, mcrfpy.Key.NUM_6: 5,
    mcrfpy.Key.NUM_7: 6, mcrfpy.Key.NUM_8: 7, mcrfpy.Key.NUM_9: 8,
}

def handle_key(key, action):
    if action != mcrfpy.InputState.PRESSED:
        return
    if key in num_keys:
        hotbar.select(num_keys[key])

scene.on_key = handle_key
```

---

## Draggable Window

A frame that can be dragged by its title bar.

```python
class DraggableWindow:
    def __init__(self, parent, pos, size, title):
        self.dragging = False
        self.drag_offset = (0, 0)

        self.frame = mcrfpy.Frame(pos=pos, size=size,
                                   fill_color=mcrfpy.Color(45, 45, 55))
        self.frame.outline = 1
        self.frame.outline_color = mcrfpy.Color(100, 100, 120)
        parent.children.append(self.frame)

        # Title bar
        self.title_bar = mcrfpy.Frame(pos=(0, 0), size=(size[0], 24),
                                       fill_color=mcrfpy.Color(60, 60, 80))
        self.frame.children.append(self.title_bar)

        title_label = mcrfpy.Caption(text=title, pos=(8, 4))
        title_label.fill_color = mcrfpy.Color(200, 200, 220)
        self.title_bar.children.append(title_label)

        self.content_y = 28

        # Drag handling
        # on_click: (pos: Vector, button: MouseButton, action: InputState)
        def start_drag(pos, button, action):
            if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
                self.dragging = True
                self.drag_offset = (pos.x - self.frame.x, pos.y - self.frame.y)

        # on_move: (pos: Vector)
        def on_move(pos):
            if self.dragging:
                self.frame.x = pos.x - self.drag_offset[0]
                self.frame.y = pos.y - self.drag_offset[1]

        # on_exit: (pos: Vector)
        def stop_drag(pos):
            self.dragging = False

        self.title_bar.on_click = start_drag
        self.title_bar.on_move = on_move
        self.title_bar.on_exit = stop_drag

# Usage
window = DraggableWindow(root, (100, 100), (250, 300), "Inventory")

# Add content to window.frame.children at y >= window.content_y
item_list = mcrfpy.Caption(text="Items here...", pos=(10, window.content_y + 10))
window.frame.children.append(item_list)
```

---

## Related Pages

- Input and Events - Event handler API reference
- [Grid Interaction Patterns](grid-interaction-patterns.md) - Patterns for grid-based gameplay
- Animation System - Animating widget transitions

---

*Last updated: 2026-02-07*
