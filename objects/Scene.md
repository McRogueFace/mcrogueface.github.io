---
layout: default
title: Scene
---

# Scene

Container for UI elements and game state.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `Scene` is a container that holds UI elements and handles input. Only one scene is active at a time. Switch between scenes for menus, gameplay, and other game states.

## Quick Reference

```python
# Create a scene
scene = mcrfpy.Scene("game")

# Activate it
scene.activate()

# Add UI elements
scene.children.append(frame)
scene.children.append(grid)

# Handle input
scene.on_key = my_key_handler
scene.on_mouse = my_mouse_handler
```

## Constructor

```python
mcrfpy.Scene(name: str)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | str | Scene identifier |
| `children` | UICollection | UI elements in this scene |
| `on_key` | callable | Keyboard input callback |
| `on_mouse` | callable | Mouse input callback |
| `on_enter` | callable | Called when scene activates |
| `on_exit` | callable | Called when scene deactivates |

## Methods

| Method | Description |
|--------|-------------|
| `activate()` | Make this scene active |

## Related

<div class="related-objects">
<div class="object-links">
<a href="Window" class="object-link">Window</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Caption" class="object-link">Caption</a>
<a href="Grid" class="object-link">Grid</a>
<a href="../systems/scene" class="object-link">Scene System</a>
</div>
</div>
