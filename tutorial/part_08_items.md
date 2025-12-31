# Part 8: Items and Inventory

In Part 7, we built a polished user interface. Now we will add items to the dungeon - health potions scattered on the floor, waiting to be discovered and used. Items add resource management and tactical depth to our roguelike.

## What You Will Learn

- Creating item entities on the ground
- Implementing pickup mechanics
- Managing a simple inventory list
- Using consumable items
- Item effects (healing)
- Spawning items in dungeon rooms

## Item Design Philosophy

Items in roguelikes serve multiple purposes:

| Purpose | Example | Gameplay Effect |
|---------|---------|-----------------|
| Recovery | Health potion | Sustain exploration |
| Power boost | Weapon | Increase damage |
| Utility | Scroll | Special abilities |
| Risk/reward | Unknown potion | Identification mechanics |

We will start with health potions - the most essential roguelike item.

## The Complete Code

Create a file called `part_08_items.py`:

```python
"""McRogueFace Tutorial - Part 8: Items and Inventory

Add health potions and inventory management.
"""
import mcrfpy
import random
from dataclasses import dataclass, field
from typing import Optional

# =============================================================================
# Constants
# =============================================================================

# Sprite indices for CP437 tileset
SPRITE_WALL = 35    # '#' - wall
SPRITE_FLOOR = 46   # '.' - floor
SPRITE_PLAYER = 64  # '@' - player
SPRITE_CORPSE = 37  # '%' - remains
SPRITE_POTION = 173 # Potion sprite (or use '!' = 33)

# Enemy sprites
SPRITE_GOBLIN = 103  # 'g'
SPRITE_ORC = 111     # 'o'
SPRITE_TROLL = 116   # 't'

# Grid dimensions
GRID_WIDTH = 50
GRID_HEIGHT = 30

# Room generation parameters
ROOM_MIN_SIZE = 6
ROOM_MAX_SIZE = 12
MAX_ROOMS = 8

# Enemy spawn parameters
MAX_ENEMIES_PER_ROOM = 3

# Item spawn parameters
MAX_ITEMS_PER_ROOM = 2

# FOV settings
FOV_RADIUS = 8

# Visibility colors
COLOR_VISIBLE = mcrfpy.Color(0, 0, 0, 0)
COLOR_DISCOVERED = mcrfpy.Color(0, 0, 40, 180)
COLOR_UNKNOWN = mcrfpy.Color(0, 0, 0, 255)

# Message colors
COLOR_PLAYER_ATTACK = mcrfpy.Color(200, 200, 200)
COLOR_ENEMY_ATTACK = mcrfpy.Color(255, 150, 150)
COLOR_PLAYER_DEATH = mcrfpy.Color(255, 50, 50)
COLOR_ENEMY_DEATH = mcrfpy.Color(100, 255, 100)
COLOR_HEAL = mcrfpy.Color(100, 255, 100)
COLOR_PICKUP = mcrfpy.Color(100, 200, 255)
COLOR_INFO = mcrfpy.Color(100, 100, 255)
COLOR_WARNING = mcrfpy.Color(255, 200, 50)
COLOR_INVALID = mcrfpy.Color(255, 100, 100)

# UI Layout constants
UI_TOP_HEIGHT = 60
UI_BOTTOM_HEIGHT = 150
GAME_AREA_Y = UI_TOP_HEIGHT
GAME_AREA_HEIGHT = 768 - UI_TOP_HEIGHT - UI_BOTTOM_HEIGHT

# =============================================================================
# Fighter Component
# =============================================================================

@dataclass
class Fighter:
    """Combat stats for an entity."""
    hp: int
    max_hp: int
    attack: int
    defense: int
    name: str
    is_player: bool = False

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        actual_damage = min(self.hp, amount)
        self.hp -= actual_damage
        return actual_damage

    def heal(self, amount: int) -> int:
        actual_heal = min(self.max_hp - self.hp, amount)
        self.hp += actual_heal
        return actual_heal

# =============================================================================
# Item Component
# =============================================================================

@dataclass
class Item:
    """Data for an item that can be picked up and used."""
    name: str
    item_type: str
    heal_amount: int = 0

    def describe(self) -> str:
        """Return a description of what this item does."""
        if self.item_type == "health_potion":
            return f"Restores {self.heal_amount} HP"
        return "Unknown item"

# =============================================================================
# Inventory System
# =============================================================================

@dataclass
class Inventory:
    """Container for items the player is carrying."""
    capacity: int = 10
    items: list = field(default_factory=list)

    def add(self, item: Item) -> bool:
        """Add an item to the inventory.

        Args:
            item: The item to add

        Returns:
            True if item was added, False if inventory is full
        """
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def remove(self, index: int) -> Optional[Item]:
        """Remove and return an item by index.

        Args:
            index: The index of the item to remove

        Returns:
            The removed item, or None if index is invalid
        """
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def get(self, index: int) -> Optional[Item]:
        """Get an item by index without removing it."""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def is_full(self) -> bool:
        """Check if the inventory is full."""
        return len(self.items) >= self.capacity

    def count(self) -> int:
        """Return the number of items in the inventory."""
        return len(self.items)

# =============================================================================
# Item Templates
# =============================================================================

ITEM_TEMPLATES = {
    "health_potion": {
        "name": "Health Potion",
        "sprite": SPRITE_POTION,
        "item_type": "health_potion",
        "heal_amount": 10
    }
}

# =============================================================================
# Enemy Templates
# =============================================================================

ENEMY_TEMPLATES = {
    "goblin": {
        "sprite": SPRITE_GOBLIN,
        "hp": 6,
        "attack": 3,
        "defense": 0
    },
    "orc": {
        "sprite": SPRITE_ORC,
        "hp": 10,
        "attack": 4,
        "defense": 1
    },
    "troll": {
        "sprite": SPRITE_TROLL,
        "hp": 16,
        "attack": 6,
        "defense": 2
    }
}

# =============================================================================
# Message Log System
# =============================================================================

class MessageLog:
    """A message log that displays recent game messages with colors."""

    def __init__(self, x: int, y: int, width: int, height: int, max_messages: int = 6):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_messages = max_messages
        self.messages: list[tuple[str, mcrfpy.Color]] = []
        self.captions: list[mcrfpy.Caption] = []

        self.frame = mcrfpy.Frame(
            pos=(x, y),
            size=(width, height)
        )
        self.frame.fill_color = mcrfpy.Color(20, 20, 30, 200)
        self.frame.outline = 2
        self.frame.outline_color = mcrfpy.Color(80, 80, 100)

        line_height = 20
        for i in range(max_messages):
            caption = mcrfpy.Caption(
                pos=(x + 10, y + 5 + i * line_height),
                text=""
            )
            caption.font_size = 14
            caption.fill_color = mcrfpy.Color(200, 200, 200)
            self.captions.append(caption)

    def add_to_scene(self, scene: mcrfpy.Scene) -> None:
        scene.children.append(self.frame)
        for caption in self.captions:
            scene.children.append(caption)

    def add(self, text: str, color: mcrfpy.Color = None) -> None:
        if color is None:
            color = mcrfpy.Color(200, 200, 200)

        self.messages.append((text, color))

        while len(self.messages) > self.max_messages:
            self.messages.pop(0)

        self._refresh()

    def _refresh(self) -> None:
        for i, caption in enumerate(self.captions):
            if i < len(self.messages):
                text, color = self.messages[i]
                caption.text = text
                caption.fill_color = color
            else:
                caption.text = ""

    def clear(self) -> None:
        self.messages.clear()
        self._refresh()

# =============================================================================
# Health Bar System
# =============================================================================

class HealthBar:
    """A visual health bar using nested frames."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = 30
        self.current_hp = 30

        self.bg_frame = mcrfpy.Frame(
            pos=(x, y),
            size=(width, height)
        )
        self.bg_frame.fill_color = mcrfpy.Color(80, 0, 0)
        self.bg_frame.outline = 2
        self.bg_frame.outline_color = mcrfpy.Color(150, 150, 150)

        self.fg_frame = mcrfpy.Frame(
            pos=(x + 2, y + 2),
            size=(width - 4, height - 4)
        )
        self.fg_frame.fill_color = mcrfpy.Color(0, 180, 0)
        self.fg_frame.outline = 0

        self.label = mcrfpy.Caption(
            pos=(x + 5, y + 2),
            text=f"HP: {self.current_hp}/{self.max_hp}"
        )
        self.label.font_size = 16
        self.label.fill_color = mcrfpy.Color(255, 255, 255)

    def add_to_scene(self, scene: mcrfpy.Scene) -> None:
        scene.children.append(self.bg_frame)
        scene.children.append(self.fg_frame)
        scene.children.append(self.label)

    def update(self, current_hp: int, max_hp: int) -> None:
        self.current_hp = current_hp
        self.max_hp = max_hp

        percent = max(0, current_hp / max_hp) if max_hp > 0 else 0

        inner_width = self.width - 4
        self.fg_frame.resize(int(inner_width * percent), self.height - 4)

        self.label.text = f"HP: {current_hp}/{max_hp}"

        if percent > 0.6:
            self.fg_frame.fill_color = mcrfpy.Color(0, 180, 0)
        elif percent > 0.3:
            self.fg_frame.fill_color = mcrfpy.Color(180, 180, 0)
        else:
            self.fg_frame.fill_color = mcrfpy.Color(180, 0, 0)

# =============================================================================
# Inventory Panel
# =============================================================================

class InventoryPanel:
    """A panel displaying the player's inventory."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.captions: list[mcrfpy.Caption] = []

        self.frame = mcrfpy.Frame(
            pos=(x, y),
            size=(width, height)
        )
        self.frame.fill_color = mcrfpy.Color(20, 20, 30, 200)
        self.frame.outline = 2
        self.frame.outline_color = mcrfpy.Color(80, 80, 100)

        self.title = mcrfpy.Caption(
            pos=(x + 10, y + 5),
            text="Inventory (G:pickup, U:use)"
        )
        self.title.font_size = 14
        self.title.fill_color = mcrfpy.Color(200, 200, 255)

        # Create slots for inventory items
        for i in range(5):  # Show up to 5 items
            caption = mcrfpy.Caption(
                pos=(x + 10, y + 25 + i * 18),
                text=""
            )
            caption.font_size = 13
            caption.fill_color = mcrfpy.Color(180, 180, 180)
            self.captions.append(caption)

    def add_to_scene(self, scene: mcrfpy.Scene) -> None:
        scene.children.append(self.frame)
        scene.children.append(self.title)
        for caption in self.captions:
            scene.children.append(caption)

    def update(self, inventory: Inventory) -> None:
        """Update the inventory display."""
        for i, caption in enumerate(self.captions):
            if i < len(inventory.items):
                item = inventory.items[i]
                caption.text = f"{i+1}. {item.name}"
                caption.fill_color = mcrfpy.Color(180, 180, 180)
            else:
                caption.text = f"{i+1}. ---"
                caption.fill_color = mcrfpy.Color(80, 80, 80)

# =============================================================================
# Global State
# =============================================================================

entity_data: dict[mcrfpy.Entity, Fighter] = {}
item_data: dict[mcrfpy.Entity, Item] = {}

player: Optional[mcrfpy.Entity] = None
player_inventory: Optional[Inventory] = None
grid: Optional[mcrfpy.Grid] = None
fov_layer = None
texture: Optional[mcrfpy.Texture] = None
game_over: bool = False
dungeon_level: int = 1

# UI components
message_log: Optional[MessageLog] = None
health_bar: Optional[HealthBar] = None
inventory_panel: Optional[InventoryPanel] = None

# =============================================================================
# Room Class
# =============================================================================

class RectangularRoom:
    """A rectangular room with its position and size."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    @property
    def inner(self) -> tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: "RectangularRoom") -> bool:
        return (
            self.x1 <= other.x2 and
            self.x2 >= other.x1 and
            self.y1 <= other.y2 and
            self.y2 >= other.y1
        )

# =============================================================================
# Exploration Tracking
# =============================================================================

explored: list[list[bool]] = []

def init_explored() -> None:
    global explored
    explored = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def mark_explored(x: int, y: int) -> None:
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        explored[y][x] = True

def is_explored(x: int, y: int) -> bool:
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        return explored[y][x]
    return False

# =============================================================================
# Dungeon Generation
# =============================================================================

def fill_with_walls(target_grid: mcrfpy.Grid) -> None:
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell = target_grid.at(x, y)
            cell.tilesprite = SPRITE_WALL
            cell.walkable = False
            cell.transparent = False

def carve_room(target_grid: mcrfpy.Grid, room: RectangularRoom) -> None:
    inner_x, inner_y = room.inner
    for y in range(inner_y.start, inner_y.stop):
        for x in range(inner_x.start, inner_x.stop):
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                cell = target_grid.at(x, y)
                cell.tilesprite = SPRITE_FLOOR
                cell.walkable = True
                cell.transparent = True

def carve_tunnel_horizontal(target_grid: mcrfpy.Grid, x1: int, x2: int, y: int) -> None:
    for x in range(min(x1, x2), max(x1, x2) + 1):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            cell = target_grid.at(x, y)
            cell.tilesprite = SPRITE_FLOOR
            cell.walkable = True
            cell.transparent = True

def carve_tunnel_vertical(target_grid: mcrfpy.Grid, y1: int, y2: int, x: int) -> None:
    for y in range(min(y1, y2), max(y1, y2) + 1):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            cell = target_grid.at(x, y)
            cell.tilesprite = SPRITE_FLOOR
            cell.walkable = True
            cell.transparent = True

def carve_l_tunnel(
    target_grid: mcrfpy.Grid,
    start: tuple[int, int],
    end: tuple[int, int]
) -> None:
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        carve_tunnel_horizontal(target_grid, x1, x2, y1)
        carve_tunnel_vertical(target_grid, y1, y2, x2)
    else:
        carve_tunnel_vertical(target_grid, y1, y2, x1)
        carve_tunnel_horizontal(target_grid, x1, x2, y2)

# =============================================================================
# Entity Management
# =============================================================================

def spawn_enemy(target_grid: mcrfpy.Grid, x: int, y: int, enemy_type: str, tex: mcrfpy.Texture) -> mcrfpy.Entity:
    template = ENEMY_TEMPLATES[enemy_type]

    enemy = mcrfpy.Entity(
        grid_pos=(x, y),
        texture=tex,
        sprite_index=template["sprite"]
    )
    enemy.visible = False

    target_grid.entities.append(enemy)

    entity_data[enemy] = Fighter(
        hp=template["hp"],
        max_hp=template["hp"],
        attack=template["attack"],
        defense=template["defense"],
        name=enemy_type.capitalize(),
        is_player=False
    )

    return enemy

def spawn_enemies_in_room(target_grid: mcrfpy.Grid, room: RectangularRoom, tex: mcrfpy.Texture) -> None:
    num_enemies = random.randint(0, MAX_ENEMIES_PER_ROOM)

    for _ in range(num_enemies):
        inner_x, inner_y = room.inner
        x = random.randint(inner_x.start, inner_x.stop - 1)
        y = random.randint(inner_y.start, inner_y.stop - 1)

        if is_position_occupied(target_grid, x, y):
            continue

        roll = random.random()
        if roll < 0.6:
            enemy_type = "goblin"
        elif roll < 0.9:
            enemy_type = "orc"
        else:
            enemy_type = "troll"

        spawn_enemy(target_grid, x, y, enemy_type, tex)

# =============================================================================
# Item Management
# =============================================================================

def spawn_item(target_grid: mcrfpy.Grid, x: int, y: int, item_type: str, tex: mcrfpy.Texture) -> mcrfpy.Entity:
    """Spawn an item at the given position.

    Args:
        target_grid: The game grid
        x: X position in tiles
        y: Y position in tiles
        item_type: Type of item to spawn
        tex: The texture to use

    Returns:
        The created item entity
    """
    template = ITEM_TEMPLATES[item_type]

    item_entity = mcrfpy.Entity(
        grid_pos=(x, y),
        texture=tex,
        sprite_index=template["sprite"]
    )
    item_entity.visible = False

    target_grid.entities.append(item_entity)

    # Create Item data
    item_data[item_entity] = Item(
        name=template["name"],
        item_type=template["item_type"],
        heal_amount=template.get("heal_amount", 0)
    )

    return item_entity

def spawn_items_in_room(target_grid: mcrfpy.Grid, room: RectangularRoom, tex: mcrfpy.Texture) -> None:
    """Spawn random items in a room.

    Args:
        target_grid: The game grid
        room: The room to spawn items in
        tex: The texture to use
    """
    num_items = random.randint(0, MAX_ITEMS_PER_ROOM)

    for _ in range(num_items):
        inner_x, inner_y = room.inner
        x = random.randint(inner_x.start, inner_x.stop - 1)
        y = random.randint(inner_y.start, inner_y.stop - 1)

        # Check if position is blocked by entity or item
        if is_position_occupied(target_grid, x, y):
            continue

        # For now, only spawn health potions
        spawn_item(target_grid, x, y, "health_potion", tex)

def get_item_at(target_grid: mcrfpy.Grid, x: int, y: int) -> Optional[mcrfpy.Entity]:
    """Get an item entity at the given position.

    Args:
        target_grid: The game grid
        x: X position to check
        y: Y position to check

    Returns:
        The item entity, or None if no item at position
    """
    for entity in target_grid.entities:
        if entity in item_data:
            if int(entity.x) == x and int(entity.y) == y:
                return entity
    return None

def pickup_item() -> bool:
    """Try to pick up an item at the player's position.

    Returns:
        True if an item was picked up, False otherwise
    """
    global player, player_inventory, grid

    px, py = int(player.x), int(player.y)
    item_entity = get_item_at(grid, px, py)

    if item_entity is None:
        message_log.add("There is nothing to pick up here.", COLOR_INVALID)
        return False

    if player_inventory.is_full():
        message_log.add("Your inventory is full!", COLOR_WARNING)
        return False

    # Get the item data
    item = item_data.get(item_entity)
    if item is None:
        return False

    # Add to inventory
    player_inventory.add(item)

    # Remove from ground
    remove_item_entity(grid, item_entity)

    message_log.add(f"You pick up the {item.name}.", COLOR_PICKUP)

    update_ui()
    return True

def use_item(index: int) -> bool:
    """Use an item from the inventory.

    Args:
        index: The inventory index of the item to use

    Returns:
        True if an item was used, False otherwise
    """
    global player, player_inventory

    item = player_inventory.get(index)
    if item is None:
        message_log.add("Invalid item selection.", COLOR_INVALID)
        return False

    # Handle different item types
    if item.item_type == "health_potion":
        fighter = entity_data.get(player)
        if fighter is None:
            return False

        if fighter.hp >= fighter.max_hp:
            message_log.add("You are already at full health!", COLOR_WARNING)
            return False

        # Apply healing
        actual_heal = fighter.heal(item.heal_amount)

        # Remove the item from inventory
        player_inventory.remove(index)

        message_log.add(f"You drink the {item.name} and recover {actual_heal} HP!", COLOR_HEAL)

        update_ui()
        return True

    message_log.add(f"You cannot use the {item.name}.", COLOR_INVALID)
    return False

def remove_item_entity(target_grid: mcrfpy.Grid, entity: mcrfpy.Entity) -> None:
    """Remove an item entity from the grid and item_data."""
    for i, e in enumerate(target_grid.entities):
        if e == entity:
            target_grid.entities.remove(i)
            break

    if entity in item_data:
        del item_data[entity]

# =============================================================================
# Position Checking
# =============================================================================

def is_position_occupied(target_grid: mcrfpy.Grid, x: int, y: int) -> bool:
    """Check if a position has any entity (enemy, item, or player).

    Args:
        target_grid: The game grid
        x: X position to check
        y: Y position to check

    Returns:
        True if position is occupied, False otherwise
    """
    for entity in target_grid.entities:
        if int(entity.x) == x and int(entity.y) == y:
            return True
    return False

def get_blocking_entity_at(target_grid: mcrfpy.Grid, x: int, y: int, exclude: mcrfpy.Entity = None) -> Optional[mcrfpy.Entity]:
    """Get any living entity that blocks movement at the given position."""
    for entity in target_grid.entities:
        if entity == exclude:
            continue
        if int(entity.x) == x and int(entity.y) == y:
            # Only fighters block movement
            if entity in entity_data and entity_data[entity].is_alive:
                return entity
    return None

def remove_entity(target_grid: mcrfpy.Grid, entity: mcrfpy.Entity) -> None:
    for i, e in enumerate(target_grid.entities):
        if e == entity:
            target_grid.entities.remove(i)
            break
    if entity in entity_data:
        del entity_data[entity]

def clear_all_entities(target_grid: mcrfpy.Grid) -> None:
    """Remove all entities (enemies and items) except the player."""
    global entity_data, item_data

    entities_to_remove = []
    for entity in target_grid.entities:
        if entity in entity_data and not entity_data[entity].is_player:
            entities_to_remove.append(entity)
        elif entity in item_data:
            entities_to_remove.append(entity)

    for entity in entities_to_remove:
        if entity in entity_data:
            del entity_data[entity]
        if entity in item_data:
            del item_data[entity]

        for i, e in enumerate(target_grid.entities):
            if e == entity:
                target_grid.entities.remove(i)
                break

# =============================================================================
# Combat System
# =============================================================================

def calculate_damage(attacker: Fighter, defender: Fighter) -> int:
    return max(0, attacker.attack - defender.defense)

def perform_attack(attacker_entity: mcrfpy.Entity, defender_entity: mcrfpy.Entity) -> None:
    global game_over

    attacker = entity_data.get(attacker_entity)
    defender = entity_data.get(defender_entity)

    if attacker is None or defender is None:
        return

    damage = calculate_damage(attacker, defender)
    defender.take_damage(damage)

    if damage > 0:
        if attacker.is_player:
            message_log.add(
                f"You hit the {defender.name} for {damage} damage!",
                COLOR_PLAYER_ATTACK
            )
        else:
            message_log.add(
                f"The {attacker.name} hits you for {damage} damage!",
                COLOR_ENEMY_ATTACK
            )
    else:
        if attacker.is_player:
            message_log.add(
                f"You hit the {defender.name} but deal no damage.",
                mcrfpy.Color(150, 150, 150)
            )
        else:
            message_log.add(
                f"The {attacker.name} hits but deals no damage.",
                mcrfpy.Color(150, 150, 200)
            )

    if not defender.is_alive:
        handle_death(defender_entity, defender)

    update_ui()

def handle_death(entity: mcrfpy.Entity, fighter: Fighter) -> None:
    global game_over, grid

    if fighter.is_player:
        message_log.add("You have died!", COLOR_PLAYER_DEATH)
        message_log.add("Press R to restart or Escape to quit.", COLOR_INFO)
        game_over = True
        entity.sprite_index = SPRITE_CORPSE
    else:
        message_log.add(f"The {fighter.name} dies!", COLOR_ENEMY_DEATH)
        remove_entity(grid, entity)

# =============================================================================
# Field of View
# =============================================================================

def update_entity_visibility(target_grid: mcrfpy.Grid) -> None:
    global player

    for entity in target_grid.entities:
        if entity == player:
            entity.visible = True
            continue

        ex, ey = int(entity.x), int(entity.y)
        entity.visible = target_grid.is_in_fov(ex, ey)

def update_fov(target_grid: mcrfpy.Grid, target_fov_layer, player_x: int, player_y: int) -> None:
    target_grid.compute_fov(player_x, player_y, FOV_RADIUS, mcrfpy.FOV.SHADOW)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if target_grid.is_in_fov(x, y):
                mark_explored(x, y)
                target_fov_layer.set(x, y, COLOR_VISIBLE)
            elif is_explored(x, y):
                target_fov_layer.set(x, y, COLOR_DISCOVERED)
            else:
                target_fov_layer.set(x, y, COLOR_UNKNOWN)

    update_entity_visibility(target_grid)

# =============================================================================
# Movement and Actions
# =============================================================================

def can_move_to(target_grid: mcrfpy.Grid, x: int, y: int, mover: mcrfpy.Entity = None) -> bool:
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        return False

    if not target_grid.at(x, y).walkable:
        return False

    blocker = get_blocking_entity_at(target_grid, x, y, exclude=mover)
    if blocker is not None:
        return False

    return True

def try_move_or_attack(dx: int, dy: int) -> None:
    global player, grid, fov_layer, game_over

    if game_over:
        return

    px, py = int(player.x), int(player.y)
    target_x = px + dx
    target_y = py + dy

    if target_x < 0 or target_x >= GRID_WIDTH or target_y < 0 or target_y >= GRID_HEIGHT:
        return

    blocker = get_blocking_entity_at(grid, target_x, target_y, exclude=player)

    if blocker is not None:
        perform_attack(player, blocker)
        enemy_turn()
    elif grid.at(target_x, target_y).walkable:
        player.x = target_x
        player.y = target_y
        update_fov(grid, fov_layer, target_x, target_y)
        enemy_turn()

    update_ui()

# =============================================================================
# Enemy AI
# =============================================================================

def enemy_turn() -> None:
    global player, grid, game_over

    if game_over:
        return

    player_x, player_y = int(player.x), int(player.y)

    enemies = []
    for entity in grid.entities:
        if entity == player:
            continue
        if entity in entity_data and entity_data[entity].is_alive:
            enemies.append(entity)

    for enemy in enemies:
        fighter = entity_data.get(enemy)
        if fighter is None or not fighter.is_alive:
            continue

        ex, ey = int(enemy.x), int(enemy.y)

        if not grid.is_in_fov(ex, ey):
            continue

        dx = player_x - ex
        dy = player_y - ey

        if abs(dx) <= 1 and abs(dy) <= 1 and (dx != 0 or dy != 0):
            perform_attack(enemy, player)
        else:
            move_toward_player(enemy, ex, ey, player_x, player_y)

def move_toward_player(enemy: mcrfpy.Entity, ex: int, ey: int, px: int, py: int) -> None:
    global grid

    dx = 0
    dy = 0

    if px < ex:
        dx = -1
    elif px > ex:
        dx = 1

    if py < ey:
        dy = -1
    elif py > ey:
        dy = 1

    new_x = ex + dx
    new_y = ey + dy

    if can_move_to(grid, new_x, new_y, enemy):
        enemy.x = new_x
        enemy.y = new_y
    elif dx != 0 and can_move_to(grid, ex + dx, ey, enemy):
        enemy.x = ex + dx
    elif dy != 0 and can_move_to(grid, ex, ey + dy, enemy):
        enemy.y = ey + dy

# =============================================================================
# UI Updates
# =============================================================================

def update_ui() -> None:
    """Update all UI components."""
    global player, health_bar, inventory_panel, player_inventory

    if player in entity_data:
        fighter = entity_data[player]
        health_bar.update(fighter.hp, fighter.max_hp)

    if player_inventory:
        inventory_panel.update(player_inventory)

# =============================================================================
# Game Setup
# =============================================================================

# Create the scene
scene = mcrfpy.Scene("game")

# Load texture
texture = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)

# Create the grid
grid = mcrfpy.Grid(
    pos=(20, GAME_AREA_Y),
    size=(700, GAME_AREA_HEIGHT - 20),
    grid_size=(GRID_WIDTH, GRID_HEIGHT),
    texture=texture
)
grid.zoom = 1.0

# Generate initial dungeon
fill_with_walls(grid)
init_explored()

rooms: list[RectangularRoom] = []

for _ in range(MAX_ROOMS):
    room_width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    room_height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    x = random.randint(1, GRID_WIDTH - room_width - 2)
    y = random.randint(1, GRID_HEIGHT - room_height - 2)

    new_room = RectangularRoom(x, y, room_width, room_height)

    overlaps = False
    for other_room in rooms:
        if new_room.intersects(other_room):
            overlaps = True
            break

    if overlaps:
        continue

    carve_room(grid, new_room)

    if rooms:
        carve_l_tunnel(grid, new_room.center, rooms[-1].center)

    rooms.append(new_room)

# Get player starting position
if rooms:
    player_start_x, player_start_y = rooms[0].center
else:
    player_start_x, player_start_y = GRID_WIDTH // 2, GRID_HEIGHT // 2

# Add FOV layer
fov_layer = grid.add_layer("color", z_index=-1)
for y in range(GRID_HEIGHT):
    for x in range(GRID_WIDTH):
        fov_layer.set(x, y, COLOR_UNKNOWN)

# Create the player
player = mcrfpy.Entity(
    grid_pos=(player_start_x, player_start_y),
    texture=texture,
    sprite_index=SPRITE_PLAYER
)
grid.entities.append(player)

entity_data[player] = Fighter(
    hp=30,
    max_hp=30,
    attack=5,
    defense=2,
    name="Player",
    is_player=True
)

# Create player inventory
player_inventory = Inventory(capacity=10)

# Spawn enemies and items
for i, room in enumerate(rooms):
    if i == 0:
        continue  # Skip player's starting room
    spawn_enemies_in_room(grid, room, texture)
    spawn_items_in_room(grid, room, texture)

# Calculate initial FOV
update_fov(grid, fov_layer, player_start_x, player_start_y)

# Add grid to scene
scene.children.append(grid)

# =============================================================================
# Create UI Elements
# =============================================================================

# Title bar
title = mcrfpy.Caption(
    pos=(20, 10),
    text="Part 8: Items and Inventory"
)
title.fill_color = mcrfpy.Color(255, 255, 255)
title.font_size = 24
scene.children.append(title)

# Instructions
instructions = mcrfpy.Caption(
    pos=(300, 15),
    text="WASD: Move | G: Pickup | 1-5: Use item | R: Restart"
)
instructions.fill_color = mcrfpy.Color(180, 180, 180)
instructions.font_size = 14
scene.children.append(instructions)

# Health Bar
health_bar = HealthBar(
    x=730,
    y=10,
    width=280,
    height=30
)
health_bar.add_to_scene(scene)

# Inventory Panel
inventory_panel = InventoryPanel(
    x=730,
    y=GAME_AREA_Y,
    width=280,
    height=150
)
inventory_panel.add_to_scene(scene)

# Message Log
message_log = MessageLog(
    x=20,
    y=768 - UI_BOTTOM_HEIGHT + 10,
    width=990,
    height=UI_BOTTOM_HEIGHT - 20,
    max_messages=6
)
message_log.add_to_scene(scene)

# Initial messages
message_log.add("Welcome to the dungeon!", COLOR_INFO)
message_log.add("Find potions to heal. Press G to pick up items.", COLOR_INFO)

# Initialize UI
update_ui()

# =============================================================================
# Input Handling
# =============================================================================

def restart_game() -> None:
    """Restart the game with a new dungeon."""
    global player, grid, fov_layer, game_over, entity_data, item_data, rooms
    global player_inventory

    game_over = False

    entity_data.clear()
    item_data.clear()

    while len(grid.entities) > 0:
        grid.entities.remove(0)

    fill_with_walls(grid)
    init_explored()
    message_log.clear()

    rooms = []

    for _ in range(MAX_ROOMS):
        room_width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        room_height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(1, GRID_WIDTH - room_width - 2)
        y = random.randint(1, GRID_HEIGHT - room_height - 2)

        new_room = RectangularRoom(x, y, room_width, room_height)

        overlaps = False
        for other_room in rooms:
            if new_room.intersects(other_room):
                overlaps = True
                break

        if overlaps:
            continue

        carve_room(grid, new_room)

        if rooms:
            carve_l_tunnel(grid, new_room.center, rooms[-1].center)

        rooms.append(new_room)

    if rooms:
        new_x, new_y = rooms[0].center
    else:
        new_x, new_y = GRID_WIDTH // 2, GRID_HEIGHT // 2

    player = mcrfpy.Entity(
        grid_pos=(new_x, new_y),
        texture=texture,
        sprite_index=SPRITE_PLAYER
    )
    grid.entities.append(player)

    entity_data[player] = Fighter(
        hp=30,
        max_hp=30,
        attack=5,
        defense=2,
        name="Player",
        is_player=True
    )

    # Reset inventory
    player_inventory = Inventory(capacity=10)

    for i, room in enumerate(rooms):
        if i == 0:
            continue
        spawn_enemies_in_room(grid, room, texture)
        spawn_items_in_room(grid, room, texture)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            fov_layer.set(x, y, COLOR_UNKNOWN)

    update_fov(grid, fov_layer, new_x, new_y)

    message_log.add("A new adventure begins!", COLOR_INFO)

    update_ui()

def handle_keys(key: str, action: str) -> None:
    global game_over

    if action != "start":
        return

    if key == "R":
        restart_game()
        return

    if key == "Escape":
        mcrfpy.exit()
        return

    if game_over:
        return

    # Movement
    if key == "W" or key == "Up":
        try_move_or_attack(0, -1)
    elif key == "S" or key == "Down":
        try_move_or_attack(0, 1)
    elif key == "A" or key == "Left":
        try_move_or_attack(-1, 0)
    elif key == "D" or key == "Right":
        try_move_or_attack(1, 0)
    # Pickup
    elif key == "G" or key == ",":
        pickup_item()
    # Use items by number key
    elif key in ["1", "2", "3", "4", "5"]:
        index = int(key) - 1
        if use_item(index):
            enemy_turn()  # Using an item takes a turn
            update_ui()

scene.on_key = handle_keys

# =============================================================================
# Start the Game
# =============================================================================

scene.activate()
print("Part 8 loaded! Pick up health potions with G, use with 1-5.")
```

## Understanding the Code

### The Item Dataclass

```python
@dataclass
class Item:
    name: str
    item_type: str
    heal_amount: int = 0

    def describe(self) -> str:
        if self.item_type == "health_potion":
            return f"Restores {self.heal_amount} HP"
        return "Unknown item"
```

Items are simple data containers with:
- A display name
- A type identifier (for handling effects)
- Effect-specific data (like heal amount)

### The Inventory Class

```python
@dataclass
class Inventory:
    capacity: int = 10
    items: list = field(default_factory=list)

    def add(self, item: Item) -> bool:
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def remove(self, index: int) -> Optional[Item]:
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None
```

The inventory:
- Has a fixed capacity
- Returns success/failure when adding items
- Validates indices when removing items

### Spawning Items

```python
def spawn_item(target_grid, x, y, item_type, tex):
    template = ITEM_TEMPLATES[item_type]

    item_entity = mcrfpy.Entity(
        grid_pos=(x, y),
        texture=tex,
        sprite_index=template["sprite"]
    )
    item_entity.visible = False

    target_grid.entities.append(item_entity)

    item_data[item_entity] = Item(
        name=template["name"],
        item_type=template["item_type"],
        heal_amount=template.get("heal_amount", 0)
    )

    return item_entity
```

Items use the same Entity system as enemies but are stored in a separate `item_data` dictionary. This lets us distinguish items from enemies when checking positions.

### Picking Up Items

```python
def pickup_item() -> bool:
    px, py = int(player.x), int(player.y)
    item_entity = get_item_at(grid, px, py)

    if item_entity is None:
        message_log.add("There is nothing to pick up here.", COLOR_INVALID)
        return False

    if player_inventory.is_full():
        message_log.add("Your inventory is full!", COLOR_WARNING)
        return False

    item = item_data.get(item_entity)
    player_inventory.add(item)
    remove_item_entity(grid, item_entity)

    message_log.add(f"You pick up the {item.name}.", COLOR_PICKUP)
    return True
```

The pickup process:
1. Check if there is an item at the player's position
2. Check if inventory has space
3. Add item to inventory
4. Remove the entity from the ground
5. Show feedback message

### Using Items

```python
def use_item(index: int) -> bool:
    item = player_inventory.get(index)
    if item is None:
        message_log.add("Invalid item selection.", COLOR_INVALID)
        return False

    if item.item_type == "health_potion":
        fighter = entity_data.get(player)

        if fighter.hp >= fighter.max_hp:
            message_log.add("You are already at full health!", COLOR_WARNING)
            return False

        actual_heal = fighter.heal(item.heal_amount)
        player_inventory.remove(index)

        message_log.add(f"You drink the {item.name} and recover {actual_heal} HP!", COLOR_HEAL)
        return True

    return False
```

Using items:
1. Validate the index
2. Check item type to determine effect
3. For health potions, check if healing is needed
4. Apply the effect
5. Remove the item from inventory
6. Report the result

### Inventory Panel UI

```python
class InventoryPanel:
    def __init__(self, x, y, width, height):
        self.frame = mcrfpy.Frame(...)
        self.title = mcrfpy.Caption(text="Inventory (G:pickup, U:use)")

        for i in range(5):
            caption = mcrfpy.Caption(
                pos=(x + 10, y + 25 + i * 18),
                text=""
            )
            self.captions.append(caption)

    def update(self, inventory: Inventory) -> None:
        for i, caption in enumerate(self.captions):
            if i < len(inventory.items):
                item = inventory.items[i]
                caption.text = f"{i+1}. {item.name}"
            else:
                caption.text = f"{i+1}. ---"
```

The inventory panel shows numbered slots. Empty slots display "---" to indicate they are available.

### Separating Items from Enemies

```python
# Two separate dictionaries
entity_data: dict[mcrfpy.Entity, Fighter] = {}  # Enemies and player
item_data: dict[mcrfpy.Entity, Item] = {}        # Items on ground

def get_blocking_entity_at(target_grid, x, y, exclude=None):
    for entity in target_grid.entities:
        if entity == exclude:
            continue
        if int(entity.x) == x and int(entity.y) == y:
            # Only fighters block movement
            if entity in entity_data and entity_data[entity].is_alive:
                return entity
    return None
```

Items do not block movement - you can walk over them. Only entities in `entity_data` (with `is_alive`) block movement.

### Using Items Takes a Turn

```python
elif key in ["1", "2", "3", "4", "5"]:
    index = int(key) - 1
    if use_item(index):
        enemy_turn()  # Using an item takes a turn
```

Using items consumes the player's turn, giving enemies a chance to act. This creates tactical decisions about when to heal.

## Item Templates

```python
ITEM_TEMPLATES = {
    "health_potion": {
        "name": "Health Potion",
        "sprite": SPRITE_POTION,
        "item_type": "health_potion",
        "heal_amount": 10
    }
}
```

Using templates makes it easy to add new item types:

```python
# Example: Add a greater health potion
"greater_health_potion": {
    "name": "Greater Health Potion",
    "sprite": SPRITE_POTION,
    "item_type": "health_potion",
    "heal_amount": 20
}
```

## Try This

1. **Add more item types**: Create mana potions, scrolls, or food

2. **Rare items**: Make some items spawn less frequently:
   ```python
   if random.random() < 0.8:
       spawn_item(..., "health_potion", ...)
   else:
       spawn_item(..., "greater_health_potion", ...)
   ```

3. **Item stacking**: Combine identical items in inventory:
   ```python
   def add(self, item):
       # Find existing stack
       for existing in self.items:
           if existing.name == item.name:
               existing.quantity += 1
               return True
       # Create new stack
       item.quantity = 1
       self.items.append(item)
   ```

4. **Drop items**: Allow dropping items from inventory back to ground

5. **Examine items**: Show item descriptions when hovering

### Challenge: Scroll of Lightning

Add a scroll that damages nearby enemies:

```python
ITEM_TEMPLATES["scroll_of_lightning"] = {
    "name": "Scroll of Lightning",
    "sprite": 63,  # '?'
    "item_type": "scroll_lightning",
    "damage": 8,
    "range": 5
}

def use_scroll_lightning(damage, range_limit):
    # Find closest enemy in range
    closest = None
    closest_dist = range_limit + 1

    for entity in grid.entities:
        if entity in entity_data and not entity_data[entity].is_player:
            dist = abs(int(entity.x) - int(player.x)) + abs(int(entity.y) - int(player.y))
            if dist < closest_dist and grid.is_in_fov(int(entity.x), int(entity.y)):
                closest = entity
                closest_dist = dist

    if closest:
        entity_data[closest].take_damage(damage)
        message_log.add(f"Lightning strikes the {entity_data[closest].name}!", COLOR_WARNING)
        return True
    else:
        message_log.add("No enemies in range!", COLOR_INVALID)
        return False
```

### Challenge: Item Identification

Add unidentified items that reveal their true nature when used:

```python
@dataclass
class Item:
    name: str
    item_type: str
    identified: bool = False
    unidentified_name: str = "Unknown Potion"

    @property
    def display_name(self) -> str:
        return self.name if self.identified else self.unidentified_name
```

## Common Mistakes

1. **Forgetting to remove item entity**: When picked up, remove from both grid and `item_data`

2. **Not validating inventory space**: Always check `is_full()` before adding

3. **Using wrong index**: Remember inventory indices are 0-based, but display is 1-based

4. **Items blocking movement**: Items should not be in `entity_data` or block movement

5. **Not updating UI**: Call `update_ui()` after inventory changes

## The Item Data Flow

```
Item on Ground                    Item in Inventory
     |                                  |
     v                                  v
Entity in grid.entities           Item in player_inventory.items
     +                                  |
item_data[entity] = Item               (no entity)
     |                                  |
     v                                  v
pickup_item():                    use_item():
  - Get Item from item_data         - Get Item from inventory
  - Add to inventory                - Apply effect
  - Remove entity                   - Remove from inventory
  - Delete from item_data           - (Item destroyed)
```

## What is Next

In Part 9, we will add ranged combat with a targeting system. You will learn:

- Implementing targeting mode
- Creating a visual targeting cursor
- Selecting targets with keyboard
- Line-of-sight validation
- Ranged attack mechanics

[Continue to Part 9: Ranged Combat and Targeting](part_09_ranged.md)

---

## Complete Code Reference

The complete code is shown above. Key additions from Part 7:

- **Item dataclass**: Simple data structure for item properties
- **Inventory class**: Container with add/remove/capacity
- **item_data dictionary**: Maps item entities to Item data
- **spawn_item()**: Creates items on the ground
- **pickup_item()**: Transfers items from ground to inventory
- **use_item()**: Applies item effects and consumes items
- **InventoryPanel**: UI component showing inventory contents
- **Number key handling**: Use items by pressing 1-5
