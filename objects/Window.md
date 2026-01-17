---
layout: default
title: Window
---

# Window

The application window that displays your game.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

`Window` represents the game window. McRogueFace creates a single window automatically - you access it through `mcrfpy.Window`.

## Quick Reference

```python
# Get window reference
window = mcrfpy.Window

# Window properties
window.title = "My Roguelike"
window.resolution = (1024, 768)
window.fullscreen = False
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `title` | str | Window title text |
| `resolution` | tuple | Window size (width, height) |
| `fullscreen` | bool | Fullscreen mode toggle |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Scene" class="object-link">Scene</a>
<a href="../systems/scene" class="object-link">Scene System</a>
</div>
</div>
