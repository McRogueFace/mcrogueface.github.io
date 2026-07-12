---
title: Viewport3D
layout: default
mcrf:
  objects:
    - Viewport3D
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Viewport3D

{% raw %}Viewport3D(pos=None, size=None, **kwargs)

A 3D rendering viewport that displays a 3D scene as a UI element.

Args:
    pos (tuple, optional): Position as (x, y) tuple. Default: (0, 0)
    size (tuple, optional): Display size as (width, height). Default: (320, 240)

Keyword Args:
    render_resolution (tuple): Internal render resolution (width, height). Default: (320, 240)
    fov (float): Camera field of view in degrees. Default: 60
    camera_pos (tuple): Camera position (x, y, z). Default: (0, 0, 5)
    camera_target (tuple): Camera look-at point (x, y, z). Default: (0, 0, 0)
    bg_color (Color): Background clear color. Default: (25, 25, 50)
    enable_vertex_snap (bool): PS1-style vertex snapping. Default: True
    enable_affine (bool): PS1-style affine texture mapping. Default: True
    enable_dither (bool): PS1-style color dithering. Default: True
    enable_fog (bool): Distance fog. Default: True
    fog_color (Color): Fog color. Default: (128, 128, 153)
    fog_near (float): Fog start distance. Default: 10
    fog_far (float): Fog end distance. Default: 100
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `bg_color` | {% raw %}Background clear color.{% endraw %} |
| `bounds` | {% raw %}Axis-aligned bounding box (tuple, read-only) as a (pos, size) pair of Vectors: (Vector(x, y), Vector(width, height)).{% endraw %} |
| `camera_pos` | {% raw %}Camera position as (x, y, z) tuple.{% endraw %} |
| `camera_target` | {% raw %}Camera look-at target as (x, y, z) tuple.{% endraw %} |
| `cell_size` | {% raw %}World units per navigation grid cell.{% endraw %} |
| `enable_affine` | {% raw %}Enable PS1-style affine texture mapping (warped textures).{% endraw %} |
| `enable_dither` | {% raw %}Enable PS1-style color dithering.{% endraw %} |
| `enable_fog` | {% raw %}Enable distance fog.{% endraw %} |
| `enable_vertex_snap` | {% raw %}Enable PS1-style vertex snapping (jittery vertices).{% endraw %} |
| `entities` | {% raw %}Collection of Entity3D objects (read-only). Use append/remove to modify.{% endraw %} |
| `fog_color` | {% raw %}Fog color.{% endraw %} |
| `fog_far` | {% raw %}Fog end distance.{% endraw %} |
| `fog_near` | {% raw %}Fog start distance.{% endraw %} |
| `fov` | {% raw %}Camera field of view in degrees.{% endraw %} |
| `global_bounds` | {% raw %}Axis-aligned bounding box in screen coordinates (tuple, read-only) as a (pos, size) pair of Vectors: (Vector(x, y), Vector(width, height)).{% endraw %} |
| `global_position` | {% raw %}Global screen position (read-only). Calculates absolute position by walking up the parent chain.{% endraw %} |
| `grid_size` | {% raw %}Navigation grid dimensions as (width, depth) tuple.{% endraw %} |
| `h` | {% raw %}Display height in pixels.{% endraw %} |
| `hovered` | {% raw %}Whether mouse is currently over this element (read-only). Updated automatically by the engine during mouse movement.{% endraw %} |
| `on_click` | {% raw %}Callable executed when object is clicked. Function receives (pos: Vector, button: MouseButton, action: InputState).{% endraw %} |
| `on_enter` | {% raw %}Callback for mouse enter events. Called with (pos: Vector) when mouse enters this element's bounds.{% endraw %} |
| `on_exit` | {% raw %}Callback for mouse exit events. Called with (pos: Vector) when mouse leaves this element's bounds.{% endraw %} |
| `on_move` | {% raw %}Callback for mouse movement within bounds. Called with (pos: Vector) for each mouse movement while inside. Performance note: Called frequently during movement - keep handlers fast.{% endraw %} |
| `opacity` | {% raw %}Opacity level (0.0 = transparent, 1.0 = opaque). Automatically clamped to valid range [0.0, 1.0].{% endraw %} |
| `parent` | {% raw %}Parent drawable. Get: Returns the parent Frame/Grid if nested, or None if at scene level. Set: Assign a Frame/Grid to reparent, or None to remove from parent.{% endraw %} |
| `pos` | {% raw %}Position as Vector (x, y).{% endraw %} |
| `render_resolution` | {% raw %}Internal render resolution (width, height). Lower values for PS1 effect.{% endraw %} |
| `visible` | {% raw %}Whether the object is visible (bool). Invisible objects are not rendered or clickable.{% endraw %} |
| `w` | {% raw %}Display width in pixels.{% endraw %} |
| `x` | {% raw %}X position in pixels.{% endraw %} |
| `y` | {% raw %}Y position in pixels.{% endraw %} |
| `z_index` | {% raw %}Z-order for rendering (lower values rendered first). Automatically triggers scene resort when changed.{% endraw %} |

## Methods

### `add_billboard(billboard)`

{% raw %}add_billboard(billboard)

Add a Billboard to the viewport.

Args:
    billboard: Billboard object to add{% endraw %}

### `add_layer(name, z_index=0) -> dict`

{% raw %}add_layer(name, z_index=0) -> dict

Add a new mesh layer to the viewport.

Args:
    name: Unique identifier for the layer
    z_index: Render order (lower = rendered first){% endraw %}

### `add_mesh(layer_name, model, pos, rotation=0, scale=1.0) -> int`

{% raw %}add_mesh(layer_name, model, pos, rotation=0, scale=1.0) -> int

Add a Model3D instance to a layer at the specified position.

Args:
    layer_name: Name of layer to add mesh to (created if needed)
    model: Model3D object to place
    pos: World position as (x, y, z) tuple
    rotation: Y-axis rotation in degrees
    scale: Uniform scale factor

Returns:
    Index of the mesh instance{% endraw %}

### `add_voxel_layer(voxel_grid, z_index=0)`

{% raw %}add_voxel_layer(voxel_grid, z_index=0)

Add a VoxelGrid as a renderable layer.

Args:
    voxel_grid: VoxelGrid object to render
    z_index: Render order (lower = rendered first){% endraw %}

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

### `apply_heightmap(heightmap, y_scale=1.0)`

{% raw %}apply_heightmap(heightmap, y_scale=1.0)

Set cell heights from HeightMap.

Args:
    heightmap: HeightMap object
    y_scale: Vertical scale factor{% endraw %}

### `apply_terrain_colors(layer_name, r_map, g_map, b_map)`

{% raw %}apply_terrain_colors(layer_name, r_map, g_map, b_map)

Apply per-vertex colors to terrain from RGB HeightMaps.

Args:
    layer_name: Name of terrain layer to colorize
    r_map: HeightMap for red channel (0-1 values)
    g_map: HeightMap for green channel (0-1 values)
    b_map: HeightMap for blue channel (0-1 values)

All HeightMaps must match the terrain's original dimensions.{% endraw %}

### `apply_threshold(heightmap, min_height, max_height, walkable=True)`

{% raw %}apply_threshold(heightmap, min_height, max_height, walkable=True)

Set cell walkability based on height thresholds.

Args:
    heightmap: HeightMap object
    min_height: Minimum height (0-1)
    max_height: Maximum height (0-1)
    walkable: Walkability value for cells in range{% endraw %}

### `at(x, z) -> VoxelPoint`

{% raw %}at(x, z) -> VoxelPoint

Get VoxelPoint at grid coordinates.

Args:
    x: X coordinate in grid
    z: Z coordinate in grid

Returns:
    VoxelPoint object for the cell{% endraw %}

### `billboard_count() -> int`

{% raw %}billboard_count() -> int

Get the number of billboards.

Returns:
    Number of billboards in the viewport{% endraw %}

### `build_terrain(layer_name, heightmap, y_scale=1.0, cell_size=1.0) -> int`

{% raw %}build_terrain(layer_name, heightmap, y_scale=1.0, cell_size=1.0) -> int

Build terrain mesh from HeightMap on specified layer.

Args:
    layer_name: Name of layer to build terrain on (created if doesn't exist)
    heightmap: HeightMap object with height data
    y_scale: Vertical exaggeration factor
    cell_size: World-space size of each grid cell

Returns:
    Number of vertices in the generated mesh{% endraw %}

### `clear_billboards()`

{% raw %}clear_billboards()

Remove all billboards from the viewport.{% endraw %}

### `clear_meshes(layer_name)`

{% raw %}clear_meshes(layer_name)

Clear all mesh instances from a layer.

Args:
    layer_name: Name of layer to clear{% endraw %}

### `clear_voxel_nav_region(voxel_grid)`

{% raw %}clear_voxel_nav_region(voxel_grid)

Clear navigation cells in a voxel grid's footprint.

Resets walkability, transparency, height, and cost to defaults
for all nav cells corresponding to the voxel grid's XZ extent.

Args:
    voxel_grid: VoxelGrid whose nav region to clear{% endraw %}

### `compute_fov(origin, radius=10) -> list`

{% raw %}compute_fov(origin, radius=10) -> list

Compute field of view from a position.

Args:
    origin: Origin point as (x, z) tuple
    radius: FOV radius

Returns:
    List of visible (x, z) positions{% endraw %}

### `find_path(start, end) -> list`

{% raw %}find_path(start, end) -> list

Find A* path between two points.

Args:
    start: Starting point as (x, z) tuple
    end: End point as (x, z) tuple

Returns:
    List of (x, z) tuples forming the path, or empty list if no path{% endraw %}

### `follow(entity, distance=10, height=5, smoothing=1.0)`

{% raw %}follow(entity, distance=10, height=5, smoothing=1.0)

Position camera to follow an entity.

Args:
    entity: Entity3D to follow
    distance: Distance behind entity
    height: Camera height above entity
    smoothing: Interpolation factor (0-1). 1 = instant, lower = smoother{% endraw %}

### `get_billboard(index) -> Billboard`

{% raw %}get_billboard(index) -> Billboard

Get a Billboard by index.

Args:
    index: Index of the billboard

Returns:
    Billboard object{% endraw %}

### `get_layer(name) -> dict or None`

{% raw %}get_layer(name) -> dict or None

Get a layer by name.{% endraw %}

### `is_in_fov(x, z) -> bool`

{% raw %}is_in_fov(x, z) -> bool

Check if a cell is in the current FOV (after compute_fov).

Args:
    x: X coordinate
    z: Z coordinate

Returns:
    True if the cell is visible{% endraw %}

### `layer_count() -> int`

{% raw %}layer_count() -> int

Get the number of mesh layers.{% endraw %}

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

### `orbit_camera(angle=0, distance=10, height=5)`

{% raw %}orbit_camera(angle=0, distance=10, height=5)

Position camera to orbit around origin.

Args:
    angle: Orbit angle in radians
    distance: Distance from origin
    height: Camera height above XZ plane{% endraw %}

### `place_blocking(grid_pos, footprint, walkable=False, transparent=False)`

{% raw %}place_blocking(grid_pos, footprint, walkable=False, transparent=False)

Mark grid cells as blocking for pathfinding and FOV.

Args:
    grid_pos: Top-left grid position as (x, z) tuple
    footprint: Size in cells as (width, depth) tuple
    walkable: Whether cells should be walkable (default: False)
    transparent: Whether cells should be transparent (default: False){% endraw %}

### `project_all_voxels_to_nav(headroom=2)`

{% raw %}project_all_voxels_to_nav(headroom=2)

Project all voxel layers to the navigation grid.

Resets navigation grid and projects each voxel layer in z_index order.
Later layers (higher z_index) overwrite earlier ones.

Args:
    headroom: Required air voxels above floor for walkability (default: 2){% endraw %}

### `project_voxel_to_nav(voxel_grid, headroom=2)`

{% raw %}project_voxel_to_nav(voxel_grid, headroom=2)

Project a VoxelGrid to the navigation grid.

Scans each column of the voxel grid and updates corresponding
navigation cells with walkability, transparency, height, and cost.

Args:
    voxel_grid: VoxelGrid to project
    headroom: Required air voxels above floor for walkability (default: 2){% endraw %}

### `realign() -> None`

{% raw %}realign() -> None

Reapply alignment relative to parent, useful for responsive layouts.


Note:
    Call this to recalculate position after parent changes size. For elements with align=None, this has no effect.
{% endraw %}

### `remove_billboard(billboard)`

{% raw %}remove_billboard(billboard)

Remove a Billboard from the viewport.

Args:
    billboard: Billboard object to remove{% endraw %}

### `remove_layer(name) -> bool`

{% raw %}remove_layer(name) -> bool

Remove a layer by name. Returns True if found and removed.{% endraw %}

### `remove_voxel_layer(voxel_grid) -> bool`

{% raw %}remove_voxel_layer(voxel_grid) -> bool

Remove a VoxelGrid layer from the viewport.

Args:
    voxel_grid: VoxelGrid object to remove

Returns:
    True if the layer was found and removed{% endraw %}

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

### `screen_to_world(x, y, y_plane=0.0) -> tuple or None`

{% raw %}screen_to_world(x, y, y_plane=0.0) -> tuple or None

Convert screen coordinates to world position via ray casting.

Args:
    x: Screen X coordinate relative to viewport
    y: Screen Y coordinate relative to viewport
    y_plane: Y value of horizontal plane to intersect (default: 0.0)

Returns:
    (x, y, z) world position tuple, or None if no intersection with the plane{% endraw %}

### `set_grid_size(width, depth)`

{% raw %}set_grid_size(width, depth)

Initialize navigation grid with specified dimensions.

Args:
    width: Grid width (X axis)
    depth: Grid depth (Z axis){% endraw %}

### `set_slope_cost(max_slope=0.5, cost_multiplier=1.0)`

{% raw %}set_slope_cost(max_slope=0.5, cost_multiplier=1.0)

Calculate slope costs and mark steep cells unwalkable.

Args:
    max_slope: Maximum height difference before marking unwalkable
    cost_multiplier: Cost increase per unit slope{% endraw %}

### `voxel_layer_count() -> int`

{% raw %}voxel_layer_count() -> int

Get the number of voxel layers.

Returns:
    Number of voxel layers in the viewport{% endraw %}
