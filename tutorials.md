# McRogueFace Tutorials

**Make 2D games with Python** - No C++ required!

---

[**Source Code**](https://github.com/jmccardle/McRogueFace) • [**Downloads**](https://github.com/jmccardle/McRogueFace/releases) • [**Quickstart**](https://mcrogueface.github.io/quickstart) • **[Tutorials](https://mcrogueface.github.io/tutorials)** • [**API Reference**](https://mcrogueface.github.io/api) • [**Cookbook**](https://mcrogueface.github.io/cookbook) • [**C++ Extensions**](https://mcrogueface.github.io/extending-cpp)

---

These tutorials will guide you through building specific game features using McRogueFace.

## Table of Contents

1. [Creating a Roguelike Dungeon](#creating-a-roguelike-dungeon)
2. [Implementing Player Movement](#implementing-player-movement)
3. [Adding Combat System](#adding-combat-system)
4. [Building an Inventory System](#building-an-inventory-system)
5. [Creating Animated Sprites](#creating-animated-sprites)
6. [Procedural Level Generation](#procedural-level-generation)
7. [Save and Load System](#save-and-load-system)
8. [Creating Particle Effects](#creating-particle-effects)

---

## Creating a Roguelike Dungeon

Learn how to create a classic roguelike dungeon with rooms, corridors, and fog of war.

### Setting Up the Grid

```python
import mcrfpy

# Create the game scene
mcrfpy.createScene("dungeon")

# Load dungeon tileset
tileset = mcrfpy.Texture("assets/dungeon_tiles.png", 16, 16)

# Create a 50x50 dungeon grid
dungeon = mcrfpy.Grid(0, 0, 50, 50, tileset, 16, 16)

# Define tile types
WALL = 0
FLOOR = 1
DOOR = 2
STAIRS = 3

# Initialize with walls
for x in range(50):
    for y in range(50):
        dungeon.set_tile(x, y, WALL)
```

### Generating Rooms

```python
import random

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def intersects(self, other):
        return (self.x <= other.x + other.width and
                self.x + self.width >= other.x and
                self.y <= other.y + other.height and
                self.y + self.height >= other.y)

def generate_dungeon(grid, num_rooms=10):
    rooms = []
    
    for _ in range(num_rooms):
        # Random room size
        w = random.randint(4, 10)
        h = random.randint(4, 10)
        x = random.randint(1, 48 - w)
        y = random.randint(1, 48 - h)
        
        new_room = Room(x, y, w, h)
        
        # Check if it overlaps with existing rooms
        if not any(new_room.intersects(room) for room in rooms):
            # Carve out the room
            for rx in range(x, x + w):
                for ry in range(y, y + h):
                    grid.set_tile(rx, ry, FLOOR)
            
            # Connect to previous room with corridor
            if rooms:
                prev_center = rooms[-1].center()
                new_center = new_room.center()
                
                # Horizontal then vertical
                for cx in range(min(prev_center[0], new_center[0]), 
                              max(prev_center[0], new_center[0]) + 1):
                    grid.set_tile(cx, prev_center[1], FLOOR)
                
                for cy in range(min(prev_center[1], new_center[1]),
                              max(prev_center[1], new_center[1]) + 1):
                    grid.set_tile(new_center[0], cy, FLOOR)
            
            rooms.append(new_room)
    
    return rooms

# Generate the dungeon
rooms = generate_dungeon(dungeon)

# Place stairs in the last room
if rooms:
    last_room = rooms[-1]
    cx, cy = last_room.center()
    dungeon.set_tile(cx, cy, STAIRS)
```

### Adding Fog of War

```python
# Create a visibility grid
visibility = [[False for _ in range(50)] for _ in range(50)]
explored = [[False for _ in range(50)] for _ in range(50)]

def update_visibility(player_x, player_y, radius=8):
    # Simple circular visibility
    for x in range(max(0, player_x - radius), min(50, player_x + radius + 1)):
        for y in range(max(0, player_y - radius), min(50, player_y + radius + 1)):
            dist = ((x - player_x) ** 2 + (y - player_y) ** 2) ** 0.5
            if dist <= radius:
                visibility[x][y] = True
                explored[x][y] = True
            else:
                visibility[x][y] = False

def render_with_fog(grid):
    for x in range(50):
        for y in range(50):
            if visibility[x][y]:
                # Fully visible
                grid.set_tile_color(x, y, (255, 255, 255))
            elif explored[x][y]:
                # Previously seen, now in fog
                grid.set_tile_color(x, y, (100, 100, 100))
            else:
                # Never seen
                grid.set_tile_color(x, y, (0, 0, 0))
```

---

## Implementing Player Movement

Create smooth, responsive player movement with collision detection.

### Basic Player Entity

```python
class Player:
    def __init__(self, x, y):
        self.entity = mcrfpy.Entity(x, y)
        self.entity.texture = mcrfpy.Texture("assets/characters.png", 16, 16)
        self.entity.sprite_index = 0  # Player sprite
        
        # Add to a grid
        self.grid = None
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check collision with walls
        if self.can_move_to(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.entity.pos = (new_x, new_y)
            
            # Update visibility
            update_visibility(new_x, new_y)
    
    def can_move_to(self, x, y):
        if x < 0 or x >= 50 or y < 0 or y >= 50:
            return False
        
        # Check if tile is walkable
        tile = self.grid.get_tile(x, y)
        return tile in [FLOOR, DOOR, STAIRS]

# Create player
player = Player(25, 25)
dungeon.entities.append(player.entity)
player.grid = dungeon

# Keyboard handler
def handle_movement(key):
    if key == "w" or key == "Up":
        player.move(0, -1)
    elif key == "s" or key == "Down":
        player.move(0, 1)
    elif key == "a" or key == "Left":
        player.move(-1, 0)
    elif key == "d" or key == "Right":
        player.move(1, 0)

mcrfpy.keypressScene(handle_movement)
```

### Smooth Animation

```python
class AnimatedPlayer(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.target_x = x
        self.target_y = y
        self.move_speed = 0.2  # seconds per tile
        self.move_timer = 0
        self.is_moving = False
        
        # Animation frames
        self.walk_frames = [0, 1, 2, 1]  # Sprite indices
        self.frame_index = 0
        self.frame_timer = 0
    
    def move(self, dx, dy):
        if self.is_moving:
            return  # Already moving
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        if self.can_move_to(new_x, new_y):
            self.target_x = new_x
            self.target_y = new_y
            self.is_moving = True
            self.move_timer = 0
    
    def update(self, dt):
        if self.is_moving:
            self.move_timer += dt
            progress = min(self.move_timer / self.move_speed, 1.0)
            
            # Interpolate position
            display_x = self.x + (self.target_x - self.x) * progress
            display_y = self.y + (self.target_y - self.y) * progress
            self.entity.pos = (display_x, display_y)
            
            # Update animation
            self.frame_timer += dt
            if self.frame_timer >= 0.1:  # Change frame every 0.1s
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                self.entity.sprite_index = self.walk_frames[self.frame_index]
            
            # Check if movement complete
            if progress >= 1.0:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
                self.entity.sprite_index = self.walk_frames[0]  # Rest frame

# Game update loop
def update_game(runtime):
    # Calculate delta time (you'd track this properly in a real game)
    dt = 0.016  # Assume 60 FPS
    
    if hasattr(player, 'update'):
        player.update(dt)

mcrfpy.setTimer("update", update_game, 16)  # ~60 FPS
```

---

## Adding Combat System

Implement a turn-based combat system with attacks, damage, and enemy AI.

### Combat Components

```python
class Combatant:
    def __init__(self, hp, attack, defense):
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.is_alive = True
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
        
        return actual_damage
    
    def deal_damage(self):
        return self.attack + random.randint(-2, 2)

class Enemy:
    def __init__(self, x, y, sprite_index, hp=10, attack=3):
        self.entity = mcrfpy.Entity(x, y)
        self.entity.texture = mcrfpy.Texture("assets/characters.png", 16, 16)
        self.entity.sprite_index = sprite_index
        
        self.x = x
        self.y = y
        self.combat = Combatant(hp, attack, 1)
        
        # AI state
        self.target = None
        self.path = []
    
    def update(self, player, grid):
        if not self.combat.is_alive:
            return
        
        # Simple AI: move towards player if in range
        dist = abs(self.x - player.x) + abs(self.y - player.y)
        
        if dist <= 1:
            # Adjacent to player - attack!
            damage = self.combat.deal_damage()
            actual = player.combat.take_damage(damage)
            show_damage(player.x, player.y, actual)
        
        elif dist <= 10:
            # Chase player
            dx = 0 if self.x == player.x else (1 if player.x > self.x else -1)
            dy = 0 if self.y == player.y else (1 if player.y > self.y else -1)
            
            # Try to move
            new_x, new_y = self.x + dx, self.y + dy
            if can_move_to(new_x, new_y, grid):
                self.x = new_x
                self.y = new_y
                self.entity.pos = (new_x, new_y)

# Combat UI
def create_health_bar(x, y, current, maximum):
    bar_width = 50
    bar_height = 6
    
    # Background
    bg = mcrfpy.Frame(x, y, bar_width, bar_height)
    bg.bgcolor = (50, 0, 0)
    
    # Health fill
    fill_width = int(bar_width * current / maximum)
    if fill_width > 0:
        fill = mcrfpy.Frame(x, y, fill_width, bar_height)
        fill.bgcolor = (200, 0, 0) if current > maximum * 0.3 else (200, 200, 0)
        mcrfpy.sceneUI("game").append(fill)
    
    mcrfpy.sceneUI("game").append(bg)
    
    # Text
    text = mcrfpy.Caption(x + bar_width + 5, y, f"{current}/{maximum}")
    text.font = mcrfpy.default_font
    text.font_size = 12
    text.font_color = (255, 255, 255)
    mcrfpy.sceneUI("game").append(text)

# Damage numbers
damage_numbers = []

def show_damage(x, y, amount):
    text = mcrfpy.Caption(x * 16 + 8, y * 16, str(amount))
    text.font = mcrfpy.default_font
    text.font_size = 16
    text.font_color = (255, 100, 100) if amount > 0 else (100, 255, 100)
    
    damage_numbers.append({
        'text': text,
        'timer': 0,
        'y_offset': 0
    })
    
    mcrfpy.sceneUI("game").append(text)

def update_damage_numbers(dt):
    for damage in damage_numbers[:]:
        damage['timer'] += dt
        damage['y_offset'] -= 30 * dt  # Float upward
        
        # Update position
        damage['text'].pos = (
            damage['text'].pos[0],
            damage['text'].pos[1] + damage['y_offset']
        )
        
        # Fade out
        alpha = max(0, 1 - damage['timer'])
        color = damage['text'].font_color
        damage['text'].font_color = (color[0], color[1], color[2], int(255 * alpha))
        
        # Remove after 1 second
        if damage['timer'] >= 1.0:
            mcrfpy.sceneUI("game").remove(damage['text'])
            damage_numbers.remove(damage)
```

---

## Building an Inventory System

Create a flexible inventory system with equipment slots and item management.

### Item System

```python
class ItemType:
    WEAPON = 0
    ARMOR = 1
    CONSUMABLE = 2
    KEY = 3

class Item:
    def __init__(self, name, sprite_index, item_type, **stats):
        self.name = name
        self.sprite_index = sprite_index
        self.item_type = item_type
        self.stats = stats
        
        # Common stats
        self.damage = stats.get('damage', 0)
        self.defense = stats.get('defense', 0)
        self.healing = stats.get('healing', 0)
        self.stackable = stats.get('stackable', False)
        self.quantity = stats.get('quantity', 1)

# Define items
ITEMS = {
    'sword': Item("Iron Sword", 100, ItemType.WEAPON, damage=5),
    'shield': Item("Wooden Shield", 101, ItemType.ARMOR, defense=2),
    'potion': Item("Health Potion", 102, ItemType.CONSUMABLE, 
                   healing=20, stackable=True),
    'key': Item("Dungeon Key", 103, ItemType.KEY)
}

class Inventory:
    def __init__(self, size=20):
        self.size = size
        self.items = [None] * size
        self.equipment = {
            'weapon': None,
            'armor': None
        }
    
    def add_item(self, item):
        # Try to stack first
        if item.stackable:
            for i, slot in enumerate(self.items):
                if slot and slot.name == item.name:
                    slot.quantity += item.quantity
                    return True
        
        # Find empty slot
        for i, slot in enumerate(self.items):
            if slot is None:
                self.items[i] = item
                return True
        
        return False  # Inventory full
    
    def remove_item(self, index):
        if 0 <= index < self.size:
            item = self.items[index]
            self.items[index] = None
            return item
        return None
    
    def equip(self, index):
        item = self.items[index]
        if not item:
            return
        
        slot = None
        if item.item_type == ItemType.WEAPON:
            slot = 'weapon'
        elif item.item_type == ItemType.ARMOR:
            slot = 'armor'
        
        if slot:
            # Swap with currently equipped
            old_item = self.equipment[slot]
            self.equipment[slot] = item
            self.items[index] = old_item
    
    def use_item(self, index, player):
        item = self.items[index]
        if not item:
            return
        
        if item.item_type == ItemType.CONSUMABLE:
            if item.healing > 0:
                player.combat.hp = min(player.combat.max_hp, 
                                     player.combat.hp + item.healing)
            
            # Consume item
            item.quantity -= 1
            if item.quantity <= 0:
                self.items[index] = None
```

### Inventory UI

```python
class InventoryUI:
    def __init__(self, inventory):
        self.inventory = inventory
        self.visible = False
        self.selected_index = 0
        
        # UI elements
        self.frame = mcrfpy.Frame(200, 100, 400, 400)
        self.frame.bgcolor = (40, 40, 60)
        self.frame.outline = 2
        
        self.title = mcrfpy.Caption(400, 120, "Inventory")
        self.title.font = mcrfpy.default_font
        self.title.font_size = 24
        self.title.font_color = (255, 255, 255)
        self.title.centered = True
        
        self.slots = []
        self.slot_frames = []
        
        # Create inventory grid (5x4)
        for i in range(20):
            x = 220 + (i % 5) * 70
            y = 160 + (i // 5) * 70
            
            # Slot frame
            slot_frame = mcrfpy.Frame(x, y, 64, 64)
            slot_frame.bgcolor = (60, 60, 80)
            slot_frame.outline = 1
            self.slot_frames.append(slot_frame)
            
            # Item sprite
            sprite = mcrfpy.Sprite(x + 16, y + 16)
            sprite.texture = mcrfpy.Texture("assets/items.png", 32, 32)
            sprite.visible = False
            self.slots.append(sprite)
        
        # Equipment slots
        self.weapon_frame = mcrfpy.Frame(220, 450, 64, 64)
        self.weapon_frame.bgcolor = (80, 60, 60)
        self.weapon_frame.outline = 2
        
        self.armor_frame = mcrfpy.Frame(300, 450, 64, 64)
        self.armor_frame.bgcolor = (60, 80, 60)
        self.armor_frame.outline = 2
        
        # Item description
        self.description = mcrfpy.Caption(400, 530, "")
        self.description.font = mcrfpy.default_font
        self.description.font_size = 14
        self.description.font_color = (200, 200, 200)
        self.description.centered = True
    
    def toggle(self):
        self.visible = not self.visible
        self.update_display()
    
    def update_display(self):
        ui = mcrfpy.sceneUI("game")
        
        if self.visible:
            # Add all UI elements
            ui.append(self.frame)
            ui.append(self.title)
            
            for frame in self.slot_frames:
                ui.append(frame)
            
            # Update item sprites
            for i, item in enumerate(self.inventory.items):
                if item:
                    self.slots[i].sprite_index = item.sprite_index
                    self.slots[i].visible = True
                    ui.append(self.slots[i])
                else:
                    self.slots[i].visible = False
            
            ui.append(self.weapon_frame)
            ui.append(self.armor_frame)
            ui.append(self.description)
            
            # Highlight selected slot
            if 0 <= self.selected_index < 20:
                self.slot_frames[self.selected_index].outline_color = (255, 255, 0)
            
        else:
            # Remove all UI elements
            # (In practice, you'd track and remove specific elements)
            pass
    
    def handle_input(self, key):
        if not self.visible:
            return
        
        # Navigation
        if key == "Right":
            self.selected_index = (self.selected_index + 1) % 20
        elif key == "Left":
            self.selected_index = (self.selected_index - 1) % 20
        elif key == "Down":
            self.selected_index = (self.selected_index + 5) % 20
        elif key == "Up":
            self.selected_index = (self.selected_index - 5) % 20
        
        # Actions
        elif key == "Return":  # Use/Equip
            self.inventory.equip(self.selected_index)
        elif key == "Delete":  # Drop
            self.inventory.remove_item(self.selected_index)
        
        self.update_display()

# Integration
player_inventory = Inventory()
inventory_ui = InventoryUI(player_inventory)

def handle_inventory_key(key):
    if key == "i":
        inventory_ui.toggle()
    else:
        inventory_ui.handle_input(key)
```

---

## Creating Animated Sprites

Learn how to create smooth sprite animations for characters and effects.

### Animation System

```python
class Animation:
    def __init__(self, frames, duration=0.1, loop=True):
        self.frames = frames  # List of sprite indices
        self.duration = duration  # Time per frame
        self.loop = loop
        self.current_frame = 0
        self.timer = 0
        self.finished = False
    
    def update(self, dt):
        if self.finished:
            return
        
        self.timer += dt
        
        if self.timer >= self.duration:
            self.timer -= self.duration
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
    
    def get_frame(self):
        return self.frames[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.timer = 0
        self.finished = False

class AnimatedSprite:
    def __init__(self, x, y):
        self.sprite = mcrfpy.Sprite(x, y)
        self.animations = {}
        self.current_animation = None
    
    def add_animation(self, name, animation):
        self.animations[name] = animation
    
    def play(self, name):
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_animation.reset()
    
    def update(self, dt):
        if self.current_animation:
            self.current_animation.update(dt)
            self.sprite.sprite_index = self.current_animation.get_frame()

# Example: Animated character
class AnimatedCharacter:
    def __init__(self, x, y):
        self.sprite = AnimatedSprite(x, y)
        self.sprite.sprite.texture = mcrfpy.Texture("assets/character.png", 32, 32)
        
        # Define animations
        self.sprite.add_animation("idle", Animation([0, 1], 0.5))
        self.sprite.add_animation("walk", Animation([2, 3, 4, 3], 0.2))
        self.sprite.add_animation("attack", Animation([5, 6, 7, 6, 5], 0.1, loop=False))
        self.sprite.add_animation("death", Animation([8, 9, 10, 11], 0.2, loop=False))
        
        # Start with idle
        self.sprite.play("idle")
        
        # State
        self.state = "idle"
        self.direction = "right"
    
    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.sprite.play(state)
    
    def update(self, dt):
        self.sprite.update(dt)
        
        # Handle state transitions
        if self.state == "attack" and self.sprite.current_animation.finished:
            self.set_state("idle")

# Particle effects
class Particle:
    def __init__(self, x, y, vx, vy, lifetime, sprite_index):
        self.sprite = mcrfpy.Sprite(x, y)
        self.sprite.sprite_index = sprite_index
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.age = 0
        self.dead = False
    
    def update(self, dt):
        self.age += dt
        
        if self.age >= self.lifetime:
            self.dead = True
            return
        
        # Update position
        x, y = self.sprite.pos
        self.sprite.pos = (x + self.vx * dt, y + self.vy * dt)
        
        # Fade out
        alpha = 1.0 - (self.age / self.lifetime)
        self.sprite.opacity = int(255 * alpha)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.texture = mcrfpy.Texture("assets/particles.png", 8, 8)
    
    def emit(self, x, y, count=10, spread=50):
        for _ in range(count):
            angle = random.random() * 2 * 3.14159
            speed = random.uniform(20, spread)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            lifetime = random.uniform(0.5, 1.5)
            sprite_index = random.randint(0, 3)
            
            particle = Particle(x, y, vx, vy, lifetime, sprite_index)
            particle.sprite.texture = self.texture
            self.particles.append(particle)
            
            # Add to scene
            mcrfpy.sceneUI("game").append(particle.sprite)
    
    def update(self, dt):
        for particle in self.particles[:]:
            particle.update(dt)
            
            if particle.dead:
                # Remove from scene
                mcrfpy.sceneUI("game").remove(particle.sprite)
                self.particles.remove(particle)
```

---

## Procedural Level Generation

Advanced techniques for generating interesting, playable levels.

### Binary Space Partitioning (BSP)

```python
class BSPNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = None
        self.right = None
        self.room = None
    
    def split(self, min_size=6):
        if self.left or self.right:
            return False  # Already split
        
        # Decide split direction
        split_h = random.random() > 0.5
        
        if self.width > self.height * 1.25:
            split_h = False
        elif self.height > self.width * 1.25:
            split_h = True
        
        max_size = (self.height if split_h else self.width) - min_size
        if max_size <= min_size:
            return False  # Too small to split
        
        split_pos = random.randint(min_size, max_size)
        
        if split_h:
            self.left = BSPNode(self.x, self.y, self.width, split_pos)
            self.right = BSPNode(self.x, self.y + split_pos, 
                               self.width, self.height - split_pos)
        else:
            self.left = BSPNode(self.x, self.y, split_pos, self.height)
            self.right = BSPNode(self.x + split_pos, self.y,
                               self.width - split_pos, self.height)
        
        return True
    
    def create_rooms(self):
        if self.left or self.right:
            # Not a leaf, recurse
            if self.left:
                self.left.create_rooms()
            if self.right:
                self.right.create_rooms()
            
            # Create corridor between children
            if self.left and self.right:
                self.create_corridor(self.left.get_room(), 
                                   self.right.get_room())
        else:
            # Create room in this leaf
            w = random.randint(3, self.width - 2)
            h = random.randint(3, self.height - 2)
            x = random.randint(self.x + 1, self.x + self.width - w - 1)
            y = random.randint(self.y + 1, self.y + self.height - h - 1)
            self.room = Room(x, y, w, h)
    
    def get_room(self):
        if self.room:
            return self.room
        
        if self.left:
            left_room = self.left.get_room()
            if left_room:
                return left_room
        
        if self.right:
            right_room = self.right.get_room()
            if right_room:
                return right_room
        
        return None
    
    def create_corridor(self, room1, room2):
        # Connect centers of rooms
        x1, y1 = room1.center()
        x2, y2 = room2.center()
        
        # Randomly choose horizontal-first or vertical-first
        if random.random() > 0.5:
            # Horizontal then vertical
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.carve(x, y1, FLOOR)
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.carve(x2, y, FLOOR)
        else:
            # Vertical then horizontal
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.carve(x1, y, FLOOR)
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.carve(x, y2, FLOOR)

def generate_bsp_dungeon(width, height, grid):
    # Initialize with walls
    for x in range(width):
        for y in range(height):
            grid.set_tile(x, y, WALL)
    
    # Create BSP tree
    root = BSPNode(0, 0, width, height)
    nodes = [root]
    
    # Split nodes
    while nodes:
        node = nodes.pop()
        if node.split():
            nodes.append(node.left)
            nodes.append(node.right)
    
    # Create rooms
    root.create_rooms()
    
    # Carve out rooms
    def carve_rooms(node):
        if node.room:
            for x in range(node.room.x, node.room.x + node.room.width):
                for y in range(node.room.y, node.room.y + node.room.height):
                    grid.set_tile(x, y, FLOOR)
        
        if node.left:
            carve_rooms(node.left)
        if node.right:
            carve_rooms(node.right)
    
    carve_rooms(root)
```

### Wave Function Collapse

```python
class WFCTile:
    def __init__(self, sprite_index, edges):
        self.sprite_index = sprite_index
        self.edges = edges  # Dict: {'north': id, 'south': id, ...}
        self.weight = 1.0

class WFCGrid:
    def __init__(self, width, height, tiles):
        self.width = width
        self.height = height
        self.tiles = tiles
        self.grid = [[None for _ in range(height)] for _ in range(width)]
        self.possibilities = [[list(range(len(tiles))) 
                             for _ in range(height)] 
                             for _ in range(width)]
    
    def collapse(self):
        while True:
            # Find cell with minimum entropy (fewest possibilities)
            min_entropy = float('inf')
            min_cell = None
            
            for x in range(self.width):
                for y in range(self.height):
                    if self.grid[x][y] is None:
                        entropy = len(self.possibilities[x][y])
                        if entropy < min_entropy and entropy > 0:
                            min_entropy = entropy
                            min_cell = (x, y)
            
            if min_cell is None:
                break  # All cells collapsed or contradiction
            
            # Collapse the cell
            x, y = min_cell
            possible = self.possibilities[x][y]
            
            if not possible:
                # Contradiction! Backtrack or restart
                return False
            
            # Choose weighted random tile
            weights = [self.tiles[i].weight for i in possible]
            chosen = random.choices(possible, weights=weights)[0]
            
            self.grid[x][y] = chosen
            self.possibilities[x][y] = [chosen]
            
            # Propagate constraints
            self.propagate(x, y)
        
        return True
    
    def propagate(self, x, y):
        stack = [(x, y)]
        
        while stack:
            cx, cy = stack.pop()
            current_tile = self.tiles[self.grid[cx][cy]]
            
            # Check all neighbors
            for dx, dy, direction, opposite in [
                (0, -1, 'north', 'south'),
                (1, 0, 'east', 'west'),
                (0, 1, 'south', 'north'),
                (-1, 0, 'west', 'east')
            ]:
                nx, ny = cx + dx, cy + dy
                
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[nx][ny] is None:
                        # Filter possibilities based on edge compatibility
                        old_possible = self.possibilities[nx][ny][:]
                        new_possible = []
                        
                        edge_type = current_tile.edges[direction]
                        
                        for tile_idx in old_possible:
                            tile = self.tiles[tile_idx]
                            if tile.edges[opposite] == edge_type:
                                new_possible.append(tile_idx)
                        
                        self.possibilities[nx][ny] = new_possible
                        
                        # If possibilities changed, propagate further
                        if len(new_possible) < len(old_possible):
                            stack.append((nx, ny))

# Example tile definitions
FLOOR_TILES = [
    WFCTile(0, {'north': 'floor', 'south': 'floor', 
                'east': 'floor', 'west': 'floor'}),
    WFCTile(1, {'north': 'wall', 'south': 'floor',
                'east': 'floor', 'west': 'floor'}),
    # ... more tile definitions
]
```

---

## Save and Load System

Implement game state persistence with save files.

### Save System

```python
import json
import base64
import zlib

class SaveGame:
    def __init__(self):
        self.version = 1
        self.data = {}
    
    def save_player(self, player):
        self.data['player'] = {
            'x': player.x,
            'y': player.y,
            'hp': player.combat.hp,
            'max_hp': player.combat.max_hp,
            'attack': player.combat.attack,
            'defense': player.combat.defense,
            'inventory': self.save_inventory(player.inventory),
            'stats': player.stats
        }
    
    def save_inventory(self, inventory):
        items = []
        for i, item in enumerate(inventory.items):
            if item:
                items.append({
                    'slot': i,
                    'name': item.name,
                    'quantity': item.quantity
                })
        
        return {
            'items': items,
            'equipment': {
                'weapon': inventory.equipment['weapon'].name 
                         if inventory.equipment['weapon'] else None,
                'armor': inventory.equipment['armor'].name
                        if inventory.equipment['armor'] else None
            }
        }
    
    def save_level(self, grid, entities):
        # Compress tile data
        tiles = []
        for x in range(grid.grid_x):
            for y in range(grid.grid_y):
                tiles.append(grid.get_tile(x, y))
        
        # Compress using zlib
        tile_bytes = bytes(tiles)
        compressed = zlib.compress(tile_bytes, 9)
        tile_data = base64.b64encode(compressed).decode('ascii')
        
        self.data['level'] = {
            'width': grid.grid_x,
            'height': grid.grid_y,
            'tiles': tile_data,
            'entities': [self.save_entity(e) for e in entities]
        }
    
    def save_entity(self, entity):
        return {
            'type': entity.__class__.__name__,
            'x': entity.x,
            'y': entity.y,
            'sprite': entity.entity.sprite_index,
            'data': entity.save_data() if hasattr(entity, 'save_data') else {}
        }
    
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump({
                'version': self.version,
                'data': self.data
            }, f, indent=2)
    
    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            save = json.load(f)
            
        if save['version'] != self.version:
            raise ValueError(f"Save version {save['version']} not compatible")
        
        self.data = save['data']
        return self.data

class GameState:
    def __init__(self):
        self.player = None
        self.level = None
        self.entities = []
    
    def save_game(self, slot=1):
        save = SaveGame()
        save.save_player(self.player)
        save.save_level(self.level, self.entities)
        
        # Additional game state
        save.data['game_time'] = mcrfpy.runtime()
        save.data['current_floor'] = self.current_floor
        save.data['seed'] = self.random_seed
        
        save.save_to_file(f"save_{slot}.json")
        
        # Show confirmation
        self.show_message("Game Saved!")
    
    def load_game(self, slot=1):
        try:
            save = SaveGame()
            data = save.load_from_file(f"save_{slot}.json")
            
            # Restore player
            player_data = data['player']
            self.player = self.create_player(
                player_data['x'], 
                player_data['y']
            )
            self.player.combat.hp = player_data['hp']
            self.player.combat.max_hp = player_data['max_hp']
            
            # Restore inventory
            self.load_inventory(self.player.inventory, 
                              player_data['inventory'])
            
            # Restore level
            self.load_level(data['level'])
            
            # Restore game state
            self.current_floor = data.get('current_floor', 1)
            self.random_seed = data.get('seed', 0)
            
            self.show_message("Game Loaded!")
            
        except FileNotFoundError:
            self.show_message("No save file found!")
        except Exception as e:
            self.show_message(f"Load failed: {str(e)}")
    
    def load_level(self, level_data):
        # Decompress tiles
        compressed = base64.b64decode(level_data['tiles'])
        tile_bytes = zlib.decompress(compressed)
        tiles = list(tile_bytes)
        
        # Recreate grid
        width = level_data['width']
        height = level_data['height']
        
        self.level = mcrfpy.Grid(0, 0, width, height, 
                                self.tileset, 16, 16)
        
        # Set tiles
        i = 0
        for x in range(width):
            for y in range(height):
                self.level.set_tile(x, y, tiles[i])
                i += 1
        
        # Recreate entities
        for entity_data in level_data['entities']:
            entity = self.create_entity(entity_data)
            if entity:
                self.entities.append(entity)
                self.level.entities.append(entity.entity)

# Auto-save system
class AutoSave:
    def __init__(self, game_state, interval=300):  # 5 minutes
        self.game_state = game_state
        self.interval = interval
        self.last_save = 0
    
    def update(self, runtime):
        if runtime - self.last_save >= self.interval:
            self.game_state.save_game(slot=0)  # Slot 0 for autosave
            self.last_save = runtime

# Save/Load UI
def create_save_menu():
    menu = mcrfpy.Frame(200, 150, 400, 300)
    menu.bgcolor = (40, 40, 60)
    menu.outline = 3
    
    title = mcrfpy.Caption(400, 170, "Save/Load Game")
    title.font_size = 24
    title.centered = True
    
    slots = []
    for i in range(3):
        y = 220 + i * 40
        
        # Slot button
        slot_frame = mcrfpy.Frame(250, y, 300, 35)
        slot_frame.bgcolor = (60, 60, 80)
        slot_frame.outline = 1
        
        # Check if save exists
        save_info = get_save_info(i + 1)
        if save_info:
            text = f"Slot {i+1}: {save_info}"
        else:
            text = f"Slot {i+1}: Empty"
        
        slot_text = mcrfpy.Caption(400, y + 17, text)
        slot_text.centered = True
        
        slots.append((slot_frame, slot_text))
    
    return menu, title, slots
```

---

## Creating Particle Effects

Add visual flair with particle systems for explosions, magic, and environmental effects.

### Advanced Particle System

```python
import math

class ParticleEmitter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
        self.particles = []
        
        # Emission properties
        self.emission_rate = 10  # particles per second
        self.emission_timer = 0
        self.max_particles = 100
        
        # Particle properties
        self.texture = mcrfpy.Texture("assets/particles.png", 8, 8)
        self.sprite_indices = [0, 1, 2, 3]
        self.lifetime_range = (0.5, 2.0)
        self.speed_range = (50, 150)
        self.direction_range = (0, 360)  # degrees
        self.scale_range = (0.5, 2.0)
        self.colors = [(255, 255, 255), (255, 200, 100)]
        
        # Physics
        self.gravity = 200  # pixels per second squared
        self.drag = 0.9
    
    def emit_burst(self, count):
        """Emit a burst of particles"""
        for _ in range(count):
            if len(self.particles) < self.max_particles:
                self.emit_particle()
    
    def emit_particle(self):
        # Random properties
        lifetime = random.uniform(*self.lifetime_range)
        speed = random.uniform(*self.speed_range)
        direction = math.radians(random.uniform(*self.direction_range))
        scale = random.uniform(*self.scale_range)
        
        # Velocity
        vx = speed * math.cos(direction)
        vy = speed * math.sin(direction)
        
        # Create particle
        particle = {
            'sprite': mcrfpy.Sprite(self.x, self.y),
            'vx': vx,
            'vy': vy,
            'lifetime': lifetime,
            'age': 0,
            'scale': scale,
            'start_scale': scale,
            'color': random.choice(self.colors)
        }
        
        particle['sprite'].texture = self.texture
        particle['sprite'].sprite_index = random.choice(self.sprite_indices)
        particle['sprite'].scale = (scale, scale)
        
        self.particles.append(particle)
        mcrfpy.sceneUI("game").append(particle['sprite'])
    
    def update(self, dt):
        if self.active:
            # Emit new particles
            self.emission_timer += dt
            particles_to_emit = int(self.emission_timer * self.emission_rate)
            self.emission_timer -= particles_to_emit / self.emission_rate
            
            for _ in range(particles_to_emit):
                if len(self.particles) < self.max_particles:
                    self.emit_particle()
        
        # Update existing particles
        for particle in self.particles[:]:
            particle['age'] += dt
            
            # Check lifetime
            if particle['age'] >= particle['lifetime']:
                mcrfpy.sceneUI("game").remove(particle['sprite'])
                self.particles.remove(particle)
                continue
            
            # Physics update
            particle['vy'] += self.gravity * dt
            particle['vx'] *= self.drag
            particle['vy'] *= self.drag
            
            # Update position
            x, y = particle['sprite'].pos
            particle['sprite'].pos = (
                x + particle['vx'] * dt,
                y + particle['vy'] * dt
            )
            
            # Age effects
            age_ratio = particle['age'] / particle['lifetime']
            
            # Fade out
            alpha = int(255 * (1 - age_ratio))
            
            # Scale down
            scale = particle['start_scale'] * (1 - age_ratio * 0.5)
            particle['sprite'].scale = (scale, scale)
            
            # Color shift (if using color modulation)
            # particle['sprite'].color = interpolate_color(
            #     particle['color'], (255, 0, 0), age_ratio)

# Specialized particle effects
class FireEffect(ParticleEmitter):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.emission_rate = 30
        self.lifetime_range = (0.3, 0.8)
        self.speed_range = (20, 60)
        self.direction_range = (260, 280)  # Mostly upward
        self.colors = [(255, 255, 100), (255, 150, 0), (255, 0, 0)]
        self.gravity = -100  # Fire rises

class ExplosionEffect(ParticleEmitter):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.active = False  # One-shot effect
        self.lifetime_range = (0.5, 1.0)
        self.speed_range = (100, 300)
        self.direction_range = (0, 360)
        self.scale_range = (1.0, 3.0)
        self.gravity = 0
        self.drag = 0.8
        
        # Initial burst
        self.emit_burst(50)

class MagicEffect(ParticleEmitter):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.emission_rate = 20
        self.lifetime_range = (1.0, 2.0)
        self.speed_range = (10, 30)
        self.colors = [(100, 100, 255), (200, 100, 255), (255, 200, 255)]
        self.gravity = -50
        
        # Spiral motion
        self.spiral_speed = 5
        self.spiral_radius = 30
    
    def emit_particle(self):
        super().emit_particle()
        
        # Add spiral motion
        particle = self.particles[-1]
        angle = random.uniform(0, 2 * math.pi)
        particle['spiral_angle'] = angle
        particle['spiral_time'] = 0
    
    def update(self, dt):
        super().update(dt)
        
        # Update spiral motion
        for particle in self.particles:
            if 'spiral_angle' in particle:
                particle['spiral_time'] += dt * self.spiral_speed
                
                # Calculate spiral offset
                angle = particle['spiral_angle'] + particle['spiral_time']
                radius = self.spiral_radius * (1 - particle['age'] / particle['lifetime'])
                
                offset_x = radius * math.cos(angle)
                offset_y = radius * math.sin(angle)
                
                # Apply offset (would need to track base position)
                # particle['sprite'].pos = (base_x + offset_x, base_y + offset_y)

# Particle manager
class ParticleManager:
    def __init__(self):
        self.emitters = []
    
    def add_fire(self, x, y, duration=None):
        emitter = FireEffect(x, y)
        if duration:
            emitter.duration = duration
        self.emitters.append(emitter)
        return emitter
    
    def add_explosion(self, x, y):
        emitter = ExplosionEffect(x, y)
        self.emitters.append(emitter)
        return emitter
    
    def add_magic(self, x, y):
        emitter = MagicEffect(x, y)
        self.emitters.append(emitter)
        return emitter
    
    def update(self, dt):
        for emitter in self.emitters[:]:
            emitter.update(dt)
            
            # Remove dead emitters
            if not emitter.active and not emitter.particles:
                self.emitters.remove(emitter)

# Usage example
particle_manager = ParticleManager()

# Add fire effect at torch location
torch_fire = particle_manager.add_fire(100, 200)

# Explosion on enemy death
def on_enemy_death(enemy):
    particle_manager.add_explosion(enemy.x * 16, enemy.y * 16)

# Magic spell effect
def cast_spell(caster, target):
    # Create magic particles at caster
    magic = particle_manager.add_magic(caster.x * 16, caster.y * 16)
    
    # Move particles toward target over time
    # (implement particle trajectory system)

# Update in game loop
def update_particles(runtime):
    dt = 0.016  # 60 FPS
    particle_manager.update(dt)

mcrfpy.setTimer("particles", update_particles, 16)
```

---

## Conclusion

These tutorials cover the essential systems needed to create a full-featured roguelike game with McRogueFace. Each system can be expanded and customized to fit your specific game design.

### Key Takeaways

1. **Use Timers**: Essential for animations and game updates
2. **Manage State**: Keep track of game objects and their relationships
3. **Layer Systems**: Build complex features from simple components
4. **Test Often**: Use the automation API to verify functionality
5. **Optimize Carefully**: Profile before optimizing, the engine is quite fast

### Next Steps

- Combine these systems to create your own unique roguelike
- Explore the [API Reference](api-reference.md) for additional features
- Share your creations with the McRogueFace community
- Contribute improvements back to the project

Happy game development!