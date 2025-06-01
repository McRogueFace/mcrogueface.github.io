# Tutorials

## Building a Complete Roguelike

This tutorial walks through building a complete roguelike game with McRogueFace.

### 1. Procedural Dungeon Generation

Let's create a dungeon using Binary Space Partitioning (BSP):

```python
import mcrfpy
import random

class Room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def center(self):
        return (self.x + self.w // 2, self.y + self.h // 2)

def generate_dungeon(grid, width, height):
    # Initialize all tiles as walls
    for i in range(width * height):
        pt = grid.at(i)
        pt.tilesprite = 35  # Wall
        pt.walkable = False
        pt.transparent = False
    
    # Generate rooms
    rooms = []
    for _ in range(6):
        w = random.randint(4, 8)
        h = random.randint(4, 8)
        x = random.randint(1, width - w - 1)
        y = random.randint(1, height - h - 1)
        
        room = Room(x, y, w, h)
        
        # Check if it overlaps with existing rooms
        overlap = False
        for other in rooms:
            if (x < other.x + other.w and x + w > other.x and
                y < other.y + other.h and y + h > other.y):
                overlap = True
                break
        
        if not overlap:
            rooms.append(room)
            # Carve out the room
            for rx in range(x, x + w):
                for ry in range(y, y + h):
                    pt = grid.at(rx + ry * width)
                    pt.tilesprite = 46  # Floor
                    pt.walkable = True
                    pt.transparent = True
    
    # Connect rooms with corridors
    for i in range(len(rooms) - 1):
        x1, y1 = rooms[i].center()
        x2, y2 = rooms[i + 1].center()
        
        # Horizontal corridor
        for x in range(min(x1, x2), max(x1, x2) + 1):
            pt = grid.at(x + y1 * width)
            pt.tilesprite = 46
            pt.walkable = True
            pt.transparent = True
        
        # Vertical corridor
        for y in range(min(y1, y2), max(y1, y2) + 1):
            pt = grid.at(x2 + y * width)
            pt.tilesprite = 46
            pt.walkable = True
            pt.transparent = True
    
    return rooms
```

### 2. Field of View (FOV) System

Implement visibility for a true roguelike experience:

```python
def calculate_fov(grid, entity, radius=8):
    """Simple FOV using ray casting"""
    ex, ey = entity.pos
    width, height = grid.grid_size
    
    # Reset visibility
    for i in range(len(entity.gridstate)):
        entity.gridstate[i].visible = False
    
    # Cast rays in all directions
    for angle in range(0, 360, 5):  # Check every 5 degrees
        dx = math.cos(math.radians(angle))
        dy = math.sin(math.radians(angle))
        
        for distance in range(radius):
            x = int(ex + dx * distance)
            y = int(ey + dy * distance)
            
            if 0 <= x < width and 0 <= y < height:
                idx = x + y * width
                entity.gridstate[idx].visible = True
                entity.gridstate[idx].discovered = True
                
                # Stop if we hit a wall
                if not grid.at(idx).transparent:
                    break

def update_display(grid, player):
    """Update tile appearance based on visibility"""
    width, height = grid.grid_size
    
    for x in range(width):
        for y in range(height):
            idx = x + y * width
            pt = grid.at(idx)
            state = player.at((x, y))
            
            if state.visible:
                # Fully visible
                pt.color = mcrfpy.Color(255, 255, 255)
            elif state.discovered:
                # Previously seen - dim it
                pt.color = mcrfpy.Color(100, 100, 100)
            else:
                # Never seen - black
                pt.color = mcrfpy.Color(0, 0, 0)
```

### 3. Turn-Based Combat System

Create a proper turn-based system:

```python
class CombatSystem:
    def __init__(self):
        self.entities = []
        self.current_turn = 0
        
    def add_entity(self, entity, stats):
        self.entities.append({
            'entity': entity,
            'hp': stats['hp'],
            'max_hp': stats['max_hp'],
            'damage': stats['damage'],
            'defense': stats['defense']
        })
    
    def player_action(self, action):
        """Process player action, then run AI turns"""
        player = self.entities[0]
        
        if action == 'move':
            # Movement handled elsewhere
            pass
        elif action == 'attack':
            # Find adjacent enemies
            px, py = player['entity'].pos
            for ent_data in self.entities[1:]:
                ex, ey = ent_data['entity'].pos
                if abs(px - ex) + abs(py - ey) == 1:  # Adjacent
                    self.attack(player, ent_data)
                    break
        
        # Enemy turns
        self.ai_turns()
    
    def attack(self, attacker, defender):
        damage = max(1, attacker['damage'] - defender['defense'])
        defender['hp'] -= damage
        
        if defender['hp'] <= 0:
            # Remove from grid
            grid.children.remove(defender['entity'])
            self.entities.remove(defender)
    
    def ai_turns(self):
        player = self.entities[0]
        px, py = player['entity'].pos
        
        for ent_data in self.entities[1:]:
            entity = ent_data['entity']
            ex, ey = entity.pos
            
            # Simple AI: move towards player
            dx = 1 if px > ex else -1 if px < ex else 0
            dy = 1 if py > ey else -1 if py < ey else 0
            
            new_x, new_y = ex + dx, ey + dy
            
            # Check if we can move there
            if grid.at(new_x + new_y * grid.grid_size[0]).walkable:
                # Check for player collision
                if (new_x, new_y) == (px, py):
                    self.attack(ent_data, player)
                else:
                    entity.pos = (new_x, new_y)
```

### 4. Inventory and Items

Add an inventory system with items:

```python
class Item:
    def __init__(self, name, sprite, effect):
        self.name = name
        self.sprite = sprite
        self.effect = effect

class Inventory:
    def __init__(self, capacity=10):
        self.items = []
        self.capacity = capacity
        
    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False
    
    def use_item(self, index, target):
        if 0 <= index < len(self.items):
            item = self.items[index]
            item.effect(target)
            self.items.pop(index)

# Create items
def heal_effect(target):
    target['hp'] = min(target['hp'] + 20, target['max_hp'])

health_potion = Item("Health Potion", 100, heal_effect)

# Place items in the world
item_entities = []
for room in rooms:
    if random.random() < 0.3:  # 30% chance per room
        item = mcrfpy.Entity(grid)
        item.pos = room.center()
        item.sprite_number = 100  # Potion sprite
        grid.children.append(item)
        item_entities.append((item, health_potion))

# Pick up items
def check_item_pickup(player_pos):
    for item_ent, item_data in item_entities:
        if item_ent.pos == player_pos:
            if inventory.add_item(item_data):
                grid.children.remove(item_ent)
                item_entities.remove((item_ent, item_data))
                show_message("Picked up " + item_data.name)
```

### 5. UI Systems

Create a complete UI with menus and dialogs:

```python
# Main menu
def create_main_menu():
    mcrfpy.createScene("menu")
    ui = mcrfpy.sceneUI("menu")
    
    # Background
    bg = mcrfpy.Frame(0, 0, 800, 600)
    bg.fill_color = mcrfpy.Color(20, 20, 20)
    ui.append(bg)
    
    # Title
    title = mcrfpy.Caption("DUNGEON CRAWLER", mcrfpy.default_font)
    title.pos = (250, 100)
    title.fill_color = mcrfpy.Color(255, 215, 0)  # Gold
    bg.children.append(title)
    
    # Menu options
    options = ["New Game", "Continue", "Options", "Exit"]
    for i, option in enumerate(options):
        btn_frame = mcrfpy.Frame(300, 200 + i * 60, 200, 40)
        btn_frame.outline = 2
        btn_frame.outline_color = mcrfpy.Color(100, 100, 100)
        
        btn_text = mcrfpy.Caption(option, mcrfpy.default_font)
        btn_text.pos = (350, 210 + i * 60)
        
        # Click handler
        def make_handler(opt):
            def handler(x, y, btn, action):
                if action == 0:  # Pressed
                    handle_menu_option(opt)
            return handler
        
        btn_frame.click = make_handler(option)
        
        bg.children.append(btn_frame)
        bg.children.append(btn_text)

# Dialog system
def show_dialog(text, options):
    # Create overlay
    dialog = mcrfpy.Frame(150, 200, 500, 200)
    dialog.fill_color = mcrfpy.Color(40, 40, 40)
    dialog.outline = 3
    dialog.outline_color = mcrfpy.Color(200, 200, 200)
    
    # Text
    lines = text.split('\n')
    for i, line in enumerate(lines):
        caption = mcrfpy.Caption(line, mcrfpy.default_font)
        caption.pos = (170, 220 + i * 20)
        dialog.children.append(caption)
    
    # Options
    for i, option in enumerate(options):
        opt_text = mcrfpy.Caption(f"{i+1}. {option}", mcrfpy.default_font)
        opt_text.pos = (170, 320 + i * 20)
        dialog.children.append(opt_text)
    
    ui.append(dialog)
    return dialog
```

### 6. Save/Load System

Implement game persistence:

```python
import json

def save_game(filename="savegame.json"):
    save_data = {
        'player': {
            'pos': player.pos,
            'hp': combat_system.entities[0]['hp'],
            'inventory': [item.name for item in inventory.items]
        },
        'dungeon': {
            'width': grid.grid_size[0],
            'height': grid.grid_size[1],
            'tiles': []
        },
        'entities': []
    }
    
    # Save tile data
    for i in range(grid.grid_size[0] * grid.grid_size[1]):
        pt = grid.at(i)
        save_data['dungeon']['tiles'].append({
            'sprite': pt.tilesprite,
            'walkable': pt.walkable,
            'transparent': pt.transparent
        })
    
    # Save entities
    for ent_data in combat_system.entities[1:]:
        save_data['entities'].append({
            'pos': ent_data['entity'].pos,
            'sprite': ent_data['entity'].sprite_number,
            'hp': ent_data['hp']
        })
    
    with open(filename, 'w') as f:
        json.dump(save_data, f)

def load_game(filename="savegame.json"):
    with open(filename, 'r') as f:
        save_data = json.load(f)
    
    # Restore player
    player.pos = tuple(save_data['player']['pos'])
    combat_system.entities[0]['hp'] = save_data['player']['hp']
    
    # Restore dungeon
    for i, tile_data in enumerate(save_data['dungeon']['tiles']):
        pt = grid.at(i)
        pt.tilesprite = tile_data['sprite']
        pt.walkable = tile_data['walkable']
        pt.transparent = tile_data['transparent']
    
    # Clear and restore entities
    grid.children.clear()
    grid.children.append(player)
    
    for ent_data in save_data['entities']:
        entity = mcrfpy.Entity(grid)
        entity.pos = tuple(ent_data['pos'])
        entity.sprite_number = ent_data['sprite']
        grid.children.append(entity)
```

## Advanced Techniques

### Animation System

Create smooth animations:

```python
class Animation:
    def __init__(self, entity, start_pos, end_pos, duration_ms):
        self.entity = entity
        self.start = start_pos
        self.end = end_pos
        self.duration = duration_ms
        self.elapsed = 0
        
    def update(self, dt_ms):
        self.elapsed += dt_ms
        t = min(1.0, self.elapsed / self.duration)
        
        # Smooth interpolation
        t = t * t * (3.0 - 2.0 * t)  # smoothstep
        
        x = self.start[0] + (self.end[0] - self.start[0]) * t
        y = self.start[1] + (self.end[1] - self.start[1]) * t
        self.entity.draw_pos = (x, y)
        
        return self.elapsed >= self.duration

# Usage
animations = []

def move_entity_animated(entity, new_pos):
    anim = Animation(entity, entity.pos, new_pos, 200)  # 200ms
    animations.append(anim)
    entity.pos = new_pos  # Set logical position immediately

def update_animations():
    global animations
    animations = [a for a in animations if not a.update(16)]  # 60 FPS

mcrfpy.setTimer("animate", update_animations, 16)
```

### Particle Effects

Add visual flair with particles:

```python
class Particle:
    def __init__(self, pos, velocity, lifetime, sprite):
        self.entity = mcrfpy.Entity(grid)
        self.entity.pos = pos
        self.entity.sprite_number = sprite
        self.velocity = velocity
        self.lifetime = lifetime
        self.age = 0
        grid.children.append(self.entity)
        
    def update(self, dt):
        self.age += dt
        if self.age >= self.lifetime:
            grid.children.remove(self.entity)
            return False
        
        # Update position
        x, y = self.entity.draw_pos
        self.entity.draw_pos = (
            x + self.velocity[0] * dt,
            y + self.velocity[1] * dt
        )
        return True

particles = []

def create_explosion(pos):
    for _ in range(10):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
        
        particle = Particle(pos, velocity, 1000, 15)  # Fire sprite
        particles.append(particle)
```

## Performance Tips

1. **Batch Operations**: Update multiple tiles at once rather than individually
2. **Limit Entities**: Keep active entity count reasonable (<100 for smooth performance)
3. **Use Timers Wisely**: Don't create too many high-frequency timers
4. **Optimize FOV**: Only recalculate when player moves
5. **Sprite Batching**: Entities on the same Grid are automatically batched

## Next Steps

- Study the included "Crypt of Sokoban" game for a complete example
- Experiment with the Wave Function Collapse system in `cos_tiles.py`
- Create your own texture packs with custom sprites
- Join the community and share your creations!