---
title: Model3D
layout: default
mcrf:
  objects:
    - Model3D
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Model3D

{% raw %}Model3D(path=None)

A 3D model resource that can be rendered by Entity3D.

Args:
    path (str, optional): Path to .glb file to load. If None, creates empty model.

Class Methods:
    cube(size=1.0) -> Model3D: Create a unit cube
    plane(width=1.0, depth=1.0, segments=1) -> Model3D: Create a flat plane
    sphere(radius=0.5, segments=16, rings=12) -> Model3D: Create a UV sphere

Properties:
    name (str, read-only): Model name
    vertex_count (int, read-only): Total vertices across all meshes
    triangle_count (int, read-only): Total triangles across all meshes
    has_skeleton (bool, read-only): Whether model has skeletal animation data
    bounds (tuple, read-only): AABB as ((min_x, min_y, min_z), (max_x, max_y, max_z))
    mesh_count (int, read-only): Number of submeshes
    bone_count (int, read-only): Number of bones in skeleton
    animation_clips (list, read-only): List of animation clip names{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `animation_clips` | {% raw %}List of animation clip names (read-only){% endraw %} |
| `bone_count` | {% raw %}Number of bones in skeleton (read-only){% endraw %} |
| `bounds` | {% raw %}AABB as ((min_x, min_y, min_z), (max_x, max_y, max_z)) (read-only){% endraw %} |
| `has_skeleton` | {% raw %}Whether model has skeletal animation data (read-only){% endraw %} |
| `mesh_count` | {% raw %}Number of submeshes (read-only){% endraw %} |
| `name` | {% raw %}Model name (read-only){% endraw %} |
| `triangle_count` | {% raw %}Total triangle count across all meshes (read-only){% endraw %} |
| `vertex_count` | {% raw %}Total vertex count across all meshes (read-only){% endraw %} |

## Methods

### `cube(size=1.0) -> Model3D`

*classmethod*

{% raw %}cube(size=1.0) -> Model3D

Create a unit cube centered at origin.{% endraw %}

### `plane(width=1.0, depth=1.0, segments=1) -> Model3D`

*classmethod*

{% raw %}plane(width=1.0, depth=1.0, segments=1) -> Model3D

Create a flat plane.{% endraw %}

### `sphere(radius=0.5, segments=16, rings=12) -> Model3D`

*classmethod*

{% raw %}sphere(radius=0.5, segments=16, rings=12) -> Model3D

Create a UV sphere.{% endraw %}
