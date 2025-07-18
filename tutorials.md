# McRogueFace Tutorials

**Make 2D games with Python** - No C++ required!

---

[**Source Code**](https://github.com/jmccardle/McRogueFace) • [**Downloads**](https://github.com/jmccardle/McRogueFace/releases) • [**Quickstart**](https://mcrogueface.github.io/quickstart) • **[Tutorials](https://mcrogueface.github.io/tutorials)** • [**API Reference**](https://mcrogueface.github.io/api) • [**Cookbook**](https://mcrogueface.github.io/cookbook) • [**C++ Extensions**](https://mcrogueface.github.io/extending-cpp)

---

These tutorials will guide you through the core concepts of McRogueFace by building real, working examples. Each tutorial builds on the previous one, introducing new concepts step by step.

## Table of Contents

1. [Part 0: Scene, Texture, and Grid](#part-0-scene-texture-and-grid)
2. [Part 1: Entities and Keyboard Input](#part-1-entities-and-keyboard-input)  
3. [Part 2: Smooth Movement with Animations](#part-2-smooth-movement-with-animations)
4. [Part 3: Building a Complete Game](#part-3-building-a-complete-game)

---

## Part 0: Scene, Texture, and Grid

This tutorial introduces the basic building blocks:
- **Scene**: A container for UI elements and game state
- **Texture**: Loading image assets for use in the game
- **Grid**: A tilemap component for rendering tile-based worlds

```python
"""
McRogueFace Tutorial - Part 0: Introduction to Scene, Texture, and Grid

This tutorial introduces the basic building blocks:
- Scene: A container for UI elements and game state
- Texture: Loading image assets for use in the game
- Grid: A tilemap component for rendering tile-based worlds
"""
import mcrfpy
import random

# Create and activate a new scene
mcrfpy.createScene("tutorial")
mcrfpy.setScene("tutorial")

# Load the texture (4x3 tiles, 64x48 pixels total, 16x16 per tile)
texture = mcrfpy.Texture("assets/tutorial2.png", 16, 16)

# Create a grid of tiles
# Each tile is 16x16 pixels, so with 2x zoom: 16*2 = 32 pixels per tile

grid_width, grid_height = 25, 20 # width, height in number of tiles

# calculating the size in pixels to fit the entire grid on-screen
zoom = 2.0
grid_size = grid_width * zoom * 16, grid_height * zoom * 16

# calculating the position to center the grid on the screen - assuming default 1024x768 resolution
grid_position = (1024 - grid_size[0]) / 2, (768 - grid_size[1]) / 2

grid = mcrfpy.Grid(
    pos=grid_position,
    grid_size=(grid_width, grid_height),
    texture=texture,
    size=grid_size,  # height and width on screen
)

grid.zoom = zoom
grid.center = (grid_width/2.0)*16, (grid_height/2.0)*16 # center on the middle of the central tile

# Define tile types
FLOOR_TILES = [0, 1, 2, 4, 5, 6, 8, 9, 10]
WALL_TILES = [3, 7, 11]

# Fill the grid with a simple pattern
for y in range(grid_height):
    for x in range(grid_width):
        # Create walls around the edges
        if x == 0 or x == grid_width-1 or y == 0 or y == grid_height-1:
            tile_index = random.choice(WALL_TILES)
        else:
            # Fill interior with floor tiles
            tile_index = random.choice(FLOOR_TILES)
        
        # Set the tile at this position
        point = grid.at(x, y)
        if point:
            point.tilesprite = tile_index

# Add the grid to the scene
mcrfpy.sceneUI("tutorial").append(grid)

# Add a title caption
title = mcrfpy.Caption((320, 10),
    text="McRogueFace Tutorial - Part 0",
)
title.fill_color = mcrfpy.Color(255, 255, 255, 255)
mcrfpy.sceneUI("tutorial").append(title)

# Add instructions
instructions = mcrfpy.Caption((280, 750),
    text="Scene + Texture + Grid = Tilemap!",
)
instructions.font_size=18
instructions.fill_color = mcrfpy.Color(200, 200, 200, 255)
mcrfpy.sceneUI("tutorial").append(instructions)

print("Tutorial Part 0 loaded!")
print(f"Created a {grid.grid_size[0]}x{grid.grid_size[1]} grid")
print(f"Grid positioned at ({grid.x}, {grid.y})")
```

### Key Concepts

**1. Scenes** are containers for your game state. You can have multiple scenes (menu, game, inventory, etc.) and switch between them.

**2. Textures** are sprite sheets loaded from image files. The two parameters (16, 16) specify the size of each sprite in the sheet.

**3. Grids** are tilemap components that efficiently render many tiles. Key properties:
   - `pos`: Screen position in pixels
   - `grid_size`: Size in tiles (not pixels!)
   - `size`: Display size in pixels
   - `zoom`: Magnification factor
   - `center`: Camera position in texture coordinates

**4. Grid Points** represent individual tiles. Use `grid.at(x, y)` to get a point and set its `tilesprite` property.

---

## Part 1: Entities and Keyboard Input

This tutorial builds on Part 0 by adding:
- **Entity**: A game object that can be placed in a grid
- **Keyboard handling**: Responding to key presses to move the entity

```python
"""
McRogueFace Tutorial - Part 1: Entities and Keyboard Input

This tutorial builds on Part 0 by adding:
- Entity: A game object that can be placed in a grid
- Keyboard handling: Responding to key presses to move the entity
"""
import mcrfpy
import random

# Create and activate a new scene
mcrfpy.createScene("tutorial")
mcrfpy.setScene("tutorial")

# Load the texture (4x3 tiles, 64x48 pixels total, 16x16 per tile)
texture = mcrfpy.Texture("assets/tutorial2.png", 16, 16)

# Load the hero sprite texture
hero_texture = mcrfpy.Texture("assets/custom_player.png", 16, 16)

# Create a grid of tiles
grid_width, grid_height = 25, 20

# calculating the size in pixels to fit the entire grid on-screen
zoom = 2.0
grid_size = grid_width * zoom * 16, grid_height * zoom * 16

# calculating the position to center the grid on the screen
grid_position = (1024 - grid_size[0]) / 2, (768 - grid_size[1]) / 2

grid = mcrfpy.Grid(
    pos=grid_position,
    grid_size=(grid_width, grid_height),
    texture=texture,
    size=grid_size,
)

grid.zoom = zoom
grid.center = (grid_width/2.0)*16, (grid_height/2.0)*16

# Define tile types
FLOOR_TILES = [0, 1, 2, 4, 5, 6, 8, 9, 10]
WALL_TILES = [3, 7, 11]

# Fill the grid with a simple pattern
for y in range(grid_height):
    for x in range(grid_width):
        # Create walls around the edges
        if x == 0 or x == grid_width-1 or y == 0 or y == grid_height-1:
            tile_index = random.choice(WALL_TILES)
        else:
            # Fill interior with floor tiles
            tile_index = random.choice(FLOOR_TILES)
        
        # Set the tile at this position
        point = grid.at(x, y)
        if point:
            point.tilesprite = tile_index

# Add the grid to the scene
mcrfpy.sceneUI("tutorial").append(grid)

# Create a player entity at position (4, 4)
player = mcrfpy.Entity(
    (4, 4),  # Entity positions are tile coordinates
    texture=hero_texture,
    sprite_index=0  # Use the first sprite in the texture
)

# Add the player entity to the grid
grid.entities.append(player)

# Define keyboard handler
def handle_keys(key, state):
    """Handle keyboard input to move the player"""
    if state == "start":  # Only respond to key press, not release
        # Get current player position in grid coordinates
        px, py = player.x, player.y 
        
        # Calculate new position based on key press
        if key == "W" or key == "Up":
            py -= 1
        elif key == "S" or key == "Down":
            py += 1
        elif key == "A" or key == "Left":
            px -= 1
        elif key == "D" or key == "Right":
            px += 1
        
        # Update player position (no collision checking yet)
        player.x = px 
        player.y = py

# Register the keyboard handler
mcrfpy.keypressScene(handle_keys)

# Add UI elements
title = mcrfpy.Caption((320, 10),
    text="McRogueFace Tutorial - Part 1",
)
title.fill_color = mcrfpy.Color(255, 255, 255, 255)
mcrfpy.sceneUI("tutorial").append(title)

instructions = mcrfpy.Caption((200, 750),
    text="Use WASD or Arrow Keys to move the hero!",
)
instructions.font_size=18
instructions.fill_color = mcrfpy.Color(200, 200, 200, 255)
mcrfpy.sceneUI("tutorial").append(instructions)

print("Tutorial Part 1 loaded!")
print(f"Player entity created at grid position (4, 4)")
print("Use WASD or Arrow keys to move!")
```

### Key Concepts

**1. Entities** are game objects that exist in grid coordinates:
   - Position is in tiles, not pixels
   - Each entity needs a texture and sprite_index
   - Entities must be added to a grid's entities collection

**2. Keyboard Input** uses a callback function:
   - `key`: The key pressed (e.g., "W", "Up", "Space")
   - `state`: Either "start" (key pressed) or "end" (key released)
   - Register with `mcrfpy.keypressScene(callback)`

**3. Entity Movement** is simple in this example:
   - Read current position with `entity.x` and `entity.y`
   - Calculate new position
   - Set new position directly
   - No collision detection yet!

### Part 1b: Camera Following

A variation that makes the camera follow the player:

```python
# After moving the player, update the grid center
grid.center = (player.x + 0.5) * 16, (player.y + 0.5) * 16

# Note: grid center is in texture/pixel coordinates, not tile coordinates!
# The +0.5 centers the camera on the middle of the player's tile
```

---

## Part 2: Smooth Movement with Animations

This tutorial adds:
- **Animation system**: Smooth transitions between positions
- **Movement queue**: Handle rapid key presses gracefully
- **Timer callbacks**: Essential for animations and game state

```python
"""
McRogueFace Tutorial - Part 2: Enhanced with Single Move Queue

This tutorial builds on Part 2 by adding:
- Single queued move system for responsive input
- Debug display showing position and queue status
- Smooth continuous movement when keys are held
- Animation callbacks to prevent race conditions
"""
import mcrfpy
import random

# Create and activate a new scene
mcrfpy.createScene("tutorial")
mcrfpy.setScene("tutorial")

# Load textures
texture = mcrfpy.Texture("assets/tutorial2.png", 16, 16)
hero_texture = mcrfpy.Texture("assets/custom_player.png", 16, 16)

# Create grid
grid_width, grid_height = 25, 20
zoom = 3.0  # Larger zoom for this example
grid_size = grid_width * zoom * 16, grid_height * zoom * 16
grid_position = (1024 - grid_size[0]) / 2, (768 - grid_size[1]) / 2

grid = mcrfpy.Grid(
    pos=grid_position,
    grid_size=(grid_width, grid_height),
    texture=texture,
    size=grid_size,
)

grid.zoom = zoom

# Fill the grid (same as before)
FLOOR_TILES = [0, 1, 2, 4, 5, 6, 8, 9, 10]
WALL_TILES = [3, 7, 11]

for y in range(grid_height):
    for x in range(grid_width):
        if x == 0 or x == grid_width-1 or y == 0 or y == grid_height-1:
            tile_index = random.choice(WALL_TILES)
        else:
            tile_index = random.choice(FLOOR_TILES)
        
        point = grid.at(x, y)
        if point:
            point.tilesprite = tile_index

# Add grid to scene
mcrfpy.sceneUI("tutorial").append(grid)

# Create player entity
player = mcrfpy.Entity(
    (4, 4),
    texture=hero_texture,
    sprite_index=0
)

grid.entities.append(player)
grid.center = (player.x + 0.5) * 16, (player.y + 0.5) * 16

# Movement state tracking
is_moving = False
move_queue = []  # List to store queued moves (max 1 item)
current_destination = None  # Track where we're currently moving to
current_move = None  # Track current move direction

# Store animation references
player_anim_x = None
player_anim_y = None
grid_anim_x = None
grid_anim_y = None

# Debug display caption
debug_caption = mcrfpy.Caption((10, 40),
    text="Pos: (4, 4) | Queue: 0 | Dest: None",
)
debug_caption.font_size = 16
debug_caption.fill_color = mcrfpy.Color(255, 255, 0, 255)
mcrfpy.sceneUI("tutorial").append(debug_caption)

# Movement state debug caption
move_debug_caption = mcrfpy.Caption((10, 60),
    text="Moving: False | Current: None | Queued: None",
)
move_debug_caption.font_size = 16
move_debug_caption.fill_color = mcrfpy.Color(255, 200, 0, 255)
mcrfpy.sceneUI("tutorial").append(move_debug_caption)

def key_to_direction(key):
    """Convert key to direction string"""
    if key == "W" or key == "Up":
        return "Up"
    elif key == "S" or key == "Down":
        return "Down"
    elif key == "A" or key == "Left":
        return "Left"
    elif key == "D" or key == "Right":
        return "Right"
    return None

def update_debug_display():
    """Update the debug caption with current state"""
    queue_count = len(move_queue)
    dest_text = f"({current_destination[0]}, {current_destination[1]})" if current_destination else "None"
    debug_caption.text = f"Pos: ({player.x}, {player.y}) | Queue: {queue_count} | Dest: {dest_text}"
    
    # Update movement state debug
    current_dir = key_to_direction(current_move) if current_move else "None"
    queued_dir = key_to_direction(move_queue[0]) if move_queue else "None"
    move_debug_caption.text = f"Moving: {is_moving} | Current: {current_dir} | Queued: {queued_dir}"

# Animation completion callback
def movement_complete(anim, target):
    """Called when movement animation completes"""
    global is_moving, move_queue, current_destination, current_move
    global player_anim_x, player_anim_y
    
    # Clear movement state
    is_moving = False
    current_move = None
    current_destination = None
    # Clear animation references
    player_anim_x = None
    player_anim_y = None
    
    # Ensure grid is centered on final position
    grid.center = (player.x + 0.5) * 16, (player.y + 0.5) * 16
    
    # Check if there's a queued move
    if move_queue:
        # Pop the next move from the queue
        next_move = move_queue.pop(0)
        # Process it like a fresh input
        process_move(next_move)
    
    update_debug_display()

motion_speed = 0.30 # seconds per tile

def process_move(key):
    """Process a move based on the key"""
    global is_moving, current_move, current_destination, move_queue
    global player_anim_x, player_anim_y, grid_anim_x, grid_anim_y
    
    # If already moving, just update the queue
    if is_moving:
        # Clear queue and add new move (only keep 1 queued move)
        move_queue.clear()
        move_queue.append(key)
        update_debug_display()
        return
    
    # Calculate new position from current position
    px, py = int(player.x), int(player.y)
    new_x, new_y = px, py
    
    # Calculate new position based on key press (only one tile movement)
    if key == "W" or key == "Up":
        new_y -= 1
    elif key == "S" or key == "Down":
        new_y += 1
    elif key == "A" or key == "Left":
        new_x -= 1
    elif key == "D" or key == "Right":
        new_x += 1
    
    # Start the move if position changed
    if new_x != px or new_y != py:
        is_moving = True
        current_move = key
        current_destination = (new_x, new_y)
        
        # Only animate a single axis, same callback from either
        if new_x != px:
            player_anim_x = mcrfpy.Animation("x", float(new_x), motion_speed, "easeInOutQuad", callback=movement_complete)
            player_anim_x.start(player)
        elif new_y != py:
            player_anim_y = mcrfpy.Animation("y", float(new_y), motion_speed, "easeInOutQuad", callback=movement_complete)
            player_anim_y.start(player)
        
        # Animate grid center to follow player
        grid_anim_x = mcrfpy.Animation("center_x", (new_x + 0.5) * 16, motion_speed, "linear")
        grid_anim_y = mcrfpy.Animation("center_y", (new_y + 0.5) * 16, motion_speed, "linear")
        grid_anim_x.start(grid)
        grid_anim_y.start(grid)
        
        update_debug_display()

# Define keyboard handler
def handle_keys(key, state):
    """Handle keyboard input to move the player"""
    if state == "start":
        # Only process movement keys
        if key in ["W", "Up", "S", "Down", "A", "Left", "D", "Right"]:
            process_move(key)

# Register the keyboard handler
mcrfpy.keypressScene(handle_keys)

# Add UI elements
title = mcrfpy.Caption((320, 10),
    text="McRogueFace Tutorial - Part 2 Enhanced",
)
title.fill_color = mcrfpy.Color(255, 255, 255, 255)
mcrfpy.sceneUI("tutorial").append(title)

instructions = mcrfpy.Caption((150, 750),
    text="One-move queue system with animation callbacks!",
)
instructions.font_size=18
instructions.fill_color = mcrfpy.Color(200, 200, 200, 255)
mcrfpy.sceneUI("tutorial").append(instructions)

print("Tutorial Part 2 Enhanced loaded!")
print(f"Player entity created at grid position (4, 4)")
print("Movement now uses animation callbacks to prevent race conditions!")
print("Use WASD or Arrow keys to move!")
```

### Key Concepts

**1. Animation System**:
   - Create with `mcrfpy.Animation(property, target_value, duration, easing, callback)`
   - Start with `animation.start(target_object)`
   - Callbacks run when animation completes
   - Store animation references to prevent garbage collection

**2. Movement Queue**:
   - Track `is_moving` state to prevent overlapping animations
   - Queue at most one move for responsive controls
   - Process queued moves in the callback

**3. Animation Properties**:
   - Entity position: `"x"` and `"y"` (in tiles)
   - Grid camera: `"center_x"` and `"center_y"` (in pixels)
   - Available easings: "linear", "easeInQuad", "easeOutQuad", "easeInOutQuad", etc.

**4. Debugging State**:
   - Display current position, destination, and queue
   - Essential for understanding complex movement logic
   - Update display whenever state changes

---

## Part 3: Building a Complete Game

Now let's combine everything into a simple but complete game with:
- Collision detection
- Multiple entity types
- Game objectives
- Sound effects
- Win/lose conditions

```python
"""
McRogueFace Tutorial - Part 3: Complete Game Example

A simple Sokoban-style puzzle game demonstrating:
- Collision detection
- Multiple entity types
- Game state management
- Sound effects
- Win conditions
"""
import mcrfpy
import random

# Game constants
GRID_WIDTH, GRID_HEIGHT = 15, 12
TILE_SIZE = 16
ZOOM = 3.0

# Tile types
FLOOR = 0
WALL = 1
GOAL = 2

# Entity types
PLAYER_SPRITE = 0
BOX_SPRITE = 1
BOX_ON_GOAL_SPRITE = 2

# Game state
class GameState:
    def __init__(self):
        self.moves = 0
        self.boxes_on_goals = 0
        self.total_goals = 0
        self.level_complete = False
        self.player = None
        self.boxes = []
        self.goals = []

game_state = GameState()

# Create scene
mcrfpy.createScene("game")
mcrfpy.setScene("game")

# Load assets
tile_texture = mcrfpy.Texture("assets/sokoban_tiles.png", TILE_SIZE, TILE_SIZE)
entity_texture = mcrfpy.Texture("assets/sokoban_entities.png", TILE_SIZE, TILE_SIZE)

# Create sound effects
mcrfpy.createSoundBuffer("move", "assets/sounds/step.wav")
mcrfpy.createSoundBuffer("push", "assets/sounds/push.wav")
mcrfpy.createSoundBuffer("goal", "assets/sounds/success.wav")
mcrfpy.createSoundBuffer("win", "assets/sounds/victory.wav")

# Set volume
mcrfpy.setVolume("move", 0.5)
mcrfpy.setVolume("push", 0.7)
mcrfpy.setVolume("goal", 0.8)
mcrfpy.setVolume("win", 1.0)

# Create grid
grid_size = GRID_WIDTH * ZOOM * TILE_SIZE, GRID_HEIGHT * ZOOM * TILE_SIZE
grid_position = (1024 - grid_size[0]) / 2, (768 - grid_size[1]) / 2

grid = mcrfpy.Grid(
    pos=grid_position,
    grid_size=(GRID_WIDTH, GRID_HEIGHT),
    texture=tile_texture,
    size=grid_size,
)
grid.zoom = ZOOM

# Level data (# = wall, . = floor, @ = player, $ = box, * = goal)
level = [
    "#############",
    "#...........#",
    "#.###...###.#",
    "#...........#",
    "#..$..@..$..#",
    "#...........#",
    "#..**..**...#",
    "#...........#",
    "#.###...###.#",
    "#...........#",
    "#############",
]

# Parse level
for y, row in enumerate(level):
    for x, char in enumerate(row):
        # Set tile
        if char == '#':
            tile = WALL
        elif char == '*':
            tile = GOAL
            game_state.goals.append((x, y))
            game_state.total_goals += 1
        else:
            tile = FLOOR
        
        point = grid.at(x, y)
        if point:
            point.tilesprite = tile
        
        # Create entities
        if char == '@':
            # Player
            game_state.player = mcrfpy.Entity(
                (x, y),
                texture=entity_texture,
                sprite_index=PLAYER_SPRITE
            )
            grid.entities.append(game_state.player)
        
        elif char == '$':
            # Box
            box = mcrfpy.Entity(
                (x, y),
                texture=entity_texture,
                sprite_index=BOX_SPRITE
            )
            grid.entities.append(box)
            game_state.boxes.append(box)

# Add grid to scene
mcrfpy.sceneUI("game").append(grid)

# Center camera on level
grid.center = (GRID_WIDTH/2.0) * TILE_SIZE, (GRID_HEIGHT/2.0) * TILE_SIZE

# UI Elements
title = mcrfpy.Caption((350, 20), text="Sokoban Tutorial")
title.font_size = 24
title.fill_color = mcrfpy.Color(255, 255, 255, 255)
mcrfpy.sceneUI("game").append(title)

moves_text = mcrfpy.Caption((20, 60), text="Moves: 0")
moves_text.font_size = 18
moves_text.fill_color = mcrfpy.Color(200, 200, 200, 255)
mcrfpy.sceneUI("game").append(moves_text)

goals_text = mcrfpy.Caption((20, 90), text=f"Goals: 0/{game_state.total_goals}")
goals_text.font_size = 18
goals_text.fill_color = mcrfpy.Color(200, 200, 200, 255)
mcrfpy.sceneUI("game").append(goals_text)

instructions = mcrfpy.Caption((512, 750), text="Push all boxes onto the goals!")
instructions.font_size = 20
instructions.fill_color = mcrfpy.Color(200, 200, 200, 255)
instructions.centered = True
mcrfpy.sceneUI("game").append(instructions)

win_text = mcrfpy.Caption((512, 400), text="Level Complete!")
win_text.font_size = 48
win_text.fill_color = mcrfpy.Color(255, 215, 0, 255)
win_text.centered = True
win_text.visible = False
mcrfpy.sceneUI("game").append(win_text)

def get_tile_at(x, y):
    """Get the tile type at grid position"""
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        return WALL
    
    point = grid.at(x, y)
    if point:
        return point.tilesprite
    return WALL

def get_entity_at(x, y, exclude=None):
    """Find any entity at the given position"""
    for entity in grid.entities:
        if entity != exclude and int(entity.x) == x and int(entity.y) == y:
            return entity
    return None

def is_box(entity):
    """Check if an entity is a box"""
    return entity in game_state.boxes

def update_box_sprites():
    """Update box sprites based on whether they're on goals"""
    boxes_on_goals = 0
    
    for box in game_state.boxes:
        x, y = int(box.x), int(box.y)
        if (x, y) in game_state.goals:
            box.sprite_index = BOX_ON_GOAL_SPRITE
            boxes_on_goals += 1
        else:
            box.sprite_index = BOX_SPRITE
    
    game_state.boxes_on_goals = boxes_on_goals
    goals_text.text = f"Goals: {boxes_on_goals}/{game_state.total_goals}"
    
    # Check win condition
    if boxes_on_goals == game_state.total_goals and not game_state.level_complete:
        game_state.level_complete = True
        win_text.visible = True
        mcrfpy.playSound("win")
        instructions.text = "Congratulations! Press R to restart."

def move_entity(entity, dx, dy):
    """Try to move an entity, returns True if successful"""
    new_x = int(entity.x) + dx
    new_y = int(entity.y) + dy
    
    # Check tile collision
    tile = get_tile_at(new_x, new_y)
    if tile == WALL:
        return False
    
    # Check entity collision
    blocking_entity = get_entity_at(new_x, new_y, exclude=entity)
    
    if blocking_entity:
        if is_box(blocking_entity):
            # Try to push the box
            if move_entity(blocking_entity, dx, dy):
                entity.x = new_x
                entity.y = new_y
                return True
            else:
                return False
        else:
            # Can't move through other entities
            return False
    
    # Move is valid
    entity.x = new_x
    entity.y = new_y
    return True

def handle_input(key, state):
    """Handle player input"""
    if state != "start" or game_state.level_complete:
        return
    
    # Get movement direction
    dx, dy = 0, 0
    if key == "W" or key == "Up":
        dy = -1
    elif key == "S" or key == "Down":
        dy = 1
    elif key == "A" or key == "Left":
        dx = -1
    elif key == "D" or key == "Right":
        dx = 1
    elif key == "R":
        # Restart level
        restart_level()
        return
    else:
        return
    
    # Try to move player
    old_x, old_y = int(game_state.player.x), int(game_state.player.y)
    
    if move_entity(game_state.player, dx, dy):
        game_state.moves += 1
        moves_text.text = f"Moves: {game_state.moves}"
        
        # Check if we pushed a box
        new_x, new_y = int(game_state.player.x), int(game_state.player.y)
        if abs(new_x - old_x) + abs(new_y - old_y) > 0:
            # Check if there's a box at our new position (we pushed through it)
            pushed_box = False
            for box in game_state.boxes:
                if (int(box.x) == new_x + dx and 
                    int(box.y) == new_y + dy):
                    pushed_box = True
                    break
            
            if pushed_box:
                mcrfpy.playSound("push")
                # Check if box is now on goal
                update_box_sprites()
                if game_state.boxes_on_goals > 0:
                    mcrfpy.playSound("goal")
            else:
                mcrfpy.playSound("move")

def restart_level():
    """Reset the level to initial state"""
    # Reset game state
    game_state.moves = 0
    game_state.boxes_on_goals = 0
    game_state.level_complete = False
    
    # Reset UI
    moves_text.text = "Moves: 0"
    goals_text.text = f"Goals: 0/{game_state.total_goals}"
    win_text.visible = False
    instructions.text = "Push all boxes onto the goals!"
    
    # Reset entity positions
    entity_index = 0
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == '@':
                game_state.player.x = x
                game_state.player.y = y
            elif char == '$':
                if entity_index < len(game_state.boxes):
                    game_state.boxes[entity_index].x = x
                    game_state.boxes[entity_index].y = y
                    game_state.boxes[entity_index].sprite_index = BOX_SPRITE
                    entity_index += 1

# Register input handler
mcrfpy.keypressScene(handle_input)

# Initial sprite update
update_box_sprites()

print("Sokoban Tutorial loaded!")
print("Push all boxes onto the goal tiles!")
print("Use WASD or Arrow keys to move, R to restart")
```

### Key Concepts in the Complete Game

**1. Game State Management**:
   - Track game variables in a class or globals
   - Update UI elements when state changes
   - Check win/lose conditions after each action

**2. Collision Detection**:
   - Check tile collisions first (walls)
   - Then check entity collisions
   - Handle special cases (pushing boxes)

**3. Entity Interactions**:
   - Use helper functions to find entities at positions
   - Recursive movement for pushing
   - Update visual state based on game logic

**4. Sound Effects**:
   - Create buffers with `mcrfpy.createSoundBuffer()`
   - Play with `mcrfpy.playSound()`
   - Use different sounds for different actions

**5. Level Design**:
   - Parse level from string data
   - Separate tiles from entities
   - Track special positions (goals)

---

## Next Steps

Now that you understand the basics, you can:

1. **Extend the examples**: Add more features like enemies, items, or multiple levels
2. **Study the game scripts**: Look at `src/scripts/` for more advanced examples
3. **Read the API Reference**: Learn about additional features not covered here
4. **Create your own game**: Start simple and build up complexity

### Tips for Success

- **Start simple**: Get basic functionality working before adding complexity
- **Use timers**: For animations, spawning, and any time-based logic
- **Debug visually**: Create debug UI elements to display game state
- **Test frequently**: Small, incremental changes are easier to debug
- **Read the error messages**: Python exceptions tell you exactly what went wrong

### Common Patterns

**Game Loop with Timer**:
```python
def game_update(runtime):
    # Update game logic
    update_enemies()
    update_particles()
    check_collisions()

mcrfpy.setTimer("gameloop", game_update, 16)  # ~60 FPS
```

**State Machine**:
```python
class GameStates:
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

current_state = GameStates.MENU

def handle_input(key, state):
    if current_state == GameStates.MENU:
        handle_menu_input(key, state)
    elif current_state == GameStates.PLAYING:
        handle_game_input(key, state)
    # etc...
```

**Entity Component Pattern**:
```python
class Entity:
    def __init__(self, x, y):
        self.sprite = mcrfpy.Entity((x, y))
        self.components = {}
    
    def add_component(self, name, component):
        self.components[name] = component
        component.entity = self
    
    def update(self, dt):
        for component in self.components.values():
            component.update(dt)
```

Happy game development with McRogueFace!