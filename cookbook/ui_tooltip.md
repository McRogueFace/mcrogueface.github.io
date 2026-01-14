# Tooltip on Hover

Tooltips provide contextual information when hovering over UI elements. This recipe shows how to use Frame click handlers with mouse events to show and hide tooltip overlays.

## The Pattern

McRogueFace provides hover detection through the `click` callback on UI elements. While the name suggests clicks, this callback also receives mouse movement events. The key is checking the `action` parameter:

- `action == "start"` - Mouse button pressed
- `action == "end"` - Mouse button released
- `action == "move"` - Mouse moved within element bounds

Additionally, you can use:
- `frame.on_enter` - Called when mouse enters the frame (not yet implemented in all versions)
- `frame.on_exit` - Called when mouse leaves the frame (not yet implemented in all versions)

For broader compatibility, we'll primarily use the click handler with coordinate checking.

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
        self.frame = mcrfpy.Frame(0, 0, width, 30)
        self.frame.fill_color = mcrfpy.Color(40, 40, 50, 240)
        self.frame.outline = 1
        self.frame.outline_color = mcrfpy.Color(100, 100, 120)
        self.frame.visible = False

        # Tooltip text
        self.caption = mcrfpy.Caption(text=text, x=5, y=5)
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
    original_click = element.click if hasattr(element, 'click') else None

    def on_hover(x, y, button, action):
        # Show tooltip on any interaction with the element
        if tooltip_text:
            tooltip.set_text(tooltip_text)
        tooltip.show(x, y)

        # Call original click handler if it exists
        if original_click and action in ("start", "end"):
            original_click(x, y, button, action)

    element.click = on_hover


# Usage Example
scene = mcrfpy.Scene("tooltip_demo")

# Create some buttons
button1 = mcrfpy.Frame(100, 100, 120, 40)
button1.fill_color = mcrfpy.Color(60, 60, 100)
button1.outline = 2
button1.outline_color = mcrfpy.Color(100, 100, 150)
scene.children.append(button1)

btn1_label = mcrfpy.Caption(text="Attack", x=125, y=112)
btn1_label.fill_color = mcrfpy.Color(255, 255, 255)
scene.children.append(btn1_label)

button2 = mcrfpy.Frame(100, 160, 120, 40)
button2.fill_color = mcrfpy.Color(60, 100, 60)
button2.outline = 2
button2.outline_color = mcrfpy.Color(100, 150, 100)
scene.children.append(button2)

btn2_label = mcrfpy.Caption(text="Defend", x=125, y=172)
btn2_label.fill_color = mcrfpy.Color(255, 255, 255)
scene.children.append(btn2_label)

# Create shared tooltip (add last for top layer)
tooltip = Tooltip("", width=250)
tooltip.add_to_scene(scene.children)

# Make buttons hoverable
make_hoverable(button1, tooltip, "Deal damage to the enemy")
make_hoverable(button2, tooltip, "Reduce incoming damage by 50%")

# Hide tooltip when mouse leaves all elements
# This requires tracking mouse position globally
last_hover_element = None

def global_mouse_check(timer, runtime):
    """Check if mouse is still over a hoverable element."""
    from mcrfpy import automation
    mx, my = automation.position()

    # Check if over any hoverable element
    over_element = False
    for elem in [button1, button2]:
        if (elem.x <= mx <= elem.x + elem.w and
            elem.y <= my <= elem.y + elem.h):
            over_element = True
            break

    if not over_element and tooltip.visible:
        tooltip.hide()

mcrfpy.Timer("tooltip_check", global_mouse_check, 100)
scene.activate()
```

## Tooltip Manager for Multiple Elements

A more robust system for managing tooltips across many elements:

```python
import mcrfpy

class TooltipManager:
    """Manages tooltips for multiple UI elements."""

    def __init__(self):
        self.elements = {}  # element -> tooltip_text mapping
        self.tooltip_frame = None
        self.tooltip_text = None
        self.current_element = None
        self.hover_delay = 500  # ms before showing tooltip
        self.hover_timer = None
        self.pending_element = None

        self._create_tooltip()

    def _create_tooltip(self):
        """Create the tooltip UI elements."""
        self.tooltip_frame = mcrfpy.Frame(0, 0, 200, 60)
        self.tooltip_frame.fill_color = mcrfpy.Color(30, 30, 45, 245)
        self.tooltip_frame.outline = 1
        self.tooltip_frame.outline_color = mcrfpy.Color(80, 80, 100)
        self.tooltip_frame.visible = False

        self.tooltip_text = mcrfpy.Caption(text="", x=0, y=0)
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

        # Set up hover detection
        def make_handler(elem):
            def handler(x, y, button, action):
                self._on_element_interact(elem, x, y, button, action)
            return handler

        element.click = make_handler(element)

    def _on_element_interact(self, element, x, y, button, action):
        """Handle mouse interaction with registered element."""
        elem_id = id(element)

        if elem_id not in self.elements:
            return

        # Cancel any pending tooltip by invalidating timer
        if self.hover_timer:
            self.hover_timer = None  # Timer callbacks check this

        # Start delay timer for showing tooltip
        self.pending_element = element
        self.pending_x = x
        self.pending_y = y

        timer_name = f"tooltip_delay_{id(self)}"
        self.hover_timer = timer_name

        def show_after_delay(timer, runtime):
            if self.pending_element == element:
                self._show_tooltip(element, self.pending_x, self.pending_y)
            self.hover_timer = None

        mcrfpy.Timer(timer_name, show_after_delay, self.hover_delay)

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

        # Invalidate pending timer (callbacks check hover_timer)
        self.hover_timer = None

    def add_to_scene(self, ui):
        """Add tooltip to scene (call last for top layer)."""
        ui.append(self.tooltip_frame)
        ui.append(self.tooltip_text)

    def update(self, mouse_x, mouse_y):
        """
        Call periodically to check if mouse left current element.

        Args:
            mouse_x, mouse_y: Current mouse position
        """
        if not self.current_element:
            return

        elem = self.current_element
        if not (elem.x <= mouse_x <= elem.x + elem.w and
                elem.y <= mouse_y <= elem.y + elem.h):
            self.hide()


# Usage
scene = mcrfpy.Scene("demo")

# Create tooltip manager
tips = TooltipManager()

# Create some items with tooltips
sword_frame = mcrfpy.Frame(100, 100, 64, 64)
sword_frame.fill_color = mcrfpy.Color(80, 60, 40)
sword_frame.outline = 2
sword_frame.outline_color = mcrfpy.Color(120, 100, 80)
scene.children.append(sword_frame)

tips.register(
    sword_frame,
    "A rusty but reliable blade.\nDamage: 5-10\nSpeed: Fast",
    title="Iron Sword"
)

shield_frame = mcrfpy.Frame(180, 100, 64, 64)
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

# Update loop to check mouse position
def update_tooltips(timer, runtime):
    from mcrfpy import automation
    x, y = automation.position()
    tips.update(x, y)

mcrfpy.Timer("tooltip_update", update_tooltips, 50)
scene.activate()
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
    icon = mcrfpy.Frame(x, y, 20, 20)
    icon.fill_color = mcrfpy.Color(70, 130, 180)
    icon.outline = 1
    icon.outline_color = mcrfpy.Color(100, 160, 210)

    icon_label = mcrfpy.Caption(text="i", x=x + 6, y=y + 2)
    icon_label.fill_color = mcrfpy.Color(255, 255, 255)

    # Tooltip (positioned to the right of icon)
    tip_frame = mcrfpy.Frame(x + 25, y - 5, 180, 50)
    tip_frame.fill_color = mcrfpy.Color(40, 40, 55, 240)
    tip_frame.outline = 1
    tip_frame.outline_color = mcrfpy.Color(80, 80, 100)
    tip_frame.visible = False

    tip_text = mcrfpy.Caption(text=tooltip_text, x=x + 33, y=y + 3)
    tip_text.fill_color = mcrfpy.Color(220, 220, 220)
    tip_text.visible = False

    # Hover behavior
    def on_icon_hover(mx, my, button, action):
        tip_frame.visible = True
        tip_text.visible = True

    icon.click = on_icon_hover

    # Track when to hide
    def check_hover(timer, runtime):
        from mcrfpy import automation
        mx, my = automation.position()
        if not (icon.x <= mx <= icon.x + icon.w and
                icon.y <= my <= icon.y + icon.h):
            if tip_frame.visible:
                tip_frame.visible = False
                tip_text.visible = False

    timer_name = f"info_hover_{id(icon)}"
    mcrfpy.Timer(timer_name, check_hover, 100)

    # Add to scene
    ui.append(icon)
    ui.append(icon_label)
    ui.append(tip_frame)
    ui.append(tip_text)

    return icon


# Usage
scene = mcrfpy.Scene("info_demo")

# Setting with info icon
setting_label = mcrfpy.Caption(text="Difficulty:", x=100, y=100)
setting_label.fill_color = mcrfpy.Color(200, 200, 200)
scene.children.append(setting_label)

create_info_icon(200, 98, "Affects enemy\nHP and damage", scene.children)
scene.activate()
```

## McRogueFace-Specific Considerations

1. **Click Handler Limitations**: The `click` callback fires for mouse interaction but doesn't distinguish hover vs click perfectly. Use button/action parameters and mouse position to determine intent.

2. **No Native Hover Events**: If `on_enter`/`on_exit` are not available in your version, implement hover detection by periodically checking mouse position against element bounds.

3. **Z-Order for Tooltips**: Always add tooltip frames last to ensure they render on top. If you add elements dynamically, you may need to remove and re-add the tooltip.

4. **Automation Module**: Use `mcrfpy.automation.position()` to get current mouse position for hover detection.

5. **Performance**: Timer-based hover checks add overhead. Use reasonable intervals (50-100ms) and clean up timers when elements are removed.

6. **Visibility Property**: Use `element.visible = False` to hide without removing from scene. This is more efficient than remove/append cycles.

## Complete Example

```python
import mcrfpy

scene = mcrfpy.Scene("game")

# Background
bg = mcrfpy.Frame(0, 0, 1024, 768)
bg.fill_color = mcrfpy.Color(25, 25, 35)
scene.children.append(bg)

# Create inventory slots with tooltips
class InventorySlot:
    def __init__(self, x, y, item_name, item_desc, tooltip_mgr):
        self.frame = mcrfpy.Frame(x, y, 50, 50)
        self.frame.fill_color = mcrfpy.Color(50, 50, 60)
        self.frame.outline = 1
        self.frame.outline_color = mcrfpy.Color(80, 80, 90)

        self.label = mcrfpy.Caption(text=item_name[:3], x=x + 10, y=y + 15)
        self.label.fill_color = mcrfpy.Color(200, 200, 200)

        tooltip_mgr.register(self.frame, item_desc, title=item_name)

    def add_to_scene(self, ui):
        ui.append(self.frame)
        ui.append(self.label)

# Setup tooltip manager
tips = TooltipManager()
tips.hover_delay = 300

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

# Update loop
def update(timer, runtime):
    from mcrfpy import automation
    x, y = automation.position()
    tips.update(x, y)

mcrfpy.Timer("update", update, 50)
scene.activate()
```
