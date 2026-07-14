---
title: LdtkProject
layout: default
mcrf:
  objects:
    - LdtkProject
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# LdtkProject

{% raw %}LdtkProject(path: str)

Load an LDtk project file (.ldtk).

Parses the project and provides access to tilesets, auto-rule sets,
levels, and enum definitions.

Args:
    path: Path to the .ldtk project file.

Properties:
    version (str, read-only): LDtk JSON format version.
    tileset_names (list[str], read-only): Names of all tilesets.
    ruleset_names (list[str], read-only): Names of all rule sets.
    level_names (list[str], read-only): Names of all levels.
    enums (dict, read-only): Enum definitions from the project.

Example:
    proj = mcrfpy.LdtkProject('dungeon.ldtk')
    ts = proj.tileset('Dungeon_Tiles')
    rs = proj.ruleset('Walls')
    level = proj.level('Level_0')
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `enums` | {% raw %}Enum definitions from the project as a list of dicts (read-only).{% endraw %} |
| `level_names` | {% raw %}List of level identifier names (list[str], read-only).{% endraw %} |
| `ruleset_names` | {% raw %}List of rule set / layer names (list[str], read-only).{% endraw %} |
| `tileset_names` | {% raw %}List of tileset identifier names (list[str], read-only).{% endraw %} |
| `version` | {% raw %}LDtk JSON format version string (str, read-only).{% endraw %} |

## Methods

### `level(name: str) -> dict`

{% raw %}level(name: str) -> dict

Get level data by name.

Args:
    name: Level identifier from the LDtk project

Returns:
    Dict with name, dimensions, world position, and layer data.

Raises:
    KeyError: If no level with the given name exists
{% endraw %}

### `ruleset(name: str) -> AutoRuleSet`

{% raw %}ruleset(name: str) -> AutoRuleSet

Get an auto-rule set by layer name.

Args:
    name: Layer identifier from the LDtk project

Returns:
    An AutoRuleSet for resolving IntGrid data to sprite tiles.

Raises:
    KeyError: If no ruleset with the given name exists
{% endraw %}

### `tileset(name: str) -> TileSetFile`

{% raw %}tileset(name: str) -> TileSetFile

Get a tileset by name.

Args:
    name: Tileset identifier from the LDtk project

Returns:
    A TileSetFile object for texture creation and tile metadata.

Raises:
    KeyError: If no tileset with the given name exists
{% endraw %}
