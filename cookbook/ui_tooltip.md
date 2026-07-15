---
mcrf:
  objects: [Frame, Caption, Color, Timer, Mouse]
  diataxis: howto
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Tooltip on Hover

Tooltips provide contextual information when hovering over UI elements. This recipe shows how to use `on_enter`/`on_exit`/`on_move` mouse callbacks to show and hide tooltip overlays.

## The Pattern

Every drawable (`Frame`, `Caption`, `Sprite`, etc.) has native hover callbacks — no click-hijacking or manual polling required:

- `element.on_enter = handler` — called with `(pos: Vector)` when the mouse enters the element's bounds
- `element.on_exit = handler` — called with `(pos: Vector)` when the mouse leaves the element's bounds
- `element.on_move = handler` — called with `(pos: Vector)` on every mouse movement while inside the bounds

Separately, `element.on_click = handler` fires on button press/release and receives `(pos: Vector, button: MouseButton, action: InputState)`. Clicks and hover are independent callbacks — you don't need to inspect `on_click` to detect hovering.

There's also a read-only `element.hovered` property if you'd rather poll state from a `Timer` than register callbacks.

## Basic Tooltip Implementation

```python
import mcrfpy

class Tooltip:
    """A simple tooltip that follows the mouse."""

    def __init__(self, text, width=200):
        """
        Create a tooltip (initially hidden).

        Args:
            text: Tooltip text
            width: Maximum width
        """
        self.text = text
        self.visible = False

        # Tooltip frame
        self.frame = mcrfpy.Frame(pos=(0, 0), size=(width, 30))
        self.frame.fill_color = mcrfpy.Color(40, 40, 50, 240)
        self.frame.outline = 1
        self.frame.outline_color = mcrfpy.Color(100, 100, 120)
        self.frame.visible = False

        # Tooltip text
        self.caption = mcrfpy.Caption(text=text, pos=(5, 5))
        self.caption.fill_color = mcrfpy.Color(255, 255, 220)
        self.caption.visible = False

    def show(self, x, y):
        """Show tooltip at position."""
        # Offset from cursor
        self.frame.x = x + 15
        self.frame.y = y + 15
        self.caption.x = self.frame.x + 8
        self.caption.y = self.frame.y + 6

        # Keep on screen
        if self.frame.x + self.frame.w > 1024:
            self.frame.x = x - self.frame.w - 5
            self.caption.x = self.frame.x + 8
        if self.frame.y + self.frame.h > 768:
            self.frame.y = y - self.frame.h - 5
            self.caption.y = self.frame.y + 6

        self.frame.visible = True
        self.caption.visible = True
        self.visible = True

    def hide(self):
        """Hide the tooltip."""
        self.frame.visible = False
        self.caption.visible = False
        self.visible = False

    def set_text(self, text):
        """Update tooltip text."""
        self.text = text
        self.caption.text = text

    def add_to_scene(self, ui):
        """Add tooltip to scene (add last for top layer)."""
        ui.append(self.frame)
        ui.append(self.caption)


def make_hoverable(element, tooltip, tooltip_text=None):
    """
    Make a UI element show a tooltip on hover.

    Args:
        element: Frame, Caption, or Sprite to make hoverable
        tooltip: Tooltip instance
        tooltip_text: Text to show (optional, uses tooltip's default)
    """
    def on_enter(pos):
        if tooltip_text:
            tooltip.set_text(tooltip_text)
        tooltip.show(pos.x, pos.y)

    def on_move(pos):
        tooltip.show(pos.x, pos.y)

    def on_exit(pos):
        tooltip.hide()

    element.on_enter = on_enter
    element.on_move = on_move
    element.on_exit = on_exit


# Usage Example
scene = mcrfpy.Scene("tooltip_demo")
mcrfpy.current_scene = scene

# Create some buttons
button1 = mcrfpy.Frame(pos=(100, 100), size=(120, 40))
button1.fill_color = mcrfpy.Color(60, 60, 100)
button1.outline = 2
button1.outline_color = mcrfpy.Color(100, 100, 150)
scene.children.append(button1)

btn1_label = mcrfpy.Caption(text="Attack", pos=(125, 112))
btn1_label.fill_color = mcrfpy.Color(255, 255, 255)
scene.children.append(btn1_label)

button2 = mcrfpy.Frame(pos=(100, 160), size=(120, 40))
button2.fill_color = mcrfpy.Color(60, 100, 60)
button2.outline = 2
button2.outline_color = mcrfpy.Color(100, 150, 100)
scene.children.append(button2)

btn2_label = mcrfpy.Caption(text="Defend", pos=(125, 172))
btn2_label.fill_color = mcrfpy.Color(255, 255, 255)
scene.children.append(btn2_label)

# Create shared tooltip (add last for top layer)
tooltip = Tooltip("", width=250)
tooltip.add_to_scene(scene.children)

# Make buttons hoverable
make_hoverable(button1, tooltip, "Deal damage to the enemy")
make_hoverable(button2, tooltip, "Reduce incoming damage by 50%")
```

Because `on_enter`/`on_exit` fire directly from the engine's mouse tracking, there's no need for a polling `Timer` just to detect "mouse left the element" — `on_exit` already tells you that.

## Tooltip Manager for Multiple Elements

A more robust system for managing tooltips across many elements, with a hover delay before the tooltip appears:

```python
import mcrfpy

class TooltipManager:
    """Manages tooltips for multiple UI elements."""

    def __init__(self):
        self.elements = {}  # id(element) -> {text, title} mapping
        self.tooltip_frame = None
        self.tooltip_text = None
        self.current_element = None
        self.hover_delay = 500  # ms before showing tooltip
        self.pending_element = None
        self.pending_x = 0
        self.pending_y = 0

        self._create_tooltip()

    def _create_tooltip(self):
        """Create the tooltip UI elements."""
        self.tooltip_frame = mcrfpy.Frame(pos=(0, 0), size=(200, 60))
        self.tooltip_frame.fill_color = mcrfpy.Color(30, 30, 45, 245)
        self.tooltip_frame.outline = 1
        self.tooltip_frame.outline_color = mcrfpy.Color(80, 80, 100)
        self.tooltip_frame.visible = False

        self.tooltip_text = mcrfpy.Caption(text="", pos=(0, 0))
        self.tooltip_text.fill_color = mcrfpy.Color(255, 255, 230)
        self.tooltip_text.visible = False

    def register(self, element, text, title=None):
        """
        Register an element for tooltips.

        Args:
            element: UI element to track
            text: Tooltip description
            title: Optional title (shown in different color)
        """
        self.elements[id(element)] = {
            'element': element,
            'text': text,
            'title': title
        }

        def on_enter(pos):
            self._on_element_enter(element, pos.x, pos.y)

        def on_exit(pos):
            self._on_element_exit(element)

        element.on_enter = on_enter
        element.on_exit = on_exit

    def _on_element_enter(self, element, x, y):
        """Handle mouse entering a registered element."""
        elem_id = id(element)
        if elem_id not in self.elements:
            return

        self.pending_element = element
        self.pending_x = x
        self.pending_y = y

        def show_after_delay(timer, runtime):
            # Only show if the mouse is still over this element
            if self.pending_element is element:
                self._show_tooltip(element, self.pending_x, self.pending_y)

        timer_name = f"tooltip_delay_{id(self)}"
        mcrfpy.Timer(timer_name, show_after_delay, self.hover_delay)

    def _on_element_exit(self, element):
        """Handle mouse leaving a registered element."""
        if self.pending_element is element:
            self.pending_element = None
        if self.current_element is element:
            self.hide()

    def _show_tooltip(self, element, x, y):
        """Display tooltip for element."""
        elem_id = id(element)
        if elem_id not in self.elements:
            return

        data = self.elements[elem_id]

        # Build tooltip content
        content = ""
        if data.get('title'):
            content = data['title'] + "\n"
        content += data['text']

        # Update tooltip text
        self.tooltip_text.text = content

        # Calculate size based on content
        lines = content.split('\n')
        max_width = max(len(line) for line in lines) * 8 + 20
        height = len(lines) * 18 + 15

        self.tooltip_frame.w = min(300, max(100, max_width))
        self.tooltip_frame.h = height

        # Position tooltip
        self.tooltip_frame.x = x + 20
        self.tooltip_frame.y = y + 20

        # Keep on screen
        if self.tooltip_frame.x + self.tooltip_frame.w > 1000:
            self.tooltip_frame.x = x - self.tooltip_frame.w - 10
        if self.tooltip_frame.y + self.tooltip_frame.h > 750:
            self.tooltip_frame.y = y - self.tooltip_frame.h - 10

        self.tooltip_text.x = self.tooltip_frame.x + 10
        self.tooltip_text.y = self.tooltip_frame.y + 8

        # Show
        self.tooltip_frame.visible = True
        self.tooltip_text.visible = True
        self.current_element = element

    def hide(self):
        """Hide the tooltip."""
        self.tooltip_frame.visible = False
        self.tooltip_text.visible = False
        self.current_element = None
        self.pending_element = None

    def add_to_scene(self, ui):
        """Add tooltip to scene (call last for top layer)."""
        ui.append(self.tooltip_frame)
        ui.append(self.tooltip_text)


# Usage
scene = mcrfpy.Scene("demo")
mcrfpy.current_scene = scene

# Create tooltip manager
tips = TooltipManager()

# Create some items with tooltips
sword_frame = mcrfpy.Frame(pos=(100, 100), size=(64, 64))
sword_frame.fill_color = mcrfpy.Color(80, 60, 40)
sword_frame.outline = 2
sword_frame.outline_color = mcrfpy.Color(120, 100, 80)
scene.children.append(sword_frame)

tips.register(
    sword_frame,
    "A rusty but reliable blade.\nDamage: 5-10\nSpeed: Fast",
    title="Iron Sword"
)

shield_frame = mcrfpy.Frame(pos=(180, 100), size=(64, 64))
shield_frame.fill_color = mcrfpy.Color(60, 60, 80)
shield_frame.outline = 2
shield_frame.outline_color = mcrfpy.Color(100, 100, 120)
scene.children.append(shield_frame)

tips.register(
    shield_frame,
    "Blocks incoming attacks.\nDefense: +5\nWeight: Medium",
    title="Steel Shield"
)

# Add tooltip last for top layer
tips.add_to_scene(scene.children)
```

## Inline Tooltip (Attached to Element)

Sometimes you want tooltips that appear adjacent to elements rather than following the cursor:

```python
import mcrfpy

def create_info_icon(x, y, tooltip_text, ui):
    """
    Create an info icon that shows tooltip on hover.

    Args:
        x, y: Position of the icon
        tooltip_text: Text to show
        ui: Scene UI to add elements to
    """
    # Info icon (small circle with "i")
    icon = mcrfpy.Frame(pos=(x, y), size=(20, 20))
    icon.fill_color = mcrfpy.Color(70, 130, 180)
    icon.outline = 1
    icon.outline_color = mcrfpy.Color(100, 160, 210)

    icon_label = mcrfpy.Caption(text="i", pos=(x + 6, y + 2))
    icon_label.fill_color = mcrfpy.Color(255, 255, 255)

    # Tooltip (positioned to the right of icon)
    tip_frame = mcrfpy.Frame(pos=(x + 25, y - 5), size=(180, 50))
    tip_frame.fill_color = mcrfpy.Color(40, 40, 55, 240)
    tip_frame.outline = 1
    tip_frame.outline_color = mcrfpy.Color(80, 80, 100)
    tip_frame.visible = False

    tip_text = mcrfpy.Caption(text=tooltip_text, pos=(x + 33, y + 3))
    tip_text.fill_color = mcrfpy.Color(220, 220, 220)
    tip_text.visible = False

    # Hover behavior — enter/exit fire directly, no polling needed
    def on_icon_enter(pos):
        tip_frame.visible = True
        tip_text.visible = True

    def on_icon_exit(pos):
        tip_frame.visible = False
        tip_text.visible = False

    icon.on_enter = on_icon_enter
    icon.on_exit = on_icon_exit

    # Add to scene
    ui.append(icon)
    ui.append(icon_label)
    ui.append(tip_frame)
    ui.append(tip_text)

    return icon


# Usage
scene = mcrfpy.Scene("info_demo")
mcrfpy.current_scene = scene

# Setting with info icon
setting_label = mcrfpy.Caption(text="Difficulty:", pos=(100, 100))
setting_label.fill_color = mcrfpy.Color(200, 200, 200)
scene.children.append(setting_label)

create_info_icon(200, 98, "Affects enemy\nHP and damage", scene.children)
```

## McRogueFace-Specific Considerations

1. **Hover Callbacks Are Native**: `on_enter`, `on_exit`, and `on_move` are real per-element callbacks maintained by the engine's mouse tracking — you don't need to fake hover detection through `on_click`, and you don't need a `Timer` just to notice the mouse left an element.

2. **`hovered` Property**: Every drawable also exposes a read-only `element.hovered` boolean if you prefer to poll state from a `Timer` loop instead of registering `on_enter`/`on_exit` callbacks (useful when many elements share one piece of update logic).

3. **Z-Order for Tooltips**: Always add tooltip frames last to ensure they render on top. If you add elements dynamically, you may need to remove and re-add the tooltip.

4. **`mcrfpy.automation.position()`**: Still useful for automated testing/screenshots, but not needed for ordinary hover detection now that `on_enter`/`on_exit`/`on_move` exist.

5. **Delay Timers Are Still Useful**: A `Timer` remains the right tool when you want a *deliberate delay* before showing a tooltip (as in `TooltipManager.hover_delay` above) — that's a UX choice, not a hover-detection workaround.

6. **Visibility Property**: Use `element.visible = False` to hide without removing from scene. This is more efficient than remove/append cycles.

## Complete Example

```python
import mcrfpy

scene = mcrfpy.Scene("game")
mcrfpy.current_scene = scene

# Background
bg = mcrfpy.Frame(pos=(0, 0), size=(1024, 768))
bg.fill_color = mcrfpy.Color(25, 25, 35)
scene.children.append(bg)

class TooltipManager:
    """Manages tooltips for multiple UI elements."""

    def __init__(self):
        self.elements = {}
        self.tooltip_frame = None
        self.tooltip_text = None
        self.current_element = None
        self.hover_delay = 300
        self.pending_element = None
        self.pending_x = 0
        self.pending_y = 0
        self._create_tooltip()

    def _create_tooltip(self):
        self.tooltip_frame = mcrfpy.Frame(pos=(0, 0), size=(200, 60))
        self.tooltip_frame.fill_color = mcrfpy.Color(30, 30, 45, 245)
        self.tooltip_frame.outline = 1
        self.tooltip_frame.outline_color = mcrfpy.Color(80, 80, 100)
        self.tooltip_frame.visible = False

        self.tooltip_text = mcrfpy.Caption(text="", pos=(0, 0))
        self.tooltip_text.fill_color = mcrfpy.Color(255, 255, 230)
        self.tooltip_text.visible = False

    def register(self, element, text, title=None):
        self.elements[id(element)] = {'element': element, 'text': text, 'title': title}

        def on_enter(pos):
            self.pending_element = element
            self.pending_x, self.pending_y = pos.x, pos.y

            def show_after_delay(timer, runtime):
                if self.pending_element is element:
                    self._show_tooltip(element, self.pending_x, self.pending_y)

            mcrfpy.Timer(f"tooltip_delay_{id(self)}", show_after_delay, self.hover_delay)

        def on_exit(pos):
            if self.pending_element is element:
                self.pending_element = None
            if self.current_element is element:
                self.hide()

        element.on_enter = on_enter
        element.on_exit = on_exit

    def _show_tooltip(self, element, x, y):
        elem_id = id(element)
        if elem_id not in self.elements:
            return
        data = self.elements[elem_id]

        content = (data['title'] + "\n" if data.get('title') else "") + data['text']
        self.tooltip_text.text = content

        lines = content.split('\n')
        max_width = max(len(line) for line in lines) * 8 + 20
        height = len(lines) * 18 + 15
        self.tooltip_frame.w = min(300, max(100, max_width))
        self.tooltip_frame.h = height

        self.tooltip_frame.x = x + 20
        self.tooltip_frame.y = y + 20
        if self.tooltip_frame.x + self.tooltip_frame.w > 1000:
            self.tooltip_frame.x = x - self.tooltip_frame.w - 10
        if self.tooltip_frame.y + self.tooltip_frame.h > 750:
            self.tooltip_frame.y = y - self.tooltip_frame.h - 10

        self.tooltip_text.x = self.tooltip_frame.x + 10
        self.tooltip_text.y = self.tooltip_frame.y + 8

        self.tooltip_frame.visible = True
        self.tooltip_text.visible = True
        self.current_element = element

    def hide(self):
        self.tooltip_frame.visible = False
        self.tooltip_text.visible = False
        self.current_element = None
        self.pending_element = None

    def add_to_scene(self, ui):
        ui.append(self.tooltip_frame)
        ui.append(self.tooltip_text)


# Create inventory slots with tooltips
class InventorySlot:
    def __init__(self, x, y, item_name, item_desc, tooltip_mgr):
        self.frame = mcrfpy.Frame(pos=(x, y), size=(50, 50))
        self.frame.fill_color = mcrfpy.Color(50, 50, 60)
        self.frame.outline = 1
        self.frame.outline_color = mcrfpy.Color(80, 80, 90)

        self.label = mcrfpy.Caption(text=item_name[:3], pos=(x + 10, y + 15))
        self.label.fill_color = mcrfpy.Color(200, 200, 200)

        tooltip_mgr.register(self.frame, item_desc, title=item_name)

    def add_to_scene(self, ui):
        ui.append(self.frame)
        ui.append(self.label)

# Setup tooltip manager
tips = TooltipManager()

# Create inventory
items = [
    ("Health Potion", "Restores 50 HP\nConsumable"),
    ("Mana Crystal", "Restores 30 MP\nConsumable"),
    ("Iron Key", "Opens iron doors\nQuest Item"),
    ("Gold Ring", "Worth 100 gold\nSell to merchant"),
]

slots = []
for i, (name, desc) in enumerate(items):
    slot = InventorySlot(100 + i * 60, 100, name, desc, tips)
    slot.add_to_scene(scene.children)
    slots.append(slot)

# Add tooltip last
tips.add_to_scene(scene.children)
```
