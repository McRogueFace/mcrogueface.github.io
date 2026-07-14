---
title: Grid
layout: default
mcrf:
  objects:
    - Grid
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Grid

{% raw %}Grid(grid_size=None, pos=None, size=None, texture=None, **kwargs)

A grid-based UI element for tile-based rendering and entity management.
Creates and owns grid data (cells, entities, layers) with an integrated
rendering view (camera, zoom, perspective).

Can also be constructed as a view of existing grid data:
    Grid(grid=existing_grid, pos=..., size=...)

Args:
    grid_size (tuple): Grid dimensions as (grid_w, grid_h). Default: (2, 2)
    pos (tuple): Position as (x, y). Default: (0, 0)
    size (tuple): Size as (w, h). Default: auto-calculated
    texture (Texture): Tile texture atlas. Default: default texture

Keyword Args:
    grid (Grid): Existing Grid to view (creates view of shared data).
    fill_color (Color): Background fill color.
    on_click (callable): Click event handler.
    center_x, center_y (float): Camera center coordinates.
    zoom (float): Zoom level. Default: 1.0
    visible (bool): Visibility. Default: True
    opacity (float): Opacity (0.0-1.0). Default: 1.0
    z_index (int): Rendering order. Default: 0
    name (str): Element name.
    layers (list): List of ColorLayer/TileLayer objects.
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `align` | {% raw %}Alignment relative to parent bounds (Alignment enum or None). When set, position is automatically calculated when parent is assigned or resized. Set to None to disable alignment and use manual positioning.{% endraw %} |
| `bounds` | {% raw %}Axis-aligned bounding box (tuple, read-only) as a (pos, size) pair of Vectors: (Vector(x, y), Vector(width, height)).{% endraw %} |
| `camera_rotation` | {% raw %}Rotation of grid contents around camera center in degrees (float).{% endraw %} |
| `center` | {% raw %}Camera center point in pixel coordinates (Vector).{% endraw %} |
| `center_x` | {% raw %}Camera center X-coordinate in pixel space (float).{% endraw %} |
| `center_y` | {% raw %}Camera center Y-coordinate in pixel space (float).{% endraw %} |
| `children` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}UICollection of UIDrawable children such as speech bubbles, effects, and range indicators anchored to grid content (UICollection, read-only).{% endraw %} |
| `fill_color` | {% raw %}Background fill color (Color). Drawn behind all tiles and entities.{% endraw %} |
| `global_bounds` | {% raw %}Axis-aligned bounding box in screen coordinates (tuple, read-only) as a (pos, size) pair of Vectors: (Vector(x, y), Vector(width, height)).{% endraw %} |
| `global_position` | {% raw %}Global screen position (read-only). Calculates absolute position by walking up the parent chain.{% endraw %} |
| `grid_data` | {% raw %}The underlying grid data object (Grid \| None). Used for multi-view scenarios where multiple GridViews share one Grid.{% endraw %} |
| `h` | {% raw %}Visible widget height (float).{% endraw %} |
| `horiz_margin` | {% raw %}Horizontal margin override (float, 0 = use general margin). Invalid for vertically-centered alignments (TOP_CENTER, BOTTOM_CENTER, CENTER).{% endraw %} |
| `hovered` | {% raw %}Whether mouse is currently over this element (read-only). Updated automatically by the engine during mouse movement.{% endraw %} |
| `hovered_cell` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Currently hovered cell as (x, y) tuple, or None if not hovering (tuple \| None, read-only).{% endraw %} |
| `margin` | {% raw %}General margin from edge when aligned (float). Applied to both horizontal and vertical edges unless overridden. Invalid for CENTER alignment (raises ValueError).{% endraw %} |
| `name` | {% raw %}Name for finding elements (str).{% endraw %} |
| `on_cell_click` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Callback when a grid cell is clicked (Callable \| None). Called with (cell_pos: Vector, button: MouseButton, action: InputState).{% endraw %} |
| `on_cell_enter` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Callback when mouse enters a grid cell (Callable \| None). Called with (cell_pos: Vector).{% endraw %} |
| `on_cell_exit` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Callback when mouse exits a grid cell (Callable \| None). Called with (cell_pos: Vector).{% endraw %} |
| `on_click` | {% raw %}Callable executed when object is clicked (Callable \| None).{% endraw %} |
| `on_enter` | {% raw %}Callback for mouse enter events. Called with (pos: Vector) when mouse enters this element's bounds.{% endraw %} |
| `on_exit` | {% raw %}Callback for mouse exit events. Called with (pos: Vector) when mouse leaves this element's bounds.{% endraw %} |
| `on_move` | {% raw %}Callback for mouse movement within bounds. Called with (pos: Vector) for each mouse movement while inside. Performance note: Called frequently during movement - keep handlers fast.{% endraw %} |
| `opacity` | {% raw %}Opacity level (0.0 = transparent, 1.0 = opaque). Automatically clamped to valid range [0.0, 1.0].{% endraw %} |
| `origin` | {% raw %}Transform origin as Vector (pivot point for rotation). Default (0,0) is top-left; set to (w/2, h/2) to rotate around center.{% endraw %} |
| `parent` | {% raw %}Parent drawable. Get: Returns the parent Frame/Grid if nested, or None if at scene level. Set: Assign a Frame/Grid to reparent, or None to remove from parent.{% endraw %} |
| `perspective` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Entity whose perspective_map drives fog-of-war rendering in this view (Entity \| None). Setting an entity enables perspective mode; setting None disables it. Cells the entity has never seen are drawn black, discovered-but-not-visible cells dimmed.{% endraw %} |
| `perspective_enabled` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Whether this view renders the perspective/FOV overlay (bool). Set automatically when assigning perspective; set False to show the whole map without clearing the entity.{% endraw %} |
| `pos` | {% raw %}Position of the grid as Vector (Vector).{% endraw %} |
| `rotate_with_camera` {% include api_badge.html kind="changed" version="0.2.8-dev" %} | {% raw %}Whether to rotate visually with parent Grid's camera_rotation (bool). False (default): stay screen-aligned. True: tilt with camera. Only affects children of a Grid; ignored for other parents.{% endraw %} |
| `rotation` | {% raw %}Rotation angle in degrees (clockwise around origin). Animatable property.{% endraw %} |
| `shader` | {% raw %}Shader for GPU visual effects (Shader or None). When set, the drawable is rendered through the shader program. Set to None to disable shader effects.{% endraw %} |
| `size` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Size of the grid widget in pixels as (w, h) (Vector). This is the viewport, not the map: the map's dimensions are grid_size.{% endraw %} |
| `texture` | {% raw %}Texture used for tile rendering (Texture \| None, read-only).{% endraw %} |
| `uniforms` | {% raw %}Collection of shader uniforms (read-only access to collection). Set uniforms via dict-like syntax: drawable.uniforms['name'] = value. Supports float, vec2/3/4 tuples, PropertyBinding, and CallableBinding.{% endraw %} |
| `vert_margin` | {% raw %}Vertical margin override (float, 0 = use general margin). Invalid for horizontally-centered alignments (CENTER_LEFT, CENTER_RIGHT, CENTER).{% endraw %} |
| `visible` | {% raw %}Whether the object is visible (bool). Invisible objects are not rendered or clickable.{% endraw %} |
| `w` | {% raw %}Visible widget width (float).{% endraw %} |
| `x` | {% raw %}Top-left corner X-coordinate (float).{% endraw %} |
| `y` | {% raw %}Top-left corner Y-coordinate (float).{% endraw %} |
| `z_index` | {% raw %}Z-order for rendering (int). Lower values are rendered first.{% endraw %} |
| `zoom` | {% raw %}Zoom level for rendering (float). Values greater than 1.0 magnify; less than 1.0 shrink.{% endraw %} |

## Methods

### `animate(property: str, target: Any, duration: float, easing=None, delta=False, loop=False, callback=None, conflict_mode='replace') -> Animation`

{% raw %}animate(property: str, target: Any, duration: float, easing=None, delta=False, loop=False, callback=None, conflict_mode='replace') -> Animation

Create and start an animation on this drawable's property.

Args:
    property: Name of the property to animate (e.g., 'x', 'fill_color', 'opacity')
    target: Target value - type depends on property (float, tuple for color/vector, etc.)
    duration: Animation duration in seconds
    easing: Easing function: Easing enum value, string name, or None for linear
    delta: If True, target is relative to current value; if False, target is absolute
    loop: If True, animation repeats from start when it reaches the end (default False)
    callback: Optional callable invoked when animation completes (not called for looping animations)
    conflict_mode: 'replace' (default), 'queue', or 'error' if property already animating

Returns:
    Animation object for monitoring progress

Raises:
    ValueError: If property name is not valid for this drawable type

Note:
    This is a convenience method that creates an Animation, starts it, and adds it to the AnimationManager.
{% endraw %}

### `center_camera(pos: tuple = None) -> None` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}center_camera(pos: tuple = None) -> None

Point this view's camera at a tile, or at the middle of the map when called with no argument.

Args:
    pos: (tile_x, tile_y) to center on. Offset by 0.5 to aim at a tile's middle rather than its top-left corner.

Note:
    The camera belongs to the VIEW, not the map: two views of one GridData pan independently.
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

### `realign() -> None`

{% raw %}realign() -> None

Reapply alignment relative to parent, useful for responsive layouts.


Note:
    Call this to recalculate position after parent changes size. For elements with align=None, this has no effect.
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
