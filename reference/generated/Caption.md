---
title: Caption
layout: default
mcrf:
  objects:
    - Caption
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Caption

{% raw %}Caption(pos=None, font=None, text='', **kwargs)

A text display UI element with customizable font and styling.

Args:
    pos (tuple, optional): Position as (x, y) tuple. Default: (0, 0)
    font (Font, optional): Font object for text rendering. Default: engine default font
    text (str, optional): The text content to display. Default: ''

Keyword Args:
    fill_color (Color): Text fill color. Default: (255, 255, 255, 255)
    outline_color (Color): Text outline color. Default: (0, 0, 0, 255)
    outline (float): Text outline thickness. Default: 0
    font_size (float): Font size in points. Default: 16
    click (callable): Click event handler. Default: None
    visible (bool): Visibility state. Default: True
    opacity (float): Opacity (0.0-1.0). Default: 1.0
    z_index (int): Rendering order. Default: 0
    name (str): Element name for finding. Default: None
    x (float): X position override. Default: 0
    y (float): Y position override. Default: 0
    align (Alignment): Alignment relative to parent. Default: None
    margin (float): Margin from parent edge when aligned. Default: 0
    horiz_margin (float): Horizontal margin override. Default: 0 (use margin)
    vert_margin (float): Vertical margin override. Default: 0 (use margin)

Attributes:
    text (str): The displayed text content
    x, y (float): Position in pixels
    pos (Vector): Position as a Vector object
    font (Font): Font used for rendering
    font_size (float): Font size in points
    fill_color, outline_color (Color): Text appearance
    outline (float): Outline thickness
    click (callable): Click event handler
    visible (bool): Visibility state
    opacity (float): Opacity value
    z_index (int): Rendering order
    name (str): Element name
    w, h (float): Read-only computed size based on text and font
    align (Alignment): Alignment relative to parent (or None)
    margin (float): General margin for alignment
    horiz_margin (float): Horizontal margin override
    vert_margin (float): Vertical margin override{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `align` | {% raw %}Alignment relative to parent bounds (Alignment enum or None). When set, position is automatically calculated when parent is assigned or resized. Set to None to disable alignment and use manual positioning.{% endraw %} |
| `bounds` | {% raw %}Axis-aligned bounding box (tuple, read-only) as a (pos, size) pair of Vectors: (Vector(x, y), Vector(width, height)).{% endraw %} |
| `fill_color` | {% raw %}Fill color of the text (Color). Returns a copy; modifying components requires reassignment. For animation, use 'fill_color.r', 'fill_color.g', etc.{% endraw %} |
| `font` | {% raw %}Font used for text rendering (Font, read-only). Reflects the engine default font when none was provided at construction.{% endraw %} |
| `font_size` | {% raw %}Font size in points (int). Clamped to the range [0, 65535].{% endraw %} |
| `global_bounds` | {% raw %}Axis-aligned bounding box in screen coordinates (tuple, read-only) as a (pos, size) pair of Vectors: (Vector(x, y), Vector(width, height)).{% endraw %} |
| `global_position` | {% raw %}Global screen position (read-only). Calculates absolute position by walking up the parent chain.{% endraw %} |
| `grid_pos` | {% raw %}Position in grid tile coordinates (Vector). Only valid when parent is a Grid.{% endraw %} |
| `grid_size` | {% raw %}Size in grid tile coordinates (Vector). Only valid when parent is a Grid.{% endraw %} |
| `h` | {% raw %}Text height in pixels (float, read-only).{% endraw %} |
| `horiz_margin` | {% raw %}Horizontal margin override (float, 0 = use general margin). Invalid for vertically-centered alignments (TOP_CENTER, BOTTOM_CENTER, CENTER).{% endraw %} |
| `hovered` | {% raw %}Whether mouse is currently over this element (read-only). Updated automatically by the engine during mouse movement.{% endraw %} |
| `margin` | {% raw %}General margin from edge when aligned (float). Applied to both horizontal and vertical edges unless overridden. Invalid for CENTER alignment (raises ValueError).{% endraw %} |
| `name` | {% raw %}Name for finding elements (str).{% endraw %} |
| `on_click` | {% raw %}Callable executed when object is clicked. Function receives (pos: Vector, button: MouseButton, action: InputState).{% endraw %} |
| `on_enter` | {% raw %}Callback for mouse enter events. Called with (pos: Vector) when mouse enters this element's bounds.{% endraw %} |
| `on_exit` | {% raw %}Callback for mouse exit events. Called with (pos: Vector) when mouse leaves this element's bounds.{% endraw %} |
| `on_move` | {% raw %}Callback for mouse movement within bounds. Called with (pos: Vector) for each mouse movement while inside. Performance note: Called frequently during movement - keep handlers fast.{% endraw %} |
| `opacity` | {% raw %}Opacity level (0.0 = transparent, 1.0 = opaque). Automatically clamped to valid range [0.0, 1.0].{% endraw %} |
| `origin` | {% raw %}Transform origin as Vector (pivot point for rotation). Default (0,0) is top-left; set to (w/2, h/2) to rotate around center.{% endraw %} |
| `outline` | {% raw %}Thickness of the text outline border (float). Clamped to non-negative values.{% endraw %} |
| `outline_color` | {% raw %}Outline color of the text (Color). Returns a copy; modifying components requires reassignment. For animation, use 'outline_color.r', 'outline_color.g', etc.{% endraw %} |
| `parent` | {% raw %}Parent drawable. Get: Returns the parent Frame/Grid if nested, or None if at scene level. Set: Assign a Frame/Grid to reparent, or None to remove from parent.{% endraw %} |
| `pos` | {% raw %}Position as (x, y) Vector.{% endraw %} |
| `rotate_with_camera` | {% raw %}Whether to rotate visually with parent Grid's camera_rotation (bool). False (default): stay screen-aligned. True: tilt with camera. Only affects children of UIGrid; ignored for other parents.{% endraw %} |
| `rotation` | {% raw %}Rotation angle in degrees (clockwise around origin). Animatable property.{% endraw %} |
| `shader` | {% raw %}Shader for GPU visual effects (Shader or None). When set, the drawable is rendered through the shader program. Set to None to disable shader effects.{% endraw %} |
| `size` | {% raw %}Text dimensions as Vector (read-only).{% endraw %} |
| `text` | {% raw %}The text string displayed by this Caption (str).{% endraw %} |
| `uniforms` | {% raw %}Collection of shader uniforms (read-only access to collection). Set uniforms via dict-like syntax: drawable.uniforms['name'] = value. Supports float, vec2/3/4 tuples, PropertyBinding, and CallableBinding.{% endraw %} |
| `vert_margin` | {% raw %}Vertical margin override (float, 0 = use general margin). Invalid for horizontally-centered alignments (CENTER_LEFT, CENTER_RIGHT, CENTER).{% endraw %} |
| `visible` | {% raw %}Whether the object is visible (bool). Invisible objects are not rendered or clickable.{% endraw %} |
| `w` | {% raw %}Text width in pixels (float, read-only).{% endraw %} |
| `x` | {% raw %}X coordinate of top-left corner (float).{% endraw %} |
| `y` | {% raw %}Y coordinate of top-left corner (float).{% endraw %} |
| `z_index` | {% raw %}Z-order for rendering (lower values rendered first). Automatically triggers scene resort when changed.{% endraw %} |

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
