---
layout: default
title: Timer
---

# Timer

Scheduled callbacks at intervals.

<div class="stub-notice">
<p>This page is a stub. Full documentation coming soon.</p>
</div>

## Overview

A `Timer` executes a callback function at regular intervals. Use timers for animations, game updates, delayed actions, and periodic events.

## Quick Reference

```python
# Create a repeating timer (every 500ms)
def update():
    print("Tick!")

mcrfpy.Timer("my_timer", update, 500)

# Control timers
mcrfpy.Timer.pause("my_timer")
mcrfpy.Timer.resume("my_timer")
mcrfpy.Timer.cancel("my_timer")

# One-shot timer
def delayed():
    print("Delayed action!")
    mcrfpy.Timer.cancel("delay")

mcrfpy.Timer("delay", delayed, 1000)
```

## Constructor

```python
mcrfpy.Timer(name: str, callback: callable, interval_ms: int)
```

## Class Methods

| Method | Description |
|--------|-------------|
| `Timer.pause(name)` | Pause a timer |
| `Timer.resume(name)` | Resume a paused timer |
| `Timer.cancel(name)` | Stop and remove a timer |

## Related

<div class="related-objects">
<div class="object-links">
<a href="../systems/input#timers" class="object-link">Timer Documentation</a>
<a href="../systems/animation" class="object-link">Animation System</a>
</div>
</div>
