# McRogueFace Tutorial Blueprint

**F2 Foundation Document - Competitor Analysis & Tutorial Structure**

*Generated: 2025-12-29*

---

## Executive Summary

This document analyzes the two most influential roguelike tutorials and synthesizes a 13-part tutorial structure specifically designed for McRogueFace. The blueprint maps tutorial concepts to McRogueFace's API, identifies where adaptations are needed, and provides estimated complexity for each part.

---

## Part I: Competitor Tutorial Analysis

### A. Python+tcod Tutorial (rogueliketutorials.com/tutorials/tcod/v2/)

The canonical roguelike tutorial, updated in 2020 for tcod's modern API. Serves as the gold standard for incremental roguelike development.

#### Chapter Structure

| Part | Title | Working Artifact | Key Concepts |
|------|-------|------------------|--------------|
| 0 | Setting Up | "Hello World" prints | Environment setup, dependency installation |
| 1 | Drawing '@' and moving it around | Movable player on screen | Game loop, rendering, input handling, action classes |
| 2 | Generic Entity, render functions, map | Player + NPC on tiled map | Entity class, Engine class, GameMap, tile types with NumPy |
| 3 | Generating a dungeon | Procedural room-corridor dungeon | RectangularRoom, tunnel generation, Bresenham lines |
| 4 | Field of view | Fog of war with memory | FOV calculation, visible/explored states, SHROUD constant |
| 5 | Placing enemies and kicking them | Monsters spawn, block movement | Entity spawning, cloning, BumpAction, turn order |
| 6 | Doing (and taking) some damage | Functional combat with death | Component architecture (Fighter, BaseAI), HP, damage calc, death |
| 7 | Creating the Interface | HP bar, message log, tooltips | render_bar(), MessageLog class, mouse tracking, history viewer |
| 8 | Items and Inventory | Pickup/use health potions | Item entity, Inventory component, Consumable component, menus |
| 9 | Ranged Scrolls and Targeting | Lightning, confusion, fireball scrolls | Targeting handlers, AoE radius, status effects, callbacks |
| 10 | Saving and Loading | Persistent game state | pickle+lzma serialization, main menu, BaseEventHandler refactor |
| 11 | Delving into the Dungeon | Multi-floor progression, XP/leveling | GameWorld, stairs tile, Level component, stat selection menu |
| 12 | Increasing Difficulty | Scaling spawn rates and types | Floor-based difficulty, weighted random selection, data-driven spawns |
| 13 | Gearing up | Equipment with stat bonuses | Equipment component, Equippable component, equip/unequip actions |

#### Pedagogical Patterns

1. **Incremental Complexity**: Each part builds directly on the previous
2. **Immediate Feedback**: Every part produces something visible/playable
3. **Refactoring as Teaching**: Code is restructured when patterns emerge (e.g., Actions, Components)
4. **Separation of Concerns**: Distinct modules for distinct responsibilities (engine, map, actions, components)
5. **Exception-Based Flow Control**: `Impossible` exception for invalid actions prevents wasted turns

#### tcod-Specific Patterns

- NumPy structured arrays for tile data
- `EventDispatch` class for input handling
- `tcod.map.compute_fov()` for FOV
- `pickle` + `lzma` for serialization
- Type hints with `TYPE_CHECKING` for circular import avoidance

---

### B. Rust bracket-lib Tutorial (bfnightly.bracketproductions.com)

A comprehensive 70+ chapter tutorial covering basic through advanced roguelike development in Rust.

#### Core Section (Chapters 1-14) - Comparable to tcod Tutorial

| Chapter | Title | Working Artifact | Key Concepts |
|---------|-------|------------------|--------------|
| 1 | Hello Rust | "Hello World" in terminal | Cargo setup, RLTK integration, GameState trait, tick() |
| 2 | Entities and Components | Player + left-walking smileys | ECS architecture (Specs), Components, Systems, tag components |
| 3 | Walking A Map | Player on random wall map | Tile enum, xy_idx conversion, collision detection |
| 4 | A More Interesting Map | Room-corridor dungeon | Rect struct, room generation, tunnel carving |
| 5 | Field of View | Fog of war with memory | Viewshed component, BaseMap/Algorithm2D traits, dirty flag optimization |
| 6 | Monsters | Named enemies that spot player | Monster/Name components, RunState enum, MonsterAI system |
| 7 | Dealing Damage | Combat with pathfinding AI | A* pathfinding, BlocksTile, CombatStats, WantsToMelee, DamageSystem |
| 8 | User Interface | HP bar, game log, tooltips | GameLog resource, gui.rs module, mouse position tracking |
| 9 | Items and Inventory | Health potions with pickup/use | Item composition, WantsTo* intents, inventory menus, render ordering |
| 10 | Ranged Scrolls/Targeting | Targeting UI with visual feedback | SelectIndexHandler, AoE visualization, Confusion AI, callbacks |
| 11 | Saving and Loading | Persistent saves with Serde | Serialization derives, SimpleMarker, main menu, WebAssembly compatibility |
| 12 | Delving Deeper | Multi-floor dungeons | Depth tracking, stairs tile, entity lifecycle on level change |
| 13 | Difficulty | Scaled spawning | RandomTable weighted selection, depth-based difficulty curves |
| 14 | Equipment | Weapons and armor | Equipment/Equippable components, slot system, stat bonuses |

#### Pedagogical Patterns

1. **ECS-First Architecture**: Specs ECS from chapter 2
2. **Systems Over Methods**: Logic in systems that query components
3. **Intent-Based Actions**: `WantsTo*` components declare intent, systems execute
4. **Resource Pattern**: Shared state as ECS resources (GameLog, Map, RunState)
5. **State Machine**: Explicit `RunState` enum for game phases

#### bracket-lib-Specific Patterns

- `#[derive(Component)]` macros
- `.join()` for component iteration
- `WriteStorage`/`ReadStorage` for system data
- WASM compilation considerations
- Chainable builder patterns

---

## Part II: API Mapping Analysis

### Direct Mappings (McRogueFace API covers cleanly)

| Tutorial Concept | McRogueFace Equivalent | Notes |
|-----------------|------------------------|-------|
| Game loop | Engine provides automatic loop | No manual loop needed |
| Rendering entities | `Grid.entities` collection + `Entity` class | Built-in sprite rendering |
| Tile-based map | `Grid` with `GridPoint` | `grid.at(x,y)` for tile access |
| Field of view | `Grid.compute_fov()`, `Grid.is_in_fov()` | Multiple algorithms via `FOV` enum |
| A* pathfinding | `Grid.find_path()`, `Entity.path_to()` | Built-in pathfinding |
| Dijkstra maps | `Grid.compute_dijkstra()`, `Grid.get_dijkstra_path()` | Full Dijkstra support |
| Keyboard input | `keypressScene(handler)` or `Scene.on_key` | Handler receives (key, pressed) |
| Mouse tracking | Click handlers on elements | `click` property on UI elements |
| UI frames | `Frame` class | Supports fill, outline, children |
| Text display | `Caption` class | Font, color, outline support |
| Sprites | `Sprite` class | Texture atlas support |
| Timers | `Timer` class or `setTimer()` | Interval-based callbacks |
| Animations | `Animation` class | Property interpolation with easing |
| Scene management | `createScene()`, `setScene()` | Transition effects available |
| Sound/music | `createSoundBuffer()`, `playSound()`, `loadMusic()` | Full audio support |

### Adaptations Needed

| Tutorial Concept | McRogueFace Approach | Adaptation Notes |
|-----------------|---------------------|------------------|
| NumPy tile arrays | `TileLayer` / direct `GridPoint` access | Use layers for tile rendering, GridPoint for walkable/transparent |
| Entity composition (ECS) | Python class composition | Build component system in Python, or use dicts/dataclasses |
| Action classes | Python classes with perform() | Standard Python OOP |
| Event handlers | Scene-based input callbacks | One handler per scene, dispatch internally |
| Message log | Build from `Frame` + `Caption` | No built-in MessageLog widget |
| Health bar | Build from `Frame` (nested) | Draw filled rect over background rect |
| Inventory menus | Build from `Frame` + `Caption` | Compose UI elements |
| Turn management | Python state + Timer or callback | No built-in turn system |
| Save/load | Python pickle/json | No engine serialization; serialize game state |
| Targeting overlay | `ColorLayer.fill()` / `ColorLayer.set()` | Paint highlights on color layer |

### Features McRogueFace Has Beyond Tutorials

| Feature | Description | Tutorial Use Case |
|---------|-------------|-------------------|
| `ColorLayer` | Per-cell color overlay | FOV shading, targeting highlights, status effects |
| `TileLayer` | Per-cell sprite overlay | Multi-layer dungeon (base tiles + decorations) |
| `Entity.visible_entities()` | Get entities in FOV | Simplified AI targeting |
| `Grid.entities_in_radius()` | Spatial query | AoE targeting, proximity checks |
| `Animation` class | Smooth property animation | Damage flash, movement interpolation |
| `Window.screenshot()` | Screenshot capture | Debug, share, documentation |
| Scene transitions | Fade, slide effects | Menu-to-game transitions |
| `Circle`, `Line`, `Arc` | Shape primitives | Targeting circles, line-of-sight indicators |

### API Gaps for Tutorial Support

| Missing Feature | Impact | Workaround |
|-----------------|--------|------------|
| No built-in message log | Part 7 requires building from scratch | Compose Frame + Captions with scroll logic |
| No built-in health bar widget | Part 7 requires manual construction | Nested Frames with fill colors |
| No turn system helper | Each tutorial builds this differently | Python state machine pattern |
| No menu widget | Inventory/targeting menus manual | Frame + Caption + keyboard dispatch |
| Click handler signature undocumented | Need to test/verify | Document during tutorial development |
| GridPoint properties undocumented | Tile data access unclear | Needs API verification |

---

## Part III: McRogueFace Tutorial Blueprint

### Design Principles

1. **Python-First**: Leverage Python's strengths (dicts, classes, comprehensions)
2. **McRogueFace-Idiomatic**: Use Grid/Entity/Layer system as designed
3. **Immediate Visual Feedback**: Every part shows something new on screen
4. **Progressive Complexity**: Simple concepts first, composition later
5. **Reusable Patterns**: Introduce patterns that scale to larger games
6. **No Hidden Magic**: Explain what the engine does vs. what Python does

### Tutorial Structure: 13 Parts

---

#### Part 0: Setting Up McRogueFace

**Learning Objectives:**
- Install McRogueFace and verify the installation
- Understand the project structure
- Create and run a minimal "Hello Roguelike" program

**What the player can do at the end:**
- See a window with "Hello Roguelike" text displayed

**McRogueFace APIs Required:**
- `mcrfpy.createScene()`
- `mcrfpy.setScene()`
- `mcrfpy.sceneUI()`
- `Caption` class

**Estimated Lines of Code:** ~15

**Key Concepts:**
- Scene creation and activation
- UI element creation
- The implicit game loop

---

#### Part 1: The '@' and the Dungeon Grid

**Learning Objectives:**
- Create a Grid for tile-based rendering
- Place an Entity (the player '@')
- Handle keyboard input to move the player
- Understand grid coordinates vs. pixel coordinates

**What the player can do at the end:**
- Move a yellow '@' symbol around a blank grid with arrow keys

**McRogueFace APIs Required:**
- `Grid` class with `grid_size`, `texture`
- `Entity` class with `grid_pos`, `sprite_index`
- `Grid.entities.append()`
- `keypressScene()` or `Scene.on_key`

**Estimated Lines of Code:** ~50

**Key Concepts:**
- Grid as the game world container
- Entity as a movable game object
- Input handling pattern
- Sprite indices for character appearance

---

#### Part 2: Walls, Floors, and Collision

**Learning Objectives:**
- Define tile types (wall, floor)
- Populate the grid with walls and floors
- Implement collision detection (walls block movement)
- Understand `GridPoint.walkable` property

**What the player can do at the end:**
- Move through a simple map with impassable walls

**McRogueFace APIs Required:**
- `Grid.at(x, y)` for GridPoint access
- `GridPoint.walkable` property
- `GridPoint.tilesprite` (or `TileLayer`)
- Nested loops for map population

**Estimated Lines of Code:** ~80

**Key Concepts:**
- Tile data vs. tile rendering
- Walkability as game logic
- Coordinate iteration patterns

---

#### Part 3: Procedural Dungeon Generation

**Learning Objectives:**
- Implement a room-and-corridor dungeon generator
- Create room and tunnel data structures
- Place the player in the first room

**What the player can do at the end:**
- Explore a randomly generated dungeon with multiple rooms

**McRogueFace APIs Required:**
- Same as Part 2
- Python `random` module

**Estimated Lines of Code:** ~150

**Key Concepts:**
- Procedural generation fundamentals
- Room/rectangle data structures
- Tunnel carving algorithms
- Random number generation

---

#### Part 4: Field of View

**Learning Objectives:**
- Implement fog of war using McRogueFace's FOV system
- Track explored vs. visible vs. unknown tiles
- Render tiles differently based on visibility state

**What the player can do at the end:**
- See only nearby tiles; explored tiles remain dimly visible

**McRogueFace APIs Required:**
- `Grid.compute_fov(x, y, radius)`
- `Grid.is_in_fov(x, y)`
- `ColorLayer` for visibility shading
- `ColorLayer.apply_perspective()` or manual FOV painting

**Estimated Lines of Code:** ~100

**Key Concepts:**
- Field of view algorithms
- Three-state visibility (unseen, seen, visible)
- Color layers for visual effects
- Recalculating FOV on movement

---

#### Part 5: Placing Enemies

**Learning Objectives:**
- Spawn enemy entities in dungeon rooms
- Make enemies visible only when in FOV
- Implement basic entity data (name, blocking)

**What the player can do at the end:**
- Encounter Orcs and Trolls in the dungeon (they don't act yet)

**McRogueFace APIs Required:**
- `Entity` class (multiple instances)
- `Grid.entities` collection
- Entity visibility based on FOV
- Python data structures for entity properties

**Estimated Lines of Code:** ~80

**Key Concepts:**
- Entity spawning patterns
- Entity visibility and FOV integration
- Game data in Python (dicts, classes, or dataclasses)
- Blocking entities concept

---

#### Part 6: Combat System

**Learning Objectives:**
- Implement HP, attack, and defense stats
- Create a melee combat system
- Handle entity death and removal
- Implement basic enemy AI (chase and attack)

**What the player can do at the end:**
- Fight and kill monsters; die if HP reaches zero

**McRogueFace APIs Required:**
- `Entity.path_to(x, y)` for AI pathfinding
- `Entity.die()` for removal
- `Grid.find_path()` for path queries
- Timer or turn-based callback for AI

**Estimated Lines of Code:** ~200

**Key Concepts:**
- Component-like data organization
- Combat calculations
- Turn order / action processing
- Entity lifecycle (spawn, act, die)
- Pathfinding for AI

---

#### Part 7: User Interface

**Learning Objectives:**
- Build a health bar from Frame elements
- Create a scrolling message log
- Display entity names on hover/selection
- Organize screen layout (map area + UI panel)

**What the player can do at the end:**
- See HP bar, combat messages, and entity information

**McRogueFace APIs Required:**
- `Frame` class (for panels, bars)
- `Caption` class (for text)
- `Frame.children` for UI composition
- Click handlers or position tracking

**Estimated Lines of Code:** ~180

**Key Concepts:**
- UI composition from primitives
- Health bar as nested frames
- Message log as scrolling text list
- Screen layout organization

---

#### Part 8: Items and Inventory

**Learning Objectives:**
- Create item entities (health potions)
- Implement pickup mechanics
- Build an inventory data structure
- Create inventory display UI
- Use consumable items

**What the player can do at the end:**
- Pick up health potions, view inventory, use potions to heal

**McRogueFace APIs Required:**
- Entity for items on ground
- Python list/dict for inventory
- Frame + Caption for inventory menu
- Input mode switching (movement vs. menu)

**Estimated Lines of Code:** ~200

**Key Concepts:**
- Items as entities with special properties
- Inventory as data structure
- Modal input handling (game vs. menu mode)
- Consumable effects

---

#### Part 9: Ranged Combat and Targeting

**Learning Objectives:**
- Implement scroll items with ranged effects
- Create a targeting mode with visual feedback
- Implement area-of-effect damage
- Add status effects (confusion)

**What the player can do at the end:**
- Use lightning, fireball, and confusion scrolls with targeting

**McRogueFace APIs Required:**
- `Grid.entities_in_radius()` for AoE
- `Entity.visible_entities()` for targeting
- `ColorLayer` for targeting highlights
- Input mode for targeting selection

**Estimated Lines of Code:** ~250

**Key Concepts:**
- Targeting as a game mode
- Visual feedback for valid/invalid targets
- Area of effect calculations
- Status effects and AI modification

---

#### Part 10: Save and Load

**Learning Objectives:**
- Serialize game state to JSON
- Implement save and load functionality
- Create a main menu with New/Continue/Quit
- Handle save file not found gracefully

**What the player can do at the end:**
- Save progress, quit, and resume from where they left off

**McRogueFace APIs Required:**
- `createScene()` for menu scene
- `setScene()` with transitions
- Python `json` module
- File I/O

**Estimated Lines of Code:** ~200

**Key Concepts:**
- Game state as serializable data
- Separating state from presentation
- Scene transitions for menus
- Error handling for missing saves

---

#### Part 11: Dungeon Levels

**Learning Objectives:**
- Implement stairs and level transitions
- Track dungeon depth
- Generate new levels on descent
- Display depth in UI

**What the player can do at the end:**
- Descend through multiple dungeon levels

**McRogueFace APIs Required:**
- `GridPoint.tilesprite` for stairs tile
- Scene or grid regeneration
- State management for depth

**Estimated Lines of Code:** ~120

**Key Concepts:**
- Level transitions
- State preservation across levels
- Dungeon progression

---

#### Part 12: Experience and Leveling

**Learning Objectives:**
- Track experience points from kills
- Implement a leveling formula
- Create level-up stat selection
- Scale difficulty with depth

**What the player can do at the end:**
- Gain XP, level up, choose stat improvements; face harder enemies deeper

**McRogueFace APIs Required:**
- Python data structures for player stats
- Frame + Caption for level-up menu
- Weighted random for spawn tables

**Estimated Lines of Code:** ~150

**Key Concepts:**
- Experience and leveling formulas
- Character progression
- Difficulty scaling
- Spawn table weighting

---

#### Part 13: Equipment System

**Learning Objectives:**
- Create equipment items (weapons, armor)
- Implement equipment slots
- Modify combat stats based on equipped items
- Build equipment management UI

**What the player can do at the end:**
- Find, equip, and swap weapons and armor that affect combat

**McRogueFace APIs Required:**
- Entity for equipment items
- Python data structures for equipment state
- Frame + Caption for equipment UI

**Estimated Lines of Code:** ~180

**Key Concepts:**
- Equipment slots and restrictions
- Stat modification through gear
- Equipment as permanent items vs. consumables

---

## Part IV: Summary Statistics

### Total Estimated Lines of Code

| Part | Topic | Lines |
|------|-------|-------|
| 0 | Setup | 15 |
| 1 | Grid + Movement | 50 |
| 2 | Tiles + Collision | 80 |
| 3 | Dungeon Generation | 150 |
| 4 | Field of View | 100 |
| 5 | Enemies | 80 |
| 6 | Combat | 200 |
| 7 | UI | 180 |
| 8 | Items + Inventory | 200 |
| 9 | Ranged + Targeting | 250 |
| 10 | Save/Load | 200 |
| 11 | Dungeon Levels | 120 |
| 12 | XP + Leveling | 150 |
| 13 | Equipment | 180 |
| **Total** | | **~1,955** |

### API Coverage by Part

| API Element | First Introduced | Used Throughout |
|-------------|------------------|-----------------|
| Scene management | Part 0 | Part 10 (menus) |
| Caption | Part 0 | Part 7+ (UI) |
| Grid | Part 1 | All subsequent |
| Entity | Part 1 | All subsequent |
| Input handling | Part 1 | All subsequent |
| GridPoint | Part 2 | All subsequent |
| TileLayer | Part 2 | All subsequent |
| Grid.compute_fov | Part 4 | Part 5+ |
| ColorLayer | Part 4 | Part 4, 9 |
| Entity.path_to | Part 6 | Part 6+ |
| Frame | Part 7 | Part 7+ |
| Timer | Part 6 | Part 6+ (AI) |
| Grid.entities_in_radius | Part 9 | Part 9 |
| Window | Part 10 | Optional |

### Dependencies Between Parts

```
Part 0 (Setup)
    |
Part 1 (Grid + Movement)
    |
Part 2 (Tiles + Collision)
    |
Part 3 (Dungeon Generation)
    |
Part 4 (FOV) -------- Part 5 (Enemies)
    |                       |
    +-------+---------------+
            |
      Part 6 (Combat)
            |
      Part 7 (UI)
            |
      Part 8 (Items)
            |
      Part 9 (Ranged)
            |
     Part 10 (Save/Load)
            |
     Part 11 (Levels)
            |
     Part 12 (XP)
            |
     Part 13 (Equipment)
```

---

## Part V: Recommendations

### Immediate Actions

1. **Verify GridPoint Properties**: Document `walkable`, `transparent`, `tilesprite`, `color`, etc.
2. **Test Click Handler Signature**: Confirm parameters passed to click callbacks
3. **Create Sprite Sheet**: Design/select a tutorial-appropriate tile set

### Tutorial Development Order

1. Write Part 0-1 first to establish code style and conventions
2. Parts 2-4 form the core "exploration" loop - develop together
3. Parts 5-6 form the core "combat" loop - develop together
4. Parts 7-9 add depth - can be developed in parallel
5. Parts 10-13 add persistence and progression - develop in order

### Code Style Recommendations

1. Use Python type hints for clarity
2. Prefer dataclasses for game data structures
3. Use constants for magic numbers (colors, sizes, stats)
4. Keep game logic separate from rendering logic
5. Use descriptive variable names over abbreviations

### Teaching Approach

1. Show the "what" first, then explain the "why"
2. Provide complete, runnable code at each step
3. Highlight McRogueFace-specific patterns
4. Compare to tcod/bracket-lib approaches where instructive
5. Include "try this" challenges for each part

---

## Appendices

### A. Color Palette Suggestion

```python
# Visibility colors
COLOR_VISIBLE = mcrfpy.Color(255, 255, 255, 255)  # White - currently seen
COLOR_EXPLORED = mcrfpy.Color(128, 128, 128, 255)  # Gray - previously seen
COLOR_UNKNOWN = mcrfpy.Color(0, 0, 0, 255)  # Black - never seen

# Entity colors
COLOR_PLAYER = mcrfpy.Color(255, 255, 0, 255)  # Yellow
COLOR_ORC = mcrfpy.Color(63, 127, 63, 255)  # Dark green
COLOR_TROLL = mcrfpy.Color(0, 127, 0, 255)  # Green

# UI colors
COLOR_HP_BAR = mcrfpy.Color(0, 192, 0, 255)  # Green
COLOR_HP_EMPTY = mcrfpy.Color(64, 0, 0, 255)  # Dark red
COLOR_UI_BACKGROUND = mcrfpy.Color(32, 32, 32, 200)  # Dark gray, semi-transparent
```

### B. Sprite Index Mapping (Example)

```python
# Using a 16x16 tile atlas
SPRITE_FLOOR = 0
SPRITE_WALL = 1
SPRITE_PLAYER = 64  # '@'
SPRITE_ORC = 111    # 'o'
SPRITE_TROLL = 116  # 'T'
SPRITE_POTION = 33  # '!'
SPRITE_SCROLL = 63  # '?'
SPRITE_STAIRS_DOWN = 62  # '>'
SPRITE_CORPSE = 37  # '%'
SPRITE_SWORD = 47   # '/'
SPRITE_SHIELD = 91  # '['
```

### C. Game State Structure (Example)

```python
@dataclass
class GameState:
    # Map
    dungeon_level: int
    map_width: int
    map_height: int
    tiles: list[list[dict]]  # Or use GridPoint directly

    # Player
    player_x: int
    player_y: int
    player_hp: int
    player_max_hp: int
    player_attack: int
    player_defense: int
    player_xp: int
    player_level: int

    # Inventory
    inventory: list[dict]
    equipment: dict[str, dict]  # slot -> item

    # Enemies
    enemies: list[dict]

    # Messages
    message_log: list[tuple[str, tuple]]  # (text, color)
```

---

*End of F2 Tutorial Blueprint*
