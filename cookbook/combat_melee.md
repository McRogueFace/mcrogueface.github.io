# Melee Combat System

![Melee Combat Recipe](/images/cookbook/combat_melee.png)

HP, attack, defense calculations and combat resolution.

## Overview

This recipe covers the fundamentals of melee combat: tracking health, calculating damage, handling death, and providing visual feedback.

## Basic Fighter Stats

```python
from dataclasses import dataclass

@dataclass
class Fighter:
    """Combat statistics for an entity."""
    hp: int
    max_hp: int
    attack: int
    defense: int

    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int):
        """Heal up to max HP."""
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount: int) -> int:
        """Take damage and return actual damage dealt."""
        actual = min(self.hp, amount)
        self.hp -= actual
        return actual
```

## Basic Attack Resolution

```python
def attack(attacker: Fighter, defender: Fighter) -> dict:
    """
    Resolve an attack between two fighters.

    Returns dict with attack results for UI/logging.
    """
    # Calculate base damage
    damage = max(0, attacker.attack - defender.defense)

    # Apply damage
    actual_damage = defender.take_damage(damage)

    return {
        "attacker": attacker,
        "defender": defender,
        "damage": actual_damage,
        "blocked": attacker.attack - damage,
        "killed": not defender.is_alive()
    }
```

## Advanced Damage Formula

More interesting combat with randomness and critical hits:

```python
import random

def calculate_damage(attacker: Fighter, defender: Fighter) -> dict:
    """
    Calculate damage with variance and critical hits.

    Formula: (ATK * variance) - DEF, minimum 1
    Critical: 10% chance for 2x damage, ignores defense
    """
    # Base damage with variance (+/- 20%)
    variance = random.uniform(0.8, 1.2)
    base_damage = int(attacker.attack * variance)

    # Critical hit check
    crit_chance = 0.10
    is_critical = random.random() < crit_chance

    if is_critical:
        # Critical hits deal double damage and ignore defense
        final_damage = base_damage * 2
    else:
        # Normal hit - subtract defense
        final_damage = max(1, base_damage - defender.defense)

    return {
        "damage": final_damage,
        "is_critical": is_critical,
        "base_roll": base_damage
    }


def attack_with_variance(attacker: Fighter, defender: Fighter) -> dict:
    """Perform attack with variance and crits."""
    result = calculate_damage(attacker, defender)
    actual = defender.take_damage(result["damage"])

    return {
        "damage": actual,
        "is_critical": result["is_critical"],
        "killed": not defender.is_alive()
    }
```

## Combat Entity Class

Combining Fighter stats with Entity:

```python
import mcrfpy

class CombatEntity:
    """Game entity with combat capabilities."""

    def __init__(self, grid, x, y, texture, sprite_index,
                 hp=10, attack=5, defense=2, name="Entity"):
        # Create visual entity
        self.entity = mcrfpy.Entity((x, y), texture, sprite_index)
        grid.entities.append(self.entity)
        self.grid = grid

        # Combat stats
        self.fighter = Fighter(hp=hp, max_hp=hp, attack=attack, defense=defense)
        self.name = name

        # State
        self.alive = True

    @property
    def x(self):
        return int(self.entity.x)

    @property
    def y(self):
        return int(self.entity.y)

    @property
    def hp(self):
        return self.fighter.hp

    @hp.setter
    def hp(self, value):
        self.fighter.hp = value
        if self.fighter.hp <= 0:
            self.die()

    def attack_target(self, target: 'CombatEntity') -> dict:
        """Attack another combat entity."""
        result = attack(self.fighter, target.fighter)

        # Log the attack
        if result["is_critical"]:
            print(f"{self.name} CRITICALLY hits {target.name} for {result['damage']}!")
        else:
            print(f"{self.name} hits {target.name} for {result['damage']}.")

        if result["killed"]:
            target.die()

        return result

    def die(self):
        """Handle death."""
        if not self.alive:
            return

        self.alive = False
        print(f"{self.name} has died!")

        # Remove from grid
        try:
            idx = self.entity.index()
            self.grid.entities.remove(idx)
        except:
            pass

    def heal(self, amount: int):
        """Restore HP."""
        old_hp = self.fighter.hp
        self.fighter.heal(amount)
        healed = self.fighter.hp - old_hp
        print(f"{self.name} heals for {healed} HP.")
```

## Visual Feedback

Show damage with animations and effects:

```python
import mcrfpy

def show_damage_number(scene, x, y, damage, is_critical=False):
    """Display floating damage number."""
    # Create damage text
    text = f"{damage}" if not is_critical else f"CRIT {damage}!"
    color = mcrfpy.Color(255, 255, 0) if is_critical else mcrfpy.Color(255, 100, 100)

    caption = mcrfpy.Caption(text=text, x=x, y=y)
    caption.fill_color = color
    scene.children.append(caption)

    # Animate upward and fade out
    anim_y = mcrfpy.Animation("y", float(y - 30), 0.8, "easeOut")
    anim_y.start(caption)

    # Remove after animation
    def cleanup(timer, runtime):
        try:
            for i, elem in enumerate(scene.children):
                if elem is caption:
                    scene.children.remove(i)
                    break
        except:
            pass

    mcrfpy.Timer(f"dmg_{id(caption)}", cleanup, 800)


def flash_entity(entity, color, duration=0.2):
    """Flash an entity a color (for damage feedback)."""
    # Store original color if available
    # Note: Entity color support depends on implementation

    # Simple flash using sprite swap
    original_sprite = entity.sprite_number

    # Damage sprite (e.g., white version)
    damage_sprite = original_sprite + 100  # Assuming damage sprites offset

    entity.sprite_number = damage_sprite

    timer_name = f"flash_{id(entity)}"

    def restore(timer, runtime):
        entity.sprite_number = original_sprite

    mcrfpy.Timer(timer_name, restore, int(duration * 1000))


def shake_screen(grid, intensity=5, duration=0.3):
    """Shake the camera for impact feedback."""
    original_center = (grid.center[0], grid.center[1])

    shake_count = [0]
    max_shakes = int(duration * 60)  # 60 fps
    timer_ref = [None]  # Store timer reference for cleanup

    def do_shake(timer, runtime):
        if shake_count[0] >= max_shakes:
            grid.center = original_center
            return

        offset_x = random.uniform(-intensity, intensity)
        offset_y = random.uniform(-intensity, intensity)
        grid.center = (original_center[0] + offset_x, original_center[1] + offset_y)
        shake_count[0] += 1

    mcrfpy.Timer("screen_shake", do_shake, 16)
```

## Health Bar Display

Show HP for entities:

```python
class HealthBar:
    """Visual health bar for an entity."""

    def __init__(self, scene, combat_entity, offset_y=-10, width=32, height=4):
        self.scene = scene
        self.entity = combat_entity
        self.offset_y = offset_y
        self.width = width
        self.height = height

        # Background (red/empty)
        self.bg = mcrfpy.Frame(0, 0, width, height)
        self.bg.fill_color = mcrfpy.Color(100, 0, 0)
        scene.children.append(self.bg)

        # Foreground (green/full)
        self.fg = mcrfpy.Frame(0, 0, width, height)
        self.fg.fill_color = mcrfpy.Color(0, 200, 0)
        scene.children.append(self.fg)

        self.update()

    def update(self):
        """Update health bar position and fill."""
        # Position above entity (convert grid to screen coords)
        screen_x = self.entity.x * 16 + self.offset_x
        screen_y = self.entity.y * 16 + self.offset_y

        self.bg.x = screen_x
        self.bg.y = screen_y

        self.fg.x = screen_x
        self.fg.y = screen_y

        # Update fill based on HP percentage
        hp_percent = self.entity.fighter.hp / self.entity.fighter.max_hp
        self.fg.w = self.width * hp_percent

        # Color based on HP
        if hp_percent > 0.6:
            self.fg.fill_color = mcrfpy.Color(0, 200, 0)  # Green
        elif hp_percent > 0.3:
            self.fg.fill_color = mcrfpy.Color(200, 200, 0)  # Yellow
        else:
            self.fg.fill_color = mcrfpy.Color(200, 0, 0)  # Red

    def remove(self):
        """Remove health bar from UI."""
        try:
            for i, elem in enumerate(self.scene.children):
                if elem is self.bg or elem is self.fg:
                    self.scene.children.remove(i)
        except:
            pass
```

## Combat Log

Keep a scrolling log of combat events:

```python
class CombatLog:
    """Scrolling combat message log."""

    def __init__(self, scene, x, y, width, height, max_messages=10):
        self.scene = scene
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_messages = max_messages
        self.messages = []
        self.captions = []

        # Background
        self.frame = mcrfpy.Frame(x, y, width, height)
        self.frame.fill_color = mcrfpy.Color(0, 0, 0, 180)
        scene.children.append(self.frame)

    def add_message(self, text, color=None):
        """Add a message to the log."""
        if color is None:
            color = mcrfpy.Color(200, 200, 200)

        self.messages.append((text, color))

        # Keep only recent messages
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

        self._refresh_display()

    def _refresh_display(self):
        """Redraw all messages."""
        # Remove old captions
        for caption in self.captions:
            try:
                for i, elem in enumerate(self.scene.children):
                    if elem is caption:
                        self.scene.children.remove(i)
                        break
            except:
                pass
        self.captions.clear()

        # Create new captions
        line_height = 18
        for i, (text, color) in enumerate(self.messages):
            caption = mcrfpy.Caption(text=text, x=self.x + 5, y=self.y + 5 + i * line_height)
            caption.fill_color = color
            self.scene.children.append(caption)
            self.captions.append(caption)

    def log_attack(self, attacker_name, defender_name, damage, killed=False, critical=False):
        """Log an attack event."""
        if critical:
            text = f"{attacker_name} CRITS {defender_name} for {damage}!"
            color = mcrfpy.Color(255, 255, 0)
        else:
            text = f"{attacker_name} hits {defender_name} for {damage}."
            color = mcrfpy.Color(200, 200, 200)

        self.add_message(text, color)

        if killed:
            self.add_message(f"{defender_name} is defeated!", mcrfpy.Color(255, 100, 100))


# Global combat log
combat_log = None

def init_combat_log(scene):
    global combat_log
    combat_log = CombatLog(scene, 10, 500, 400, 200)
```

## Complete Combat Resolution

Tying it all together:

```python
def resolve_combat(scene, attacker: CombatEntity, defender: CombatEntity, grid):
    """Full combat resolution with effects."""
    # Perform attack
    result = attack_with_variance(attacker.fighter, defender.fighter)

    # Visual feedback
    screen_x = defender.x * 16 + grid.x + 8
    screen_y = defender.y * 16 + grid.y

    show_damage_number(scene, screen_x, screen_y, result["damage"], result["is_critical"])
    flash_entity(defender.entity, mcrfpy.Color(255, 0, 0))

    if result["is_critical"]:
        shake_screen(grid, intensity=8)

    # Log it
    if combat_log:
        combat_log.log_attack(
            attacker.name,
            defender.name,
            result["damage"],
            killed=result["killed"],
            critical=result["is_critical"]
        )

    # Handle death
    if result["killed"]:
        defender.die()
        # Could trigger loot drop, XP gain, etc.
        on_enemy_killed(defender)

    return result


def on_enemy_killed(enemy):
    """Handle enemy death rewards."""
    # Grant XP, drop loot, etc.
    pass
```

## Tips

1. **Balance**: Start with attack roughly equal to defense + 5 for interesting fights

2. **Scaling**: Increase stats slowly. Double HP is more impactful than double attack.

3. **Feedback**: Always show damage numbers - players need to see their impact

4. **Death Animation**: Consider delaying entity removal for a death animation:
   ```python
   def die_with_animation(entity):
       # Play death animation
       anim = mcrfpy.Animation("opacity", 0.0, 0.5, "linear")
       anim.start(entity)
       # Remove after animation
       mcrfpy.Timer("remove", lambda timer, runtime: remove_entity(entity), 500)
   ```

5. **Armor Types**: For more depth, add damage types and resistances:
   ```python
   @dataclass
   class AdvancedFighter(Fighter):
       fire_resist: float = 0.0
       ice_resist: float = 0.0
       physical_resist: float = 0.0
   ```

## See Also

- [Turn System](combat_turn_system.md) - When attacks happen
- [Enemy AI](combat_enemy_ai.md) - Making enemies attack intelligently
- [Status Effects](combat_status_effects.md) - Poison, buffs, debuffs
