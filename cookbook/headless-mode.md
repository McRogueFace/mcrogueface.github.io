---
title: Headless Mode
mcrf:
  objects: [Timer, Frame, Scene, Color, Easing]
  diataxis: howto
  disposition: current
  verified: "0.3.0-dev"
  verified_commit: 73acab0
---

# Headless Mode

McRogueFace supports headless operation for automated testing, CI pipelines, and LLM agent orchestration. In headless mode, no window is created and simulation time is controlled programmatically via Python.

**Related Pages:**
- Writing Tests - Test patterns using headless mode
- Input and Events - Timer and event system
- Animation System - Animations work with step()

**Key Files:**
- `src/GameEngine.cpp::step()` - Simulation advancement
- `src/McRFPy_API.cpp::_step()` / `_advance()` - Python bindings for `step()` and `advance()`
- `src/McRFPy_Automation.cpp::_screenshot()` - Synchronous capture

---

## Running in Headless Mode

Launch McRogueFace with the `--headless` flag:

```bash
# Run a script in headless mode
./mcrogueface --headless --exec my_script.py

# Run inline Python
./mcrogueface --headless -c "import mcrfpy; print('Hello headless')"
```

In headless mode:
- No window is created (uses RenderTexture internally)
- Simulation time is frozen until `step()` or `advance()` is called
- Screenshots capture current state synchronously

---

## Simulation Control with step()

The `mcrfpy.step()` function advances simulation time in headless mode:

```python
import mcrfpy

# Advance by specific duration (seconds)
dt = mcrfpy.step(0.1)  # Advance 100ms
print(f"Advanced by {dt} seconds")

# Advance by integer (converts to float)
dt = mcrfpy.step(1)  # Advance 1 second

# Advance to next scheduled event (timer or animation)
dt = mcrfpy.step(None)  # or mcrfpy.step()
print(f"Advanced {dt} seconds to next event")
```

### What step() Does

`step()` runs one full simulation frame:

1. Advances the simulation clock by the specified duration
2. Runs the scene update, timers whose intervals have elapsed, and Python `Scene.update()` callbacks
3. Updates all active animations and scene transitions (including their completion)
4. Records frame-time metrics and increments the frame counter
5. Does NOT render or process input (call `screenshot()` to trigger a render)

To let a span of simulated time pass with timer intervals honored, use `advance()`:

```python
mcrfpy.advance(2500)   # int MILLISECONDS (step() takes float seconds)
print(mcrfpy.get_metrics()["simulation_time_ms"])  # simulated ms; "runtime" is wall-clock seconds
```

`advance(ms)` is headless-only; `ms` must be an int >= 0. Prefer `step()` for single-frame control and `advance()` for moving the clock across a longer span.

### Reproducible runs

Seed the engine's internal random streams (entity behaviors, `Sound.play_varied`) before anything consumes randomness:

```python
mcrfpy.set_random_seed(1234)    # unsigned 32-bit int
print(mcrfpy.get_random_seed())  # 1234; record this to replay an unseeded run
```

---

## Timers in Headless Mode

Timers run on simulation time in headless mode, so they fire deterministically. Timer callbacks receive `(timer_object, runtime_ms)`:

```python
import mcrfpy
import sys

fired = [False]

def on_timer(timer, runtime):
    """Timer callback receives (timer, runtime_ms)."""
    fired[0] = True
    print(f"Timer fired at {runtime}ms")

# Create timer for 500ms interval
t = mcrfpy.Timer("my_timer", on_timer, 500)

# Advance past the timer interval
mcrfpy.step(0.6)  # 600ms - timer will fire

if fired[0]:
    print("Success!")

t.stop()  # Clean up timer
```

### Timer API

```python
t = mcrfpy.Timer("name", callback, interval_ms)

# Control methods
t.stop()      # Stop the timer
t.pause()     # Pause (can resume later)
t.resume()    # Resume after pause
t.restart()   # Restart from beginning
t.start()     # Start (or re-add) the timer

# Properties
t.name        # Timer name (str)
t.interval    # Interval in ms (int)
t.active      # Running state (bool, read-write)
t.paused      # Is timer paused? (bool, read-only)
t.stopped     # Is timer stopped? (bool, read-only)
t.remaining   # Time until next fire, in ms (int, read-only)
t.once        # Fire only once? (bool)
t.callback    # The callback function
```

---

## Animations with step()

Animations update when `step()` is called:

```python
import mcrfpy

scene = mcrfpy.Scene("test")
frame = mcrfpy.Frame(pos=(0, 0), size=(100, 100))
scene.children.append(frame)
mcrfpy.current_scene = scene

# Start animation: move x from 0 to 500 over 2 seconds
frame.animate("x", 500.0, 2.0, mcrfpy.Easing.EASE_IN_OUT)

# Advance halfway through animation
mcrfpy.step(1.0)
print(f"Frame x: {frame.x}")  # ~250 (halfway)

# Complete the animation
mcrfpy.step(1.0)
print(f"Frame x: {frame.x}")  # 500 (complete)
```

---

## Synchronous Screenshots

In headless mode, `automation.screenshot()` is synchronous - it renders the current scene state before capturing:

```python
import mcrfpy
from mcrfpy import automation

scene = mcrfpy.Scene("test")
ui = scene.children

frame = mcrfpy.Frame(pos=(100, 100), size=(200, 200),
                      fill_color=mcrfpy.Color(255, 0, 0))
ui.append(frame)
mcrfpy.current_scene = scene

# Screenshot captures current state immediately (no timer needed)
automation.screenshot("/tmp/red_frame.png")

# Change to green
frame.fill_color = mcrfpy.Color(0, 255, 0)

# Next screenshot shows green
automation.screenshot("/tmp/green_frame.png")
```

### Windowed vs Headless Screenshot Behavior

| Mode | Behavior |
|------|----------|
| Windowed | Captures previous frame's buffer (async) |
| Headless | Renders current state, then captures (sync) |

In windowed mode, you need timer callbacks to ensure the frame has rendered:

```python
# Windowed mode pattern (NOT needed in headless)
def capture(timer, runtime):
    automation.screenshot("output.png")
    sys.exit(0)

capture_timer = mcrfpy.Timer("capture", capture, 100)
```

---

## Use Cases

### Automated Testing

```python
"""Headless test example."""
import mcrfpy
from mcrfpy import automation
import sys

# Setup
scene = mcrfpy.Scene("test")
mcrfpy.current_scene = scene

frame = mcrfpy.Frame(pos=(50, 50), size=(100, 100))
scene.children.append(frame)

# Verify
assert frame.x == 50
assert frame.w == 100

# Take verification screenshot
automation.screenshot("/tmp/test_output.png")

print("PASS")
sys.exit(0)
```

### LLM Agent Orchestration

The `step()` function enables external agents to control simulation pacing:

```python
import mcrfpy
from mcrfpy import automation

def agent_loop():
    """External agent controls simulation."""
    while not game_over():
        # Agent observes current state
        automation.screenshot("/tmp/current_state.png")

        # Agent decides action
        action = get_agent_action("/tmp/current_state.png")

        # Execute action
        execute_action(action)

        # Advance simulation to see results
        mcrfpy.step(0.1)
```

### Batch Rendering

Generate multiple frames without real-time constraints:

```python
import mcrfpy
from mcrfpy import automation

for i in range(100):
    update_scene(i)
    mcrfpy.step(1/60)  # 60 FPS equivalent
    automation.screenshot(f"/tmp/frame_{i:04d}.png")
```

---

## API Reference

**Module Functions:**
- `mcrfpy.step(dt=None)` - Run one full simulation frame
  - `dt` (float or None): Seconds to advance, or None for next event
  - Returns: Actual time advanced (float)
  - In windowed mode: Returns 0.0 (no-op)
  - Raises `RuntimeError` if called from a background thread holding `mcrfpy.lock()`
- `mcrfpy.advance(ms)` - Advance the simulation clock by `ms` milliseconds (int >= 0, headless only)
- `mcrfpy.get_metrics()["simulation_time_ms"]` - Simulated milliseconds (`"runtime"` is wall-clock seconds)
- `mcrfpy.set_random_seed(n)` / `mcrfpy.get_random_seed()` - Seed / read the engine's random streams

A headless `--exec` script must end with `sys.exit()`, since `step()`/`advance()` are the only headless clock; pass `--run-forever` for a long-lived self-driving headless process.

**Automation Functions:**
- `automation.screenshot(filename)` - Capture current frame
  - In headless: Synchronous (renders then captures)
  - In windowed: Asynchronous (captures previous frame buffer)

---

*Migrated from the project wiki (last modified 2026-02-07).*
