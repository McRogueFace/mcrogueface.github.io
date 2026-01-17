---
layout: default
title: Easing
---

# Easing

Easing function enumeration for animations.

## Overview

The `Easing` IntEnum provides a variety of easing functions that control how animation values change over time. Different easing functions create different "feels" - from smooth and natural to bouncy and elastic.

## Quick Reference

```python
# Use with animate() method
sprite.animate("x", 500, 1.0, mcrfpy.Easing.EASE_OUT_QUAD)
sprite.animate("opacity", 0, 0.5, mcrfpy.Easing.EASE_IN_OUT)

# Bouncy effect
button.animate("scale", 1.2, 0.3, mcrfpy.Easing.EASE_OUT_ELASTIC)

# Anticipation (pullback before action)
character.animate("x", 100, 0.5, mcrfpy.Easing.EASE_IN_BACK)
```

## Values

### Linear

| Value | Description |
|-------|-------------|
| `LINEAR` | Constant speed, no acceleration |

### Basic Ease

| Value | Description |
|-------|-------------|
| `EASE_IN` | Start slow, accelerate |
| `EASE_OUT` | Start fast, decelerate |
| `EASE_IN_OUT` | Slow at both ends |

### Quadratic (Power of 2)

| Value | Description |
|-------|-------------|
| `EASE_IN_QUAD` | Quadratic acceleration |
| `EASE_OUT_QUAD` | Quadratic deceleration |
| `EASE_IN_OUT_QUAD` | Quadratic both ends |

### Cubic (Power of 3)

| Value | Description |
|-------|-------------|
| `EASE_IN_CUBIC` | Cubic acceleration |
| `EASE_OUT_CUBIC` | Cubic deceleration |
| `EASE_IN_OUT_CUBIC` | Cubic both ends |

### Quartic (Power of 4)

| Value | Description |
|-------|-------------|
| `EASE_IN_QUART` | Quartic acceleration |
| `EASE_OUT_QUART` | Quartic deceleration |
| `EASE_IN_OUT_QUART` | Quartic both ends |

### Sine

| Value | Description |
|-------|-------------|
| `EASE_IN_SINE` | Sinusoidal acceleration |
| `EASE_OUT_SINE` | Sinusoidal deceleration |
| `EASE_IN_OUT_SINE` | Sinusoidal both ends |

### Exponential

| Value | Description |
|-------|-------------|
| `EASE_IN_EXPO` | Exponential acceleration |
| `EASE_OUT_EXPO` | Exponential deceleration |
| `EASE_IN_OUT_EXPO` | Exponential both ends |

### Circular

| Value | Description |
|-------|-------------|
| `EASE_IN_CIRC` | Circular acceleration |
| `EASE_OUT_CIRC` | Circular deceleration |
| `EASE_IN_OUT_CIRC` | Circular both ends |

### Elastic (Spring-like)

| Value | Description |
|-------|-------------|
| `EASE_IN_ELASTIC` | Elastic wind-up |
| `EASE_OUT_ELASTIC` | Elastic release with overshoot |
| `EASE_IN_OUT_ELASTIC` | Elastic both ends |

### Back (Overshoot)

| Value | Description |
|-------|-------------|
| `EASE_IN_BACK` | Pull back then accelerate |
| `EASE_OUT_BACK` | Overshoot then settle |
| `EASE_IN_OUT_BACK` | Back effect both ends |

### Bounce

| Value | Description |
|-------|-------------|
| `EASE_IN_BOUNCE` | Bounces at start |
| `EASE_OUT_BOUNCE` | Bounces at end |
| `EASE_IN_OUT_BOUNCE` | Bounces at both ends |

## Choosing an Easing

- **UI transitions**: `EASE_OUT_QUAD` or `EASE_OUT_CUBIC` (fast start, smooth stop)
- **Dialog popups**: `EASE_OUT_BACK` (slight overshoot feels snappy)
- **Button presses**: `EASE_OUT_ELASTIC` (bouncy feedback)
- **Fade effects**: `EASE_IN_OUT` or `LINEAR`
- **Game objects**: `EASE_IN_OUT_QUAD` (natural movement)

## Related

<div class="related-objects">
<div class="object-links">
<a href="Animation" class="object-link">Animation</a>
<a href="Frame" class="object-link">Frame</a>
<a href="Sprite" class="object-link">Sprite</a>
</div>
</div>
