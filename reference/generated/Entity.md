---
title: Entity
layout: default
mcrf:
  objects:
    - Entity
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Entity

{% raw %}Entity(grid_pos=None, texture=None, sprite_index=0, **kwargs)

A game entity that exists on a grid with sprite rendering.

Args:
    grid_pos (tuple, optional): Grid position as (x, y) tuple. Default: (0, 0)
    texture (Texture, optional): Texture object for sprite. Default: default texture
    sprite_index (int, optional): Index into texture atlas. Default: 0

Keyword Args:
    grid (Grid): Grid to attach entity to. Default: None
    visible (bool): Visibility state. Default: True
    opacity (float): Opacity (0.0-1.0). Default: 1.0
    name (str): Element name for finding. Default: None
    x (float): X grid position override (tile coords). Default: 0
    y (float): Y grid position override (tile coords). Default: 0
    sprite_offset (tuple): Pixel offset for oversized sprites. Default: (0, 0)
    sprite_grid (list): Per-tile sprite indices for composite entities. Default: None

Attributes:
    pos (Vector): Pixel position relative to grid (requires grid attachment)
    x, y (float): Pixel position components (requires grid attachment)
    grid_pos (Vector): Integer tile coordinates (logical game position)
    grid_x, grid_y (int): Integer tile coordinate components
    draw_pos (Vector): Fractional tile position for smooth animation
    perspective_map (DiscreteMap | None): 3-state per-entity FOV memory
    texture (Texture): Texture atlas used by the entity's sprite
    sprite_index (int): Current sprite index
    visible (bool): Visibility state
    opacity (float): Opacity value
    name (str): Element name
    sprite_offset (Vector): Pixel offset for oversized sprites
    sprite_offset_x (float): X component of sprite offset
    sprite_offset_y (float): Y component of sprite offset{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `behavior_type` | {% raw %}Current behavior type (int, read-only). Use set_behavior() to change.{% endraw %} |
| `cell_pos` | {% raw %}Integer logical cell position (Vector). Alias for grid_pos (the canonical name).{% endraw %} |
| `cell_x` | {% raw %}Integer X cell coordinate (int). Alias for grid_x.{% endraw %} |
| `cell_y` | {% raw %}Integer Y cell coordinate (int). Alias for grid_y.{% endraw %} |
| `default_behavior` | {% raw %}Default behavior type (int, maps to Behavior enum). Entity reverts to this after DONE trigger. Default: 0 (IDLE).{% endraw %} |
| `draw_pos` | {% raw %}Fractional tile position for rendering (Vector). Use for smooth animation between grid cells.{% endraw %} |
| `grid` | {% raw %}Grid this entity belongs to (Grid or None). Assign a Grid to attach the entity, or None to remove it from its current grid.{% endraw %} |
| `grid_pos` | {% raw %}Integer logical cell position (Vector). Canonical cell-position property matching the 'grid_pos' constructor argument. Decoupled from draw_pos. Determines which cell this entity logically occupies for collision and pathfinding.{% endraw %} |
| `grid_x` | {% raw %}Integer X cell coordinate (int). Canonical; matches grid_pos.{% endraw %} |
| `grid_y` | {% raw %}Integer Y cell coordinate (int). Canonical; matches grid_pos.{% endraw %} |
| `labels` | {% raw %}String labels for collision and targeting (frozenset). Assign any iterable of strings to replace all labels.{% endraw %} |
| `move_speed` | {% raw %}Animation duration for behavior movement in seconds (float). 0 = instant. Default: 0.15.{% endraw %} |
| `name` | {% raw %}Entity name for lookup (str).{% endraw %} |
| `opacity` | {% raw %}Render opacity (float). 0.0 = fully transparent, 1.0 = fully opaque.{% endraw %} |
| `perspective_map` | {% raw %}Per-entity FOV memory (DiscreteMap). 3-state values per cell: 0=unknown, 1=discovered, 2=visible. Lazy-allocated on first access once entity has a grid; returns None otherwise. The returned DiscreteMap is a live reference. Assigning a DiscreteMap replaces the entity's memory (e.g. loading a saved perspective via from_bytes); size must match the grid or ValueError is raised, and the next updateVisibility() demotes any loaded visible cells to discovered before recomputing FOV. Assign None to clear. Note: updateVisibility() only auto-demotes visible cells the engine itself promoted; if you write 2 (visible) into the live map by hand at a cell outside the entity's current FOV, it will not be auto-demoted -- use 1 (discovered) to reveal remembered cells, or assign a whole map to set arbitrary state.{% endraw %} |
| `pos` | {% raw %}Pixel position relative to grid (Vector). Computed as draw_pos * tile_size. Requires entity to be attached to a grid.{% endraw %} |
| `shader` | {% raw %}GPU shader for visual effects (Shader or None). Set to None to disable shader rendering.{% endraw %} |
| `sight_radius` | {% raw %}FOV radius for TARGET trigger (int). Default: 10.{% endraw %} |
| `sprite_grid` | {% raw %}Per-tile sprite indices for composite multi-tile entities (list of lists or None). Row-major, dimensions must match tile_width x tile_height. Use -1 for empty tiles.{% endraw %} |
| `sprite_index` | {% raw %}Sprite index into the entity's texture atlas (int).{% endraw %} |
| `sprite_offset` | {% raw %}Pixel offset for oversized sprites (Vector). Applied pre-zoom during grid rendering.{% endraw %} |
| `sprite_offset_x` | {% raw %}X component of sprite pixel offset (float).{% endraw %} |
| `sprite_offset_y` | {% raw %}Y component of sprite pixel offset (float).{% endraw %} |
| `step` | {% raw %}Step callback for grid.step() turn management (Callable or None). Called with (trigger, data) when behavior triggers fire.{% endraw %} |
| `target_label` | {% raw %}Label to search for with TARGET trigger (str or None). Default: None.{% endraw %} |
| `texture` | {% raw %}Sprite texture atlas (Texture). Defaults to mcrfpy.default_texture at construction. Setting preserves sprite_index (not re-validated against the new atlas).{% endraw %} |
| `tile_height` | {% raw %}Entity height in tiles (int). Must be >= 1. Default 1.{% endraw %} |
| `tile_size` | {% raw %}Entity size in tiles as (width, height) (Vector). Default (1, 1).{% endraw %} |
| `tile_width` | {% raw %}Entity width in tiles (int). Must be >= 1. Default 1.{% endraw %} |
| `turn_order` | {% raw %}Turn order for grid.step() (int). 0 = skip, higher values go later. Default: 1.{% endraw %} |
| `uniforms` | {% raw %}Collection of shader uniforms (UniformCollection, read-only). Set values via dict-like syntax: entity.uniforms['name'] = value.{% endraw %} |
| `visible` | {% raw %}Visibility flag (bool). When False, the entity is not rendered.{% endraw %} |
| `x` | {% raw %}Pixel X position relative to grid (float). Requires entity to be attached to a grid.{% endraw %} |
| `y` | {% raw %}Pixel Y position relative to grid (float). Requires entity to be attached to a grid.{% endraw %} |

## Methods

### `add_label(label: str) -> None`

{% raw %}add_label(label: str) -> None

Add a label to this entity. Idempotent; adding the same label twice is safe.

Args:
    label: String label to add

Returns:
    None
{% endraw %}

### `animate(property: str, target: Any, duration: float, easing=None, delta=False, loop=False, callback=None, conflict_mode='replace') -> Animation`

{% raw %}animate(property: str, target: Any, duration: float, easing=None, delta=False, loop=False, callback=None, conflict_mode='replace') -> Animation

Create and start an animation on this entity's property.

Args:
    property: Name of the property to animate: 'draw_x', 'draw_y' (tile coords), 'sprite_scale', 'sprite_index', 'sprite_offset_x', 'sprite_offset_y'
    target: Target value - float, int, or list of int (for sprite frame sequences)
    duration: Animation duration in seconds
    easing: Easing function: Easing enum value, string name, or None for linear
    delta: If True, target is relative to current value; if False, target is absolute
    loop: If True, animation repeats from start when it reaches the end (default False)
    callback: Optional callable invoked when animation completes (not called for looping animations)
    conflict_mode: 'replace' (default), 'queue', or 'error' if property already animating

Returns:
    Animation object for monitoring progress

Raises:
    ValueError: If property name is not valid for Entity (draw_x, draw_y, sprite_scale, sprite_index, sprite_offset_x, sprite_offset_y)

Note:
    Use 'draw_x'/'draw_y' to animate tile coordinates for smooth movement between grid cells. Use list target with loop=True for repeating sprite frame animations. 'x' and 'y' are accepted as aliases for 'draw_x' and 'draw_y'.
{% endraw %}

### `at(x: int, y: int) -> GridPoint | None`

{% raw %}at(x: int, y: int) -> GridPoint | None

Return the GridPoint at (x, y) if currently VISIBLE to this entity's perspective_map, otherwise None.

Args:
    x: Grid X coordinate (also accepts a tuple/Vector as first positional arg)
    y: Grid Y coordinate (omit when passing a tuple or Vector)

Returns:
    GridPoint if visible, None if undiscovered or not currently in FOV

Note:
    To inspect discovered-but-not-visible cells, read entity.perspective_map[x, y] directly.
{% endraw %}

### `die() -> None`

{% raw %}die() -> None

Remove this entity from its grid.


Returns:
    None

Note:
    Do not call during iteration over grid.entities; modifying the collection during iteration raises RuntimeError.
{% endraw %}

### `find_path(target, diagonal_cost: float = 1.41, collide: str = None) -> AStarPath | None`

{% raw %}find_path(target, diagonal_cost: float = 1.41, collide: str = None) -> AStarPath | None

Find a path from this entity to the target position.

Args:
    target: Target as Vector, Entity, or (x, y) tuple
    diagonal_cost: Cost of diagonal movement (default 1.41)
    collide: Label string; entities with this label block pathfinding

Returns:
    AStarPath object, or None if no path exists

Raises:
    ValueError: If entity has no grid or positions are out of bounds
{% endraw %}

### `has_label(label: str) -> bool`

{% raw %}has_label(label: str) -> bool

Check if this entity has the given label.

Args:
    label: String label to check

Returns:
    True if the entity has the label, False otherwise
{% endraw %}

### `index() -> int`

{% raw %}index() -> int

Return the index of this entity in its grid's entity collection.


Returns:
    Zero-based index of this entity in grid.entities

Raises:
    RuntimeError: If entity is not associated with a grid
{% endraw %}

### `move(dx, dy) or (delta) -> None`

{% raw %}move(dx, dy) or (delta) -> None

Move the element by a relative offset.

Args:
    dx: Horizontal offset in pixels (or use delta)
    dy: Vertical offset in pixels (or use delta)
    delta: Offset as tuple, list, or Vector: (dx, dy)

Note:
    Accepts move(dx, dy), move((dx, dy)), move(Vector), or move(pos=(dx, dy)).
{% endraw %}

### `path_to(x: int, y: int) -> list`

{% raw %}path_to(x: int, y: int) -> list

Find a path to the target position using A* pathfinding.

Args:
    x: Target X coordinate (also accepts a tuple/Vector as first positional arg)
    y: Target Y coordinate (omit when passing a tuple or Vector)

Returns:
    List of (x, y) tuples representing the path from current position to target

Raises:
    ValueError: If entity has no grid or target is out of bounds
{% endraw %}

### `remove_label(label: str) -> None`

{% raw %}remove_label(label: str) -> None

Remove a label from this entity. No-op if label is not present.

Args:
    label: String label to remove

Returns:
    None
{% endraw %}

### `resize(width, height) or (size) -> None`

{% raw %}resize(width, height) or (size) -> None

Resize the element to new dimensions.

Args:
    width: New width in pixels (or use size)
    height: New height in pixels (or use size)
    size: Size as tuple, list, or Vector: (width, height)

Note:
    Accepts resize(w, h), resize((w, h)), resize(Vector), or resize(pos=(w, h)).
{% endraw %}

### `set_behavior(type, waypoints=None, turns: int = 0, path=None, pathfinder=None) -> None`

{% raw %}set_behavior(type, waypoints=None, turns: int = 0, path=None, pathfinder=None) -> None

Configure this entity's behavior for grid.step() turn management.

Args:
    type: Behavior type (int or Behavior enum, e.g., Behavior.PATROL)
    waypoints: List of (x, y) tuples for WAYPOINT/PATROL/LOOP behaviors
    turns: Number of turns for SLEEP behavior
    path: Pre-computed path as list of (x, y) tuples for PATH behavior
    pathfinder: DijkstraMap, AStarPath, or (x, y) target tuple for SEEK behavior

Returns:
    None
{% endraw %}

### `update_visibility() -> None`

{% raw %}update_visibility() -> None

Recompute which cells are visible from this entity's position and update perspective_map.


Returns:
    None

Note:
    Called automatically when the entity moves if the grid has FOV configured.
{% endraw %}

### `visible_entities(fov=None, radius: int | None = None) -> list[Entity]`

{% raw %}visible_entities(fov=None, radius: int | None = None) -> list[Entity]

Get list of other entities visible from this entity's position.

Args:
    fov: FOV algorithm to use (FOV enum or None to use grid.fov)
    radius: FOV radius as int; pass None, omit, or pass -1 to use the grid's default fov_radius

Returns:
    List of Entity objects within field of view, excluding self

Raises:
    ValueError: If entity is not associated with a grid

Raises:
    TypeError: If radius is neither an int nor None
{% endraw %}
