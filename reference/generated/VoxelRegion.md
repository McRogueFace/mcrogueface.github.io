---
title: VoxelRegion
layout: default
mcrf:
  objects:
    - VoxelRegion
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# VoxelRegion

{% raw %}VoxelRegion - Portable voxel data for copy/paste operations.

Created by VoxelGrid.copy_region(), used with paste_region().
Cannot be instantiated directly.

Properties:
    size (tuple, read-only): Dimensions as (width, height, depth)
    width, height, depth (int, read-only): Individual dimensions{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `depth` | {% raw %}Region depth. Read-only.{% endraw %} |
| `height` | {% raw %}Region height. Read-only.{% endraw %} |
| `size` | {% raw %}Dimensions (width, height, depth) of the region. Read-only.{% endraw %} |
| `width` | {% raw %}Region width. Read-only.{% endraw %} |
