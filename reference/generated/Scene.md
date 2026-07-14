---
title: Scene
layout: default
mcrf:
  objects:
    - Scene
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Scene

{% raw %}Scene(name: str)

Object-oriented scene management with lifecycle callbacks.

This is the recommended approach for scene management, replacing module-level
functions like createScene(), setScene(), and sceneUI(). Key advantage: you can
set on_key handlers on ANY scene, not just the currently active one.

Args:
    name: Unique identifier for this scene. Used for scene transitions.

Properties:
    name (str, read-only): Scene's unique identifier.
    active (bool, read-only): Whether this scene is currently displayed.
    children (UICollection, read-only): UI elements in this scene. Modify to add/remove elements.
    on_key (callable): Keyboard handler. Set on ANY scene, regardless of which is active!
    pos (Vector): Position offset for all UI elements.
    visible (bool): Whether the scene renders.
    opacity (float): Scene transparency (0.0-1.0).

Lifecycle Callbacks (override in subclass):
    on_enter(): Called when scene becomes active via activate().
    on_exit(): Called when scene is deactivated (another scene activates).
    on_key(key: str, action: str): Called for keyboard events (subclass method).
    update(dt: float): Called every frame with delta time in seconds.
    on_resize(new_size: Vector): Called when window is resized.

Example:
    # Basic usage (replacing module functions):
    scene = mcrfpy.Scene('main_menu')
    scene.children.append(mcrfpy.Caption(text='Welcome', pos=(100, 100)))
    scene.on_key = lambda key, action: print(f'Key: {key}')
    scene.activate()  # Switch to this scene

    # Subclassing for lifecycle:
    class GameScene(mcrfpy.Scene):
        def on_enter(self):
            print('Game started!')
        def update(self, dt):
            self.player.move(dt)
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `active` | {% raw %}Whether this scene is currently active (bool, read-only). Only one scene can be active at a time.{% endraw %} |
| `children` | {% raw %}UI element collection for this scene (UICollection, read-only). Use to add, remove, or iterate over UI elements. Changes are reflected immediately.{% endraw %} |
| `name` | {% raw %}Scene name (str, read-only). Unique identifier for this scene.{% endraw %} |
| `on_key` | {% raw %}Keyboard event handler (callable or None). Function receives (key: Key, action: InputState) for keyboard events. Set to None to remove the handler.{% endraw %} |
| `opacity` | {% raw %}Scene opacity (0.0-1.0). Applied to all UI elements during rendering.{% endraw %} |
| `pos` | {% raw %}Scene position offset (Vector). Applied to all UI elements during rendering.{% endraw %} |
| `registered` | {% raw %}Whether this scene is registered with the game engine (bool, read-only). Unregistered scenes still exist but won't receive lifecycle callbacks.{% endraw %} |
| `visible` | {% raw %}Scene visibility (bool). If False, scene is not rendered.{% endraw %} |

## Methods

### `activate(transition: Transition = None, duration: float = None) -> None`

{% raw %}activate(transition: Transition = None, duration: float = None) -> None

Make this the active scene with optional transition effect.

Args:
    transition: Transition type (mcrfpy.Transition enum). Defaults to mcrfpy.default_transition
    duration: Transition duration in seconds. Defaults to mcrfpy.default_transition_duration

Returns:
    None

Note:
    Deactivates the current scene and activates this one. Lifecycle callbacks (on_exit, on_enter) are triggered.
{% endraw %}

### `realign() -> None`

{% raw %}realign() -> None

Recalculate alignment for all children with alignment set.


Note:
    Call this after window resize or when game_resolution changes. For responsive layouts, connect this to on_resize callback.
{% endraw %}

### `register() -> None`

{% raw %}register() -> None

Register this scene with the game engine.


Note:
    Makes the scene available for activation and receives lifecycle callbacks. If another scene with the same name exists, it will be unregistered first. Called automatically by activate() if needed.
{% endraw %}

### `unregister() -> None`

{% raw %}unregister() -> None

Unregister this scene from the game engine.


Note:
    Removes the scene from the engine's registry but keeps the Python object alive. The scene's UI elements and state are preserved. Call register() to re-add it. Useful for temporary scenes or scene pooling.
{% endraw %}
