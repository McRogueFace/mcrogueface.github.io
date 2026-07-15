---
mcrf:
  objects: [Entity, Grid, Timer, Animation, Behavior, AStarPath]
  diataxis: howto
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Path Animation (Multi-Step Movement)

Animate an entity along a path with chained animations, useful for smooth multi-tile movement, patrol routes, or cinematic sequences.

## Quick Example

```python
import mcrfpy

class PathAnimator:
    """Animate an entity along a series of waypoints."""

    def __init__(self, entity, path, step_duration=0.2, easing=None):
        """
        Args:
            entity: The Entity to animate
            path: List of (x, y) waypoints in grid coordinates
            step_duration: Seconds per step
            easing: mcrfpy.Easing value (default: EASE_IN_OUT)
        """
        self.entity = entity
        self.path = path
        self.step_duration = step_duration
        self.easing = easing if easing is not None else mcrfpy.Easing.EASE_IN_OUT
        self.index = 0
        self.on_complete = None
        self.on_step = None

    def start(self):
        """Begin path animation from current position."""
        self.index = 0
        self._animate_next()

    def _animate_next(self):
        """Animate to the next waypoint."""
        if self.index >= len(self.path):
            # Path complete
            if self.on_complete:
                self.on_complete(self)
            return

        target_x, target_y = self.path[self.index]

        # Create animations for this step
        def on_step_complete(target, prop, value):
            # Callback for step completion
            if self.on_step:
                self.on_step(self, self.index)
            self.index += 1
            self._animate_next()

        # Animate X (draw_x/draw_y are the tile-coordinate properties used
        # for smooth movement between grid cells; compare against draw_pos,
        # not entity.x/entity.y, which are pixel coordinates)
        pos = self.entity.draw_pos
        if pos.x != target_x:
            self.entity.animate("draw_x", float(target_x), self.step_duration,
                                 self.easing, callback=on_step_complete)
        # Animate Y
        elif pos.y != target_y:
            self.entity.animate("draw_y", float(target_y), self.step_duration,
                                 self.easing, callback=on_step_complete)
        else:
            # Already at position, skip to next
            self.index += 1
            self._animate_next()


# Usage
path = [(5, 5), (5, 8), (8, 8), (8, 5)]  # Square patrol route
animator = PathAnimator(enemy, path, step_duration=0.3)
animator.on_complete = lambda a: print("Patrol complete!")
animator.start()
```

## Diagonal Movement Support

Animate both X and Y simultaneously for diagonal paths:

```python
import mcrfpy

class DiagonalPathAnimator:
    """Path animator with diagonal movement support."""

    def __init__(self, entity, path, step_duration=0.2, easing=None):
        self.entity = entity
        self.path = path
        self.step_duration = step_duration
        self.easing = easing if easing is not None else mcrfpy.Easing.EASE_IN_OUT
        self.index = 0
        self.on_complete = None
        self.on_step = None
        self._pending_anims = 0

    def start(self):
        """Begin path animation."""
        self.index = 0
        self._animate_next()

    def _on_anim_done(self, target, prop, value):
        """Track when both X and Y animations complete."""
        self._pending_anims -= 1
        if self._pending_anims <= 0:
            if self.on_step:
                self.on_step(self, self.index)
            self.index += 1
            self._animate_next()

    def _animate_next(self):
        """Animate to next waypoint (diagonal if needed)."""
        if self.index >= len(self.path):
            if self.on_complete:
                self.on_complete(self)
            return

        target_x, target_y = self.path[self.index]
        pos = self.entity.draw_pos
        current_x, current_y = pos.x, pos.y

        self._pending_anims = 0

        # Animate X if different (draw_x/draw_y = tile-coordinate properties)
        if current_x != target_x:
            self._pending_anims += 1
            self.entity.animate("draw_x", float(target_x), self.step_duration,
                                 self.easing, callback=self._on_anim_done)

        # Animate Y if different
        if current_y != target_y:
            self._pending_anims += 1
            self.entity.animate("draw_y", float(target_y), self.step_duration,
                                 self.easing, callback=self._on_anim_done)

        # If already at target, move to next
        if self._pending_anims == 0:
            self.index += 1
            self._animate_next()


# Usage - diagonal path
path = [(2, 2), (5, 5), (8, 2), (5, 5)]  # Diamond pattern
animator = DiagonalPathAnimator(entity, path, step_duration=0.4)
animator.start()
```

## Looping Patrol Route

Create an enemy that continuously patrols a route:

```python
import mcrfpy

class PatrolAnimator:
    """Endlessly loop through a patrol path."""

    def __init__(self, entity, path, step_duration=0.3, pause_duration=0.5):
        """
        Args:
            entity: Entity to animate
            path: List of (x, y) waypoints
            step_duration: Time per movement step
            pause_duration: Pause at each waypoint
        """
        self.entity = entity
        self.path = path
        self.step_duration = step_duration
        self.pause_duration = pause_duration
        self.index = 0
        self.is_paused = False
        self.is_running = False

    def start(self):
        """Start the patrol loop."""
        self.is_running = True
        self._move_to_next()

    def stop(self):
        """Stop the patrol."""
        self.is_running = False

    def _move_to_next(self):
        """Move to the next waypoint."""
        if not self.is_running:
            return

        target_x, target_y = self.path[self.index]

        def on_arrive(target, prop, value):
            if not self.is_running:
                return
            # Pause at waypoint
            def resume(timer, runtime):
                if self.is_running:
                    self.index = (self.index + 1) % len(self.path)
                    self._move_to_next()

            mcrfpy.Timer(f"patrol_pause_{id(self)}", resume,
                        int(self.pause_duration * 1000), once=True)

        # Animate movement (draw_x/draw_y = tile-coordinate properties)
        pos = self.entity.draw_pos
        if pos.x != target_x:
            self.entity.animate("draw_x", float(target_x), self.step_duration,
                                 mcrfpy.Easing.EASE_IN_OUT, callback=on_arrive)
        elif pos.y != target_y:
            self.entity.animate("draw_y", float(target_y), self.step_duration,
                                 mcrfpy.Easing.EASE_IN_OUT, callback=on_arrive)
        else:
            # Already there, move to next after pause
            on_arrive(None, None, None)


# Usage
patrol_route = [(3, 3), (3, 7), (7, 7), (7, 3)]
guard = PatrolAnimator(guard_entity, patrol_route, pause_duration=1.0)
guard.start()

# Later, to stop:
# guard.stop()
```

## Path with Variable Speeds

Different speeds for different path segments:

```python
import mcrfpy

class VariableSpeedPath:
    """Path animator with per-segment speed control."""

    def __init__(self, entity, waypoints):
        """
        Args:
            entity: Entity to animate
            waypoints: List of (x, y, duration, easing) tuples
                       duration and easing are optional
        """
        self.entity = entity
        self.waypoints = []
        for wp in waypoints:
            if len(wp) == 2:
                self.waypoints.append((wp[0], wp[1], 0.3, mcrfpy.Easing.EASE_IN_OUT))
            elif len(wp) == 3:
                self.waypoints.append((wp[0], wp[1], wp[2], mcrfpy.Easing.EASE_IN_OUT))
            else:
                self.waypoints.append(wp)

        self.index = 0
        self.on_complete = None

    def start(self):
        self.index = 0
        self._next()

    def _next(self):
        if self.index >= len(self.waypoints):
            if self.on_complete:
                self.on_complete(self)
            return

        x, y, duration, easing = self.waypoints[self.index]

        def done(target, prop, value):
            self.index += 1
            self._next()

        # Animate (using the Y callback since we animate both; draw_x/draw_y
        # are the tile-coordinate properties)
        pos = self.entity.draw_pos
        need_x = pos.x != x
        need_y = pos.y != y

        if need_x and need_y:
            self.entity.animate("draw_x", float(x), duration, easing)
            self.entity.animate("draw_y", float(y), duration, easing, callback=done)
        elif need_x:
            self.entity.animate("draw_x", float(x), duration, easing, callback=done)
        elif need_y:
            self.entity.animate("draw_y", float(y), duration, easing, callback=done)
        else:
            done(None, None, None)


# Usage - different speeds for different segments
waypoints = [
    (5, 5),                                        # Default speed
    (5, 10, 0.5),                                   # Slower
    (10, 10, 0.2, mcrfpy.Easing.LINEAR),             # Fast, linear
    (10, 5, 1.0, mcrfpy.Easing.EASE_OUT),            # Slow arrival
]
path = VariableSpeedPath(entity, waypoints)
path.start()
```

## Pathfinding Integration

Use with McRogueFace's built-in pathfinding:

```python
import mcrfpy

def animate_to_target(entity, grid, target_x, target_y, step_duration=0.15):
    """
    Find path and animate entity to target.

    Args:
        entity: Entity to move
        grid: Grid with walkable tiles (unused directly - entity.find_path
               consults the grid the entity is attached to)
        target_x, target_y: Destination in grid coordinates
        step_duration: Animation time per tile
    """
    # Use the entity's own pathfinding (A* algorithm)
    path = entity.find_path((target_x, target_y))

    if not path:
        print("No path found!")
        return None

    # Consume the path into a waypoint list
    waypoints = []
    while path:
        step = path.walk()
        waypoints.append((step.x, step.y))

    # Create and start animator
    animator = PathAnimator(entity, waypoints, step_duration)
    animator.start()
    return animator


# Usage
animator = animate_to_target(player, grid, 15, 10)
if animator:
    animator.on_complete = lambda a: print("Arrived at destination!")
```

## Camera Following Path

Animate camera to follow the entity along the path:

```python
import mcrfpy

class CameraFollowingPath:
    """Path animator that also moves the camera."""

    def __init__(self, entity, grid, path, step_duration=0.2):
        self.entity = entity
        self.grid = grid
        self.path = path
        self.step_duration = step_duration
        self.index = 0
        self.on_complete = None

    def start(self):
        self.index = 0
        self._next()

    def _next(self):
        if self.index >= len(self.path):
            if self.on_complete:
                self.on_complete(self)
            return

        x, y = self.path[self.index]

        def done(target, prop, value):
            self.index += 1
            self._next()

        # Animate entity (draw_x/draw_y = tile-coordinate properties)
        pos = self.entity.draw_pos
        if pos.x != x:
            self.entity.animate("draw_x", float(x), self.step_duration,
                                 mcrfpy.Easing.EASE_IN_OUT, callback=done)
        elif pos.y != y:
            self.entity.animate("draw_y", float(y), self.step_duration,
                                 mcrfpy.Easing.EASE_IN_OUT, callback=done)
        else:
            done(None, None, None)
            return

        # Animate camera to follow (center_x/center_y are in pixel space;
        # tile size here is 16px)
        self.grid.animate("center_x", (x + 0.5) * 16,
                           self.step_duration, mcrfpy.Easing.EASE_IN_OUT)
        self.grid.animate("center_y", (y + 0.5) * 16,
                           self.step_duration, mcrfpy.Easing.EASE_IN_OUT)


# Usage
path = [(5, 5), (5, 10), (10, 10)]
mover = CameraFollowingPath(player, grid, path)
mover.on_complete = lambda m: print("Journey complete!")
mover.start()
```

## Key Concepts

1. **Animation callbacks**: Chain animations using the `callback` parameter
2. **Index tracking**: Keep track of current position in path
3. **Completion handling**: Fire callbacks when path is complete
4. **Diagonal support**: Animate both X and Y simultaneously with completion tracking
5. **Pathfinding integration**: Use `entity.find_path(target)` (or `grid.find_path(start, end)`) for dynamic routes

## Tips

- Store animator references to prevent garbage collection during animation
- Use shorter step durations for more responsive movement
- Combine with camera following for smooth cinematic sequences
- For NPCs, add pause_duration at waypoints to feel more natural
- Check for obstacles before starting path animation
- Cancel paths gracefully when interrupted by player action
