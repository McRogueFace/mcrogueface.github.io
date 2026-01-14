# Status Effects

Tracking and applying temporary effects like poison, confusion, and buffs.

## Overview

Status effects add tactical depth to combat by applying temporary modifiers that change over time. This recipe covers implementing stackable, time-limited effects.

## Basic Status Effect

```python
class StatusEffect:
    """A temporary effect applied to an entity."""

    def __init__(self, name, duration, on_tick=None, on_apply=None, on_expire=None):
        """
        Args:
            name: Effect identifier
            duration: Turns remaining
            on_tick: Called each turn (receives target)
            on_apply: Called when effect is applied (receives target)
            on_expire: Called when effect expires (receives target)
        """
        self.name = name
        self.duration = duration
        self.on_tick = on_tick
        self.on_apply = on_apply
        self.on_expire = on_expire

    def tick(self, target):
        """Process one turn of the effect."""
        if self.on_tick:
            self.on_tick(target)

        self.duration -= 1
        return self.duration > 0  # Return False when expired

    def apply(self, target):
        """Called when effect is first applied."""
        if self.on_apply:
            self.on_apply(target)

    def expire(self, target):
        """Called when effect expires."""
        if self.on_expire:
            self.on_expire(target)
```

## Effect Manager

Track effects on entities:

```python
class EffectManager:
    """Manages status effects for an entity."""

    def __init__(self, owner):
        self.owner = owner
        self.effects = []  # List of active StatusEffects

    def add_effect(self, effect):
        """Add a new effect, stacking or refreshing as appropriate."""
        # Check for existing effect of same type
        for existing in self.effects:
            if existing.name == effect.name:
                # Refresh duration (take the longer one)
                existing.duration = max(existing.duration, effect.duration)
                return

        # New effect
        self.effects.append(effect)
        effect.apply(self.owner)

    def remove_effect(self, name):
        """Remove an effect by name."""
        for effect in self.effects[:]:
            if effect.name == name:
                effect.expire(self.owner)
                self.effects.remove(effect)

    def has_effect(self, name):
        """Check if entity has an effect."""
        return any(e.name == name for e in self.effects)

    def get_effect(self, name):
        """Get an effect by name."""
        for effect in self.effects:
            if effect.name == name:
                return effect
        return None

    def tick_all(self):
        """Process all effects for one turn."""
        expired = []

        for effect in self.effects:
            still_active = effect.tick(self.owner)
            if not still_active:
                expired.append(effect)

        # Remove expired effects
        for effect in expired:
            effect.expire(self.owner)
            self.effects.remove(effect)

    def clear_all(self):
        """Remove all effects."""
        for effect in self.effects:
            effect.expire(self.owner)
        self.effects.clear()
```

## Common Effect Types

### Poison

```python
def create_poison(damage=2, duration=5):
    """Create a poison effect that deals damage each turn."""

    def on_tick(target):
        target.hp -= damage
        print(f"{target.name} takes {damage} poison damage!")

        # Visual feedback
        show_damage_number(target.entity.x * 16, target.entity.y * 16, damage)
        flash_entity_green(target.entity)

    def on_apply(target):
        print(f"{target.name} is poisoned!")

    def on_expire(target):
        print(f"{target.name} is no longer poisoned.")

    return StatusEffect("poison", duration, on_tick=on_tick,
                       on_apply=on_apply, on_expire=on_expire)
```

### Burning

```python
def create_burning(damage=3, duration=3):
    """Fire damage that can spread."""

    def on_tick(target):
        target.hp -= damage
        print(f"{target.name} burns for {damage} damage!")

        # Chance to spread to adjacent enemies (optional)
        # spread_fire(target)

    def on_apply(target):
        print(f"{target.name} catches fire!")
        # Visual: change sprite or add particle effect
        target.entity.sprite_number = target.burning_sprite

    def on_expire(target):
        print(f"{target.name} stops burning.")
        target.entity.sprite_number = target.normal_sprite

    return StatusEffect("burning", duration, on_tick=on_tick,
                       on_apply=on_apply, on_expire=on_expire)
```

### Confusion

```python
import random

def create_confusion(duration=3):
    """Target moves randomly instead of intentionally."""

    def on_apply(target):
        print(f"{target.name} is confused!")
        target.confused = True

    def on_expire(target):
        print(f"{target.name} snaps out of confusion.")
        target.confused = False

    return StatusEffect("confusion", duration,
                       on_apply=on_apply, on_expire=on_expire)


# In AI/movement code:
def get_move_direction(entity):
    if hasattr(entity, 'confused') and entity.confused:
        # Random direction instead of intended
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return random.choice(directions)
    else:
        return entity.intended_direction
```

### Stun/Freeze

```python
def create_stun(duration=2):
    """Target cannot act."""

    def on_apply(target):
        print(f"{target.name} is stunned!")
        target.can_act = False

    def on_expire(target):
        print(f"{target.name} recovers from stun.")
        target.can_act = True

    return StatusEffect("stun", duration,
                       on_apply=on_apply, on_expire=on_expire)


# In turn processing:
def process_turn(entity):
    if not getattr(entity, 'can_act', True):
        print(f"{entity.name} is stunned and cannot act!")
        return  # Skip turn
    # Normal turn processing...
```

### Stat Buffs/Debuffs

```python
def create_strength_buff(bonus=5, duration=5):
    """Temporarily increase attack."""

    def on_apply(target):
        print(f"{target.name} gains +{bonus} attack!")
        target.fighter.attack += bonus

    def on_expire(target):
        print(f"{target.name}'s strength returns to normal.")
        target.fighter.attack -= bonus

    return StatusEffect("strength", duration,
                       on_apply=on_apply, on_expire=on_expire)


def create_weakness(penalty=3, duration=4):
    """Temporarily decrease attack."""

    def on_apply(target):
        print(f"{target.name} feels weakened!")
        target.fighter.attack = max(1, target.fighter.attack - penalty)

    def on_expire(target):
        print(f"{target.name}'s strength returns.")
        target.fighter.attack += penalty

    return StatusEffect("weakness", duration,
                       on_apply=on_apply, on_expire=on_expire)


def create_armor_buff(bonus=3, duration=5):
    """Temporarily increase defense."""

    def on_apply(target):
        print(f"{target.name} gains +{bonus} defense!")
        target.fighter.defense += bonus

    def on_expire(target):
        target.fighter.defense -= bonus

    return StatusEffect("armored", duration,
                       on_apply=on_apply, on_expire=on_expire)
```

### Regeneration

```python
def create_regeneration(heal_amount=2, duration=5):
    """Heal each turn."""

    def on_tick(target):
        old_hp = target.fighter.hp
        target.fighter.heal(heal_amount)
        actual_heal = target.fighter.hp - old_hp

        if actual_heal > 0:
            print(f"{target.name} regenerates {actual_heal} HP.")
            show_heal_number(target, actual_heal)

    return StatusEffect("regeneration", duration, on_tick=on_tick)
```

### Invisibility

```python
def create_invisibility(duration=5):
    """Enemies cannot see or target entity."""

    def on_apply(target):
        print(f"{target.name} becomes invisible!")
        target.invisible = True
        # Visual: make sprite semi-transparent
        # target.entity.opacity = 0.3  (if supported)

    def on_expire(target):
        print(f"{target.name} becomes visible again.")
        target.invisible = False
        # target.entity.opacity = 1.0

    return StatusEffect("invisibility", duration,
                       on_apply=on_apply, on_expire=on_expire)


# In AI targeting:
def find_target(enemy, potential_targets):
    visible_targets = [t for t in potential_targets
                       if not getattr(t, 'invisible', False)]
    if not visible_targets:
        return None
    # Return nearest visible target
    return min(visible_targets, key=lambda t: distance_to(enemy, t))
```

## Entity Integration

Add effect manager to combat entities:

```python
class CombatEntity:
    """Entity with combat and effect support."""

    def __init__(self, grid, x, y, texture, sprite_index, **stats):
        self.entity = mcrfpy.Entity((x, y), texture, sprite_index)
        grid.entities.append(self.entity)
        self.grid = grid

        # Combat stats
        self.fighter = Fighter(**stats)
        self.name = stats.get('name', 'Entity')

        # Status effects
        self.effects = EffectManager(self)

        # State flags (set by effects)
        self.can_act = True
        self.confused = False
        self.invisible = False

    def start_turn(self):
        """Called at the start of this entity's turn."""
        # Process all status effects
        self.effects.tick_all()

    def apply_effect(self, effect):
        """Apply a status effect."""
        self.effects.add_effect(effect)

    def has_effect(self, name):
        """Check for an effect."""
        return self.effects.has_effect(name)
```

## Visual Effect Indicators

Show active effects in UI:

```python
import mcrfpy

class EffectIndicator:
    """Visual indicator for active effects."""

    # Effect icons (sprite indices in UI texture)
    EFFECT_SPRITES = {
        "poison": 10,
        "burning": 11,
        "stun": 12,
        "strength": 13,
        "weakness": 14,
        "regeneration": 15,
        "invisibility": 16,
        "confusion": 17,
    }

    def __init__(self, scene, entity, ui_texture, offset_x=0, offset_y=-20):
        self.scene = scene
        self.entity = entity
        self.texture = ui_texture
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.icons = {}  # effect_name -> sprite

    def update(self, effect_manager):
        """Update displayed effect icons."""
        # Get current effects
        current_effects = {e.name for e in effect_manager.effects}

        # Remove icons for expired effects
        for name in list(self.icons.keys()):
            if name not in current_effects:
                try:
                    for i, elem in enumerate(self.scene.children):
                        if elem is self.icons[name]:
                            self.scene.children.remove(i)
                            break
                except:
                    pass
                del self.icons[name]

        # Add icons for new effects
        for i, name in enumerate(current_effects):
            if name not in self.icons and name in self.EFFECT_SPRITES:
                sprite_idx = self.EFFECT_SPRITES[name]
                x = self.entity.entity.x * 16 + self.offset_x + i * 10
                y = self.entity.entity.y * 16 + self.offset_y

                icon = mcrfpy.Sprite(self.texture, sprite_idx, x, y, 0.5)
                self.scene.children.append(icon)
                self.icons[name] = icon

    def clear(self):
        """Remove all icons."""
        for icon in self.icons.values():
            try:
                for i, elem in enumerate(self.scene.children):
                    if elem is icon:
                        self.scene.children.remove(i)
                        break
            except:
                pass
        self.icons.clear()
```

## Effect Application

Applying effects through attacks and items:

```python
def poison_attack(attacker, defender):
    """Attack that may poison the target."""
    # Do normal attack
    result = attack(attacker.fighter, defender.fighter)

    # 30% chance to poison
    if random.random() < 0.3:
        poison = create_poison(damage=2, duration=3)
        defender.apply_effect(poison)

    return result


def use_healing_potion(user, heal_amount=20):
    """Use a healing potion."""
    user.fighter.heal(heal_amount)
    print(f"{user.name} heals for {heal_amount} HP!")


def use_strength_potion(user):
    """Use a strength potion."""
    buff = create_strength_buff(bonus=5, duration=10)
    user.apply_effect(buff)


def use_antidote(user):
    """Cure poison."""
    if user.has_effect("poison"):
        user.effects.remove_effect("poison")
        print(f"{user.name} is cured of poison!")
    else:
        print(f"{user.name} is not poisoned.")
```

## Stacking Behavior

Different stacking modes for effects:

```python
class StackableEffect(StatusEffect):
    """Effect that stacks intensity."""

    def __init__(self, name, duration, intensity=1, max_stacks=5, **kwargs):
        super().__init__(name, duration, **kwargs)
        self.intensity = intensity
        self.max_stacks = max_stacks
        self.stacks = 1

    def add_stack(self):
        """Add another stack."""
        if self.stacks < self.max_stacks:
            self.stacks += 1
            return True
        return False


class StackingEffectManager(EffectManager):
    """Effect manager with stacking support."""

    def add_effect(self, effect):
        if isinstance(effect, StackableEffect):
            # Check for existing stacks
            for existing in self.effects:
                if existing.name == effect.name:
                    if existing.add_stack():
                        # Refresh duration
                        existing.duration = max(existing.duration, effect.duration)
                        return
                    else:
                        return  # Max stacks

        # Default behavior
        super().add_effect(effect)


# Stacking poison example
def create_stacking_poison(base_damage=1, duration=5):
    def on_tick(target):
        # Find the poison effect to get stack count
        effect = target.effects.get_effect("poison")
        if effect:
            damage = base_damage * effect.stacks
            target.hp -= damage
            print(f"{target.name} takes {damage} poison damage! ({effect.stacks} stacks)")

    return StackableEffect("poison", duration, on_tick=on_tick, max_stacks=5)
```

## Tips

1. **Effect Processing Order**: Process effects at turn start, before the entity acts

2. **Cleanup on Death**: Clear effects when entity dies:
   ```python
   def die(self):
       self.effects.clear_all()
       # Rest of death logic...
   ```

3. **Resist/Immunity**: Add resistance checks:
   ```python
   def apply_effect(self, effect):
       if effect.name in self.immunities:
           print(f"{self.name} is immune to {effect.name}!")
           return
       if effect.name in self.resistances:
           effect.duration //= 2  # Half duration
       self.effects.add_effect(effect)
   ```

4. **Save/Load**: Serialize effects for save games:
   ```python
   def serialize_effects(effect_manager):
       return [{"name": e.name, "duration": e.duration}
               for e in effect_manager.effects]
   ```

5. **Visual Clarity**: Always show effect icons and remaining duration to players

6. **Balance**: DoT effects (poison, burn) should deal less per-tick than direct damage to be fair

## See Also

- [Melee Combat](combat_melee.md) - Applying effects on hit
- [Turn System](combat_turn_system.md) - When effects tick
- [Enemy AI](combat_enemy_ai.md) - AI behavior with status effects
