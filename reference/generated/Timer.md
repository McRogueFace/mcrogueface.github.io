---
title: Timer
layout: default
mcrf:
  objects:
    - Timer
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Timer

{% raw %}Timer(name, callback, interval, once=False, start=True)

Create a timer that calls a function at regular intervals.

Args:
    name (str): Unique identifier for the timer
    callback (callable): Function to call - receives (timer, runtime) args
    interval (int): Time between calls in milliseconds
    once (bool): If True, timer stops after first call. Default: False
    start (bool): If True, timer starts immediately. Default: True

Attributes:
    interval (int): Time between calls in milliseconds
    remaining (int): Time until next call in milliseconds (read-only)
    paused (bool): Whether timer is paused (read-only)
    stopped (bool): Whether timer is stopped (read-only)
    active (bool): Running state (read-write). Set True to start, False to pause
    callback (callable): The callback function (preserved when stopped)
    once (bool): Whether timer stops after firing once

Methods:
    start(): Start the timer, adding to engine tick loop
    stop(): Stop the timer (removes from engine, preserves callback)
    pause(): Pause the timer, preserving time remaining
    resume(): Resume a paused timer
    restart(): Reset timer and ensure it's running

Example:
    def on_timer(timer, runtime):
        print(f'Timer {timer} fired at {runtime}ms')
        if runtime > 5000:
            timer.stop()  # Stop but can restart later
    
    timer = mcrfpy.Timer('my_timer', on_timer, 1000)
    timer.pause()  # Pause timer
    timer.resume() # Resume timer
    timer.stop()   # Stop completely
    timer.start()  # Restart from beginning{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `active` | {% raw %}Running state (bool, read-write). True if running (not paused, not stopped). Set True to start/resume, False to pause.{% endraw %} |
| `callback` | {% raw %}The callback function (callable). Preserved when stopped, allowing timer restart.{% endraw %} |
| `interval` | {% raw %}Timer interval in milliseconds (int). Must be positive. Can be changed while timer is running.{% endraw %} |
| `name` | {% raw %}Timer name (str, read-only). Unique identifier for this timer.{% endraw %} |
| `once` | {% raw %}Whether the timer stops after firing once (bool). One-shot timers can be restarted.{% endraw %} |
| `paused` | {% raw %}Whether the timer is paused (bool, read-only). Paused timers preserve their remaining time.{% endraw %} |
| `remaining` | {% raw %}Time remaining until next trigger in milliseconds (int, read-only). Full interval when stopped.{% endraw %} |
| `stopped` | {% raw %}Whether the timer is stopped (bool, read-only). Stopped timers are not in the engine tick loop but preserve their callback.{% endraw %} |

## Methods

### `pause() -> None`

{% raw %}pause() -> None

Pause the timer, preserving the time remaining until next trigger.


Returns:
    None

Note:
    The timer can be resumed later with resume(). Time spent paused does not count toward the interval.
{% endraw %}

### `restart() -> None`

{% raw %}restart() -> None

Restart the timer from the beginning and ensure it's running.


Returns:
    None

Note:
    Resets progress and adds timer to engine if stopped. Equivalent to stop() followed by start().
{% endraw %}

### `resume() -> None`

{% raw %}resume() -> None

Resume a paused timer from where it left off.


Returns:
    None

Note:
    Has no effect if the timer is not paused. Timer will fire after the remaining time elapses.
{% endraw %}

### `start() -> None`

{% raw %}start() -> None

Start the timer, adding it to the engine tick loop.


Returns:
    None

Note:
    Resets progress and begins counting toward the next fire. If another timer has this name, it will be stopped.
{% endraw %}

### `stop() -> None`

{% raw %}stop() -> None

Stop the timer and remove it from the engine tick loop.


Returns:
    None

Note:
    The callback is preserved, so the timer can be restarted with start() or restart().
{% endraw %}
