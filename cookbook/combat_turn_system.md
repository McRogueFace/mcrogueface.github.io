# Turn-Based Game Loop

A state machine approach to managing turn-based combat and gameplay.

## Overview

Turn-based games require careful management of game state to ensure actors take turns in order. This recipe provides a `TurnManager` class that handles actor ordering, speed-based initiative, and turn cycling.

## Basic Turn Manager

```python
import mcrfpy

class TurnManager:
    """Manages turn order for actors in a turn-based game."""

    def __init__(self):
        self.actors = []      # List of (actor, speed) tuples
        self.current = 0      # Index of current actor
        self.turn_number = 0  # Global turn counter
        self.state = "waiting"  # waiting, player_turn, enemy_turn

    def add_actor(self, actor, speed=100):
        """Add an actor with a speed value (higher = acts first)."""
        self.actors.append({"actor": actor, "speed": speed, "energy": 0})
        self._sort_by_speed()

    def remove_actor(self, actor):
        """Remove an actor from the turn order."""
        self.actors = [a for a in self.actors if a["actor"] != actor]
        if self.current >= len(self.actors):
            self.current = 0

    def _sort_by_speed(self):
        """Sort actors by speed (descending)."""
        self.actors.sort(key=lambda a: a["speed"], reverse=True)

    def current_actor(self):
        """Get the actor whose turn it is."""
        if not self.actors:
            return None
        return self.actors[self.current]["actor"]

    def end_turn(self):
        """End the current actor's turn and advance to next."""
        if not self.actors:
            return None

        self.current = (self.current + 1) % len(self.actors)

        # Increment turn number when we wrap around
        if self.current == 0:
            self.turn_number += 1

        return self.current_actor()

    def is_player_turn(self, player):
        """Check if it's the player's turn."""
        return self.current_actor() == player
```

## Energy-Based System

For more complex games, use an energy system where faster actors get more frequent turns:

```python
class EnergyTurnManager:
    """Turn manager using energy accumulation for speed differences."""

    ENERGY_THRESHOLD = 100  # Energy needed to take a turn

    def __init__(self):
        self.actors = []
        self.current_actor_data = None

    def add_actor(self, actor, speed=100):
        """Add actor with speed (determines energy gain per tick)."""
        self.actors.append({
            "actor": actor,
            "speed": speed,
            "energy": 0
        })

    def remove_actor(self, actor):
        """Remove an actor from the system."""
        self.actors = [a for a in self.actors if a["actor"] != actor]

    def tick(self):
        """Advance time and return next actor ready to act, or None."""
        # Give energy to all actors
        for actor_data in self.actors:
            actor_data["energy"] += actor_data["speed"]

        # Find actor with most energy above threshold
        ready = [a for a in self.actors if a["energy"] >= self.ENERGY_THRESHOLD]

        if ready:
            # Highest energy acts first
            ready.sort(key=lambda a: a["energy"], reverse=True)
            self.current_actor_data = ready[0]
            return self.current_actor_data["actor"]

        return None

    def end_turn(self):
        """Spend energy for the current actor's turn."""
        if self.current_actor_data:
            self.current_actor_data["energy"] -= self.ENERGY_THRESHOLD
            self.current_actor_data = None

    def get_next_actor(self):
        """Get next actor to act, ticking time if needed."""
        # Keep ticking until someone can act
        for _ in range(1000):  # Safety limit
            actor = self.tick()
            if actor:
                return actor
        return None
```

## Complete Game Loop Example

```python
import mcrfpy

# Game state
class GameState:
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    ANIMATING = "animating"
    GAME_OVER = "game_over"

# Initialize turn manager
turn_manager = TurnManager()
game_state = GameState.PLAYER_TURN

# Track player and enemies
player = None
enemies = []

def setup_game(grid, player_entity, enemy_entities):
    """Initialize the turn system with game entities."""
    global player, enemies

    player = player_entity
    enemies = enemy_entities

    # Add player first (or with high speed)
    turn_manager.add_actor(player, speed=100)

    # Add enemies
    for enemy in enemies:
        turn_manager.add_actor(enemy, speed=80)

def process_turn():
    """Process the current actor's turn."""
    global game_state

    current = turn_manager.current_actor()

    if current == player:
        # Player's turn - wait for input
        game_state = GameState.PLAYER_TURN
    else:
        # Enemy turn - run AI
        game_state = GameState.ENEMY_TURN
        process_enemy_turn(current)

def process_enemy_turn(enemy):
    """Execute enemy AI and end their turn."""
    # Enemy AI logic here (see combat_enemy_ai.md)
    # ...

    # End turn after action
    end_current_turn()

def end_current_turn():
    """End current turn and advance to next actor."""
    global game_state

    # Check for dead actors
    cleanup_dead_actors()

    # Advance to next
    turn_manager.end_turn()

    # Check win/lose conditions
    if not enemies:
        game_state = GameState.GAME_OVER
        show_victory()
    elif player_is_dead():
        game_state = GameState.GAME_OVER
        show_defeat()
    else:
        # Continue to next turn
        process_turn()

def cleanup_dead_actors():
    """Remove dead actors from turn order."""
    global enemies

    # Remove dead enemies
    for enemy in enemies[:]:
        if enemy.hp <= 0:
            turn_manager.remove_actor(enemy)
            enemies.remove(enemy)

def handle_player_input(key, action):
    """Handle keyboard input during player's turn."""
    if action != "start":
        return

    if game_state != GameState.PLAYER_TURN:
        return  # Not player's turn

    # Movement keys
    dx, dy = 0, 0
    if key in ["W", "Up"]:
        dy = -1
    elif key in ["S", "Down"]:
        dy = 1
    elif key in ["A", "Left"]:
        dx = -1
    elif key in ["D", "Right"]:
        dx = 1
    elif key == "Space":
        # Wait/skip turn
        end_current_turn()
        return

    if dx != 0 or dy != 0:
        # Try to move or attack
        if try_move_or_attack(player, dx, dy):
            end_current_turn()

scene.on_key = handle_player_input
```

## Turn Display UI

Show the turn order to the player:

```python
def create_turn_order_ui(scene, turn_manager, x=800, y=50):
    """Create a visual turn order display."""
    # Background frame
    frame = mcrfpy.Frame(x, y, 200, 300)
    frame.fill_color = mcrfpy.Color(30, 30, 30, 200)
    frame.outline = 2
    frame.outline_color = mcrfpy.Color(100, 100, 100)
    scene.children.append(frame)

    # Title
    title = mcrfpy.Caption(text="Turn Order", x=x + 10, y=y + 10)
    title.fill_color = mcrfpy.Color(255, 255, 255)
    scene.children.append(title)

    return frame

def update_turn_order_display(scene, frame, turn_manager, x=800, y=50):
    """Update the turn order display."""

    # Clear old entries (keep frame and title)
    # In practice, store references to caption objects and update them

    for i, actor_data in enumerate(turn_manager.actors):
        actor = actor_data["actor"]
        is_current = (i == turn_manager.current)

        # Actor name/type
        name = getattr(actor, 'name', f"Actor {i}")
        color = mcrfpy.Color(255, 255, 0) if is_current else mcrfpy.Color(200, 200, 200)

        caption = mcrfpy.Caption(name, x + 10, y + 40 + i * 25)
        caption.fill_color = color
        ui.append(caption)
```

## Tips

1. **Player Input Blocking**: Only accept player input when `game_state == PLAYER_TURN`

2. **Animation Sync**: Set state to `ANIMATING` during movement/attack animations, then continue turns after animation completes

3. **Speed Balancing**:
   - Player: 100 (baseline)
   - Fast enemies: 120-150 (act before player sometimes)
   - Slow enemies: 50-80 (player acts more often)

4. **Initiative Rolls**: For variety, add randomness to speed at combat start:
   ```python
   import random
   speed = base_speed + random.randint(-10, 10)
   ```

5. **Reaction System**: For counter-attacks or interrupts, check conditions before finalizing turn end

## See Also

- [Enemy AI](combat_enemy_ai.md) - Making enemies take intelligent actions
- [Melee Combat](combat_melee.md) - Damage calculation when attacking
- [Animated Movement](combat_animated_movement.md) - Smooth movement during turns
