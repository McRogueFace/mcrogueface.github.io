---
title: Module Functions
layout: default
mcrf:
  objects:
    - Module Functions
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Module Functions

Top-level functions in the `mcrfpy` module.

## `mcrfpy.bresenham(start, end, include_start=True, include_end=True) -> list[tuple[int, int]]`

{% raw %}bresenham(start, end, include_start=True, include_end=True) -> list[tuple[int, int]]

Compute grid cells along a line using Bresenham's algorithm.

Args:
    start: (x, y) tuple or Vector - starting point
    end: (x, y) tuple or Vector - ending point
    include_start: Include the starting point in results (default: True)
    include_end: Include the ending point in results (default: True)

Returns:
    list[tuple[int, int]]: List of (x, y) grid coordinates along the line

Note:
    Useful for line-of-sight checks, projectile paths, and drawing lines on grids. The algorithm ensures minimal grid traversal between two points.
{% endraw %}

## `mcrfpy.end_benchmark() -> str`

{% raw %}end_benchmark() -> str

Stop benchmark capture and write data to JSON file.


Returns:
    str: The filename of the written benchmark data

Raises:
    RuntimeError: If no benchmark is currently running

Note:
    Returns the auto-generated filename (e.g., 'benchmark_12345_20250528_143022.json')
{% endraw %}

## `mcrfpy.exit() -> None`

{% raw %}exit() -> None

Cleanly shut down the game engine and exit the application.


Returns:
    None

Note:
    This immediately closes the window and terminates the program.
{% endraw %}

## `mcrfpy.find(name: str, scene: str = None) -> UIDrawable | None`

{% raw %}find(name: str, scene: str = None) -> UIDrawable | None

Find the first UI element with the specified name.

Args:
    name: Exact name to search for
    scene: Scene to search in (default: current scene)

Returns:
    Frame, Caption, Sprite, Grid, or Entity if found; None otherwise

Note:
    Searches scene UI elements and entities within grids.
{% endraw %}

## `mcrfpy.find_all(pattern: str, scene: str = None) -> list`

{% raw %}find_all(pattern: str, scene: str = None) -> list

Find all UI elements matching a name pattern.

Args:
    pattern: Name pattern with optional wildcards (* matches any characters)
    scene: Scene to search in (default: current scene)

Returns:
    list: All matching UI elements and entities

Note:
    Example: find_all('enemy*') finds all elements starting with 'enemy', find_all('*_button') finds all elements ending with '_button'
{% endraw %}

## `mcrfpy.get_metrics() -> dict`

{% raw %}get_metrics() -> dict

Get current performance metrics.


Returns:
    dict: Performance data with keys: frame_time (last frame duration in seconds), avg_frame_time (average frame time), fps (frames per second), draw_calls (number of draw calls), ui_elements (total UI element count), visible_elements (visible element count), current_frame (frame counter), runtime (total runtime in seconds), grid_render_time (grid rendering time in ms), entity_render_time (entity rendering time in ms), fov_overlay_time (FOV overlay rendering time in ms), python_time (Python script execution time in ms), animation_time (animation processing time in ms), grid_cells_rendered (number of grid cells rendered this frame), entities_rendered (number of entities rendered this frame), total_entities (total entity count across all grids)
{% endraw %}

## `mcrfpy.lock() -> _LockContext`

{% raw %}lock() -> _LockContext

Get a context manager for thread-safe access to mcrfpy objects from background threads.


Returns:
    _LockContext: A context manager that blocks until safe to touch engine objects

Note:
    Any access to mcrfpy objects from a non-main thread must happen inside `with mcrfpy.lock():`; behavior outside the lock is undefined. On a worker thread the context manager blocks (GIL released) until the render loop opens a safe window between frames; on the main thread it is a no-op.

See also: Threading Model (docs/threading-model.md)
{% endraw %}

## `mcrfpy.log_benchmark(message: str) -> None`

{% raw %}log_benchmark(message: str) -> None

Add a log message to the current benchmark frame.

Args:
    message: Text to associate with the current frame

Returns:
    None

Raises:
    RuntimeError: If no benchmark is currently running

Note:
    Messages appear in the 'logs' array of each frame in the output JSON.
{% endraw %}

## `mcrfpy.set_dev_console(enabled: bool) -> None`

{% raw %}set_dev_console(enabled: bool) -> None

Enable or disable the developer console overlay.

Args:
    enabled: True to enable the console (default), False to disable

Returns:
    None

Note:
    When disabled, the grave/tilde key will not open the console. Use this to ship games without debug features.
{% endraw %}

## `mcrfpy.set_scale(multiplier: float) -> None`

{% raw %}set_scale(multiplier: float) -> None

Deprecated: use Window.resolution instead. Scale the game window size.

Args:
    multiplier: Scale factor (e.g., 2.0 for double size)

Returns:
    None

Note:
    The internal resolution remains 1024x768, but the window is scaled. This is deprecated - use Window.resolution instead.
{% endraw %}

## `mcrfpy.start_benchmark() -> None`

{% raw %}start_benchmark() -> None

Start capturing benchmark data to a file.


Returns:
    None

Raises:
    RuntimeError: If a benchmark is already running

Note:
    Benchmark filename is auto-generated from PID and timestamp. Use end_benchmark() to stop and get filename.
{% endraw %}

## `mcrfpy.step(dt: float = None) -> float`

{% raw %}step(dt: float = None) -> float

Advance simulation time (headless mode only).

Args:
    dt: Time to advance in seconds. If None, advances to the next scheduled event (timer/animation).

Returns:
    float: Actual time advanced in seconds. Returns 0.0 in windowed mode.

Note:
    In windowed mode, this is a no-op and returns 0.0. Use this for deterministic simulation control in headless/testing scenarios.
{% endraw %}
