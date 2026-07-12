---
title: Window
layout: default
mcrf:
  objects:
    - Window
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# Window

{% raw %}Window singleton for accessing and modifying the game window properties{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `framerate_limit` | {% raw %}Frame rate limit in FPS (int, 0 for unlimited). Caps maximum frame rate.{% endraw %} |
| `fullscreen` | {% raw %}Window fullscreen state (bool). Setting this recreates the window.{% endraw %} |
| `game_resolution` | {% raw %}Fixed game resolution as (width, height) tuple. Enables resolution-independent rendering with scaling.{% endraw %} |
| `resolution` | {% raw %}Window resolution as (width, height) tuple. Setting this recreates the window.{% endraw %} |
| `scaling_mode` | {% raw %}Viewport scaling mode (str): 'center' (no scaling), 'stretch' (fill window), or 'fit' (maintain aspect ratio).{% endraw %} |
| `title` | {% raw %}Window title string (str). Displayed in the window title bar.{% endraw %} |
| `visible` | {% raw %}Window visibility state (bool). Hidden windows still process events.{% endraw %} |
| `vsync` | {% raw %}Vertical sync enabled state (bool). Prevents screen tearing but may limit framerate.{% endraw %} |

## Methods

### `center() -> None`

{% raw %}center() -> None

Center the window on the screen.


Returns:
    None

Note:
    Only works in windowed mode. Has no effect when fullscreen or in headless mode.
{% endraw %}

### `get() -> Window`

*classmethod*

{% raw %}get() -> Window

Get the Window singleton instance.


Returns:
    Window: The global window object

Note:
    This is a class method. Call as Window.get(). There is only one window instance per application.
{% endraw %}

### `screenshot(filename: str = None) -> bytes | None`

{% raw %}screenshot(filename: str = None) -> bytes | None

Take a screenshot of the current window contents.

Args:
    filename: Optional path to save screenshot. If omitted, returns raw RGBA bytes.

Returns:
    bytes | None: Raw RGBA pixel data if no filename given, otherwise None after saving

Note:
    Screenshot is taken at the actual window resolution. Use after render loop update for current frame.
{% endraw %}
