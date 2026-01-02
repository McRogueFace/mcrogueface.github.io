# McRogueFace API Developer Experience Audit

**Status:** Foundation Research Document
**Date:** 2025-12-29
**Scope:** Full API surface analysis, first-5-minutes experience, gap analysis

---

## Executive Summary

McRogueFace provides a substantial roguelike-focused game engine API with ~35 public classes/functions, built-in FOV/pathfinding algorithms, and an animation system. However, significant documentation/API mismatches exist between the actual API (API_REFERENCE_DYNAMIC.md) and existing documentation (markdown/), creating developer confusion. The "first 5 minutes" experience requires ~15-25 lines of working code, competitive with Pygame but with friction from inconsistent documentation.

**Priority Issues:**
1. Documentation shows non-existent API patterns (critical mismatch)
2. No simple `run()` function - unclear how game loop starts
3. Inconsistent constructor signatures across documentation
4. Missing "batteries" for common roguelike needs (turn system, message log)

---

## 1. First-5-Minutes Analysis

### Minimum Code for Window + Movable @ Symbol

Based on the **actual API** (API_REFERENCE_DYNAMIC.md):

```python
import mcrfpy

# Create scene with grid
mcrfpy.createScene("game")
texture = mcrfpy.Texture("assets/sprites.png", 16, 16)
grid = mcrfpy.Grid(
    pos=(0, 0),
    grid_size=(20, 15),
    texture=texture
)

# Add player entity
player = mcrfpy.Entity(grid_pos=(10, 7), texture=texture, sprite_index=64)
grid.entities.append(player)

# Add to scene
ui = mcrfpy.sceneUI("game")
ui.append(grid)

# Input handler
def on_key(key, pressed):
    if not pressed:
        return
    x, y = player.pos
    if key == "Up": player.pos = (x, y-1)
    elif key == "Down": player.pos = (x, y+1)
    elif key == "Left": player.pos = (x-1, y)
    elif key == "Right": player.pos = (x+1, y)

mcrfpy.keypressScene(on_key)
mcrfpy.setScene("game")
# HOW DOES THE GAME LOOP START? - Not documented
```

**Line Count:** ~20 lines (without game loop start mechanism)

### Friction Points Identified

| Issue | Severity | Description |
|-------|----------|-------------|
| **Game loop start** | CRITICAL | No `mcrfpy.run()` or equivalent documented. How does the game actually start? |
| **Texture path** | HIGH | Must provide texture file but no default roguelike tileset bundled |
| **Constructor confusion** | HIGH | Documentation shows `Caption(x, y, text)` but API shows `Caption(pos, font, text)` |
| **Grid creation** | MEDIUM | Must calculate pixel sizes, no auto-sizing from grid dimensions |
| **Entity parenting** | MEDIUM | Entity requires manual append to grid.entities (not auto-parented) |

### Comparison with Competitors

| Framework | Lines for Window + Movable Character | Main Friction |
|-----------|--------------------------------------|---------------|
| **Pygame** | ~25 lines | Manual event loop, surface management |
| **arcade** | ~30 lines | Boilerplate class structure |
| **tcod** | ~40 lines | Complex console setup |
| **McRogueFace** | ~20 lines* | *Unclear game loop mechanism |

McRogueFace is competitive IF the game loop start mechanism is documented.

---

## 2. API Surface Inventory

### Module-Level Functions (24 total)

| Function | Docstring Quality | Purpose |
|----------|-------------------|---------|
| `createScene(name)` | Good | Create new empty scene |
| `setScene(scene, transition, duration)` | Good | Switch active scene with optional transition |
| `currentScene()` | Good | Get current scene name |
| `sceneUI(scene)` | Good | Get UICollection for scene |
| `keypressScene(handler)` | Good | Set keyboard handler |
| `setTimer(name, handler, interval)` | Good | Create recurring timer |
| `delTimer(name)` | Good | Remove timer |
| `createSoundBuffer(filename)` | Good | Load sound effect |
| `playSound(buffer_id)` | Good | Play loaded sound |
| `loadMusic(filename)` | Good | Load and play music |
| `setMusicVolume(volume)` | Good | Set music volume 0-100 |
| `setSoundVolume(volume)` | Good | Set SFX volume 0-100 |
| `getMusicVolume()` | Good | Get music volume |
| `getSoundVolume()` | Good | Get SFX volume |
| `find(name, scene)` | Good | Find UI element by name |
| `findAll(pattern, scene)` | Good | Find elements by pattern |
| `getMetrics()` | Good | Performance metrics |
| `setScale(multiplier)` | Good | Scale window (DEPRECATED) |
| `setDevConsole(enabled)` | Good | Toggle dev console |
| `exit()` | Good | Exit application |
| `step(dt)` | Good | Advance simulation (headless only) |
| `start_benchmark()` | Good | Start benchmark capture |
| `end_benchmark()` | Good | End benchmark capture |
| `log_benchmark(message)` | Good | Log to benchmark |

**Assessment:** Function-level documentation is generally good. Missing: `run()` or equivalent.

### Classes (26 total)

#### Core UI Classes

| Class | Docstring | Constructor Signature Documented | Notes |
|-------|-----------|----------------------------------|-------|
| `Frame` | Good | Yes | Container with children |
| `Caption` | Good | Yes | Text display |
| `Sprite` | Good | Yes | Single sprite display |
| `Grid` | Good | Yes | Tilemap + entity container |
| `Entity` | Good | Yes | Grid-based game object |

#### Drawable Primitives (NEW in API)

| Class | Docstring | Constructor Signature | Notes |
|-------|-----------|----------------------|-------|
| `Arc` | Good | Yes | Curved line segment |
| `Circle` | Good | Yes | Filled/outlined circle |
| `Line` | Good | Yes | Straight line |
| `Drawable` | Minimal | Base class | Abstract base |

#### Grid System

| Class | Docstring | Notes |
|-------|-----------|-------|
| `GridPoint` | Minimal | Individual tile data - **needs better docs** |
| `GridPointState` | Minimal | Entity visibility state - **needs better docs** |
| `ColorLayer` | Good | Color overlay layer |
| `TileLayer` | Good | Tile index layer |

#### Collections

| Class | Docstring | Notes |
|-------|-----------|-------|
| `UICollection` | Good | Scene UI container |
| `EntityCollection` | Good | Grid entity container |
| `UICollectionIter` | None | Iterator - internal |
| `UIEntityCollectionIter` | None | Iterator - internal |

#### Utility Classes

| Class | Docstring | Notes |
|-------|-----------|-------|
| `Color` | Minimal | RGBA color - **needs method docs** |
| `Vector` | Good | 2D vector with math methods |
| `Font` | Minimal | Font resource - **needs docs** |
| `Texture` | Minimal | Sprite sheet - **needs docs** |
| `Timer` | Good | Timer object (NEW class-based API) |
| `Animation` | Good | Property animation |
| `Scene` | Minimal | OOP scene base class |
| `Window` | Good | Window singleton |
| `FOV` | Minimal | FOV algorithm enum |

### Missing Docstrings / Incomplete Documentation

**CRITICAL - Missing or minimal documentation:**
1. `GridPoint` - What properties? How to use?
2. `GridPointState` - visible/discovered flags underdocumented
3. `Color` - Constructor variants, component access
4. `Font` - How to load, what formats?
5. `Texture` - How sprite indices work, grid layout
6. `FOV` - What algorithms available? (FOV_BASIC, FOV_DIAMOND, etc. mentioned but not enumerated)

---

## 3. Naming Pattern Analysis

### Inconsistencies Found

| Pattern | Examples | Issue |
|---------|----------|-------|
| **camelCase vs snake_case** | `createScene` vs `start_benchmark` | Mixed conventions |
| **Abbreviations** | `pos`, `w`, `h` vs `width`, `height` | Inconsistent abbreviation |
| **Property access** | `entity.pos` (tuple) vs `entity.x, entity.y` (floats) | Dual access patterns |
| **Collection naming** | `UICollection` vs `EntityCollection` | Consistent (good) |
| **get/set patterns** | `getMusicVolume()`/`setMusicVolume()` vs `Window.resolution` property | Mixed patterns |

### Non-Pythonic Patterns

1. **camelCase functions** - Python convention is snake_case
   - `createScene` should be `create_scene`
   - `keypressScene` should be `on_keypress` or `set_key_handler`

2. **Callback naming** - `keypressScene(handler)` is unclear
   - Better: `on_key(handler)` or `register_key_handler(handler)`

3. **Property vs method inconsistency**
   - `entity.pos` is a property (tuple)
   - `entity.path_to(x, y)` is a method
   - Why not `entity.move_to(x, y)` for consistency?

4. **Return type inconsistency**
   - `find()` returns element or None
   - `findAll()` returns list (potentially empty)
   - Good pattern, consistently applied

### Recommended Naming Standardization

For 1.0, consider:
- **Keep camelCase** for backward compatibility OR
- **Add snake_case aliases** for Pythonic access
- Document the chosen convention explicitly

---

## 4. "Batteries Missing" Analysis

What would a roguelike developer expect that isn't there?

### HIGH Priority Missing Features

| Feature | Use Case | Current Workaround |
|---------|----------|-------------------|
| **Turn system** | Traditional roguelike turns | Manual timer + state machine |
| **Message log** | "You hit the goblin for 5 damage" | Custom Caption management |
| **Input modes** | Movement vs menu vs targeting | Manual state tracking |
| **Map generators** | BSP, cellular automata, etc. | Write from scratch |
| **Save/Load** | Game persistence | JSON + manual serialization |

### MEDIUM Priority Missing Features

| Feature | Use Case | Current Workaround |
|---------|----------|-------------------|
| **Scrolling text** | Long messages, dialogue | Not possible without custom code |
| **Tooltip system** | Item/entity descriptions | Custom Frame positioning |
| **Menu widgets** | Selection lists, buttons | Manual Frame + Caption |
| **Health bars** | Entity status display | Custom Frame overlay |
| **Minimap** | Navigation aid | Second Grid with different zoom |

### LOW Priority (Nice to Have)

| Feature | Use Case |
|---------|----------|
| **Particle system** | Spell effects, ambient |
| **Lighting system** | Beyond FOV darkness |
| **Sound positioning** | 3D audio for location |
| **Screen shake** | Impact feedback |
| **Palette swap** | Sprite recoloring |

---

## 5. Cookbook Category Extraction

### Scene Management
- **createScene** - Create game states (menu, gameplay, inventory)
- **setScene** - Transition between states with optional effects
- **currentScene** - Check current state for conditional logic
- **sceneUI** - Access UI elements for dynamic modification

### Grid & Tilemap
- **Grid** - Create tile-based game world
- **Grid.at()** - Access individual tile properties
- **Grid.add_layer()** - Add color/tile overlay layers
- **Grid.compute_fov()** - Calculate field of view
- **Grid.find_path()** - A* pathfinding
- **Grid.compute_dijkstra()** - Distance mapping
- **Grid.entities_in_radius()** - Spatial queries

### Entities & Movement
- **Entity** - Create game objects on grid
- **Entity.path_to()** - Automatic pathfinding movement
- **Entity.visible_entities()** - FOV-based entity detection
- **Entity.update_visibility()** - Refresh FOV state
- **EntityCollection** - Manage multiple entities

### UI Elements
- **Frame** - Containers, panels, windows
- **Caption** - Text labels, dynamic text
- **Sprite** - Icons, decorations
- **Circle/Arc/Line** - Shape drawing

### Animation
- **Animation** - Property tweening
- **Animation.start()** - Begin animation on target
- **Animation.complete()** - Skip to end

### Audio
- **createSoundBuffer** - Load sound effects
- **playSound** - Play loaded sounds
- **loadMusic** - Background music
- **set/getMusicVolume** - Volume control

### Input
- **keypressScene** - Keyboard handling
- **click property** - Mouse handling on elements

### Timing
- **Timer** - Recurring/one-shot callbacks
- **setTimer/delTimer** - Legacy timer API

### Utilities
- **Color** - RGBA colors with lerp, hex conversion
- **Vector** - 2D math (magnitude, normalize, distance)
- **Font/Texture** - Resource loading
- **Window** - Window control, screenshots

---

## 6. Gap Analysis: Impossible Tutorials

### Tutorials That Cannot Be Written

| Tutorial | Blocking Issue |
|----------|---------------|
| **"Hello World in 3 lines"** | No `run()` function documented |
| **"Basic Menu System"** | No keyboard navigation example, unclear click handling |
| **"Save Your Game"** | No serialization helpers, Entity has no `to_dict()` |
| **"Turn-Based Combat"** | No turn system, would require 100+ lines of scaffolding |
| **"Scrolling Message Log"** | No text scrolling, no text wrapping |
| **"Item Tooltips"** | No hover events documented |
| **"Animated Sprites"** | Animation class exists but sprite_index animation unclear |

### Tutorials That Would Be Difficult

| Tutorial | Difficulty | Issue |
|----------|------------|-------|
| **"Fog of War"** | HIGH | FOV exists but GridPointState poorly documented |
| **"Enemy AI"** | MEDIUM | Dijkstra exists but pathfinding integration unclear |
| **"Inventory Grid"** | MEDIUM | Frame.children + click handling needs examples |
| **"Particle Effects"** | HIGH | No particle system, would need manual Sprite management |

### Tutorials That Are Possible

| Tutorial | Notes |
|----------|-------|
| **"Creating a Dungeon"** | Grid + layers well documented |
| **"Moving the Player"** | Entity + keyboard handler clear |
| **"Field of View"** | FOV methods documented |
| **"Pathfinding"** | A* and Dijkstra available |
| **"Scene Transitions"** | setScene with transitions documented |
| **"Playing Sounds"** | Audio API complete |
| **"Custom Animations"** | Animation class documented |

---

## 7. Documentation vs API Mismatches

### CRITICAL Mismatches

| Documentation Says | API Actually Has | Severity |
|-------------------|------------------|----------|
| `Caption(x, y, "text")` | `Caption(pos, font, text, **kwargs)` | HIGH |
| `mcrfpy.bind_keys(handler)` | `mcrfpy.keypressScene(handler)` | HIGH |
| `mcrfpy.run()` | Not found | CRITICAL |
| `grid.set_tile(x, y, index)` | `grid.at(x,y).tilesprite = index` | HIGH |
| `entity.pos = (x, y)` | `entity.pos` is tuple, also has `.x`, `.y` | MEDIUM |
| `sprite.click_callable` | `sprite.click` | MEDIUM |

### Functions in Docs Not in API

- `mcrfpy.run()` - Not found
- `mcrfpy.set_font()` - Not found (use Font class)
- `mcrfpy.debug_mode()` - Not found
- `scene.add_grid()` - Not found (use sceneUI().append())
- `scene.set_background_color()` - Not found
- `grid.set_entity()` - Not found (use entities.append())
- `grid.clear_entity()` - Not found
- `grid.get_grid()` - Not found

### API Features Not in Docs

- `Scene` class (OOP alternative to createScene)
- `ColorLayer` / `TileLayer` for grid overlays
- `Timer` class (object-oriented timer)
- `Animation` class with conflict modes
- `Window` singleton with resolution, fullscreen
- Drawable primitives (Arc, Circle, Line)
- `Grid.entities_in_radius()` spatial query
- `Entity.visible_entities()` FOV query

---

## 8. Prioritized Issue Checklist for 1.0

### P0 - Must Fix Before Any Docs

- [ ] Document how game loop starts (missing `run()` or equivalent)
- [ ] Reconcile Caption/Sprite/Frame constructor signatures
- [ ] Document Grid.at() vs set_tile pattern
- [ ] Fix `keypressScene` vs `bind_keys` naming

### P1 - Must Fix for Usable Docs

- [ ] Complete GridPoint/GridPointState documentation
- [ ] Document Color class methods (from_hex, lerp, etc.)
- [ ] Document Font loading
- [ ] Document Texture sprite index calculation
- [ ] Add FOV algorithm enum values
- [ ] Document click handler signature `(x, y, button, action)` or similar

### P2 - Should Fix for Good DX

- [ ] Add snake_case aliases for all camelCase functions
- [ ] Create "minimal example" showing actual working code
- [ ] Document Scene class as OOP alternative
- [ ] Document ColorLayer/TileLayer usage
- [ ] Document Animation conflict modes

### P3 - Nice to Have

- [ ] Add type hints to all function signatures
- [ ] Create interactive API explorer
- [ ] Add "common patterns" section to each class
- [ ] Document performance characteristics

---

## 9. Recommended API Additions for 1.0

### Essential Additions

```python
# 1. Simple game start
mcrfpy.run()  # Start the game loop

# 2. Turn system helper
class TurnManager:
    def add_actor(entity, speed): ...
    def next_turn(): ...

# 3. Message log widget
class MessageLog(Frame):
    def add_message(text, color): ...

# 4. Input modes
class InputMode(Enum):
    MOVEMENT = 0
    MENU = 1
    TARGETING = 2
```

### Desirable Additions

```python
# 5. Serialization helpers
entity.to_dict() -> dict
Entity.from_dict(data) -> Entity

# 6. Tooltip system
element.tooltip = "Description text"

# 7. Simple menu
menu = mcrfpy.Menu(options=["New Game", "Load", "Quit"])
menu.on_select = handler
```

---

## Appendix A: Complete Class/Function List

### Functions (24)
createScene, setScene, currentScene, sceneUI, keypressScene, setTimer, delTimer, createSoundBuffer, playSound, loadMusic, setMusicVolume, getMusicVolume, setSoundVolume, getSoundVolume, find, findAll, getMetrics, setScale, setDevConsole, exit, step, start_benchmark, end_benchmark, log_benchmark

### Classes (26)
Animation, Arc, Caption, Circle, Color, ColorLayer, Drawable, Entity, EntityCollection, FOV, Font, Frame, Grid, GridPoint, GridPointState, Line, Scene, Sprite, Texture, TileLayer, Timer, UICollection, UICollectionIter, UIEntityCollectionIter, Vector, Window

---

## Appendix B: Constructor Signature Reference (Actual API)

```python
# From API_REFERENCE_DYNAMIC.md

Animation()  # No documented constructor args

Arc(center=None, radius=0, start_angle=0, end_angle=90,
    color=None, thickness=1, **kwargs)

Caption(pos=None, font=None, text='', **kwargs)
# kwargs: fill_color, outline_color, outline, font_size, click,
#         visible, opacity, z_index, name, x, y

Circle(radius=0, center=None, fill_color=None, outline_color=None,
       outline=0, **kwargs)

Color(r, g, b, a=255)  # or tuple

Entity(grid_pos=None, texture=None, sprite_index=0, **kwargs)
# kwargs: grid, visible, opacity, name, x, y

Frame(pos=None, size=None, **kwargs)
# kwargs: fill_color, outline_color, outline, click, children,
#         visible, opacity, z_index, name, x, y, w, h,
#         clip_children, cache_subtree

Grid(pos=None, size=None, grid_size=None, texture=None, **kwargs)
# kwargs: fill_color, click, center_x, center_y, zoom, perspective,
#         visible, opacity, z_index, name, x, y, w, h, grid_x, grid_y

Line(start=None, end=None, thickness=1.0, color=None, **kwargs)

Sprite(pos=None, texture=None, sprite_index=0, **kwargs)
# kwargs: scale, scale_x, scale_y, click, visible, opacity,
#         z_index, name, x, y

Timer(name, callback, interval, once=False)

Vector(x=0.0, y=0.0)  # or tuple
```
