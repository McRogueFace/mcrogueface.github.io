# Path Animation (Multi-Step Movement)

Animate an entity along a path with chained animations, useful for smooth multi-tile movement, patrol routes, or cinematic sequences.

## Quick Example

```python
import mcrfpy

class PathAnimator:
    """Animate an entity along a series of waypoints."""

    def __init__(self, entity, path, step_duration=0.2, easing="easeInOut"):
        """
        Args:
            entity: The Entity to animate
            path: List of (x, y) waypoints in grid coordinates
            step_duration: Seconds per step
            easing: Animation easing function
        """
        self.entity = entity
        self.path = path
        self.step_duration = step_duration
        self.easing = easing
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
        def on_step_complete(anim, target):
            # Callback for step completion
            if self.on_step:
                self.on_step(self, self.index)
            self.index += 1
            self._animate_next()

        # Animate X
        if self.entity.x != target_x:
            anim_x = mcrfpy.Animation("x", float(target_x), self.step_duration,
                                       self.easing, callback=on_step_complete)
            anim_x.start(self.entity)
        # Animate Y
        elif self.entity.y != target_y:
            anim_y = mcrfpy.Animation("y", float(target_y), self.step_duration,
                                       self.easing, callback=on_step_complete)
            anim_y.start(self.entity)
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

    def __init__(self, entity, path, step_duration=0.2, easing="easeInOut"):
        self.entity = entity
        self.path = path
        self.step_duration = step_duration
        self.easing = easing
        self.index = 0
        self.on_complete = None
        self.on_step = None
        self._pending_anims = 0

    def start(self):
        """Begin path animation."""
        self.index = 0
        self._animate_next()

    def _on_anim_done(self, anim, target):
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
        current_x, current_y = self.entity.x, self.entity.y

        self._pending_anims = 0

        # Animate X if different
        if current_x != target_x:
            self._pending_anims += 1
            anim_x = mcrfpy.Animation("x", float(target_x), self.step_duration,
                                       self.easing, callback=self._on_anim_done)
            anim_x.start(self.entity)

        # Animate Y if different
        if current_y != target_y:
            self._pending_anims += 1
            anim_y = mcrfpy.Animation("y", float(target_y), self.step_duration,
                                       self.easing, callback=self._on_anim_done)
            anim_y.start(self.entity)

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

        def on_arrive(anim, target):
            if not self.is_running:
                return
            # Pause at waypoint
            def resume(timer_name):
                if self.is_running:
                    self.index = (self.index + 1) % len(self.path)
                    self._move_to_next()

            mcrfpy.Timer(f"patrol_pause_{id(self)}", resume,
                        int(self.pause_duration * 1000), once=True)

        # Animate movement
        if self.entity.x != target_x:
            anim = mcrfpy.Animation("x", float(target_x), self.step_duration,
                                    "easeInOut", callback=on_arrive)
            anim.start(self.entity)
        elif self.entity.y != target_y:
            anim = mcrfpy.Animation("y", float(target_y), self.step_duration,
                                    "easeInOut", callback=on_arrive)
            anim.start(self.entity)
        else:
            # Already there, move to next after pause
            on_arrive(None, None)


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
                self.waypoints.append((wp[0], wp[1], 0.3, "easeInOut"))
            elif len(wp) == 3:
                self.waypoints.append((wp[0], wp[1], wp[2], "easeInOut"))
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

        def done(anim, target):
            self.index += 1
            self._next()

        # Animate (using Y callback since we animate both)
        need_x = self.entity.x != x
        need_y = self.entity.y != y

        if need_x and need_y:
            anim_x = mcrfpy.Animation("x", float(x), duration, easing)
            anim_y = mcrfpy.Animation("y", float(y), duration, easing, callback=done)
            anim_x.start(self.entity)
            anim_y.start(self.entity)
        elif need_x:
            anim = mcrfpy.Animation("x", float(x), duration, easing, callback=done)
            anim.start(self.entity)
        elif need_y:
            anim = mcrfpy.Animation("y", float(y), duration, easing, callback=done)
            anim.start(self.entity)
        else:
            done(None, None)


# Usage - different speeds for different segments
waypoints = [
    (5, 5),                    # Default speed
    (5, 10, 0.5),              # Slower
    (10, 10, 0.2, "linear"),   # Fast, linear
    (10, 5, 1.0, "easeOut"),   # Slow arrival
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
        grid: Grid with walkable tiles
        target_x, target_y: Destination in grid coordinates
        step_duration: Animation time per tile
    """
    # Use grid's pathfinding (A* algorithm)
    start_x, start_y = int(entity.x), int(entity.y)

    # Compute path using grid's pathfinding
    path = grid.compute_path(start_x, start_y, target_x, target_y)

    if not path or len(path) == 0:
        print("No path found!")
        return None

    # Convert path to waypoint list (skip first point - current position)
    waypoints = [(p.x, p.y) for p in path[1:]]

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

        def done(anim, target):
            self.index += 1
            self._next()

        # Animate entity
        if self.entity.x != x:
            anim = mcrfpy.Animation("x", float(x), self.step_duration,
                                    "easeInOut", callback=done)
            anim.start(self.entity)
        elif self.entity.y != y:
            anim = mcrfpy.Animation("y", float(y), self.step_duration,
                                    "easeInOut", callback=done)
            anim.start(self.entity)
        else:
            done(None, None)
            return

        # Animate camera to follow
        cam_x = mcrfpy.Animation("center_x", (x + 0.5) * 16,
                                  self.step_duration, "easeInOut")
        cam_y = mcrfpy.Animation("center_y", (y + 0.5) * 16,
                                  self.step_duration, "easeInOut")
        cam_x.start(self.grid)
        cam_y.start(self.grid)


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
5. **Pathfinding integration**: Use `grid.compute_path()` for dynamic routes

## Tips

- Store animator references to prevent garbage collection during animation
- Use shorter step durations for more responsive movement
- Combine with camera following for smooth cinematic sequences
- For NPCs, add pause_duration at waypoints to feel more natural
- Check for obstacles before starting path animation
- Cancel paths gracefully when interrupted by player action
