---
title: AutoRuleSet
layout: default
mcrf:
  objects:
    - AutoRuleSet
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# AutoRuleSet

{% raw %}AutoRuleSet - LDtk auto-tile rule set for pattern-based terrain rendering.

AutoRuleSets are obtained from LdtkProject.ruleset().
They map IntGrid terrain values to sprite tiles using LDtk's
pattern-matching auto-rule system.

Properties:
    name (str, read-only): Rule set name (layer identifier).
    grid_size (int, read-only): Cell size in pixels.
    value_count (int, read-only): Number of IntGrid values.
    values (list, read-only): List of value dicts.
    rule_count (int, read-only): Total rules across all groups.
    group_count (int, read-only): Number of rule groups.

Example:
    rs = project.ruleset('Walls')
    Terrain = rs.terrain_enum()
    rs.apply(discrete_map, tile_layer, seed=42)
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `grid_size` | {% raw %}Cell size in pixels (int, read-only).{% endraw %} |
| `group_count` | {% raw %}Number of rule groups (int, read-only).{% endraw %} |
| `name` | {% raw %}Rule set name / layer identifier (str, read-only).{% endraw %} |
| `rule_count` | {% raw %}Total number of rules across all groups (int, read-only).{% endraw %} |
| `value_count` | {% raw %}Number of IntGrid terrain values (int, read-only).{% endraw %} |
| `values` | {% raw %}List of IntGrid value dicts with value and name (read-only).{% endraw %} |

## Methods

### `apply(discrete_map: DiscreteMap, tile_layer: TileLayer, seed: int = 0) -> None`

{% raw %}apply(discrete_map: DiscreteMap, tile_layer: TileLayer, seed: int = 0) -> None

Resolve auto-rules and write tile indices directly into a TileLayer.

Args:
    discrete_map: A DiscreteMap with IntGrid values
    tile_layer: Target TileLayer to write resolved tiles into
    seed: Random seed for deterministic results (default: 0)
{% endraw %}

### `resolve(discrete_map: DiscreteMap, seed: int = 0) -> list[int]`

{% raw %}resolve(discrete_map: DiscreteMap, seed: int = 0) -> list[int]

Resolve IntGrid data to tile indices using LDtk auto-rules.

Args:
    discrete_map: A DiscreteMap with IntGrid values matching this rule set
    seed: Random seed for deterministic tile selection and probability (default: 0)

Returns:
    List of tile IDs (one per cell). -1 means no matching rule.
{% endraw %}

### `terrain_enum() -> IntEnum`

{% raw %}terrain_enum() -> IntEnum

Generate a Python IntEnum from this rule set's IntGrid values.


Returns:
    IntEnum class with NONE=0 and one member per IntGrid value (UPPER_SNAKE_CASE).
{% endraw %}
