---
layout: default
title: Timer
---

# Timer

Scheduled callback execution at regular intervals.

## Overview

A `Timer` executes a callback function at specified intervals. Use timers for game loops, delayed actions, periodic updates, cooldowns, and any time-based game logic. Timers can be paused, resumed, and configured to fire once or repeatedly.

## Quick Reference

```python
import mcrfpy

# Create a repeating timer (fires every 500ms)
def on_tick(timer, runtime):
    print(f"Tick at {runtime}ms")

timer = mcrfpy.Timer("game_tick", on_tick, 500)

# One-shot timer (fires once after 2 seconds)
def delayed_action(timer, runtime):
    print("Delayed action executed!")

mcrfpy.Timer("delay", delayed_action, 2000, once=True)

# Control timer state
timer.pause()
timer.resume()
timer.restart()
timer.stop()

# Create paused (start manually later)
timer = mcrfpy.Timer("manual", callback, 1000, start=False)
timer.start()
```

## Constructor

```python
mcrfpy.Timer(name: str, callback: callable, interval: int, once: bool = False, start: bool = True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | required | Unique identifier for the timer |
| `callback` | callable | required | Function to call on each interval |
| `interval` | int | required | Time between calls in milliseconds |
| `once` | bool | False | If True, timer fires once then stops |
| `start` | bool | True | If False, timer is created paused |

### Callback Signature

The callback receives two arguments:

```python
def my_callback(timer, runtime):
    # timer: the Timer instance that fired
    # runtime: total milliseconds since game started
    pass
```

## Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `name` | str | read-only | Timer identifier |
| `interval` | int | read/write | Milliseconds between callbacks |
| `remaining` | int | read-only | Milliseconds until next fire |
| `paused` | bool | read-only | True if timer is paused |
| `stopped` | bool | read-only | True if timer is stopped |
| `active` | bool | read/write | Whether timer is running |
| `callback` | callable | read/write | The callback function |
| `once` | bool | read/write | Whether timer fires only once |

## Methods

| Method | Description |
|--------|-------------|
| `start()` | Start or restart the timer |
| `stop()` | Stop the timer completely |
| `pause()` | Pause the timer (preserves remaining time) |
| `resume()` | Resume a paused timer |
| `restart()` | Reset and start the timer |

### Method Details

```python
timer.start()    # Begin running (resets interval)
timer.stop()     # Fully stop (cannot resume)
timer.pause()    # Temporarily halt (can resume)
timer.resume()   # Continue from paused state
timer.restart()  # Reset to full interval and start
```

## Examples

### Game Update Loop

```python
import mcrfpy

class Game:
    def __init__(self):
        self.player_x = 0
        self.velocity = 5

        # Update at 60 FPS (approximately)
        self.update_timer = mcrfpy.Timer(
            "game_update",
            self.update,
            16  # ~60 FPS
        )

    def update(self, timer, runtime):
        self.player_x += self.velocity
        if self.player_x > 800:
            self.player_x = 0
```

### Delayed Action

```python
def spawn_enemy(timer, runtime):
    enemy = create_enemy()
    game.enemies.append(enemy)

# Spawn enemy after 3 seconds
mcrfpy.Timer("spawn_delay", spawn_enemy, 3000, once=True)
```

### Cooldown System

```python
class Player:
    def __init__(self):
        self.can_attack = True
        self.cooldown_timer = None

    def attack(self):
        if not self.can_attack:
            return

        self.can_attack = False
        perform_attack()

        # Reset cooldown after 500ms
        def reset_cooldown(timer, runtime):
            self.can_attack = True

        self.cooldown_timer = mcrfpy.Timer(
            "attack_cooldown",
            reset_cooldown,
            500,
            once=True
        )
```

### Animation Sequencing

```python
def animate_sequence():
    sprites = [sprite1, sprite2, sprite3]
    current = [0]  # Use list to allow modification in closure

    def next_frame(timer, runtime):
        sprites[current[0]].visible = False
        current[0] = (current[0] + 1) % len(sprites)
        sprites[current[0]].visible = True

    mcrfpy.Timer("frame_anim", next_frame, 200)

animate_sequence()
```

### Pausable Game Timer

```python
game_timer = mcrfpy.Timer("game", game_update, 16)

def on_key(key, action):
    if key == "P" and action == "start":
        if game_timer.paused:
            game_timer.resume()
        else:
            game_timer.pause()
```

## Related

<div class="related-objects">
<div class="object-links">
<a href="Animation" class="object-link">Animation</a>
<a href="Scene" class="object-link">Scene</a>
</div>
</div>
