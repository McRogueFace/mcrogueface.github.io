---
mcrf:
  objects: [Scene, Frame, Color, Timer, Transition, Easing]
  diataxis: howto
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Scene Transition Effects

Smooth transitions between scenes for a polished game feel. McRogueFace supports built-in transitions and custom overlay-based effects.

## Built-in Transitions

McRogueFace provides simple built-in scene transitions:

```python
import mcrfpy

# Create scenes, then switch between them with activate()
menu_scene = mcrfpy.Scene("menu")
game_scene = mcrfpy.Scene("game")

# Instant switch (default) -- also settable via mcrfpy.current_scene = scene
menu_scene.activate()
game_scene.activate()
```

## Custom Fade Transition

Create a manual fade transition with more control:

```python
import mcrfpy

class FadeTransition:
    """Custom fade transition with callback support."""

    def __init__(self, current_scene, target_scene):
        """
        Args:
            current_scene: The mcrfpy.Scene object to transition from
            target_scene: The mcrfpy.Scene object to transition to
        """
        self.current_scene = current_scene
        self.target_scene = target_scene
        self.overlay = None

    def _create_overlay(self, scene):
        """Create a full-screen black overlay in the given scene."""
        self.overlay = mcrfpy.Frame(pos=(0, 0), size=(1024, 768))
        self.overlay.fill_color = mcrfpy.Color(0, 0, 0, 255)
        self.overlay.opacity = 0.0
        self.overlay.z_index = 9999  # On top of everything
        scene.children.append(self.overlay)

    def fade_out_in(self, duration=0.5, on_complete=None):
        """
        Fade to black, switch scene, fade in.

        Args:
            duration: Total transition time (half for out, half for in)
            on_complete: Callback when transition finishes
        """
        half_duration = duration / 2

        # Create overlay in current scene
        self._create_overlay(self.current_scene)

        # Fade to black
        self.overlay.animate("opacity", 1.0, half_duration, mcrfpy.Easing.EASE_IN)

        # Switch scene and fade in
        def switch_and_fade_in(timer, runtime):
            # Switch to new scene
            self.target_scene.activate()

            # Create overlay in new scene
            self._create_overlay(self.target_scene)
            self.overlay.opacity = 1.0  # Start fully opaque

            # Fade in
            self.overlay.animate("opacity", 0.0, half_duration, mcrfpy.Easing.EASE_OUT)

            # Cleanup and callback
            def cleanup(timer, runtime):
                self.target_scene.children.remove(self.overlay)
                if on_complete:
                    on_complete()

            mcrfpy.Timer("fade_cleanup", cleanup, int(half_duration * 1000) + 50, once=True)

        mcrfpy.Timer("fade_switch", switch_and_fade_in, int(half_duration * 1000), once=True)


# Usage
menu_scene = mcrfpy.Scene("menu")
game_scene = mcrfpy.Scene("game")

def on_transition_complete():
    print("Transition complete, game starting!")

# Start on menu, then transition to game
menu_scene.activate()

transition = FadeTransition(menu_scene, game_scene)
transition.fade_out_in(duration=0.8, on_complete=on_transition_complete)
```

## Color Flash Transition

Flash to a color (like white for teleport or red for damage):

```python
import mcrfpy

def flash_transition(current_scene, target_scene, color=(255, 255, 255), duration=0.4):
    """
    Flash to a color, then switch scene.

    Args:
        current_scene: The mcrfpy.Scene object to transition from
        target_scene: The mcrfpy.Scene object to transition to
        color: Flash color RGB tuple
        duration: Total transition time
    """
    # Create colored overlay in current scene
    overlay = mcrfpy.Frame(pos=(0, 0), size=(1024, 768))
    overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
    overlay.opacity = 0.0
    overlay.z_index = 9999
    current_scene.children.append(overlay)

    quarter = duration / 4

    # Flash in (fast)
    overlay.animate("opacity", 1.0, quarter, mcrfpy.Easing.EASE_OUT)

    # Hold, then switch and fade out
    def switch_scene(timer, runtime):
        target_scene.activate()

        # Create overlay in new scene
        new_overlay = mcrfpy.Frame(pos=(0, 0), size=(1024, 768))
        new_overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
        new_overlay.z_index = 9999
        target_scene.children.append(new_overlay)

        # Fade out (slower)
        new_overlay.animate("opacity", 0.0, duration / 2, mcrfpy.Easing.EASE_IN)

        # Cleanup
        def cleanup(timer, runtime):
            target_scene.children.remove(new_overlay)

        mcrfpy.Timer("flash_cleanup", cleanup, int(duration * 500) + 50, once=True)

    mcrfpy.Timer("flash_switch", switch_scene, int(quarter * 2000), once=True)


# Usage
game_scene = mcrfpy.Scene("game")
next_level_scene = mcrfpy.Scene("next_level")
death_scene = mcrfpy.Scene("death_screen")

flash_transition(game_scene, next_level_scene, color=(255, 255, 255), duration=0.5)  # White flash
flash_transition(game_scene, death_scene, color=(255, 0, 0), duration=0.8)   # Red flash
```

## Wipe Transition

A frame that expands to cover the screen:

```python
import mcrfpy

def wipe_transition(current_scene, target_scene, direction="right", duration=0.5, color=(0, 0, 0)):
    """
    Wipe transition from one edge.

    Args:
        current_scene: The mcrfpy.Scene object to transition from
        target_scene: The mcrfpy.Scene object to transition to
        direction: "left", "right", "up", "down"
        duration: Total transition time
        color: Wipe color
    """
    half = duration / 2

    # Set up wipe overlay based on direction
    if direction == "right":
        overlay = mcrfpy.Frame(pos=(0, 0), size=(0, 768))
        anim_prop = "w"
        anim_target = 1024
    elif direction == "left":
        overlay = mcrfpy.Frame(pos=(1024, 0), size=(0, 768))
        anim_prop = "x"  # Move left edge
        anim_target = 0
    elif direction == "down":
        overlay = mcrfpy.Frame(pos=(0, 0), size=(1024, 0))
        anim_prop = "h"
        anim_target = 768
    else:  # up
        overlay = mcrfpy.Frame(pos=(0, 768), size=(1024, 0))
        anim_prop = "y"
        anim_target = 0

    overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
    overlay.z_index = 9999
    current_scene.children.append(overlay)

    # Wipe in
    overlay.animate(anim_prop, float(anim_target), half, mcrfpy.Easing.EASE_IN_OUT)

    # Switch and wipe out
    def switch_and_wipe(timer, runtime):
        target_scene.activate()

        # Create covering overlay
        if direction == "right":
            new_overlay = mcrfpy.Frame(pos=(0, 0), size=(1024, 768))
            new_anim_prop = "x"
            new_anim_target = 1024
        elif direction == "left":
            new_overlay = mcrfpy.Frame(pos=(0, 0), size=(1024, 768))
            new_anim_prop = "w"
            new_anim_target = 0
        elif direction == "down":
            new_overlay = mcrfpy.Frame(pos=(0, 0), size=(1024, 768))
            new_anim_prop = "y"
            new_anim_target = -768
        else:
            new_overlay = mcrfpy.Frame(pos=(0, 0), size=(1024, 768))
            new_anim_prop = "h"
            new_anim_target = 0

        new_overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
        new_overlay.z_index = 9999
        target_scene.children.append(new_overlay)

        # Wipe out
        new_overlay.animate(new_anim_prop, float(new_anim_target), half, mcrfpy.Easing.EASE_IN_OUT)

        # Cleanup
        def cleanup(timer, runtime):
            target_scene.children.remove(new_overlay)

        mcrfpy.Timer("wipe_cleanup", cleanup, int(half * 1000) + 50, once=True)

    mcrfpy.Timer("wipe_switch", switch_and_wipe, int(half * 1000), once=True)


# Usage
game_scene = mcrfpy.Scene("game")
next_level = mcrfpy.Scene("next_level")
menu_scene = mcrfpy.Scene("menu")

wipe_transition(game_scene, next_level, direction="right", duration=0.6)
wipe_transition(game_scene, menu_scene, direction="down", duration=0.4)
```

## Transition Manager

A centralized manager for consistent transitions:

```python
import mcrfpy

class TransitionManager:
    """Manages scene transitions with multiple effect types."""

    def __init__(self, screen_width=1024, screen_height=768):
        self.width = screen_width
        self.height = screen_height
        self.is_transitioning = False
        self.current_scene = None  # Track active scene

    def go_to(self, target_scene, effect="fade", duration=0.5, **kwargs):
        """
        Transition to a scene with the specified effect.

        Args:
            target_scene: The mcrfpy.Scene object to transition to
            effect: "fade", "flash", "wipe", "instant"
            duration: Transition duration
            **kwargs: Effect-specific options (color, direction)
        """
        if self.is_transitioning:
            return

        if self.current_scene is None:
            # No current scene tracked, just activate target
            target_scene.activate()
            self.current_scene = target_scene
            return

        self.is_transitioning = True

        if effect == "instant":
            target_scene.activate()
            self.current_scene = target_scene
            self.is_transitioning = False

        elif effect == "fade":
            color = kwargs.get("color", (0, 0, 0))
            self._fade(target_scene, duration, color)

        elif effect == "flash":
            color = kwargs.get("color", (255, 255, 255))
            self._flash(target_scene, duration, color)

        elif effect == "wipe":
            direction = kwargs.get("direction", "right")
            color = kwargs.get("color", (0, 0, 0))
            self._wipe(target_scene, duration, direction, color)

    def _fade(self, target_scene, duration, color):
        half = duration / 2

        overlay = mcrfpy.Frame(pos=(0, 0), size=(self.width, self.height))
        overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
        overlay.opacity = 0.0
        overlay.z_index = 9999
        self.current_scene.children.append(overlay)

        overlay.animate("opacity", 1.0, half, mcrfpy.Easing.EASE_IN)

        def phase2(timer, runtime):
            target_scene.activate()

            new_overlay = mcrfpy.Frame(pos=(0, 0), size=(self.width, self.height))
            new_overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
            new_overlay.z_index = 9999
            target_scene.children.append(new_overlay)

            new_overlay.animate("opacity", 0.0, half, mcrfpy.Easing.EASE_OUT)

            def cleanup(timer, runtime):
                target_scene.children.remove(new_overlay)
                self.current_scene = target_scene
                self.is_transitioning = False

            mcrfpy.Timer("fade_done", cleanup, int(half * 1000) + 50, once=True)

        mcrfpy.Timer("fade_switch", phase2, int(half * 1000), once=True)

    def _flash(self, target_scene, duration, color):
        quarter = duration / 4

        overlay = mcrfpy.Frame(pos=(0, 0), size=(self.width, self.height))
        overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
        overlay.opacity = 0.0
        overlay.z_index = 9999
        self.current_scene.children.append(overlay)

        overlay.animate("opacity", 1.0, quarter, mcrfpy.Easing.EASE_OUT)

        def phase2(timer, runtime):
            target_scene.activate()

            new_overlay = mcrfpy.Frame(pos=(0, 0), size=(self.width, self.height))
            new_overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
            new_overlay.z_index = 9999
            target_scene.children.append(new_overlay)

            new_overlay.animate("opacity", 0.0, duration / 2, mcrfpy.Easing.EASE_IN)

            def cleanup(timer, runtime):
                target_scene.children.remove(new_overlay)
                self.current_scene = target_scene
                self.is_transitioning = False

            mcrfpy.Timer("flash_done", cleanup, int(duration * 500) + 50, once=True)

        mcrfpy.Timer("flash_switch", phase2, int(quarter * 2000), once=True)

    def _wipe(self, target_scene, duration, direction, color):
        # Simplified wipe - right direction only for brevity
        half = duration / 2

        overlay = mcrfpy.Frame(pos=(0, 0), size=(0, self.height))
        overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
        overlay.z_index = 9999
        self.current_scene.children.append(overlay)

        overlay.animate("w", float(self.width), half, mcrfpy.Easing.EASE_IN_OUT)

        def phase2(timer, runtime):
            target_scene.activate()

            new_overlay = mcrfpy.Frame(pos=(0, 0), size=(self.width, self.height))
            new_overlay.fill_color = mcrfpy.Color(color[0], color[1], color[2], 255)
            new_overlay.z_index = 9999
            target_scene.children.append(new_overlay)

            new_overlay.animate("x", float(self.width), half, mcrfpy.Easing.EASE_IN_OUT)

            def cleanup(timer, runtime):
                target_scene.children.remove(new_overlay)
                self.current_scene = target_scene
                self.is_transitioning = False

            mcrfpy.Timer("wipe_done", cleanup, int(half * 1000) + 50, once=True)

        mcrfpy.Timer("wipe_switch", phase2, int(half * 1000), once=True)


# Usage
# Create scenes
menu_scene = mcrfpy.Scene("menu")
game_scene = mcrfpy.Scene("game")
options_scene = mcrfpy.Scene("options")
next_level_scene = mcrfpy.Scene("next_level")

# Create transition manager and set initial scene
transitions = TransitionManager()
transitions.current_scene = menu_scene
menu_scene.activate()

# Various transition styles
transitions.go_to(game_scene, effect="fade", duration=0.5)
transitions.go_to(menu_scene, effect="flash", color=(255, 255, 255), duration=0.4)
transitions.go_to(next_level_scene, effect="wipe", direction="right", duration=0.6)
transitions.go_to(options_scene, effect="instant")
```

## Key Concepts

1. **Frame overlays**: Use full-screen Frames with high z_index for transition effects
2. **Opacity animation**: Animate `opacity` property for fade effects
3. **Two-phase transitions**: Fade out in current scene, switch, fade in
4. **Timer coordination**: Use timers to sequence transition phases
5. **Cleanup**: Always remove transition overlays after completion

## Tips

- Keep transitions short (0.3-0.6s) for responsive feel
- Use faster transitions for frequent switches (inventory, pause)
- Use slower, dramatic transitions for major moments (level complete, death)
- Match transition style to game theme (wipes for action, fades for story)
- Prevent input during transitions to avoid state confusion
- Consider adding sound effects to enhance transitions
