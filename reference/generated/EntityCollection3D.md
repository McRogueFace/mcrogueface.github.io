---
title: EntityCollection3D
layout: default
mcrf:
  objects:
    - EntityCollection3D
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# EntityCollection3D

{% raw %}Collection of Entity3D objects belonging to a Viewport3D.

Supports list-like operations: indexing, iteration, append, remove.

Example:
    viewport.entities.append(entity)
    for entity in viewport.entities:
        print(entity.pos){% endraw %}

## Methods

### `append(entity)`

{% raw %}append(entity)

Add an Entity3D to the collection.{% endraw %}

### `clear()`

{% raw %}clear()

Remove all entities from the collection.{% endraw %}

### `extend(iterable)`

{% raw %}extend(iterable)

Add all Entity3D objects from iterable to the collection.{% endraw %}

### `find(name) -> Entity3D or None`

{% raw %}find(name) -> Entity3D or None

Find an Entity3D by name. Returns None if not found.{% endraw %}

### `pop(index=-1) -> Entity3D`

{% raw %}pop(index=-1) -> Entity3D

Remove and return Entity3D at index (default: last).{% endraw %}

### `remove(entity)`

{% raw %}remove(entity)

Remove an Entity3D from the collection.{% endraw %}
