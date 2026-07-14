---
title: GridData
layout: default
mcrf:
  objects:
    - GridData
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# GridData {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}GridData(grid_size=None, texture=None, layers=None)

A tile map: cells, entities, layers, FOV and pathfinding state.

GridData is DATA, not a widget -- it has no position, no size, no
camera, and is never drawn. Appending one to a scene raises TypeError.
To display it, point one or more Grid (GridView) cameras at it:

    data = mcrfpy.GridData(grid_size=(80, 40))
    main = mcrfpy.Grid(grid=data, pos=(0, 0), size=(800, 400))
    mini = mcrfpy.Grid(grid=data, pos=(820, 0), size=(160, 80))

Both views show the same map and the same entities, each through its
own camera. A map with no view at all is perfectly valid (an offscreen
level, still steppable and queryable).

mcrfpy.Grid(grid_size=...) is sugar for a GridView that creates its own
GridData; reach it with `grid.grid_data`.

Args:
    grid_size (tuple): Grid dimensions as (grid_w, grid_h). Default: (2, 2)
    texture (Texture): Tile atlas; defines the cell size in pixels.
    layers (list): ColorLayer/TileLayer objects. Omit for a default
        'tilesprite' TileLayer; pass None for no layers at all.

Attributes:
    grid_size (Vector, read-only): Dimensions in tiles
    grid_w, grid_h (int, read-only): Dimensions in tiles
    texture (Texture, read-only): Tile atlas
    entities (EntityCollection): Entities on this map
    layers (tuple, read-only): Layers sorted by z_index
    fov (FOV): Default field-of-view algorithm
    fov_radius (int): Default field-of-view radius{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `entities` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}EntityCollection of entities on this map (EntityCollection, read-only). Shared by every view of this data.{% endraw %} |
| `fov` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}FOV algorithm for this map (FOV enum). Used by entity.updateVisibility() and layer methods when fov=None.{% endraw %} |
| `fov_radius` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Default FOV radius for this map (int). Used when radius is not specified.{% endraw %} |
| `grid_h` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Grid height in cells (int, read-only).{% endraw %} |
| `grid_size` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Grid dimensions as (grid_w, grid_h) (Vector, read-only).{% endraw %} |
| `grid_w` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Grid width in cells (int, read-only).{% endraw %} |
| `layers` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Tuple of grid layers sorted by z_index (tuple, read-only). Contains ColorLayer and TileLayer objects.{% endraw %} |
| `texture` {% include api_badge.html kind="added" version="0.2.8-dev" %} | {% raw %}Tile atlas for this map (Texture \| None, read-only). Defines the cell size in pixels.{% endraw %} |

## Methods

### `add_layer(layer: ColorLayer | TileLayer) -> ColorLayer | TileLayer` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}add_layer(layer: ColorLayer | TileLayer) -> ColorLayer | TileLayer

Add a layer to the grid. Layers with size (0, 0) are automatically resized to match the grid.

Args:
    layer: A ColorLayer or TileLayer object. Named layers replace any existing layer with the same name.

Returns:
    The added layer object

Raises:
    ValueError: If layer is already attached to another grid, or if layer size doesn't match grid (and isn't (0,0))

Raises:
    TypeError: If argument is not a ColorLayer or TileLayer
{% endraw %}

### `apply_ranges(source: HeightMap, ranges: list) -> GridData` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}apply_ranges(source: HeightMap, ranges: list) -> GridData

Apply multiple walkability thresholds to the grid in a single pass.

Args:
    source: HeightMap with values to check. Must match grid size.
    ranges: List of (range_tuple, properties_dict) tuples where range_tuple=(min,max) and properties_dict has 'walkable'/'transparent' keys

Returns:
    GridData: self, for method chaining
{% endraw %}

### `apply_threshold(source: HeightMap, range: tuple, walkable: bool = None, transparent: bool = None) -> GridData` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}apply_threshold(source: HeightMap, range: tuple, walkable: bool = None, transparent: bool = None) -> GridData

Apply walkable/transparent properties to cells where heightmap values fall within range.

Args:
    source: HeightMap with values to check. Must match grid size.
    range: Tuple of (min, max) - cells with values in this range are affected
    walkable: If not None, set walkable to this value for cells in range
    transparent: If not None, set transparent to this value for cells in range

Returns:
    GridData: self, for method chaining

Raises:
    ValueError: If HeightMap size doesn't match grid size
{% endraw %}

### `at(x: int, y: int) -> GridPoint` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}at(x: int, y: int) -> GridPoint

Return the GridPoint cell at grid coordinates (x, y).

Args:
    x: Column index (0-based)
    y: Row index (0-based)

Returns:
    GridPoint: the cell at the given position

Raises:
    IndexError: If x or y is out of range

Note:
    Also accepts a single positional tuple/list/Vector: at((x, y)) or at(vec), or keyword form: at(pos=(x, y)).
{% endraw %}

### `clear_dijkstra_maps() -> None` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}clear_dijkstra_maps() -> None

Clear all cached Dijkstra maps. Call this after modifying grid cell walkability to ensure pathfinding uses updated walkability data.

{% endraw %}

### `compute_fov(pos, radius: int = 0, light_walls: bool = True, algorithm: FOV | int = FOV.BASIC) -> None` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}compute_fov(pos, radius: int = 0, light_walls: bool = True, algorithm: FOV | int = FOV.BASIC) -> None

Compute field of view from a position. Updates the internal FOV state; use is_in_fov() to query visibility.

Args:
    pos: Position as (x, y) tuple, list, or Vector
    radius: Maximum view distance (0 = unlimited)
    light_walls: Whether walls are lit when visible
    algorithm: FOV algorithm to use (FOV.BASIC, FOV.DIAMOND, FOV.SHADOW, FOV.PERMISSIVE_0-8)

Returns:
    None
{% endraw %}

### `entities_in_radius(pos: tuple | Vector, radius: float) -> list` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}entities_in_radius(pos: tuple | Vector, radius: float) -> list

Query entities within radius using spatial hash (O(k) where k = nearby entities).

Args:
    pos: Center position as (x, y) tuple, Vector, or other 2-element sequence
    radius: Search radius

Returns:
    List of Entity objects within the radius
{% endraw %}

### `find_path(start, end, diagonal_cost: float = 1.41, collide: str = None, heuristic = None, weight: float = 1.0) -> AStarPath | None` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}find_path(start, end, diagonal_cost: float = 1.41, collide: str = None, heuristic = None, weight: float = 1.0) -> AStarPath | None

Compute A* path between two points. The returned AStarPath can be iterated or walked step-by-step.

Args:
    start: Starting position as Vector, Entity, or (x, y) tuple
    end: Target position as Vector, Entity, or (x, y) tuple
    diagonal_cost: Cost of diagonal movement (default: 1.41)
    collide: Label string. Entities with this label block pathfinding.
    heuristic: Heuristic enum member, string name, or int (EUCLIDEAN=0, MANHATTAN=1, CHEBYSHEV=2). None uses default (Euclidean).
    weight: Heuristic weight multiplier. Values > 1.0 trade optimality for speed (weighted A*).

Returns:
    AStarPath object if path exists, None otherwise
{% endraw %}

### `get_dijkstra_map(root=None, diagonal_cost: float = 1.41, collide: str = None, roots=None) -> DijkstraMap` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}get_dijkstra_map(root=None, diagonal_cost: float = 1.41, collide: str = None, roots=None) -> DijkstraMap

Get or create a cached Dijkstra distance map for a root position. Call clear_dijkstra_maps() after changing grid walkability to invalidate.

Args:
    root: Root position as Vector, Entity, or (x, y) tuple. Use 'root' for single-source maps (cached by position).
    diagonal_cost: Cost of diagonal movement (default: 1.41)
    collide: Label string. Entities with this label block pathfinding.
    roots: Sequence of root positions or a DiscreteMap mask for multi-source Dijkstra. Pass 'roots' instead of 'root' for multi-source maps (not cached).

Returns:
    DijkstraMap object for querying distances and paths
{% endraw %}

### `is_in_fov(x: int, y: int) -> bool` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}is_in_fov(x: int, y: int) -> bool

Check if a cell is in the field of view. Must call compute_fov() first to calculate visibility.

Args:
    x: Column index (0-based)
    y: Row index (0-based)

Returns:
    True if the cell is visible, False otherwise

Note:
    Also accepts a single positional tuple/list/Vector: is_in_fov((x, y)) or is_in_fov(vec), or keyword form: is_in_fov(pos=(x, y)).
{% endraw %}

### `layer(name: str) -> ColorLayer | TileLayer | None` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}layer(name: str) -> ColorLayer | TileLayer | None

Get a layer by its name.

Args:
    name: The name of the layer to find

Returns:
    The layer with the specified name, or None if not found
{% endraw %}

### `remove_layer(name_or_layer: str | ColorLayer | TileLayer) -> None` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}remove_layer(name_or_layer: str | ColorLayer | TileLayer) -> None

Remove a layer from the grid by name or by object reference.

Args:
    name_or_layer: Either a layer name (str) or the layer object itself

Raises:
    KeyError: If name is provided but no layer with that name exists

Raises:
    TypeError: If argument is not a string, ColorLayer, or TileLayer
{% endraw %}

### `step(n: int = 1, turn_order: int = None) -> None` {% include api_badge.html kind="added" version="0.2.8-dev" %}

{% raw %}step(n: int = 1, turn_order: int = None) -> None

Execute n rounds of turn-based entity behavior. Each round: entities grouped by turn_order (ascending), behaviors executed, triggers fired (TARGET, DONE, BLOCKED), movement animated.

Args:
    n: Number of rounds to execute (default: 1)
    turn_order: If provided, only process entities with this turn_order value
{% endraw %}
