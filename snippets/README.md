---
mcrf:
  objects: []
  diataxis: meta
  disposition: current
  verified: "0.2.8"
  verified_commit: b6720f6
---

# McRogueFace Playground Snippets

This directory contains 130 runnable code snippets demonstrating every feature of the McRogueFace engine. Each snippet is designed to be:

- **Self-contained**: Copy and paste directly into the [playground](https://mcrogueface.github.io/playground/)
- **Visual**: Fills the 1024x768 canvas with clear demonstrations
- **Focused**: One concept per snippet

## Categories

### Getting Started (001-005)
- `001_hello_frame.py` - Basic Frame element
- `002_hello_caption.py` - Text display
- `003_hello_sprite.py` - Textured sprites
- `004_hello_grid.py` - Tile-based grids
- `005_hello_entity.py` - Grid entities

### Frame Properties (006-016)
- Colors, opacity, outline, children, clipping, z-index, visibility, naming, rotation, origin, alignment

### Caption & Sprite (017-022)
- Text styling, dimensions, sprite atlas, scaling, tinting

### Grid Features (023-027)
- Tiles, walkability, cell colors, camera, zoom

### Entity (028-030)
- Movement, multiple entities, smooth draw position

### Animation (031-045)
- Basic animation, all easing types, color/opacity/size animation, callbacks, chaining

### Timer (046-048)
- Periodic callbacks, one-shot timers, pause/resume/stop

### Input Handling (049-053)
- Keyboard events, mouse clicks, hover events, grid cell interaction

### Pathfinding & FOV (054-059)
- A* pathfinding, Dijkstra maps, field of view algorithms

### Procedural Generation (060, 086, 102)
- BSP dungeon generation, cellular automata caves, BSP traversal

### Scene Management (061-063, 090, 099, 105)
- Scene switching, transitions (fade, slide), lifecycle callbacks

### Utility Types (064-065)
- Vector operations, Color RGBA

### Element Lookup (066-068)
- find(), findAll(), collection iteration

### Window & Input State (069-071)
- Window properties, keyboard polling, mouse polling

### UI Patterns (072-075, 118)
- Buttons, health bars, tooltips, message logs, modal dialogs

### Visual Effects (076-079)
- Screen shake, damage flash, floating text, pulse

### Game Examples (080-082, 100, 119)
- Turn-based movement, inventory, minimap, complete mini-game, collision

### Advanced Grid (083-085, 087, 098, 101, 127)
- Layers, Bresenham lines, entity visibility, cell state, fill color, camera rotation, display size

### Animation Advanced (088, 103, 107, 112, 120, 123, 128)
- Multiple animations, Vector animation, animation list, delta mode, state checking, stop/complete, color channels

### Performance & Debug (091, 108)
- Metrics display, cache_subtree optimization

### Position & Hierarchy (092-093)
- Global coordinates, parent references

### Entity Methods (094-095, 121)
- die(), index(), at()

### Timer Advanced (096, 106, 126)
- remaining time, timer list, restart

### Easing Functions (113-117)
- Cubic, Sine, Exponential, Circular, Quartic variants

### Miscellaneous (097, 104, 109-111, 122, 124-125, 129-130)
- Hovered state, texture properties, realign, version info, margins, default FOV, sprite rotation, vector normalization, scene update, exit

## Usage

1. Browse to [mcrogueface.github.io/playground/](https://mcrogueface.github.io/playground/)
2. Copy any snippet from this directory
3. Paste into the code editor
4. Click "Run" or press Ctrl+Enter

## Contributing

When adding new snippets:
- Number sequentially: `NNN_category_feature.py`
- Keep under 50 lines when possible
- Fill the 1024x768 canvas visually
- Include descriptive comments
- Test in the playground before committing
