---
title: VoxelGrid
layout: default
mcrf:
  objects:
    - VoxelGrid
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# VoxelGrid

{% raw %}VoxelGrid(size: tuple[int, int, int], cell_size: float = 1.0)

A dense 3D grid of voxel material IDs with a material palette.

VoxelGrids provide volumetric storage for 3D structures like buildings,
caves, and dungeon walls. Each cell stores a uint8 material ID (0-255),
where 0 is always air.

Args:
    size: (width, height, depth) dimensions. Immutable after creation.
    cell_size: World units per voxel. Default 1.0.

Properties:
    size (tuple, read-only): Grid dimensions as (width, height, depth)
    width, height, depth (int, read-only): Individual dimensions
    cell_size (float, read-only): World units per voxel
    offset (tuple): World-space position (x, y, z)
    rotation (float): Y-axis rotation in degrees
    material_count (int, read-only): Number of defined materials

Example:
    voxels = mcrfpy.VoxelGrid(size=(16, 8, 16), cell_size=1.0)
    stone = voxels.add_material('stone', color=mcrfpy.Color(128, 128, 128))
    voxels.set(5, 0, 5, stone)
    assert voxels.get(5, 0, 5) == stone
    print(f'Non-air voxels: {voxels.count_non_air()}'){% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `cell_size` | {% raw %}World units per voxel. Read-only.{% endraw %} |
| `depth` | {% raw %}Grid depth (Z dimension). Read-only.{% endraw %} |
| `greedy_meshing` | {% raw %}Enable greedy meshing optimization (reduces vertex count for uniform regions).{% endraw %} |
| `height` | {% raw %}Grid height (Y dimension). Read-only.{% endraw %} |
| `material_count` | {% raw %}Number of materials in the palette. Read-only.{% endraw %} |
| `offset` | {% raw %}World-space position (x, y, z) of the grid origin.{% endraw %} |
| `rotation` | {% raw %}Y-axis rotation in degrees.{% endraw %} |
| `size` | {% raw %}Dimensions (width, height, depth) of the grid. Read-only.{% endraw %} |
| `vertex_count` | {% raw %}Number of vertices after mesh generation. Read-only.{% endraw %} |
| `visible` | {% raw %}Show or hide this voxel grid in rendering.{% endraw %} |
| `width` | {% raw %}Grid width (X dimension). Read-only.{% endraw %} |

## Methods

### `add_material(name, color=Color(255,255,255), sprite_index=-1, transparent=False, path_cost=1.0) -> int`

{% raw %}add_material(name, color=Color(255,255,255), sprite_index=-1, transparent=False, path_cost=1.0) -> int

Add a new material to the palette. Returns the material ID (1-indexed).

Material 0 is always air (implicit, never stored in palette).
Maximum 255 materials can be added.{% endraw %}

### `clear() -> None`

{% raw %}clear() -> None

Clear the grid (fill with air, material 0).{% endraw %}

### `copy_region(min_coord, max_coord) -> VoxelRegion`

{% raw %}copy_region(min_coord, max_coord) -> VoxelRegion

Copy a rectangular region to a VoxelRegion prefab.

Args:
    min_coord: (x0, y0, z0) - minimum corner (inclusive)
    max_coord: (x1, y1, z1) - maximum corner (inclusive)

Returns:
    VoxelRegion object that can be pasted elsewhere.{% endraw %}

### `count_material(material) -> int`

{% raw %}count_material(material) -> int

Count the number of voxels with the specified material ID.{% endraw %}

### `count_non_air() -> int`

{% raw %}count_non_air() -> int

Count the number of non-air voxels in the grid.{% endraw %}

### `fill(material) -> None`

{% raw %}fill(material) -> None

Fill the entire grid with the specified material ID.{% endraw %}

### `fill_box(min_coord, max_coord, material) -> None`

{% raw %}fill_box(min_coord, max_coord, material) -> None

Fill a rectangular region with the specified material.

Args:
    min_coord: (x0, y0, z0) - minimum corner (inclusive)
    max_coord: (x1, y1, z1) - maximum corner (inclusive)
    material: material ID (0-255)

Coordinates are clamped to grid bounds.{% endraw %}

### `fill_box_hollow(min_coord, max_coord, material, thickness=1) -> None`

{% raw %}fill_box_hollow(min_coord, max_coord, material, thickness=1) -> None

Create a hollow rectangular room (walls only, hollow inside).

Args:
    min_coord: (x0, y0, z0) - minimum corner (inclusive)
    max_coord: (x1, y1, z1) - maximum corner (inclusive)
    material: material ID for walls (0-255)
    thickness: wall thickness in voxels (default 1){% endraw %}

### `fill_cylinder(base_pos, radius, height, material) -> None`

{% raw %}fill_cylinder(base_pos, radius, height, material) -> None

Fill a vertical cylinder (Y-axis aligned).

Args:
    base_pos: (cx, cy, cz) - base center position
    radius: cylinder radius in voxels
    height: cylinder height in voxels
    material: material ID (0-255){% endraw %}

### `fill_noise(min_coord, max_coord, material, threshold=0.5, scale=0.1, seed=0) -> None`

{% raw %}fill_noise(min_coord, max_coord, material, threshold=0.5, scale=0.1, seed=0) -> None

Fill region with 3D noise-based pattern (caves, clouds).

Args:
    min_coord: (x0, y0, z0) - minimum corner
    max_coord: (x1, y1, z1) - maximum corner
    material: material ID for solid areas
    threshold: noise threshold (0-1, higher = more solid)
    scale: noise scale (smaller = larger features)
    seed: random seed (0 for default){% endraw %}

### `fill_sphere(center, radius, material) -> None`

{% raw %}fill_sphere(center, radius, material) -> None

Fill a spherical region.

Args:
    center: (cx, cy, cz) - sphere center coordinates
    radius: sphere radius in voxels
    material: material ID (0-255, use 0 to carve){% endraw %}

### `from_bytes(data) -> bool`

{% raw %}from_bytes(data) -> bool

Load voxel data from a bytes object.

Args:
    data: bytes object containing serialized grid data

Returns:
    True on success, False on failure.

Note: This replaces the current grid data entirely.{% endraw %}

### `get(x, y, z) -> int`

{% raw %}get(x, y, z) -> int

Get the material ID at integer coordinates.

Returns 0 (air) for out-of-bounds coordinates.{% endraw %}

### `get_material(id) -> dict`

{% raw %}get_material(id) -> dict

Get material properties by ID.

Returns dict with keys: name, color, sprite_index, transparent, path_cost.
ID 0 returns the implicit air material.{% endraw %}

### `load(path) -> bool`

{% raw %}load(path) -> bool

Load voxel data from a binary file.

Args:
    path: File path to load from

Returns:
    True on success, False on failure.

Note: This replaces the current grid data entirely, including
dimensions and material palette.{% endraw %}

### `paste_region(region, position, skip_air=True) -> None`

{% raw %}paste_region(region, position, skip_air=True) -> None

Paste a VoxelRegion prefab at the specified position.

Args:
    region: VoxelRegion from copy_region()
    position: (x, y, z) - paste destination
    skip_air: if True, air voxels don't overwrite (default True){% endraw %}

### `project_column(x, z, headroom=2) -> dict`

{% raw %}project_column(x, z, headroom=2) -> dict

Project a single column to navigation info.

Scans the column from top to bottom, finding the topmost floor
(solid voxel with air above) and checking for adequate headroom.

Args:
    x: X coordinate in voxel grid
    z: Z coordinate in voxel grid
    headroom: Required air voxels above floor (default 2)

Returns:
    dict with keys:
        height (float): World Y of floor surface
        walkable (bool): True if floor found with adequate headroom
        transparent (bool): True if no opaque voxels in column
        path_cost (float): Floor material's path cost{% endraw %}

### `rebuild_mesh() -> None`

{% raw %}rebuild_mesh() -> None

Force immediate mesh rebuild for rendering.{% endraw %}

### `save(path) -> bool`

{% raw %}save(path) -> bool

Save the voxel grid to a binary file.

Args:
    path: File path to save to (.mcvg extension recommended)

Returns:
    True on success, False on failure.

The file format includes grid dimensions, cell size, material palette,
and RLE-compressed voxel data.{% endraw %}

### `set(x, y, z, material) -> None`

{% raw %}set(x, y, z, material) -> None

Set the material ID at integer coordinates.

Out-of-bounds coordinates are silently ignored.{% endraw %}

### `to_bytes() -> bytes`

{% raw %}to_bytes() -> bytes

Serialize the voxel grid to a bytes object.

Returns:
    bytes object containing the serialized grid data.

Useful for network transmission or custom storage.{% endraw %}
