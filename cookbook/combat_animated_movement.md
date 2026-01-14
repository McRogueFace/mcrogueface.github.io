# Animated Movement

Smooth entity movement using the Animation system.

## Overview

McRogueFace's `Animation` class provides smooth interpolation for entity properties. This recipe covers using animations for fluid movement instead of instant teleportation.

## Basic Animated Move

```python
import mcrfpy

def move_with_animation(entity, new_x, new_y, duration=0.2):
    """Move entity smoothly to new position."""
    anim_x = mcrfpy.Animation("x", float(new_x), duration, "easeInOut")
    anim_y = mcrfpy.Animation("y", float(new_y), duration, "easeInOut")

    anim_x.start(entity)
    anim_y.start(entity)
```

## Animation with Callback

Know when movement completes for turn-based games:

```python
import mcrfpy

# Track animation state
is_animating = False

def move_with_callback(entity, new_x, new_y, duration=0.2, on_complete=None):
    """Move entity with completion callback."""
    global is_animating
    is_animating = True

    def animation_done(anim, target):
        global is_animating
        is_animating = False
        if on_complete:
            on_complete()

    # Only need callback on one animation
    anim_x = mcrfpy.Animation("x", float(new_x), duration, "easeInOut", callback=animation_done)
    anim_y = mcrfpy.Animation("y", float(new_y), duration, "easeInOut")

    anim_x.start(entity)
    anim_y.start(entity)


# Usage in turn-based game
def player_move(direction):
    if is_animating:
        return  # Block input during animation

    dx, dy = direction
    new_x = int(player.x) + dx
    new_y = int(player.y) + dy

    def on_move_complete():
        end_player_turn()

    move_with_callback(player, new_x, new_y, on_complete=on_move_complete)
```

## Available Easing Functions

```python
# Easing options:
# "linear"     - Constant speed
# "easeIn"     - Slow start, fast end
# "easeOut"    - Fast start, slow end
# "easeInOut"  - Slow start and end (smooth)

# Examples of each
def demo_easings(entity, target_x):
    # Linear - mechanical, robotic movement
    anim = mcrfpy.Animation("x", target_x, 0.5, "linear")

    # EaseIn - accelerating (good for falling)
    anim = mcrfpy.Animation("x", target_x, 0.5, "easeIn")

    # EaseOut - decelerating (good for stopping)
    anim = mcrfpy.Animation("x", target_x, 0.5, "easeOut")

    # EaseInOut - natural movement (best for walking)
    anim = mcrfpy.Animation("x", target_x, 0.5, "easeInOut")
```

## Camera Follow Animation

Animate the grid camera to follow the player:

```python
def animate_camera_follow(grid, target_x, target_y, duration=0.2):
    """Smoothly pan camera to follow entity."""
    # Grid center is in pixel coordinates (tile_size = 16)
    center_x = (target_x + 0.5) * 16
    center_y = (target_y + 0.5) * 16

    anim_x = mcrfpy.Animation("center_x", center_x, duration, "linear")
    anim_y = mcrfpy.Animation("center_y", center_y, duration, "linear")

    anim_x.start(grid)
    anim_y.start(grid)


def move_player_with_camera(player, grid, new_x, new_y, duration=0.2):
    """Move player and camera together."""

    def on_complete(anim, target):
        # Ensure camera is exactly centered after animation
        grid.center = ((new_x + 0.5) * 16, (new_y + 0.5) * 16)

    # Animate player
    anim_x = mcrfpy.Animation("x", float(new_x), duration, "easeInOut", callback=on_complete)
    anim_y = mcrfpy.Animation("y", float(new_y), duration, "easeInOut")
    anim_x.start(player)
    anim_y.start(player)

    # Animate camera
    animate_camera_follow(grid, new_x, new_y, duration)
```

## Path Animation

Animate movement along a path from A* pathfinding:

```python
class PathAnimator:
    """Animate entity movement along a path."""

    def __init__(self, entity, path, step_duration=0.2, on_complete=None):
        self.entity = entity
        self.path = list(path)  # Copy the path
        self.step_duration = step_duration
        self.on_complete = on_complete
        self.current_step = 0
        self.animating = False

    def start(self):
        """Begin path animation."""
        if not self.path or self.animating:
            return

        self.animating = True
        self.current_step = 0
        self._animate_next_step()

    def _animate_next_step(self):
        """Animate to next path position."""
        if self.current_step >= len(self.path):
            # Path complete
            self.animating = False
            if self.on_complete:
                self.on_complete()
            return

        target_x, target_y = self.path[self.current_step]

        # Create step animation
        anim_x = mcrfpy.Animation("x", float(target_x), self.step_duration, "easeInOut")
        anim_y = mcrfpy.Animation("y", float(target_y), self.step_duration, "easeInOut")

        anim_x.start(self.entity)
        anim_y.start(self.entity)

        # Schedule next step
        self.current_step += 1
        delay_ms = int(self.step_duration * 1000) + 20  # Small buffer

        def continue_path(timer, runtime):
            if self.animating:  # Check if still active
                self._animate_next_step()

        mcrfpy.Timer(f"path_{id(self)}", continue_path, delay_ms)

    def stop(self):
        """Stop path animation."""
        self.animating = False  # Timer callbacks will check this flag


# Usage
def move_enemy_along_path(enemy, player, grid):
    path = enemy.path_to(int(player.x), int(player.y))

    if not path:
        return

    # Only move a few steps per turn
    path = path[:3]

    def on_path_complete():
        end_enemy_turn()

    animator = PathAnimator(enemy, path, step_duration=0.15, on_complete=on_path_complete)
    animator.start()
```

## Movement Queue

Handle rapid input by queuing moves:

```python
class MovementController:
    """Handles queued movement with animations."""

    def __init__(self, entity, grid, move_duration=0.2):
        self.entity = entity
        self.grid = grid
        self.move_duration = move_duration
        self.is_moving = False
        self.move_queue = []
        self.max_queue = 2

    def queue_move(self, dx, dy):
        """Add a move to the queue."""
        if len(self.move_queue) < self.max_queue:
            self.move_queue.append((dx, dy))

        if not self.is_moving:
            self._process_queue()

    def _process_queue(self):
        """Process the next queued move."""
        if not self.move_queue:
            self.is_moving = False
            return

        dx, dy = self.move_queue.pop(0)
        current_x = int(self.entity.x)
        current_y = int(self.entity.y)
        new_x = current_x + dx
        new_y = current_y + dy

        # Validate move
        if not self._is_valid_move(new_x, new_y):
            self._process_queue()  # Try next queued move
            return

        self.is_moving = True
        self._animate_move(new_x, new_y)

    def _is_valid_move(self, x, y):
        """Check if move is valid."""
        grid_w, grid_h = self.grid.grid_size
        if x < 0 or x >= grid_w or y < 0 or y >= grid_h:
            return False
        return self.grid.at(x, y).walkable

    def _animate_move(self, new_x, new_y):
        """Perform the animated move."""

        def on_complete(anim, target):
            self._process_queue()

        anim_x = mcrfpy.Animation("x", float(new_x), self.move_duration, "easeInOut", callback=on_complete)
        anim_y = mcrfpy.Animation("y", float(new_y), self.move_duration, "easeInOut")

        anim_x.start(self.entity)
        anim_y.start(self.entity)

        # Also animate camera
        center_x = (new_x + 0.5) * 16
        center_y = (new_y + 0.5) * 16

        cam_x = mcrfpy.Animation("center_x", center_x, self.move_duration, "linear")
        cam_y = mcrfpy.Animation("center_y", center_y, self.move_duration, "linear")
        cam_x.start(self.grid)
        cam_y.start(self.grid)


# Usage (assumes scene, player, game_grid already defined)
controller = MovementController(player, game_grid, move_duration=0.15)

def handle_input(key, action):
    if action != "start":
        return

    if key in ["W", "Up"]:
        controller.queue_move(0, -1)
    elif key in ["S", "Down"]:
        controller.queue_move(0, 1)
    elif key in ["A", "Left"]:
        controller.queue_move(-1, 0)
    elif key in ["D", "Right"]:
        controller.queue_move(1, 0)

scene.on_key = handle_input
```

## Bounce Effect

Add a bounce when hitting walls:

```python
def move_or_bump(entity, new_x, new_y, grid, duration=0.2):
    """Move to position, or bump animation if blocked."""

    if grid.at(new_x, new_y).walkable:
        # Normal move
        anim_x = mcrfpy.Animation("x", float(new_x), duration, "easeInOut")
        anim_y = mcrfpy.Animation("y", float(new_y), duration, "easeInOut")
        anim_x.start(entity)
        anim_y.start(entity)
    else:
        # Bump animation - move partway then back
        current_x = entity.x
        current_y = entity.y

        # Calculate bump position (1/4 of the way)
        bump_x = current_x + (new_x - current_x) * 0.25
        bump_y = current_y + (new_y - current_y) * 0.25

        def bump_back(anim, target):
            # Return to original position
            back_x = mcrfpy.Animation("x", float(current_x), duration * 0.5, "easeOut")
            back_y = mcrfpy.Animation("y", float(current_y), duration * 0.5, "easeOut")
            back_x.start(entity)
            back_y.start(entity)

        # Bump forward
        bump_anim_x = mcrfpy.Animation("x", bump_x, duration * 0.5, "easeOut", callback=bump_back)
        bump_anim_y = mcrfpy.Animation("y", bump_y, duration * 0.5, "easeOut")
        bump_anim_x.start(entity)
        bump_anim_y.start(entity)
```

## Attack Lunge

Quick lunge toward target then return:

```python
def attack_lunge(attacker, target, duration=0.15):
    """Lunge toward target for attack animation."""
    start_x = attacker.x
    start_y = attacker.y

    # Calculate lunge position (halfway to target)
    lunge_x = start_x + (target.x - start_x) * 0.5
    lunge_y = start_y + (target.y - start_y) * 0.5

    def return_to_start(anim, entity):
        # Return to starting position
        back_x = mcrfpy.Animation("x", float(start_x), duration, "easeOut")
        back_y = mcrfpy.Animation("y", float(start_y), duration, "easeOut")
        back_x.start(entity)
        back_y.start(entity)

    # Lunge forward
    lunge_anim_x = mcrfpy.Animation("x", lunge_x, duration, "easeIn", callback=return_to_start)
    lunge_anim_y = mcrfpy.Animation("y", lunge_y, duration, "easeIn")

    lunge_anim_x.start(attacker)
    lunge_anim_y.start(attacker)
```

## Tips

1. **Duration Tuning**: 0.15-0.25 seconds feels responsive. Slower for larger movements.

2. **Single Axis Movement**: For 4-directional movement, only animate the changing axis:
   ```python
   if new_x != current_x:
       anim = mcrfpy.Animation("x", float(new_x), duration, "easeInOut", callback=done)
   else:
       anim = mcrfpy.Animation("y", float(new_y), duration, "easeInOut", callback=done)
   ```

3. **Input Blocking**: Always check `is_animating` before accepting new input in turn-based games.

4. **Callback on One Animation**: When animating x and y together, only put the callback on one.

5. **Camera Smoothness**: Use "linear" for camera, "easeInOut" for entities - prevents jarring camera.

6. **Animation References**: Keep references to running animations if you need to cancel them:
   ```python
   current_anim = mcrfpy.Animation("x", 100.0, 0.5, "linear")
   current_anim.start(entity)
   # Later: current_anim = None  # Let it complete or create new one
   ```

## See Also

- [Turn System](combat_turn_system.md) - Coordinating animations with turns
- [Enemy AI](combat_enemy_ai.md) - Animating AI movement
- [Melee Combat](combat_melee.md) - Attack animations
