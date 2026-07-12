---
title: ColorLayer
layout: default
mcrf:
  objects:
    - ColorLayer
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# ColorLayer

{% raw %}ColorLayer(z_index=-1, name=None, grid_size=None)

A grid layer that stores RGBA colors per cell for background/overlay effects.

ColorLayers can be created standalone and attached to a Grid via add_layer()
or passed to the Grid constructor's layers parameter. Layers with size (0, 0)
automatically resize to match the Grid when attached.

Args:
    z_index (int): Render order relative to entities. Negative values render
        below entities (as backgrounds), positive values render above entities
        (as overlays). Default: -1 (background)
    name (str): Layer name for Grid.layer(name) lookup. Default: None
    grid_size (tuple): Dimensions as (width, height). If None or (0, 0), the
        layer will auto-resize when attached to a Grid. Default: None

Attributes:
    z_index (int): Layer z-order relative to entities (read/write)
    name (str): Layer name for lookup (read-only)
    visible (bool): Whether layer is rendered (read/write)
    grid_size (tuple): Layer dimensions as (width, height) (read-only)
    grid (Grid): Parent Grid or None. Setting manages layer association.

Methods:
    at(x, y) -> Color: Get the color at cell position (x, y)
    set(x, y, color): Set the color at cell position (x, y)
    fill(color): Fill the entire layer with a single color
    fill_rect(x, y, w, h, color): Fill a rectangular region with a color
    draw_fov(...): Draw FOV-based visibility colors
    apply_perspective(entity, ...): Bind layer to entity for automatic FOV updates

Example:
    fog = mcrfpy.ColorLayer(z_index=-1, name='fog')
    grid = mcrfpy.Grid(grid_size=(20, 15), layers=[fog])
    fog.fill(mcrfpy.Color(40, 40, 40))  # Dark gray background
    grid.layer('fog').set(5, 5, mcrfpy.Color(255, 0, 0, 128)){% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `grid` | {% raw %}Parent Grid or None (Grid \| None). Setting manages layer association and handles lazy allocation.{% endraw %} |
| `grid_size` | {% raw %}Layer dimensions as (width, height) tuple (tuple, read-only).{% endraw %} |
| `name` | {% raw %}Layer name (str, read-only). Used for Grid.layer(name) lookup.{% endraw %} |
| `visible` | {% raw %}Whether the layer is rendered (bool).{% endraw %} |
| `z_index` | {% raw %}Layer z-order (int). Negative values render below entities.{% endraw %} |

## Methods

### `apply_gradient(source: HeightMap, range: tuple, color_low: Color, color_high: Color) -> ColorLayer`

{% raw %}apply_gradient(source: HeightMap, range: tuple, color_low: Color, color_high: Color) -> ColorLayer

Interpolate between two colors based on HeightMap value within a range. Uses the original heightmap value for smooth transitions.

Args:
    source: Source heightmap (must match layer dimensions)
    range: Value range as (min, max) inclusive
    color_low: Color at range minimum
    color_high: Color at range maximum

Returns:
    self for method chaining
{% endraw %}

### `apply_perspective(entity: Entity, visible: Color | None = None, discovered: Color | None = None, unknown: Color | None = None) -> None`

{% raw %}apply_perspective(entity: Entity, visible: Color | None = None, discovered: Color | None = None, unknown: Color | None = None) -> None

Bind this layer to an entity for automatic FOV updates. After binding, call update_perspective() when the entity moves.

Args:
    entity: The entity whose perspective to track
    visible: Color for currently visible cells
    discovered: Color for previously seen cells
    unknown: Color for never-seen cells
{% endraw %}

### `apply_ranges(source: HeightMap, ranges: list) -> ColorLayer`

{% raw %}apply_ranges(source: HeightMap, ranges: list) -> ColorLayer

Apply multiple color assignments from a HeightMap in a single pass. Later ranges override earlier ones if overlapping.

Args:
    source: Source heightmap (must match layer dimensions)
    ranges: List of range specs: ((min, max), color) for fixed or ((min, max), (color_low, color_high)) for gradient

Returns:
    self for method chaining

Note:
    Cells not matching any range are left unchanged.
{% endraw %}

### `apply_threshold(source: HeightMap, range: tuple, color: Color) -> ColorLayer`

{% raw %}apply_threshold(source: HeightMap, range: tuple, color: Color) -> ColorLayer

Set a fixed color for cells where the HeightMap value falls within a range.

Args:
    source: Source heightmap (must match layer dimensions)
    range: Value range as (min, max) inclusive
    color: Color or (r, g, b[, a]) tuple to set for cells in range

Returns:
    self for method chaining
{% endraw %}

### `at(pos: tuple | Vector) or (x: int, y: int) -> Color`

{% raw %}at(pos: tuple | Vector) or (x: int, y: int) -> Color

Get the color at a cell position.

Args:
    pos: Position as (x, y) tuple, list, or Vector; or pass x and y separately

Returns:
    Color at the specified cell

Raises:
    IndexError: If coordinates are out of bounds
{% endraw %}

### `clear_perspective() -> None`

{% raw %}clear_perspective() -> None

Remove the perspective binding from this layer.

{% endraw %}

### `draw_fov(source: tuple, radius: int | None = None, fov: FOV | None = None, visible: Color | None = None, discovered: Color | None = None, unknown: Color | None = None) -> None`

{% raw %}draw_fov(source: tuple, radius: int | None = None, fov: FOV | None = None, visible: Color | None = None, discovered: Color | None = None, unknown: Color | None = None) -> None

Paint cells based on field-of-view visibility from a source position.

Args:
    source: FOV origin as (x, y)
    radius: FOV radius; defaults to the grid's fov_radius
    fov: FOV algorithm; defaults to the grid's fov setting
    visible: Color for currently visible cells
    discovered: Color for previously seen cells
    unknown: Color for never-seen cells

Note:
    Layer must be attached to a grid for FOV calculation.
{% endraw %}

### `edit() -> context manager`

{% raw %}edit() -> context manager

Context manager yielding a zero-copy, writable view of the layer's RGBA data with shape (height, width, 4), dtype uint8. Writes to the view alias the layer's storage (no copy). On exit the whole layer is invalidated and re-rendered.


Note:
    Use as `with layer.edit() as view:` -- e.g. np.asarray(view)[...] = ....

See also: Bulk-edit convention (#328) (docs/api-stability.md)
{% endraw %}

### `fill(color: Color) -> None`

{% raw %}fill(color: Color) -> None

Fill the entire layer with the specified color.

Args:
    color: Color object or (r, g, b[, a]) tuple
{% endraw %}

### `fill_rect(pos: tuple, size: tuple, color: Color) -> None`

{% raw %}fill_rect(pos: tuple, size: tuple, color: Color) -> None

Fill a rectangular region with a color.

Args:
    pos: Top-left corner as (x, y)
    size: Dimensions as (width, height)
    color: Color object or (r, g, b[, a]) tuple
{% endraw %}

### `set(pos, color: Color) -> None`

{% raw %}set(pos, color: Color) -> None

Set the color at a cell position.

Args:
    pos: Position as (x, y) tuple, list, or Vector
    color: Color object or (r, g, b[, a]) tuple

Raises:
    IndexError: If coordinates are out of bounds
{% endraw %}

### `update_perspective() -> None`

{% raw %}update_perspective() -> None

Redraw FOV based on the bound entity's current position. Call this after the entity moves to update the visibility layer.


Raises:
    RuntimeError: If no perspective binding has been set via apply_perspective()
{% endraw %}
