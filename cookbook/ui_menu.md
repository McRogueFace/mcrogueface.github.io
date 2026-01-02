# Selection Menu Widget

Keyboard-navigable menus are essential for any game. This recipe shows how to build a reusable menu system using Frame and Caption elements with keyboard input handling.

## The Pattern

A selection menu consists of:
1. **Container Frame** - Background panel holding the menu
2. **Option Captions** - Text for each menu option
3. **Selection index** - Tracks which option is highlighted
4. **Visual feedback** - Changes color/style of selected option
5. **Callback system** - Executes actions when options are selected

## Basic Implementation

```python
import mcrfpy

class Menu:
    """A keyboard-navigable menu widget."""

    def __init__(self, x, y, options, on_select, title=None):
        """
        Create a menu.

        Args:
            x, y: Position on screen
            options: List of option strings
            on_select: Callback function(index, option_text)
            title: Optional title string
        """
        self.x = x
        self.y = y
        self.options = options
        self.on_select = on_select
        self.selected_index = 0

        # Style settings
        self.padding = 15
        self.line_height = 30
        self.width = 250

        # Colors
        self.color_normal = mcrfpy.Color(200, 200, 200)
        self.color_selected = mcrfpy.Color(255, 255, 100)
        self.color_bg = mcrfpy.Color(30, 30, 50, 230)

        # Calculate frame height
        title_offset = self.line_height if title else 0
        height = self.padding * 2 + len(options) * self.line_height + title_offset

        # Create container frame
        self.frame = mcrfpy.Frame(x, y, self.width, height)
        self.frame.fill_color = self.color_bg
        self.frame.outline = 2
        self.frame.outline_color = mcrfpy.Color(100, 100, 150)

        # Create title if provided
        self.title_caption = None
        if title:
            self.title_caption = mcrfpy.Caption(
                title,
                mcrfpy.default_font,
                x + self.padding,
                y + self.padding
            )
            self.title_caption.fill_color = mcrfpy.Color(255, 255, 255)

        # Create option captions
        self.option_captions = []
        for i, option in enumerate(options):
            caption_y = y + self.padding + title_offset + i * self.line_height
            caption = mcrfpy.Caption(
                option,
                mcrfpy.default_font,
                x + self.padding,
                caption_y
            )
            caption.fill_color = self.color_normal
            self.option_captions.append(caption)

        # Update visual selection
        self._update_selection()

    def _update_selection(self):
        """Update visual highlight for selected option."""
        for i, caption in enumerate(self.option_captions):
            if i == self.selected_index:
                caption.fill_color = self.color_selected
                caption.text = "> " + self.options[i]
            else:
                caption.fill_color = self.color_normal
                caption.text = "  " + self.options[i]

    def move_up(self):
        """Move selection up (with wraparound)."""
        self.selected_index = (self.selected_index - 1) % len(self.options)
        self._update_selection()

    def move_down(self):
        """Move selection down (with wraparound)."""
        self.selected_index = (self.selected_index + 1) % len(self.options)
        self._update_selection()

    def select(self):
        """Trigger the callback for the current selection."""
        if self.on_select:
            self.on_select(self.selected_index, self.options[self.selected_index])

    def add_to_scene(self, ui):
        """Add menu to scene UI."""
        ui.append(self.frame)
        if self.title_caption:
            ui.append(self.title_caption)
        for caption in self.option_captions:
            ui.append(caption)

    def handle_key(self, key):
        """
        Handle keyboard input.

        Args:
            key: Key name string

        Returns:
            True if key was handled, False otherwise
        """
        if key == "Up" or key == "W":
            self.move_up()
            return True
        elif key == "Down" or key == "S":
            self.move_down()
            return True
        elif key == "Return" or key == "Space":
            self.select()
            return True
        return False


# Usage Example
mcrfpy.createScene("menu_demo")
mcrfpy.setScene("menu_demo")
ui = mcrfpy.sceneUI("menu_demo")

def on_menu_select(index, option):
    print(f"Selected: {option} (index {index})")
    if option == "Start Game":
        mcrfpy.setScene("game")
    elif option == "Options":
        mcrfpy.setScene("options")
    elif option == "Quit":
        mcrfpy.exit()

menu = Menu(
    300, 200,
    ["Start Game", "Options", "Quit"],
    on_menu_select,
    title="Main Menu"
)
menu.add_to_scene(ui)

def handle_keys(key, state):
    if state != "start":
        return
    menu.handle_key(key)

mcrfpy.keypressScene(handle_keys)
```

## Enhanced Menu with Submenus and Descriptions

A more feature-rich version with option descriptions and submenu support:

```python
import mcrfpy

class EnhancedMenu:
    """Menu with descriptions, submenus, and visual polish."""

    def __init__(self, x, y, options, title=None):
        """
        Create an enhanced menu.

        Args:
            x, y: Position
            options: List of dicts with keys:
                     'label': Display text
                     'action': Callback function (optional)
                     'description': Help text (optional)
                     'submenu': EnhancedMenu instance (optional)
                     'enabled': Boolean (optional, default True)
        """
        self.x = x
        self.y = y
        self.options = options
        self.title = title
        self.selected_index = 0
        self.active = True
        self.parent_menu = None

        # Layout
        self.padding = 20
        self.line_height = 32
        self.width = 300

        # Colors
        self.colors = {
            'bg': mcrfpy.Color(25, 25, 40, 240),
            'border': mcrfpy.Color(80, 80, 120),
            'title': mcrfpy.Color(255, 220, 100),
            'normal': mcrfpy.Color(180, 180, 180),
            'selected': mcrfpy.Color(255, 255, 255),
            'disabled': mcrfpy.Color(80, 80, 80),
            'description': mcrfpy.Color(150, 150, 180),
            'highlight_bg': mcrfpy.Color(60, 60, 100),
        }

        self._build_ui()

    def _build_ui(self):
        """Construct UI elements."""
        title_offset = self.line_height + 10 if self.title else 0
        desc_height = 50  # Space for description
        height = (
            self.padding * 2 +
            len(self.options) * self.line_height +
            title_offset +
            desc_height
        )

        # Main frame
        self.frame = mcrfpy.Frame(self.x, self.y, self.width, height)
        self.frame.fill_color = self.colors['bg']
        self.frame.outline = 2
        self.frame.outline_color = self.colors['border']

        # Title
        self.title_caption = None
        if self.title:
            self.title_caption = mcrfpy.Caption(
                self.title,
                mcrfpy.default_font,
                self.x + self.padding,
                self.y + self.padding
            )
            self.title_caption.fill_color = self.colors['title']

        # Selection highlight frame
        self.highlight = mcrfpy.Frame(
            self.x + 5,
            self.y + self.padding + title_offset,
            self.width - 10,
            self.line_height
        )
        self.highlight.fill_color = self.colors['highlight_bg']
        self.highlight.outline = 0

        # Option labels
        self.option_captions = []
        for i, opt in enumerate(self.options):
            caption_y = self.y + self.padding + title_offset + i * self.line_height + 5
            caption = mcrfpy.Caption(
                opt.get('label', '???'),
                mcrfpy.default_font,
                self.x + self.padding + 10,
                caption_y
            )
            enabled = opt.get('enabled', True)
            caption.fill_color = self.colors['normal'] if enabled else self.colors['disabled']
            self.option_captions.append(caption)

            # Add arrow for submenus
            if opt.get('submenu'):
                arrow = mcrfpy.Caption(
                    ">",
                    mcrfpy.default_font,
                    self.x + self.width - self.padding - 15,
                    caption_y
                )
                arrow.fill_color = caption.fill_color
                opt['_arrow'] = arrow

        # Description text at bottom
        desc_y = self.y + height - desc_height + 5
        self.description = mcrfpy.Caption(
            "",
            mcrfpy.default_font,
            self.x + self.padding,
            desc_y
        )
        self.description.fill_color = self.colors['description']

        self._update_selection()

    def _update_selection(self):
        """Update visuals for current selection."""
        title_offset = self.line_height + 10 if self.title else 0

        # Move highlight
        self.highlight.y = self.y + self.padding + title_offset + self.selected_index * self.line_height

        # Update caption colors
        for i, caption in enumerate(self.option_captions):
            opt = self.options[i]
            enabled = opt.get('enabled', True)

            if i == self.selected_index:
                caption.fill_color = self.colors['selected'] if enabled else self.colors['disabled']
            else:
                caption.fill_color = self.colors['normal'] if enabled else self.colors['disabled']

        # Update description
        desc = self.options[self.selected_index].get('description', '')
        self.description.text = desc

    def move_up(self):
        """Move selection up, skipping disabled options."""
        if not self.active:
            return

        start = self.selected_index
        while True:
            self.selected_index = (self.selected_index - 1) % len(self.options)
            if self.options[self.selected_index].get('enabled', True):
                break
            if self.selected_index == start:
                break  # All disabled, stay put
        self._update_selection()

    def move_down(self):
        """Move selection down, skipping disabled options."""
        if not self.active:
            return

        start = self.selected_index
        while True:
            self.selected_index = (self.selected_index + 1) % len(self.options)
            if self.options[self.selected_index].get('enabled', True):
                break
            if self.selected_index == start:
                break
        self._update_selection()

    def select(self):
        """Execute the selected option."""
        if not self.active:
            return None

        opt = self.options[self.selected_index]

        if not opt.get('enabled', True):
            return None

        if opt.get('submenu'):
            return opt['submenu']

        if opt.get('action'):
            opt['action']()

        return None

    def back(self):
        """Return to parent menu."""
        return self.parent_menu

    def add_to_scene(self, ui):
        """Add all elements to scene."""
        ui.append(self.frame)
        ui.append(self.highlight)
        if self.title_caption:
            ui.append(self.title_caption)
        for i, caption in enumerate(self.option_captions):
            ui.append(caption)
            if '_arrow' in self.options[i]:
                ui.append(self.options[i]['_arrow'])
        ui.append(self.description)

    def remove_from_scene(self, ui):
        """Remove all elements from scene."""
        elements = [self.frame, self.highlight, self.description]
        if self.title_caption:
            elements.append(self.title_caption)
        elements.extend(self.option_captions)
        for i, opt in enumerate(self.options):
            if '_arrow' in opt:
                elements.append(opt['_arrow'])

        for elem in elements:
            try:
                ui.remove(elem)
            except:
                pass


# Usage with submenus
mcrfpy.createScene("menu")
mcrfpy.setScene("menu")
ui = mcrfpy.sceneUI("menu")

# Create options submenu
options_menu = EnhancedMenu(350, 220, [
    {'label': 'Sound Volume', 'description': 'Adjust sound effects volume'},
    {'label': 'Music Volume', 'description': 'Adjust background music volume'},
    {'label': 'Fullscreen', 'description': 'Toggle fullscreen mode'},
    {'label': 'Back', 'action': lambda: switch_menu(main_menu)},
])
options_menu.title = "Options"

# Create main menu
main_menu = EnhancedMenu(300, 200, [
    {
        'label': 'New Game',
        'description': 'Start a new adventure',
        'action': lambda: print("Starting new game...")
    },
    {
        'label': 'Continue',
        'description': 'Load your saved game',
        'enabled': False,  # Disabled if no save exists
    },
    {
        'label': 'Options',
        'description': 'Configure game settings',
        'submenu': options_menu
    },
    {
        'label': 'Quit',
        'description': 'Exit the game',
        'action': lambda: mcrfpy.exit()
    },
])
main_menu.title = "My Game"

options_menu.parent_menu = main_menu
current_menu = main_menu
main_menu.add_to_scene(ui)

def switch_menu(new_menu):
    global current_menu
    current_menu.remove_from_scene(ui)
    current_menu = new_menu
    current_menu.add_to_scene(ui)

def handle_keys(key, state):
    global current_menu
    if state != "start":
        return

    if key == "Up" or key == "W":
        current_menu.move_up()
    elif key == "Down" or key == "S":
        current_menu.move_down()
    elif key == "Return" or key == "Space":
        result = current_menu.select()
        if result:  # Submenu returned
            switch_menu(result)
    elif key == "Escape":
        parent = current_menu.back()
        if parent:
            switch_menu(parent)

mcrfpy.keypressScene(handle_keys)
```

## Horizontal Menu Bar

For top-of-screen menu bars:

```python
import mcrfpy

class MenuBar:
    """Horizontal menu bar with dropdown submenus."""

    def __init__(self, y=0, items=None):
        """
        Create a menu bar.

        Args:
            y: Y position (usually 0 for top)
            items: List of dicts with 'label' and 'options' keys
        """
        self.y = y
        self.items = items or []
        self.selected_item = 0
        self.dropdown_open = False
        self.dropdown_selected = 0

        self.item_width = 100
        self.height = 30

        # Main bar frame
        self.bar = mcrfpy.Frame(0, y, 1024, self.height)
        self.bar.fill_color = mcrfpy.Color(50, 50, 70)
        self.bar.outline = 0

        # Item captions
        self.item_captions = []
        for i, item in enumerate(items):
            cap = mcrfpy.Caption(
                item['label'],
                mcrfpy.default_font,
                10 + i * self.item_width,
                y + 7
            )
            cap.fill_color = mcrfpy.Color(200, 200, 200)
            self.item_captions.append(cap)

        # Dropdown panel (hidden initially)
        self.dropdown = None
        self.dropdown_captions = []

    def _update_highlight(self):
        """Update visual selection on bar."""
        for i, cap in enumerate(self.item_captions):
            if i == self.selected_item and self.dropdown_open:
                cap.fill_color = mcrfpy.Color(255, 255, 100)
            else:
                cap.fill_color = mcrfpy.Color(200, 200, 200)

    def _show_dropdown(self, ui):
        """Show dropdown for selected item."""
        # Remove existing dropdown
        self._hide_dropdown(ui)

        item = self.items[self.selected_item]
        options = item.get('options', [])

        if not options:
            return

        x = 5 + self.selected_item * self.item_width
        y = self.y + self.height
        width = 150
        height = len(options) * 25 + 10

        self.dropdown = mcrfpy.Frame(x, y, width, height)
        self.dropdown.fill_color = mcrfpy.Color(40, 40, 60, 250)
        self.dropdown.outline = 1
        self.dropdown.outline_color = mcrfpy.Color(80, 80, 100)
        ui.append(self.dropdown)

        self.dropdown_captions = []
        for i, opt in enumerate(options):
            cap = mcrfpy.Caption(
                opt['label'],
                mcrfpy.default_font,
                x + 10,
                y + 5 + i * 25
            )
            cap.fill_color = mcrfpy.Color(200, 200, 200)
            self.dropdown_captions.append(cap)
            ui.append(cap)

        self.dropdown_selected = 0
        self._update_dropdown_highlight()

    def _hide_dropdown(self, ui):
        """Hide dropdown menu."""
        if self.dropdown:
            try:
                ui.remove(self.dropdown)
            except:
                pass
            self.dropdown = None

        for cap in self.dropdown_captions:
            try:
                ui.remove(cap)
            except:
                pass
        self.dropdown_captions = []

    def _update_dropdown_highlight(self):
        """Update dropdown selection highlight."""
        for i, cap in enumerate(self.dropdown_captions):
            if i == self.dropdown_selected:
                cap.fill_color = mcrfpy.Color(255, 255, 100)
            else:
                cap.fill_color = mcrfpy.Color(200, 200, 200)

    def add_to_scene(self, ui):
        ui.append(self.bar)
        for cap in self.item_captions:
            ui.append(cap)

    def handle_key(self, key, ui):
        """Handle keyboard navigation."""
        if not self.dropdown_open:
            if key == "Left":
                self.selected_item = (self.selected_item - 1) % len(self.items)
                self._update_highlight()
            elif key == "Right":
                self.selected_item = (self.selected_item + 1) % len(self.items)
                self._update_highlight()
            elif key == "Return" or key == "Down":
                self.dropdown_open = True
                self._show_dropdown(ui)
                self._update_highlight()
        else:
            if key == "Up":
                options = self.items[self.selected_item].get('options', [])
                self.dropdown_selected = (self.dropdown_selected - 1) % len(options)
                self._update_dropdown_highlight()
            elif key == "Down":
                options = self.items[self.selected_item].get('options', [])
                self.dropdown_selected = (self.dropdown_selected + 1) % len(options)
                self._update_dropdown_highlight()
            elif key == "Return":
                opt = self.items[self.selected_item]['options'][self.dropdown_selected]
                if opt.get('action'):
                    opt['action']()
                self.dropdown_open = False
                self._hide_dropdown(ui)
                self._update_highlight()
            elif key == "Escape":
                self.dropdown_open = False
                self._hide_dropdown(ui)
                self._update_highlight()
```

## McRogueFace-Specific Considerations

1. **Keyboard Input**: The `keypressScene` callback receives key names as strings like "Up", "Down", "Return", "Escape". Handle both arrow keys and WASD for accessibility.

2. **Focus Management**: Only one menu should handle input at a time. Use an `active` flag or a global `current_menu` reference.

3. **Z-Order**: Elements added later render on top. For dropdowns/submenus, add them after the main menu or use `remove` and `append` to bring to front.

4. **State Persistence**: Menus retain their state when hidden. Reset `selected_index` if you want fresh state on re-open.

5. **Key Repeat**: McRogueFace sends "start" and "end" states for key events. Filter to only "start" to avoid double-processing.

## Complete Example

```python
import mcrfpy

# Setup
mcrfpy.createScene("main_menu")
mcrfpy.setScene("main_menu")
ui = mcrfpy.sceneUI("main_menu")

# Background
bg = mcrfpy.Frame(0, 0, 1024, 768)
bg.fill_color = mcrfpy.Color(20, 20, 35)
ui.append(bg)

# Title
title = mcrfpy.Caption("DUNGEON QUEST", mcrfpy.default_font, 350, 100)
title.fill_color = mcrfpy.Color(255, 200, 50)
ui.append(title)

# Menu
def start_game():
    print("Starting game...")

def show_options():
    print("Options...")

menu = Menu(
    362, 250,
    ["New Game", "Continue", "Options", "Quit"],
    lambda i, opt: {
        0: start_game,
        1: lambda: print("Continue..."),
        2: show_options,
        3: mcrfpy.exit
    }.get(i, lambda: None)(),
    title="Main Menu"
)
menu.add_to_scene(ui)

# Input
def on_key(key, state):
    if state != "start":
        return
    menu.handle_key(key)

mcrfpy.keypressScene(on_key)
```
