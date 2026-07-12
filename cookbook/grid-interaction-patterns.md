---
title: Grid Interaction Patterns
mcrf:
  objects: [Grid, Entity, ColorLayer, TileLayer, Frame, Caption, MouseButton, InputState, Key, Vector]
  diataxis: howto
  disposition: migrated-from-wiki-needs-review
---

# Grid Interaction Patterns

Patterns for handling mouse and keyboard interaction with Grids, cells, and entities. These patterns build on the grid-specific event handlers.

**Related Pages:**
- Grid System - Grid architecture and layers
- Entity Management - Entity behavior patterns
- Input and Events - General event handling

---

## Grid Cell Events

Grids provide cell-level mouse events in addition to standard UIDrawable events:

| Property | Signature | Description |
|----------|-----------|-------------|
| `on_cell_click` | `(cell_pos: Vector, button: MouseButton, action: InputState) -> None` | Cell clicked |
| `on_cell_enter` | `(cell_pos: Vector) -> None` | Mouse enters cell |
| `on_cell_exit` | `(cell_pos: Vector) -> None` | Mouse leaves cell |
| `hovered_cell` | `(x, y)` or `None` | Currently hovered cell (read-only) |

Cell positions arrive as `Vector` objects. Use `int(cell_pos.x)`, `int(cell_pos.y)` to get grid coordinates.

---

## Setup Template

Most grid interaction patterns fit into this structure:

```python
import mcrfpy

# Scene setup
scene = mcrfpy.Scene("game")
ui = scene.children

# Load tileset texture
texture = mcrfpy.Texture("assets/sprites/tileset.png", 16, 16)

# Create layers
terrain = mcrfpy.TileLayer(name="terrain", z_index=-2, texture=texture)
highlight = mcrfpy.ColorLayer(name="highlight", z_index=-1)
overlay = mcrfpy.ColorLayer(name="overlay", z_index=1)

# Create grid with layers
grid = mcrfpy.Grid(
    grid_size=(20, 15),
    pos=(50, 50),
    size=(640, 480),
    layers=[terrain, highlight, overlay]
)
grid.fill_color = mcrfpy.Color(20, 20, 30)
ui.append(grid)

# Create player entity
player = mcrfpy.Entity(grid_pos=(10, 7), sprite_index=0)
grid.entities.append(player)

# Wire up events (patterns below fill these in)
# grid.on_cell_click = ...
# grid.on_cell_enter = ...
# grid.on_cell_exit = ...

mcrfpy.current_scene = scene
```

---

## Cell Hover Highlighting

Show which cell the mouse is over using a ColorLayer.

```python
current_highlight = [None]

def on_cell_enter(cell_pos):
    x, y = int(cell_pos.x), int(cell_pos.y)
    highlight.set((x, y), mcrfpy.Color(255, 255, 255, 40))
    current_highlight[0] = (x, y)

def on_cell_exit(cell_pos):
    x, y = int(cell_pos.x), int(cell_pos.y)
    highlight.set((x, y), mcrfpy.Color(0, 0, 0, 0))
    current_highlight[0] = None

grid.on_cell_enter = on_cell_enter
grid.on_cell_exit = on_cell_exit
```

---

## Cell Click Actions

Respond to clicks on specific cells. Callbacks receive `(cell_pos, button, action)`.

```python
def on_cell_click(cell_pos, button, action):
    x, y = int(cell_pos.x), int(cell_pos.y)
    point = grid.at(x, y)

    if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
        if point.walkable:
            player.grid_x = x
            player.grid_y = y

    elif button == mcrfpy.MouseButton.RIGHT and action == mcrfpy.InputState.PRESSED:
        # Inspect cell
        show_cell_info(x, y, point)

    elif button == mcrfpy.MouseButton.MIDDLE and action == mcrfpy.InputState.PRESSED:
        # Toggle walkability (level editor)
        point.walkable = not point.walkable

grid.on_cell_click = on_cell_click
```

---

## WASD Movement

Use `scene.on_key` with Key enums for movement.

```python
move_map = {
    mcrfpy.Key.W: (0, -1),
    mcrfpy.Key.A: (-1, 0),
    mcrfpy.Key.S: (0, 1),
    mcrfpy.Key.D: (1, 0),
}

def handle_key(key, action):
    if action != mcrfpy.InputState.PRESSED:
        return
    if key in move_map:
        dx, dy = move_map[key]
        new_x = int(player.grid_x + dx)
        new_y = int(player.grid_y + dy)
        point = player.grid.at(new_x, new_y)
        if point and point.walkable:
            player.grid_x = new_x
            player.grid_y = new_y

scene.on_key = handle_key
```

### Smooth Animated Movement

For visual smoothness, animate the entity position:

```python
def handle_key(key, action):
    if action != mcrfpy.InputState.PRESSED:
        return
    if key in move_map:
        dx, dy = move_map[key]
        new_x = int(player.grid_x + dx)
        new_y = int(player.grid_y + dy)
        point = player.grid.at(new_x, new_y)
        if point and point.walkable:
            player.animate("x", float(new_x), 0.15, mcrfpy.Easing.EASE_OUT_QUAD)
            player.animate("y", float(new_y), 0.15, mcrfpy.Easing.EASE_OUT_QUAD)
            player.grid_x = new_x
            player.grid_y = new_y

scene.on_key = handle_key
```

---

## Entity Selection

Click to select entities using a ColorLayer overlay.

```python
selected = [None]

def select_entity(entity):
    # Clear previous selection
    if selected[0]:
        ex, ey = int(selected[0].grid_x), int(selected[0].grid_y)
        overlay.set((ex, ey), mcrfpy.Color(0, 0, 0, 0))

    selected[0] = entity

    if entity:
        overlay.set((int(entity.grid_x), int(entity.grid_y)),
                     mcrfpy.Color(255, 200, 0, 80))

def on_cell_click(cell_pos, button, action):
    if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
        x, y = int(cell_pos.x), int(cell_pos.y)
        for entity in grid.entities:
            if int(entity.grid_x) == x and int(entity.grid_y) == y:
                select_entity(entity)
                return
        select_entity(None)

grid.on_cell_click = on_cell_click
```

---

## Path Preview

Show pathfinding path on hover using a ColorLayer.

```python
current_path_cells = []

def show_path_to(target_x, target_y):
    global current_path_cells
    # Clear previous path
    for cx, cy in current_path_cells:
        highlight.set((cx, cy), mcrfpy.Color(0, 0, 0, 0))
    current_path_cells = []

    # Calculate path
    path = grid.find_path(
        (int(player.grid_x), int(player.grid_y)),
        (target_x, target_y)
    )
    if not path:
        return

    # Draw path cells
    i = 0
    while len(path) > 0:
        step = path.walk()
        if step:
            x, y = int(step.x), int(step.y)
            alpha = max(30, 100 - (i * 5))
            highlight.set((x, y), mcrfpy.Color(100, 200, 255, alpha))
            current_path_cells.append((x, y))
            i += 1

def on_cell_enter(cell_pos):
    show_path_to(int(cell_pos.x), int(cell_pos.y))

grid.on_cell_enter = on_cell_enter
```

---

## Tile Inspector Panel

Click a cell to show information in a side panel.

```python
# Create inspector UI
inspector = mcrfpy.Frame(pos=(700, 50), size=(200, 150),
                          fill_color=mcrfpy.Color(30, 30, 40, 230))
inspector.outline = 1
inspector.outline_color = mcrfpy.Color(80, 80, 100)
inspector.visible = False
ui.append(inspector)

title = mcrfpy.Caption(text="Cell Info", pos=(10, 8))
title.fill_color = mcrfpy.Color(180, 180, 200)
inspector.children.append(title)

info_lines = []
for i in range(4):
    line = mcrfpy.Caption(text="", pos=(10, 30 + i * 20))
    line.fill_color = mcrfpy.Color(160, 160, 180)
    inspector.children.append(line)
    info_lines.append(line)

def on_cell_click(cell_pos, button, action):
    if button == mcrfpy.MouseButton.LEFT and action == mcrfpy.InputState.PRESSED:
        x, y = int(cell_pos.x), int(cell_pos.y)
        point = grid.at(x, y)

        title.text = f"Cell ({x}, {y})"
        info_lines[0].text = f"Walkable: {point.walkable}"
        info_lines[1].text = f"Transparent: {point.transparent}"

        entities_here = [e for e in grid.entities
                         if int(e.grid_x) == x and int(e.grid_y) == y]
        info_lines[2].text = f"Entities: {len(entities_here)}"

        if entities_here:
            info_lines[3].text = f"  {entities_here[0].name or 'unnamed'}"
        else:
            info_lines[3].text = ""

        inspector.visible = True

grid.on_cell_click = on_cell_click
```

---

## Related Pages

- Entity Management - Entity behavior and pathfinding
- Grid System - Layer management and rendering
- UI Widget Patterns - Non-grid UI patterns
- Input and Events - Event API reference

---

*Last updated: 2026-02-07*
