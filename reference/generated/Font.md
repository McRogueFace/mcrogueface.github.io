---
title: Font
layout: default
mcrf:
  objects:
    - Font
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Font

{% raw %}Font(filename: str)

A font resource for rendering text in Caption elements.

Args:
    filename: Path to a TrueType (.ttf) or OpenType (.otf) font file.

Properties:
    family (str, read-only): Font family name from metadata.
    source (str, read-only): File path used to load this font.
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `family` | {% raw %}Font family name (str, read-only). Retrieved from font metadata.{% endraw %} |
| `source` | {% raw %}Source filename path (str, read-only). The path used to load this font.{% endraw %} |
