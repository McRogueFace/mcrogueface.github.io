---
layout: default
title: Animation
---

# Animation

Property animation system.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

The Animation system provides smooth property transitions for UI elements and entities. Animations interpolate values over time with configurable easing functions.

## Quick Reference

```python
# Animate position
sprite.animate("x", 200, duration=0.5, easing="easeOutQuad")
sprite.animate("y", 100, duration=0.5, easing="easeOutQuad")

# Animate with callback
def on_complete():
    print("Done!")

sprite.animate("opacity", 0, duration=1.0, callback=on_complete)

# Chain animations
def step2():
    sprite.animate("x", 0, callback=step3)

def step3():
    sprite.animate("y", 0)

sprite.animate("x", 100, callback=step2)
```

## The animate() Method

```python
element.animate(
    property: str,      # Property name ("x", "y", "scale", etc.)
    target: float,      # Target value
    duration: float,    # Duration in seconds
    easing: str,        # Easing function name
    callback: callable  # Completion callback
)
```

## Easing Functions

- `linear` - Constant speed
- `easeInQuad`, `easeOutQuad`, `easeInOutQuad` - Quadratic
- `easeInCubic`, `easeOutCubic`, `easeInOutCubic` - Cubic
- `easeInExpo`, `easeOutExpo` - Exponential
- `easeOutBounce` - Bounce effect

## Related

<div class="related-objects">
<div class="object-links">
<a href="Entity" class="object-link">Entity</a>
<a href="Sprite" class="object-link">Sprite</a>
<a href="Frame" class="object-link">Frame</a>
<a href="../systems/animation" class="object-link">Animation System</a>
</div>
</div>
