---
layout: default
title: Font
---

# Font

SFML Font object for text rendering.

## Overview

A `Font` loads a TrueType font file (TTF) for use with Caption elements. Fonts are loaded once and can be shared across multiple captions. McRogueFace caches fonts internally, so loading the same font file multiple times returns the same font object.

## Quick Reference

```python
import mcrfpy

# Load a font
font = mcrfpy.Font("assets/fonts/DejaVuSans.ttf")

# Use with Caption
caption = mcrfpy.Caption(
    text="Hello, World!",
    pos=(100, 100),
    font=font
)

# Check font properties
print(f"Font family: {font.family}")
print(f"Loaded from: {font.source}")
```

## Constructor

```python
mcrfpy.Font(filename: str)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `filename` | str | Path to TTF font file |

Raises `IOError` if the font file cannot be loaded.

## Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `family` | str | read-only | Font family name (e.g., "DejaVu Sans") |
| `source` | str | read-only | Path to the loaded font file |

## Examples

### Basic Font Loading

```python
import mcrfpy

# Load font
font = mcrfpy.Font("assets/fonts/monospace.ttf")

# Create caption with font
title = mcrfpy.Caption(
    text="Game Title",
    pos=(400, 100),
    font=font
)
title.size = 48
title.fill_color = mcrfpy.Color(255, 255, 255)

scene.children.append(title)
```

### Multiple Font Styles

```python
# Load different fonts for different purposes
title_font = mcrfpy.Font("assets/fonts/fantasy.ttf")
body_font = mcrfpy.Font("assets/fonts/readable.ttf")
mono_font = mcrfpy.Font("assets/fonts/monospace.ttf")

# Title text
title = mcrfpy.Caption(text="Dungeon Quest", pos=(400, 50), font=title_font)
title.size = 64

# Description text
desc = mcrfpy.Caption(text="A roguelike adventure", pos=(400, 130), font=body_font)
desc.size = 24

# Stats display (monospace for alignment)
stats = mcrfpy.Caption(text="HP: 100  MP: 50", pos=(50, 500), font=mono_font)
stats.size = 16
```

### Font Manager Class

```python
class FontManager:
    _fonts = {}

    @classmethod
    def get(cls, name, path=None):
        """Get a font by name, loading if necessary."""
        if name not in cls._fonts:
            if path is None:
                raise ValueError(f"Font '{name}' not loaded")
            cls._fonts[name] = mcrfpy.Font(path)
        return cls._fonts[name]

    @classmethod
    def preload(cls):
        """Preload all game fonts."""
        fonts = {
            "title": "assets/fonts/title.ttf",
            "body": "assets/fonts/body.ttf",
            "mono": "assets/fonts/mono.ttf",
        }
        for name, path in fonts.items():
            cls._fonts[name] = mcrfpy.Font(path)

# Usage
FontManager.preload()
caption.font = FontManager.get("title")
```

### Error Handling

```python
def load_font_safe(path, fallback_path="assets/fonts/default.ttf"):
    """Load a font with fallback."""
    try:
        return mcrfpy.Font(path)
    except IOError:
        print(f"Warning: Could not load font '{path}', using fallback")
        return mcrfpy.Font(fallback_path)

# Usage
custom_font = load_font_safe("assets/fonts/custom.ttf")
```

### Debug Font Info

```python
font = mcrfpy.Font("assets/fonts/DejaVuSansMono.ttf")
print(f"Loaded font: {font.family}")
print(f"Source file: {font.source}")
```

## Notes

- Supported format: TrueType fonts (.ttf)
- Fonts are cached internally - loading the same file twice returns the same object
- Font size is set on the Caption, not the Font itself
- For pixel-perfect rendering at small sizes, consider bitmap fonts via Texture

## Related

<div class="related-objects">
<div class="object-links">
<a href="Caption" class="object-link">Caption</a>
<a href="Texture" class="object-link">Texture</a>
</div>
</div>
