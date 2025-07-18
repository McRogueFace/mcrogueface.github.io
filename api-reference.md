# McRogueFace API Reference

**Make 2D games with Python** - No C++ required!

---

[**Source Code**](https://github.com/jmccardle/McRogueFace) • [**Downloads**](https://github.com/jmccardle/McRogueFace/releases) • [**Quickstart**](https://mcrogueface.github.io/quickstart) • [**Tutorials**](https://mcrogueface.github.io/tutorials) • **[API Reference](https://mcrogueface.github.io/api-reference)** • [**Cookbook**](https://mcrogueface.github.io/cookbook) • [**C++ Extensions**](https://mcrogueface.github.io/extending-cpp)

---

This is the complete API reference for the McRogueFace game engine. All functionality is accessed through the `mcrfpy` module.

```python
import mcrfpy
```

## Table of Contents

1. [Core Functions](#core-functions)
   - [Scene Management](#scene-management)
   - [Timer System](#timer-system)
   - [Audio Functions](#audio-functions)
   - [Window Control](#window-control)
   - [Input Handling](#input-handling)
2. [UI Classes](#ui-classes)
   - [Caption](#caption)
   - [Sprite](#sprite)
   - [Frame](#frame)
   - [Grid](#grid)
3. [Collections](#collections)
   - [UICollection](#uicollection)
   - [EntityCollection](#entitycollection)
4. [Entity System](#entity-system)
   - [Entity](#entity)
   - [GridPoint](#gridpoint)
   - [GridPointState](#gridpointstate)
5. [Automation API](#automation-api)
   - [Screenshot](#screenshot)
   - [Mouse Functions](#mouse-functions)
   - [Keyboard Functions](#keyboard-functions)
6. [Type Classes](#type-classes)
   - [Color](#color)
   - [Vector](#vector)
   - [Font](#font)
   - [Texture](#texture)
7. [Constants and Module Attributes](#constants-and-module-attributes)

## Core Functions

### Scene Management

**⚠️ Caution:** Scene Management is currently being transitioned in McRogueFace. `createScene` and `setScene` are some of the oldest methods in the API, from when this game engine was a fork of [COMP 4300 taught by Dave Churchill, free on Youtube](https://www.youtube.com/playlist?list=PL_xRyXins84_Sq7yZkxGP_MgYAH-Zo8Uu). a `Scene` object is available, and will be the only way to manage scenes in the near future.

#### `createScene(name: str) -> None`

Creates a new empty scene with the given name. Scenes are containers for all game objects and UI elements.

**Parameters:**
- `name` (str): Unique name for the scene

**Returns:** None

**Examples:**
```python
# Create a main menu scene
mcrfpy.createScene("main_menu")

# Create multiple scenes for different game states
mcrfpy.createScene("gameplay")
mcrfpy.createScene("inventory")
mcrfpy.createScene("game_over")

# Scene names can contain underscores, numbers, and letters
mcrfpy.createScene("level_1")
mcrfpy.createScene("boss_fight_arena")
```

**Notes:**
- Scene names must be unique
- Creating a scene with an existing name will raise an error
- Scenes are not automatically set as active after creation

---

#### `setScene(name: str) -> None`

Switches the active scene to the one with the given name. Only one scene can be active at a time.

**Parameters:**
- `name` (str): Name of the scene to activate

**Returns:** None

**Examples:**
```python
# Switch to gameplay scene
mcrfpy.setScene("gameplay")

# Create a scene transition system
def transition_to_scene(scene_name):
    # Fade out effect could go here
    mcrfpy.setScene(scene_name)
    # Fade in effect could go here

transition_to_scene("main_menu")

# Switch scenes based on game state
if player_died:
    mcrfpy.setScene("game_over")
elif level_complete:
    mcrfpy.setScene("level_select")
```

**Notes:**
- The scene must exist before you can set it
- Switching scenes does not destroy the previous scene's contents
- UI elements and entities remain in their scenes when switching

---

#### `currentScene() -> str`

Returns the name of the currently active scene.

**Parameters:** None

**Returns:** str - The name of the active scene

**Examples:**
```python
# Get current scene name
scene = mcrfpy.currentScene()
print(f"Currently in: {scene}")

# Conditional logic based on scene
if mcrfpy.currentScene() == "main_menu":
    # Show menu-specific UI
    pass
elif mcrfpy.currentScene() == "gameplay":
    # Update game logic
    pass

# Debug helper
def debug_scene():
    print(f"Active scene: {mcrfpy.currentScene()}")
    ui = mcrfpy.sceneUI(mcrfpy.currentScene())
    print(f"UI elements: {len(ui)}")
```

**Notes:**
- Always returns a valid scene name
- Useful for conditional logic and debugging

---

#### `sceneUI(name: str) -> UICollection`

Returns the UICollection containing all UI elements (Frame, Caption, Sprite, Grid) in the specified scene.

**Parameters:**
- `name` (str): Name of the scene to get UI from

**Returns:** UICollection - Container of all UI elements in the scene

**Examples:**
```python
# Get all UI elements in current scene
ui = mcrfpy.sceneUI("gameplay")

# Add a new caption to the scene
ui = mcrfpy.sceneUI("main_menu")
title = mcrfpy.Caption("GAME TITLE", mcrfpy.default_font, 100, 50)
ui.append(title)

# Iterate through all UI elements
ui = mcrfpy.sceneUI("hud")
for element in ui:
    if hasattr(element, 'text') and element.text == "Score:":
        element.fill_color = mcrfpy.Color(255, 255, 0)  # Yellow

# Clear all UI from a scene
ui = mcrfpy.sceneUI("temp_scene")
while len(ui) > 0:
    ui.remove(0)
```

**Notes:**
- The returned UICollection is live - changes affect the scene immediately
- Can be used to dynamically add/remove UI elements
- Elements are rendered in the order they appear in the collection

---

### Timer System

**⚠️ Caution:** a `Timer` class is available in the Python API already, and will become the preferred/only way to interact with timers soon.

#### `setTimer(name: str, callback: callable, interval_ms: int) -> None`

Creates a recurring timer that calls the specified function at regular intervals.

**Parameters:**
- `name` (str): Unique identifier for the timer
- `callback` (callable): Function to call when timer fires
- `interval_ms` (int): Interval between calls in milliseconds

**Returns:** None

**Examples:**
```python
# Create a simple timer
def update_game():
    print("Game updated!")
    
mcrfpy.setTimer("game_update", update_game, 16)  # ~60 FPS

# Timer with game logic
enemy_spawn_delay = 3000  # 3 seconds

def spawn_enemy():
    x = random.randint(0, 49)
    y = random.randint(0, 49)
    enemy = Enemy(grid, x, y)
    
mcrfpy.setTimer("enemy_spawner", spawn_enemy, enemy_spawn_delay)

# Timer that modifies itself
spawn_count = 0
def accelerating_spawner():
    global spawn_count
    spawn_count += 1
    spawn_enemy()
    
    # Make spawning faster over time
    new_delay = max(500, 3000 - (spawn_count * 100))
    mcrfpy.delTimer("accelerating")
    mcrfpy.setTimer("accelerating", accelerating_spawner, new_delay)

mcrfpy.setTimer("accelerating", accelerating_spawner, 3000)
```

**Notes:**
- Timer names must be unique - setting a timer with an existing name replaces it
- Timers continue running when switching scenes
- Callback functions should be fast to avoid blocking the game loop
- Minimum practical interval is around 16ms (60 FPS)

---

#### `delTimer(name: str) -> None`

Stops and removes a timer by name.

**Parameters:**
- `name` (str): Name of the timer to remove

**Returns:** None

**Examples:**
```python
# Stop a timer
mcrfpy.delTimer("enemy_spawner")

# Conditional timer removal
if game_over:
    mcrfpy.delTimer("game_update")
    mcrfpy.delTimer("enemy_spawner")
    mcrfpy.delTimer("powerup_timer")

# Timer that removes itself after N calls
call_count = 0
def limited_timer():
    global call_count
    call_count += 1
    print(f"Timer called {call_count} times")
    
    if call_count >= 10:
        mcrfpy.delTimer("limited")
        print("Timer finished")

mcrfpy.setTimer("limited", limited_timer, 1000)
```

**Notes:**
- Deleting a non-existent timer is safe (no error)
- Useful for cleanup when changing game states
- Can be called from within the timer's own callback

---

### Audio Functions

**⚠️ Caution:** The Audio system of McRogueFace will become more object-oriented *soon* (TM).

#### `createSoundBuffer(filename: str) -> int`

Loads a sound effect file and returns its buffer index for playback.

**Parameters:**
- `filename` (str): Path to the sound file (WAV, OGG, FLAC supported)

**Returns:** int - Buffer index for use with playSound()

**Examples:**
```python
# Load sound effects
explosion_sound = mcrfpy.createSoundBuffer("assets/explosion.wav")
coin_sound = mcrfpy.createSoundBuffer("assets/coin_pickup.ogg")
jump_sound = mcrfpy.createSoundBuffer("assets/jump.wav")

# Organize sounds in a dictionary
sounds = {
    'explosion': mcrfpy.createSoundBuffer("assets/explosion.wav"),
    'coin': mcrfpy.createSoundBuffer("assets/coin.ogg"),
    'jump': mcrfpy.createSoundBuffer("assets/jump.wav"),
    'hurt': mcrfpy.createSoundBuffer("assets/hurt.wav"),
    'powerup': mcrfpy.createSoundBuffer("assets/powerup.wav")
}

# Load multiple variations
footstep_sounds = []
for i in range(1, 5):
    sound = mcrfpy.createSoundBuffer(f"assets/footstep{i}.wav")
    footstep_sounds.append(sound)
```

**Notes:**
- Sound files should be in assets/ directory
- Supported formats: WAV, OGG, FLAC
- Returns -1 if loading fails
- Keep buffer indices for later playback

---

#### `playSound(buffer_index: int) -> None`

Plays a loaded sound effect by its buffer index.

**Parameters:**
- `buffer_index` (int): Index returned by createSoundBuffer()

**Returns:** None

**Examples:**
```python
# Simple playback
mcrfpy.playSound(explosion_sound)

# Play from dictionary
def on_coin_collected():
    mcrfpy.playSound(sounds['coin'])
    score += 10

# Random sound variation
def play_footstep():
    sound = random.choice(footstep_sounds)
    mcrfpy.playSound(sound)

# Conditional sound effects
def take_damage(amount):
    global player_health
    player_health -= amount
    
    if player_health <= 0:
        mcrfpy.playSound(sounds['death'])
    else:
        mcrfpy.playSound(sounds['hurt'])
```

**Notes:**
- Multiple sounds can play simultaneously
- Volume is controlled by setSoundVolume()
- Invalid buffer indices are ignored
- Same sound can be played multiple times overlapping

---

#### `loadMusic(filename: str) -> None`

Loads and immediately starts playing background music. Music loops by default.

**Parameters:**
- `filename` (str): Path to the music file (OGG recommended)

**Returns:** None

**Examples:**
```python
# Load and play background music
mcrfpy.loadMusic("assets/music/dungeon_theme.ogg")

# Change music based on game state
def enter_boss_room():
    mcrfpy.loadMusic("assets/music/boss_battle.ogg")
    
def return_to_overworld():
    mcrfpy.loadMusic("assets/music/peaceful_meadow.ogg")

# Music playlist system
playlist = [
    "assets/music/track1.ogg",
    "assets/music/track2.ogg",
    "assets/music/track3.ogg"
]
current_track = 0

def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    mcrfpy.loadMusic(playlist[current_track])
```

**Notes:**
- Only one music track can play at a time
- Loading new music stops the previous track
- Music loops automatically
- Use OGG format for best compatibility

---

#### `setMusicVolume(volume: int) -> None`

Sets the volume level for background music.

**Parameters:**
- `volume` (int): Volume level from 0 (mute) to 100 (maximum)

**Returns:** None

**Examples:**
```python
# Set music to half volume
mcrfpy.setMusicVolume(50)

# Mute music
mcrfpy.setMusicVolume(0)

# Volume slider implementation
def on_music_slider_change(value):
    # value is 0.0 to 1.0 from slider
    volume = int(value * 100)
    mcrfpy.setMusicVolume(volume)

# Fade out effect
def fade_out_music(duration_ms=1000):
    steps = 20
    delay = duration_ms // steps
    current_vol = mcrfpy.getMusicVolume()
    
    def fade_step():
        nonlocal current_vol, steps
        if steps > 0:
            current_vol -= current_vol // steps
            mcrfpy.setMusicVolume(max(0, current_vol))
            steps -= 1
        else:
            mcrfpy.delTimer("fade_out")
    
    mcrfpy.setTimer("fade_out", fade_step, delay)
```

**Notes:**
- Volume changes take effect immediately
- Volume persists between music tracks
- Values outside 0-100 are clamped

---

#### `setSoundVolume(volume: int) -> None`

Sets the volume level for all sound effects.

**Parameters:**
- `volume` (int): Volume level from 0 (mute) to 100 (maximum)

**Returns:** None

**Examples:**
```python
# Set sound effects to 80% volume
mcrfpy.setSoundVolume(80)

# Mute all sound effects
mcrfpy.setSoundVolume(0)

# Separate volume controls
music_volume = 70
sfx_volume = 85

def apply_audio_settings():
    mcrfpy.setMusicVolume(music_volume)
    mcrfpy.setSoundVolume(sfx_volume)

# Dynamic volume based on distance
def play_sound_at_distance(sound_index, distance):
    # Reduce volume based on distance
    max_distance = 20
    if distance < max_distance:
        volume = int(100 * (1 - distance / max_distance))
        old_volume = mcrfpy.getSoundVolume()
        mcrfpy.setSoundVolume(volume)
        mcrfpy.playSound(sound_index)
        mcrfpy.setSoundVolume(old_volume)
```

**Notes:**
- Affects all sound effects globally
- Does not affect music volume
- Changes apply to currently playing sounds

---

#### `getMusicVolume() -> int`

Returns the current music volume setting.

**Parameters:** None

**Returns:** int - Current music volume (0-100)

**Examples:**
```python
# Get current volume
volume = mcrfpy.getMusicVolume()
print(f"Music volume: {volume}%")

# Toggle mute
previous_volume = 50

def toggle_music_mute():
    global previous_volume
    current = mcrfpy.getMusicVolume()
    
    if current > 0:
        previous_volume = current
        mcrfpy.setMusicVolume(0)
    else:
        mcrfpy.setMusicVolume(previous_volume)

# Save volume settings
def save_settings():
    settings = {
        'music_volume': mcrfpy.getMusicVolume(),
        'sound_volume': mcrfpy.getSoundVolume()
    }
    # Save to file...
```

**Notes:**
- Returns value between 0 and 100
- Useful for UI sliders and settings menus

---

#### `getSoundVolume() -> int`

Returns the current sound effects volume setting.

**Parameters:** None

**Returns:** int - Current sound volume (0-100)

**Examples:**
```python
# Display current volume
volume = mcrfpy.getSoundVolume()
volume_text.text = f"SFX Volume: {volume}%"

# Volume up/down controls
def increase_sfx_volume():
    current = mcrfpy.getSoundVolume()
    new_volume = min(100, current + 10)
    mcrfpy.setSoundVolume(new_volume)

def decrease_sfx_volume():
    current = mcrfpy.getSoundVolume()
    new_volume = max(0, current - 10)
    mcrfpy.setSoundVolume(new_volume)

# Audio debugging
def debug_audio():
    print(f"Music: {mcrfpy.getMusicVolume()}%")
    print(f"SFX: {mcrfpy.getSoundVolume()}%")
```

**Notes:**
- Returns value between 0 and 100
- Independent from music volume

---

### Window Control

#### `exit() -> None`

Closes the game window and exits the application cleanly.

**Parameters:** None

**Returns:** None

**Examples:**
```python
# Simple exit
mcrfpy.exit()

# Exit with confirmation
def confirm_exit():
    # Show confirmation dialog
    if user_confirmed:
        mcrfpy.exit()

# Exit on escape key
def on_key_press(key):
    if key == 27:  # Escape key
        mcrfpy.exit()

# Cleanup before exit
def quit_game():
    save_game_state()
    stop_all_timers()
    mcrfpy.exit()
```

**Notes:**
- Immediately closes the window
- Cleans up resources automatically
- Cannot be cancelled once called

---

#### `setScale(multiplier: float) -> None`

Resizes the game window by the specified multiplier. Base resolution is 1024x768.

**Parameters:**
- `multiplier` (float): Scale factor between 0.2 and 4.0

**Returns:** None

**Examples:**
```python
# Double the window size
mcrfpy.setScale(2.0)  # 2048x1536

# Half size window
mcrfpy.setScale(0.5)  # 512x384

# Fullscreen-like (depends on monitor)
mcrfpy.setScale(2.5)  # 2560x1920

# Resolution presets
resolutions = {
    'small': 0.75,
    'normal': 1.0,
    'large': 1.5,
    'huge': 2.0
}

def set_resolution(preset):
    mcrfpy.setScale(resolutions[preset])
```

**Notes:**
- Base resolution is always 1024x768
- Values outside 0.2-4.0 are clamped
- Window is recreated, which may affect performance briefly
- UI positions remain the same (scaled with window)

---

### Input Handling

#### `keypressScene(callback: callable) -> None`

Sets a function to handle keyboard input for the current scene. The callback receives the key code when a key is pressed.

**Parameters:**
- `callback` (callable): Function that takes one parameter (key_code: int)

**Returns:** None

**Examples:**
```python
# Basic keyboard handler
def handle_keypress(key, state):
    print(f"Key pressed: {key}")
    
    if state != "start": # can also be "end"
        return # if you're not tracking held/released keys, you can probably drop "end" events

    if key == 'W':
        player.move_up()
    elif key == 'A':
        player.move_left()
    elif key == 'S':
        player.move_down()
    elif key == 'D':
        player.move_right()

mcrfpy.keypressScene(handle_keypress)
```

**Notes:**
- Only one handler per scene. `keypressScene` changes the active scene's keypress handler; this will be fixed when `Scene` objects are finished
- Key codes are SFML key name strings (not ASCII for special keys)
- Setting a new handler replaces the previous one

---

## UI Classes

### Caption

Text display element for UI labels, titles, and dynamic text.

#### Constructor

```python
Caption(text: str, font: Font = None, x: float = 0, y: float = 0) -> Caption
```

**Parameters:**
- `text` (str): The text to display
- `font` (Font, optional): Font to use (defaults to mcrfpy.default_font)
- `x` (float, optional): X position (default 0)
- `y` (float, optional): Y position (default 0)

**Properties:**
- `text` (str): The displayed text
- `x` (float): X position
- `y` (float): Y position
- `pos` (Vector): Position as a Vector object
- `fill_color` (Color): Text color
- `outline_color` (Color): Text outline color
- `outline` (float): Outline thickness in pixels
- `click` (callable): Click handler function

**Examples:**
```python
# Basic caption
title = mcrfpy.Caption("Game Title", mcrfpy.default_font, 400, 100)
title.fill_color = mcrfpy.Color(255, 255, 0)  # Yellow text

# Score display
score_text = mcrfpy.Caption("Score: 0", mcrfpy.default_font, 10, 10)
score_text.fill_color = mcrfpy.Color(255, 255, 255)
score_text.outline = 2
score_text.outline_color = mcrfpy.Color(0, 0, 0)

# Update score dynamically
def update_score(points):
    global score
    score += points
    score_text.text = f"Score: {score}"

# Clickable text button
start_button = mcrfpy.Caption("Start Game", mcrfpy.default_font, 400, 300)
start_button.fill_color = mcrfpy.Color(0, 255, 0)

def on_start_click(x, y, button, action):
    if button == 0 and action == 1:  # Left click release
        mcrfpy.setScene("gameplay")

start_button.click = on_start_click

# Animated text
def pulse_text():
    # Pulse between white and red
    if title.fill_color.r == 255 and title.fill_color.g == 255:
        title.fill_color = mcrfpy.Color(255, 0, 0)
    else:
        title.fill_color = mcrfpy.Color(255, 255, 255)

mcrfpy.setTimer("pulse", pulse_text, 500)
```

**Common Pitfalls:**
- Text position is top-left corner of the text
- Outline can make text hard to read if too thick
- Click handlers fire for both press and release
- Very long text may extend outside screen bounds

---

### Sprite

Single sprite/image display element for icons, decorations, and simple graphics.

#### Constructor

```python
Sprite(texture: Texture, sprite_index: int = 0, x: float = 0, y: float = 0, scale: float = 1.0) -> Sprite
```

**Parameters:**
- `texture` (Texture): The texture containing the sprite
- `sprite_index` (int, optional): Which sprite in the texture (default 0)
- `x` (float, optional): X position (default 0)
- `y` (float, optional): Y position (default 0)
- `scale` (float, optional): Size multiplier (default 1.0)

**Properties:**
- `x` (float): X position
- `y` (float): Y position
- `scale` (float): Size multiplier
- `sprite_number` (int): Index of the sprite in the texture
- `texture` (Texture, read-only): The texture being used
- `click` (callable): Click handler function

**Examples:**
```python
# Load texture and create sprite
ui_texture = mcrfpy.Texture("assets/ui_icons.png", 32, 32)
heart_icon = mcrfpy.Sprite(ui_texture, 0, 10, 10, 2.0)  # 2x scale

# Animated sprite
coin_sprite = mcrfpy.Sprite(ui_texture, 16, 100, 100)
coin_frames = [16, 17, 18, 19]  # Animation frames
current_frame = 0

def animate_coin():
    global current_frame
    current_frame = (current_frame + 1) % len(coin_frames)
    coin_sprite.sprite_number = coin_frames[current_frame]

mcrfpy.setTimer("coin_anim", animate_coin, 100)

# Clickable inventory slots
inventory_slots = []
for i in range(10):
    slot = mcrfpy.Sprite(ui_texture, 32, 50 + i * 40, 400)
    
    def make_click_handler(slot_index):
        def handler(x, y, button, action):
            if button == 0 and action == 1:
                use_item(slot_index)
        return handler
    
    slot.click = make_click_handler(i)
    inventory_slots.append(slot)

# Button with hover effect
button_sprite = mcrfpy.Sprite(ui_texture, 64, 300, 200, 1.5)
button_normal = 64
button_hover = 65

def on_button_hover(x, y, button, action):
    if action == 0:  # Mouse moved
        button_sprite.sprite_number = button_hover

button_sprite.click = on_button_hover
```

**Common Pitfalls:**
- Sprite indices must be valid for the texture (0 to texture sprite count - 1)
- Scale affects click detection area
- Cannot change texture after creation (create new Sprite instead)
- Position is top-left corner of the sprite

---

### Frame

Container element that can hold other UI elements and provide backgrounds.

#### Constructor

```python
Frame(x: float, y: float, w: float, h: float) -> Frame
```

**Parameters:**
- `x` (float): X position
- `y` (float): Y position  
- `w` (float): Width
- `h` (float): Height

**Properties:**
- `x` (float): X position
- `y` (float): Y position
- `w` (float): Width
- `h` (float): Height
- `fill_color` (Color): Background color
- `outline_color` (Color): Border color
- `outline` (float): Border thickness in pixels
- `children` (UICollection): Child UI elements
- `click` (callable): Click handler function

**Examples:**
```python
# Basic panel
panel = mcrfpy.Frame(100, 100, 400, 300)
panel.fill_color = mcrfpy.Color(50, 50, 50, 200)  # Semi-transparent gray
panel.outline = 2
panel.outline_color = mcrfpy.Color(255, 255, 255)

# Inventory window
inventory_frame = mcrfpy.Frame(200, 150, 600, 400)
inventory_frame.fill_color = mcrfpy.Color(139, 69, 19)  # Brown
inventory_frame.outline = 4
inventory_frame.outline_color = mcrfpy.Color(255, 215, 0)  # Gold

# Add title to inventory
inv_title = mcrfpy.Caption("Inventory", mcrfpy.default_font, 450, 170)
inventory_frame.children.append(inv_title)

# Dialog box with text
dialog = mcrfpy.Frame(100, 500, 824, 200)
dialog.fill_color = mcrfpy.Color(0, 0, 0, 230)
dialog.outline = 3
dialog.outline_color = mcrfpy.Color(100, 100, 255)

dialog_text = mcrfpy.Caption("", mcrfpy.default_font, 120, 520)
dialog_text.fill_color = mcrfpy.Color(255, 255, 255)
dialog.children.append(dialog_text)

def show_dialog(text):
    dialog_text.text = text
    ui.append(dialog)

# Draggable window
dragging = False
drag_offset = (0, 0)

def on_window_click(x, y, button, action):
    global dragging, drag_offset
    
    if button == 0:  # Left mouse
        if action == 0:  # Pressed
            dragging = True
            drag_offset = (x - panel.x, y - panel.y)
        else:  # Released
            dragging = False

def on_mouse_move(x, y):
    if dragging:
        panel.x = x - drag_offset[0]
        panel.y = y - drag_offset[1]

panel.click = on_window_click
```

**Common Pitfalls:**
- Children positions are absolute, not relative to frame
- Frame click handler receives screen coordinates
- Transparent fill_color still captures clicks
- Children are drawn in order (last child on top)

---

### Grid

Tile-based game world display with camera controls and entity management.

#### Constructor

```python
Grid(grid_x: int, grid_y: int, texture: Texture, x: float, y: float, w: float, h: float) -> Grid
```

**Parameters:**
- `grid_x` (int): Width of grid in tiles
- `grid_y` (int): Height of grid in tiles
- `texture` (Texture): Texture for rendering tiles
- `x` (float): Screen X position
- `y` (float): Screen Y position
- `w` (float): Display width in pixels
- `h` (float): Display height in pixels

**Properties:**
- `grid_size` (tuple, read-only): Grid dimensions as (width, height)
- `position` (Vector): Screen position
- `size` (Vector): Display size
- `x`, `y`, `w`, `h` (float): Individual position/size components
- `center` (tuple): Camera center as (x, y) in grid coordinates
- `center_x`, `center_y` (float): Individual camera center components
- `zoom` (float): Camera zoom level (1.0 = normal)
- `texture` (Texture, read-only): Texture used for tiles
- `entities` (EntityCollection): Entities on this grid
- `click` (callable): Click handler (receives grid coordinates)

**Methods:**
- `at(x: int, y: int) -> GridPoint`: Get the GridPoint at the specified coordinates

**Examples:**
```python
# Create a game world
world_texture = mcrfpy.Texture("assets/tileset.png", 16, 16)
game_grid = mcrfpy.Grid(100, 100, world_texture, 0, 0, 1024, 768)

# Set up tiles
for x in range(100):
    for y in range(100):
        point = game_grid.at(x, y)
        if y > 50:
            point.tilesprite = 1  # Grass
            point.walkable = True
        else:
            point.tilesprite = 2  # Stone
            point.walkable = False

# Camera following player
def update_camera():
    # Center camera on player
    game_grid.center = player.pos
    
    # Smooth camera with offset
    target_x = player.pos[0]
    target_y = player.pos[1] - 5  # Look ahead
    
    current_x = game_grid.center_x
    current_y = game_grid.center_y
    
    # Lerp to target
    game_grid.center_x = current_x + (target_x - current_x) * 0.1
    game_grid.center_y = current_y + (target_y - current_y) * 0.1

# Click to move system
def on_grid_click(x, y, button, action):
    if button == 0 and action == 1:  # Left click release
        # x, y are grid coordinates
        if game_grid.at(x, y).walkable:
            player.move_to(x, y)
        else:
            print(f"Can't walk to ({x}, {y})")

game_grid.click = on_grid_click

# Minimap (second grid showing same data)
minimap = mcrfpy.Grid(100, 100, world_texture, 824, 10, 200, 200)
minimap.zoom = 0.1  # See more area

# Fog of war
def update_visibility():
    px, py = player.pos
    sight_range = 10
    
    for x in range(100):
        for y in range(100):
            dist = abs(x - px) + abs(y - py)  # Manhattan distance
            point = game_grid.at(x, y)
            
            if dist <= sight_range:
                point.color_overlay = mcrfpy.Color(255, 255, 255, 0)  # Clear
            else:
                point.color_overlay = mcrfpy.Color(0, 0, 0, 200)  # Dark
```

**Common Pitfalls:**
- Grid coordinates start at (0, 0) in top-left
- Null texture causes errors - use mcrfpy.Texture("", 1, 1) for invisible grid
- Camera center can go outside grid bounds
- Click coordinates are grid tiles, not pixels

---

## Collections

### UICollection

Container for UI elements (Frame, Caption, Sprite, Grid) in a scene.

**Methods:**
- `append(element)`: Add a UI element to the collection
- `remove(index: int)`: Remove element at the specified index
- `remove(element)`: Remove the specified element
- `__len__() -> int`: Get number of elements
- `__getitem__(index: int)`: Get element at index (supports negative indexing)
- `__iter__()`: Iterate through elements

**Examples:**
```python
# Get scene UI collection
ui = mcrfpy.sceneUI("main_menu")

# Add elements
title = mcrfpy.Caption("My Game", mcrfpy.default_font, 400, 100)
ui.append(title)

background = mcrfpy.Frame(0, 0, 1024, 768)
background.fill_color = mcrfpy.Color(20, 20, 40)
ui.append(background)

# Reorder - put background behind title
ui.remove(background)
ui.insert(0, background)  # Not yet implemented, use remove/append

# Access elements
print(f"UI has {len(ui)} elements")
first_element = ui[0]
last_element = ui[-1]

# Iterate through all elements
for element in ui:
    if isinstance(element, mcrfpy.Caption):
        element.fill_color = mcrfpy.Color(255, 255, 255)

# Find specific element
def find_by_text(ui, text):
    for element in ui:
        if hasattr(element, 'text') and element.text == text:
            return element
    return None

score_label = find_by_text(ui, "Score:")

# Clear all UI
while len(ui) > 0:
    ui.remove(0)

# Layer management
def bring_to_front(element):
    ui = mcrfpy.sceneUI(mcrfpy.currentScene())
    ui.remove(element)
    ui.append(element)  # Now on top
```

**Common Pitfalls:**
- Removing elements while iterating can cause issues
- No insert() method - must remove and re-add for ordering
- Elements render in order (first = bottom, last = top)
- Modifying collection affects scene immediately

---

### EntityCollection

**⚠️  EntityCollection cannot be instantiated.** Use a list, dictionary, or any other container to manage your entities. `EntityCollection` is the interface for C++ to handle rendering for entities that are placed on a Grid.

Container for Entity objects on a Grid.

**Methods:**
- `append(entity: Entity)`: Add an entity to the grid
- `remove(index: int)`: Remove entity at index
- `remove(entity: Entity)`: Remove specific entity
- `extend(entities: list)`: Add multiple entities at once
- `__len__() -> int`: Get number of entities
- `__getitem__(index: int)`: Get entity at index
- `__iter__()`: Iterate through entities

**Examples:**
```python
# Access grid entities
entities = game_grid.entities

# Add entities
player = mcrfpy.Entity((10, 10), texture, 0)
entities.append(player)

# Add multiple enemies
enemies = []
for i in range(10):
    x = random.randint(0, 99)
    y = random.randint(0, 99)
    enemy = mcrfpy.Entity((x, y), texture, 1)
    enemies.append(enemy)

entities.extend(enemies)

# Remove entity by reference
entities.remove(player)

# Remove by index
if len(entities) > 0:
    entities.remove(0)  # Remove first entity

# Find entities at position
def entities_at(x, y):
    found = []
    for entity in entities:
        if entity.pos == (x, y):
            found.append(entity)
    return found

# Count entity types
enemy_count = 0
for entity in entities:
    if entity.sprite_number == 1:  # Enemy sprite
        enemy_count += 1

print(f"Enemies remaining: {enemy_count}")

# Process all entities
for entity in entities:
    # Update AI, animations, etc.
    if hasattr(entity, 'update'):
        entity.update()

# Clear all entities
while len(entities) > 0:
    entities.remove(0)
```

**Common Pitfalls:**
- Entities must be created with a parent grid
- Removing entities during iteration requires care
- Entity positions are integer grid coordinates
- Same entity cannot be in multiple grids

---

## Entity System

### Entity

Game object that exists on a Grid with position and sprite.

#### Constructor

```python
Entity(pos: tuple, texture: Texture, sprite_index: int, grid: Grid = None) -> Entity
```

**Parameters:**
- `pos` (tuple): Starting position as (x, y) integers
- `texture` (Texture): Texture for the entity sprite
- `sprite_index` (int): Which sprite to display
- `grid` (Grid, optional): Parent grid (deprecated, add to grid.entities instead)

**Properties:**
- `pos` (tuple): Grid position as (x, y) integers
- `draw_pos` (tuple): Smooth position as (x, y) floats for animation
- `sprite_number` (int): Current sprite index
- `gridstate` (list, read-only): List of GridPointState objects for visibility

**Methods:**
- `at(x: int, y: int) -> GridPointState`: Get visibility state at grid position
- `index() -> int`: Get this entity's index in its parent collection

**Examples:**
```python
# Create entities
texture = mcrfpy.Texture("assets/characters.png", 16, 16)
player = mcrfpy.Entity((5, 5), texture, 0)
game_grid.entities.append(player)

# Movement
def move_entity(entity, dx, dy):
    old_x, old_y = entity.pos
    new_x = old_x + dx
    new_y = old_y + dy
    
    # Check bounds
    if 0 <= new_x < 100 and 0 <= new_y < 100:
        # Check walkable
        if game_grid.at(new_x, new_y).walkable:
            entity.pos = (new_x, new_y)
            return True
    return False

# Smooth movement animation
def animate_movement(entity, target_x, target_y, duration_ms):
    start_x, start_y = entity.draw_pos
    steps = duration_ms // 16  # 60 FPS
    
    def move_step():
        nonlocal steps
        if steps > 0:
            progress = 1 - (steps / (duration_ms // 16))
            entity.draw_pos = (
                start_x + (target_x - start_x) * progress,
                start_y + (target_y - start_y) * progress
            )
            steps -= 1
        else:
            entity.draw_pos = (target_x, target_y)
            entity.pos = (int(target_x), int(target_y))
            mcrfpy.delTimer(f"move_{id(entity)}")
    
    mcrfpy.setTimer(f"move_{id(entity)}", move_step, 16)

# Visibility/FOV system
def update_fov(entity, sight_range=5):
    ex, ey = entity.pos
    
    for x in range(max(0, ex - sight_range), min(100, ex + sight_range + 1)):
        for y in range(max(0, ey - sight_range), min(100, ey + sight_range + 1)):
            dist = abs(x - ex) + abs(y - ey)
            if dist <= sight_range:
                state = entity.at(x, y)
                state.visible = True

# Find and remove entity
def remove_entity(entity):
    try:
        index = entity.index()
        game_grid.entities.remove(index)
    except:
        # Entity not in collection
        pass

# Entity with behavior
class Enemy:
    def __init__(self, x, y):
        self.entity = mcrfpy.Entity((x, y), texture, 10)
        game_grid.entities.append(self.entity)
        self.hp = 10
        
    def update(self):
        # Random movement
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        move_entity(self.entity, dx, dy)
        
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.die()
            
    def die(self):
        remove_entity(self.entity)
```

**Common Pitfalls:**
- pos must be integers, draw_pos can be floats
- Entity must be added to grid.entities to be visible
- Sprite number must be valid for the texture
- gridstate is read-only, modify through at() method

---

### GridPoint

Individual tile in a Grid with rendering and property information.

**Properties:**
- `color` (Color): Base color tint for the tile
- `color_overlay` (Color): Overlay color (for fog of war, highlighting)
- `walkable` (bool): Whether entities can walk on this tile
- `transparent` (bool): Whether vision passes through this tile
- `tilesprite` (int): Base tile sprite index
- `tile_overlay` (int): Overlay sprite index (-1 for none)
- `uisprite` (int): UI layer sprite index (-1 for none)

**Examples:**
```python
# Access grid points
point = game_grid.at(10, 10)

# Set up different tile types
def set_tile_type(x, y, tile_type):
    point = game_grid.at(x, y)
    
    if tile_type == "grass":
        point.tilesprite = 0
        point.walkable = True
        point.transparent = True
        point.color = mcrfpy.Color(100, 255, 100)
    elif tile_type == "wall":
        point.tilesprite = 5
        point.walkable = False
        point.transparent = False
        point.color = mcrfpy.Color(150, 150, 150)
    elif tile_type == "water":
        point.tilesprite = 10
        point.walkable = False
        point.transparent = True
        point.color = mcrfpy.Color(100, 100, 255)

# Highlight tiles
def highlight_area(center_x, center_y, radius, color):
    for x in range(max(0, center_x - radius), min(100, center_x + radius + 1)):
        for y in range(max(0, center_y - radius), min(100, center_y + radius + 1)):
            if abs(x - center_x) + abs(y - center_y) <= radius:
                point = game_grid.at(x, y)
                point.color_overlay = color

# Show spell range
highlight_area(player.pos[0], player.pos[1], 3, mcrfpy.Color(255, 0, 0, 100))

# Animated tiles
water_frames = [10, 11, 12, 11]
frame_index = 0

def animate_water():
    global frame_index
    frame_index = (frame_index + 1) % len(water_frames)
    
    for x in range(100):
        for y in range(100):
            point = game_grid.at(x, y)
            if point.tilesprite in water_frames:
                point.tilesprite = water_frames[frame_index]

mcrfpy.setTimer("water_anim", animate_water, 500)

# Pathfinding visualization
def show_path(path):
    for x, y in path:
        point = game_grid.at(x, y)
        point.tile_overlay = 50  # Arrow or highlight sprite
        point.color_overlay = mcrfpy.Color(0, 255, 0, 128)

# Clear all overlays
def clear_overlays():
    for x in range(100):
        for y in range(100):
            point = game_grid.at(x, y)
            point.tile_overlay = -1
            point.color_overlay = mcrfpy.Color(255, 255, 255, 0)
```

**Common Pitfalls:**
- Sprite indices must be valid for the grid's texture
- Color alpha affects transparency (255 = opaque)
- tile_overlay -1 means no overlay
- Cannot directly create GridPoint objects

---

### GridPointState

Visibility state for a specific grid position from an entity's perspective.

💡 TCOD is used to calculate visible and discovered tiles - set walkable and transparent on the Grid tiles, and call `.update_visibility()` on the entity after moving or modifying terrain to get accurate `GridPointState` values from `Entity.at(x, y)`.

**Properties:**
- `visible` (bool): Whether this tile is currently visible
- `discovered` (bool): Whether this tile has ever been seen

**Examples:**
```python
# Access entity's vision state
state = player_entity.at(10, 10)

# Fog of war system
def render_fog_of_war(entity):
    grid_w, grid_h = game_grid.grid_size
    
    for x in range(grid_w):
        for y in range(grid_h):
            state = entity.at(x, y)
            point = game_grid.at(x, y)
            
            if state.visible:
                # Currently visible - full brightness
                point.color_overlay = mcrfpy.Color(255, 255, 255, 0)
            elif state.discovered:
                # Previously seen - dim
                point.color_overlay = mcrfpy.Color(0, 0, 0, 128)
            else:
                # Never seen - black
                point.color_overlay = mcrfpy.Color(0, 0, 0, 255)

# Check what player knows about a tile
def examine_tile(x, y):
    state = player_entity.at(x, y)
    
    if not state.discovered:
        return "You haven't explored this area yet."
    elif not state.visible:
        return "You remember seeing something here..."
    else:
        point = game_grid.at(x, y)
        return describe_tile(point)

# Memory-based pathfinding
def find_path_using_memory(entity, target_x, target_y):
    # Only path through discovered tiles
    valid_tiles = []
    
    for x in range(100):
        for y in range(100):
            if entity.at(x, y).discovered:
                if game_grid.at(x, y).walkable:
                    valid_tiles.append((x, y))
    
    # Pathfind using only valid_tiles
    return pathfind(entity.pos, (target_x, target_y), valid_tiles)
```

**Common Pitfalls:**
- State is per-entity (each entity has its own vision)
- Cannot directly create GridPointState objects
- Discovered state persists, visible state should be updated each turn
- State is not automatically updated - implement your own vision system

---

## Automation API

The automation API (`mcrfpy.automation`) provides programmatic control over mouse and keyboard input for testing and automation.

**⚠️) Caution:** The mouse input automation is in quite bad shape at the moment.

**⚠️) Caution:** Don't start McRogueFace in headless mode without a scripted way to exit. The game will run with no interface, and You'll have to close the program with `Ctrl+C`.

### Screenshot

#### `screenshot(filename: str) -> None`

Captures the current game display and saves it as a PNG file.

**Parameters:**
- `filename` (str): Path where the screenshot will be saved

**Returns:** None

**Examples:**
```python
import mcrfpy
from mcrfpy import automation

# Basic screenshot
automation.screenshot("game_state.png")

# Screenshot with timestamp
import time
timestamp = int(time.time())
automation.screenshot(f"screenshot_{timestamp}.png")

# Capture sequence for animation
for i in range(10):
    # Update game state
    player.move(1, 0)
    
    # Capture frame
    automation.screenshot(f"frames/frame_{i:03d}.png")
    
    # Wait a bit
    time.sleep(0.1)

# Test automation with screenshots
def test_menu_navigation():
    # Start state
    automation.screenshot("test_1_initial.png")
    
    # Click start button
    automation.click(500, 300)
    automation.screenshot("test_2_after_start.png")
    
    # Verify we're in game
    assert mcrfpy.currentScene() == "gameplay"
```

**Notes:**
- Screenshots only work after the game loop has started
- Use in timer callbacks for reliable capture
- Path is relative to game executable
- Captures exactly what's on screen including UI

---

### Mouse Functions

#### `position() -> tuple`

Returns the current mouse cursor position.

**Parameters:** None

**Returns:** tuple - (x, y) coordinates of mouse cursor

**Examples:**
```python
# Get current position
x, y = automation.position()
print(f"Mouse at: {x}, {y}")

# Track mouse movement
def track_mouse():
    pos = automation.position()
    cursor_sprite.x = pos[0]
    cursor_sprite.y = pos[1]

mcrfpy.setTimer("track", track_mouse, 16)

# Hover detection
def is_hovering_over(element):
    mx, my = automation.position()
    return (element.x <= mx <= element.x + element.w and
            element.y <= my <= element.y + element.h)
```

---

#### `size() -> tuple`

Returns the size of the game window.

**Parameters:** None

**Returns:** tuple - (width, height) of the window in pixels

**Examples:**
```python
# Get window dimensions
width, height = automation.size()
print(f"Window size: {width}x{height}")

# Center something on screen
window_w, window_h = automation.size()
element.x = (window_w - element.w) / 2
element.y = (window_h - element.h) / 2

# Check if mouse is in window
def mouse_in_window():
    x, y = automation.position()
    w, h = automation.size()
    return 0 <= x < w and 0 <= y < h
```

---

#### `onScreen(x: int, y: int) -> bool`

Checks if the given coordinates are within the game window.

**Parameters:**
- `x` (int): X coordinate to check
- `y` (int): Y coordinate to check

**Returns:** bool - True if coordinates are on screen

**Examples:**
```python
# Validate coordinates
if automation.onScreen(100, 100):
    automation.click(100, 100)

# Clamp position to screen
def clamp_to_screen(x, y):
    w, h = automation.size()
    x = max(0, min(x, w - 1))
    y = max(0, min(y, h - 1))
    return x, y

# Safe click function
def safe_click(x, y):
    if automation.onScreen(x, y):
        automation.click(x, y)
    else:
        print(f"Position {x}, {y} is off screen")
```

---

#### `moveTo(x: int, y: int, duration: float = 0.0) -> None`

Moves the mouse cursor to the specified position.

**Parameters:**
- `x` (int): Target X coordinate
- `y` (int): Target Y coordinate
- `duration` (float, optional): Time to take for movement in seconds

**Returns:** None

**Examples:**
```python
# Instant movement
automation.moveTo(500, 300)

# Smooth movement over 1 second
automation.moveTo(800, 600, duration=1.0)

# Move through a path
waypoints = [(100, 100), (400, 100), (400, 400), (100, 400)]
for x, y in waypoints:
    automation.moveTo(x, y, duration=0.5)
    time.sleep(0.5)

# Circle movement
import math
center_x, center_y = 500, 400
radius = 100

for angle in range(0, 360, 10):
    x = center_x + radius * math.cos(math.radians(angle))
    y = center_y + radius * math.sin(math.radians(angle))
    automation.moveTo(int(x), int(y), duration=0.1)
```

---

#### `moveRel(xOffset: int, yOffset: int, duration: float = 0.0) -> None`

Moves the mouse cursor relative to its current position.

**Parameters:**
- `xOffset` (int): Horizontal movement (positive = right)
- `yOffset` (int): Vertical movement (positive = down)
- `duration` (float, optional): Time for movement in seconds

**Returns:** None

**Examples:**
```python
# Quick nudge
automation.moveRel(10, 0)  # Move right 10 pixels

# Smooth drift
automation.moveRel(100, 100, duration=2.0)

# Shake effect
for i in range(10):
    automation.moveRel(random.randint(-5, 5), random.randint(-5, 5))
    time.sleep(0.05)

# Follow a pattern
movements = [(10, 0), (0, 10), (-10, 0), (0, -10)]  # Square
for dx, dy in movements * 5:  # 5 squares
    automation.moveRel(dx, dy, duration=0.1)
```

---

#### `click(x: int = None, y: int = None, clicks: int = 1, interval: float = 0.0, button: str = 'left') -> None`

Performs mouse clicks at the specified position.

**Parameters:**
- `x` (int, optional): X coordinate (uses current position if None)
- `y` (int, optional): Y coordinate (uses current position if None)
- `clicks` (int, optional): Number of clicks (default 1)
- `interval` (float, optional): Delay between clicks in seconds
- `button` (str, optional): Mouse button ('left', 'right', 'middle')

**Returns:** None

**Examples:**
```python
# Simple click
automation.click(400, 300)

# Double-click
automation.click(400, 300, clicks=2)

# Right-click menu
automation.click(600, 400, button='right')

# Multiple clicks with delay
automation.click(500, 500, clicks=5, interval=0.5)

# Click at current position
automation.moveTo(250, 250)
automation.click()  # Clicks at 250, 250

# Test all buttons on an element
def test_element_clicks(x, y):
    automation.click(x, y, button='left')
    time.sleep(0.5)
    automation.click(x, y, button='right')
    time.sleep(0.5)
    automation.click(x, y, button='middle')
```

**Notes:**
- Middle mouse button issue fixed in recent version
- Click coordinates are screen pixels
- None for x, y uses current mouse position

---

#### `rightClick(x: int = None, y: int = None) -> None`

Convenience function for right mouse button click.

**Parameters:**
- `x` (int, optional): X coordinate
- `y` (int, optional): Y coordinate

**Returns:** None

**Examples:**
```python
# Right-click for context menu
automation.rightClick(500, 300)

# Right-click on entity
entity_screen_x = grid.x + entity.pos[0] * 16
entity_screen_y = grid.y + entity.pos[1] * 16
automation.rightClick(entity_screen_x, entity_screen_y)
```

---

#### `middleClick(x: int = None, y: int = None) -> None`

Convenience function for middle mouse button click.

**Parameters:**
- `x` (int, optional): X coordinate
- `y` (int, optional): Y coordinate

**Returns:** None

**Examples:**
```python
# Middle-click for camera pan
automation.middleClick(512, 384)

# Test middle-click functionality
automation.middleClick(400, 300)
automation.screenshot("after_middle_click.png")
```

---

#### `doubleClick(x: int = None, y: int = None) -> None`

Performs a double-click at the specified position.

**Parameters:**
- `x` (int, optional): X coordinate
- `y` (int, optional): Y coordinate

**Returns:** None

**Examples:**
```python
# Double-click to activate
automation.doubleClick(600, 450)

# Double-click on inventory item
slot_x = inventory_frame.x + 50
slot_y = inventory_frame.y + 100
automation.doubleClick(slot_x, slot_y)
```

---

#### `tripleClick(x: int = None, y: int = None) -> None`

Performs a triple-click at the specified position.

**Parameters:**
- `x` (int, optional): X coordinate
- `y` (int, optional): Y coordinate

**Returns:** None

**Examples:**
```python
# Triple-click to select all text
automation.tripleClick(text_field_x, text_field_y)

# Special activation
automation.tripleClick(secret_button_x, secret_button_y)
```

---

#### `dragTo(x: int, y: int, duration: float = 0.0, button: str = 'left') -> None`

Drags from current position to the specified position.

**Parameters:**
- `x` (int): Target X coordinate
- `y` (int): Target Y coordinate
- `duration` (float, optional): Time for drag in seconds
- `button` (str, optional): Mouse button to hold

**Returns:** None

**Examples:**
```python
# Drag window
automation.moveTo(window.x + 10, window.y + 10)
automation.dragTo(300, 200, duration=1.0)

# Drag inventory item
automation.moveTo(slot1_x, slot1_y)
automation.dragTo(slot2_x, slot2_y, duration=0.5)

# Draw a line
automation.moveTo(100, 100)
automation.dragTo(500, 500, duration=2.0)

# Drag with right button
automation.moveTo(200, 200)
automation.dragTo(400, 400, button='right')
```

---

#### `dragRel(xOffset: int, yOffset: int, duration: float = 0.0, button: str = 'left') -> None`

Drags relative to current position.

**Parameters:**
- `xOffset` (int): Horizontal drag distance
- `yOffset` (int): Vertical drag distance
- `duration` (float, optional): Time for drag in seconds
- `button` (str, optional): Mouse button to hold

**Returns:** None

**Examples:**
```python
# Drag right 100 pixels
automation.dragRel(100, 0)

# Smooth camera pan
automation.moveTo(512, 384)
automation.dragRel(-200, -150, duration=2.0)

# Resize something
automation.moveTo(resize_handle_x, resize_handle_y)
automation.dragRel(50, 50, duration=0.5)
```

---

#### `scroll(clicks: int, x: int = None, y: int = None) -> None`

Performs mouse wheel scrolling.

**Parameters:**
- `clicks` (int): Number of scroll clicks (positive = up, negative = down)
- `x` (int, optional): X position for scroll
- `y` (int, optional): Y position for scroll

**Returns:** None

**Examples:**
```python
# Scroll up 5 clicks
automation.scroll(5)

# Scroll down at specific position
automation.scroll(-3, 400, 300)

# Zoom in/out with scroll
def zoom_camera(direction):
    # Scroll at center of grid
    grid_center_x = game_grid.x + game_grid.w / 2
    grid_center_y = game_grid.y + game_grid.h / 2
    automation.scroll(direction, grid_center_x, grid_center_y)

zoom_camera(3)  # Zoom in
zoom_camera(-3)  # Zoom out

# Scroll through inventory
inv_x = inventory_list.x + 50
inv_y = inventory_list.y + 50
automation.scroll(-10, inv_x, inv_y)  # Scroll down
```

---

#### `mouseDown(x: int = None, y: int = None, button: str = 'left') -> None`

Presses and holds a mouse button.

**Parameters:**
- `x` (int, optional): X coordinate
- `y` (int, optional): Y coordinate
- `button` (str, optional): Mouse button

**Returns:** None

**Examples:**
```python
# Hold for drag operation
automation.mouseDown(100, 100)
# Do something while held
time.sleep(1)
automation.mouseUp(100, 100)

# Custom drag behavior
automation.mouseDown(start_x, start_y)
for i in range(10):
    automation.moveTo(start_x + i * 10, start_y + i * 10)
    time.sleep(0.1)
automation.mouseUp()
```

---

#### `mouseUp(x: int = None, y: int = None, button: str = 'left') -> None`

Releases a held mouse button.

**Parameters:**
- `x` (int, optional): X coordinate
- `y` (int, optional): Y coordinate
- `button` (str, optional): Mouse button

**Returns:** None

**Examples:**
```python
# Complete a drag
automation.mouseDown(200, 200)
automation.moveTo(400, 400)
automation.mouseUp(400, 400)

# Measure hold time
automation.mouseDown(300, 300)
time.sleep(2)  # Hold for 2 seconds
automation.mouseUp(300, 300)
```

---

### Keyboard Functions

#### `typewrite(message: str, interval: float = 0.0) -> None`

Types text by simulating keyboard input.

**Parameters:**
- `message` (str): Text to type
- `interval` (float, optional): Delay between keystrokes in seconds

**Returns:** None

**Examples:**
```python
# Type text instantly
automation.typewrite("Hello, World!")

# Type with realistic speed
automation.typewrite("This is a test message.", interval=0.1)

# Type player name
automation.click(name_field_x, name_field_y)
automation.typewrite("PlayerOne", interval=0.05)

# Type commands
automation.typewrite("/teleport 50 50", interval=0.05)
automation.keyDown("enter")
automation.keyUp("enter")

# Animated typing effect
message = "Welcome to the game!"
automation.typewrite(message, interval=0.15)
```

**Notes:**
- Only works with printable characters
- Use keyDown/keyUp for special keys
- Text goes to whatever has focus

---

#### `hotkey(*keys) -> None`

Presses a combination of keys simultaneously.

**Parameters:**
- `*keys` (str): Variable number of key names to press together

**Returns:** None

**Examples:**
```python
# Common hotkeys
automation.hotkey('ctrl', 's')  # Save
automation.hotkey('ctrl', 'c')  # Copy
automation.hotkey('ctrl', 'v')  # Paste

# Game shortcuts
automation.hotkey('shift', 'i')  # Open inventory
automation.hotkey('alt', 'f4')  # Quit game

# Multiple modifiers
automation.hotkey('ctrl', 'shift', 's')  # Save as

# Custom game commands
automation.hotkey('ctrl', '1')  # Quick slot 1
automation.hotkey('f5')  # Quick save
```

**Notes:**
- Keys are pressed in order given
- All keys released simultaneously
- Key names are case-insensitive

---

#### `keyDown(key: str) -> None`

Presses and holds a keyboard key.

**Parameters:**
- `key` (str): Name of the key to press

**Returns:** None

**Examples:**
```python
# Hold movement key
automation.keyDown('w')
time.sleep(2)  # Move forward for 2 seconds
automation.keyUp('w')

# Sprint while moving
automation.keyDown('shift')
automation.keyDown('w')
time.sleep(1)
automation.keyUp('w')
automation.keyUp('shift')

# Charge attack
automation.keyDown('space')
time.sleep(3)  # Charge for 3 seconds
automation.keyUp('space')
```

---

#### `keyUp(key: str) -> None`

Releases a held keyboard key.

**Parameters:**
- `key` (str): Name of the key to release

**Returns:** None

**Examples:**
```python
# Complete key press
automation.keyDown('enter')
time.sleep(0.1)
automation.keyUp('enter')

# Movement pattern
for key in ['w', 'a', 's', 'd']:
    automation.keyDown(key)
    time.sleep(0.5)
    automation.keyUp(key)

# Release all movement keys
for key in ['w', 'a', 's', 'd']:
    automation.keyUp(key)
```

**Supported Key Names:**
- Letters: 'a' through 'z'
- Numbers: '0' through '9'
- Function keys: 'f1' through 'f12'
- Modifiers: 'ctrl', 'shift', 'alt', 'cmd'
- Special: 'space', 'enter', 'tab', 'escape', 'backspace', 'delete'
- Arrows: 'up', 'down', 'left', 'right'
- Others: 'home', 'end', 'pageup', 'pagedown', 'insert'

---

## Type Classes

### Color

RGBA color representation for all rendering operations.

#### Constructor

```python
Color(r: int, g: int, b: int, a: int = 255) -> Color
Color(tuple: tuple) -> Color
```

**Parameters:**
- `r` (int): Red component (0-255)
- `g` (int): Green component (0-255)
- `b` (int): Blue component (0-255)
- `a` (int, optional): Alpha component (0-255, default 255)
- `tuple` (tuple): Color as (r, g, b) or (r, g, b, a)

**Properties:**
- `r` (int): Red component
- `g` (int): Green component
- `b` (int): Blue component
- `a` (int): Alpha component

**Examples:**
```python
# Create colors
red = mcrfpy.Color(255, 0, 0)
green = mcrfpy.Color(0, 255, 0)
blue = mcrfpy.Color(0, 0, 255)
transparent_black = mcrfpy.Color(0, 0, 0, 128)

# From tuple
yellow = mcrfpy.Color((255, 255, 0))
semi_white = mcrfpy.Color((255, 255, 255, 200))

# Modify colors
color = mcrfpy.Color(100, 100, 100)
color.r = 255  # Make it red-tinted
color.a = 128  # Make it semi-transparent

# Color utilities
def lighten(color, amount=50):
    return mcrfpy.Color(
        min(255, color.r + amount),
        min(255, color.g + amount),
        min(255, color.b + amount),
        color.a
    )

def darken(color, amount=50):
    return mcrfpy.Color(
        max(0, color.r - amount),
        max(0, color.g - amount),
        max(0, color.b - amount),
        color.a
    )

# Fade effect
def fade_to_black(element, steps=10):
    original = element.fill_color
    
    def fade_step():
        nonlocal steps
        if steps > 0:
            factor = steps / 10
            element.fill_color = mcrfpy.Color(
                int(original.r * factor),
                int(original.g * factor),
                int(original.b * factor),
                original.a
            )
            steps -= 1
        else:
            mcrfpy.delTimer("fade")
    
    mcrfpy.setTimer("fade", fade_step, 100)

# Color palettes
ui_colors = {
    'background': mcrfpy.Color(30, 30, 40),
    'text': mcrfpy.Color(255, 255, 255),
    'highlight': mcrfpy.Color(100, 200, 255),
    'danger': mcrfpy.Color(255, 50, 50),
    'success': mcrfpy.Color(50, 255, 50)
}
```

**Common Pitfalls:**
- Values outside 0-255 may cause unexpected results
- Alpha 0 = fully transparent, 255 = fully opaque
- Color objects are mutable - changes affect all references

---

### Vector

2D vector for positions and sizes.

#### Constructor

```python
Vector(x: float = 0.0, y: float = 0.0) -> Vector
Vector(tuple: tuple) -> Vector
```

**Parameters:**
- `x` (float, optional): X component (default 0.0)
- `y` (float, optional): Y component (default 0.0)
- `tuple` (tuple): Vector as (x, y)

**Properties:**
- `x` (float): X component
- `y` (float): Y component

**Examples:**
```python
# Create vectors
pos = mcrfpy.Vector(100, 200)
size = mcrfpy.Vector(50, 75)
zero = mcrfpy.Vector()  # (0, 0)

# From tuple
velocity = mcrfpy.Vector((5.5, -2.3))

# Vector math
def add_vectors(v1, v2):
    return mcrfpy.Vector(v1.x + v2.x, v1.y + v2.y)

def scale_vector(v, scale):
    return mcrfpy.Vector(v.x * scale, v.y * scale)

def distance(v1, v2):
    dx = v2.x - v1.x
    dy = v2.y - v1.y
    return (dx*dx + dy*dy) ** 0.5

# Movement with vectors
position = mcrfpy.Vector(100, 100)
velocity = mcrfpy.Vector(2, 1)

def update_position():
    position.x += velocity.x
    position.y += velocity.y
    sprite.x = position.x
    sprite.y = position.y

# Interpolation
def lerp_vector(start, end, t):
    return mcrfpy.Vector(
        start.x + (end.x - start.x) * t,
        start.y + (end.y - start.y) * t
    )

# Apply to UI elements
element.pos = mcrfpy.Vector(300, 200)
# Equivalent to:
# element.x = 300
# element.y = 200
```

**Common Pitfalls:**
- Vector objects are mutable
- No built-in vector math operations
- Used mainly for position/size properties

---

### Font

Font resource for text rendering.

#### Constructor

```python
Font(filename: str) -> Font
```

**Parameters:**
- `filename` (str): Path to font file (TTF format)

**Properties:**
- None (fonts are immutable once loaded)

**Examples:**
```python
# Load custom font
game_font = mcrfpy.Font("assets/GameFont.ttf")
ui_font = mcrfpy.Font("assets/UIFont.ttf")

# Use in captions
title = mcrfpy.Caption("GAME TITLE", game_font, 400, 100)
score = mcrfpy.Caption("Score: 0", ui_font, 10, 10)

# Font manager
fonts = {
    'title': mcrfpy.Font("assets/TitleFont.ttf"),
    'body': mcrfpy.Font("assets/BodyFont.ttf"),
    'mono': mcrfpy.Font("assets/MonospaceFont.ttf")
}

def create_text(text, font_name, x, y):
    return mcrfpy.Caption(text, fonts[font_name], x, y)

# Use default font
caption = mcrfpy.Caption("Text", mcrfpy.default_font, 0, 0)
```

**Common Pitfalls:**
- Font file must exist and be valid TTF
- Fonts cannot be modified after creation
- Large font sizes may impact performance

---

### Texture

Sprite sheet containing fixed-size sprite tiles.

#### Constructor

```python
Texture(filename: str, sprite_width: int, sprite_height: int) -> Texture
```

**Parameters:**
- `filename` (str): Path to image file (PNG recommended)
- `sprite_width` (int): Width of each sprite in pixels
- `sprite_height` (int): Height of each sprite in pixels

**Properties:**
- `sprite_width` (int, read-only): Width of sprites
- `sprite_height` (int, read-only): Height of sprites
- `sprite_count` (int, read-only): Total number of sprites

**Examples:**
```python
# Load textures
character_tex = mcrfpy.Texture("assets/characters.png", 16, 16)
tile_tex = mcrfpy.Texture("assets/tiles.png", 32, 32)
ui_tex = mcrfpy.Texture("assets/ui_elements.png", 64, 64)

# Use in sprites
player_sprite = mcrfpy.Sprite(character_tex, 0, 100, 100)
enemy_sprite = mcrfpy.Sprite(character_tex, 5, 200, 100)

# Use in grid
world_grid = mcrfpy.Grid(50, 50, tile_tex, 0, 0, 800, 600)

# Texture atlas info
print(f"Texture has {character_tex.sprite_count} sprites")
print(f"Each sprite is {character_tex.sprite_width}x{character_tex.sprite_height}")

# Calculate sprite index from row/column
def sprite_index(row, col, texture):
    sprites_per_row = texture.sprite_count // texture.sprite_height
    return row * sprites_per_row + col

# Validate sprite index
def is_valid_sprite(index, texture):
    return 0 <= index < texture.sprite_count

# Create invisible texture
invisible_tex = mcrfpy.Texture("", 1, 1)  # Special case
```

**Common Pitfalls:**
- Texture must be loaded before creating sprites/grids
- Sprite indices start at 0
- Empty filename creates invisible texture
- Texture is divided evenly by sprite dimensions

---

## Constants and Module Attributes

### `default_font`

The default font (JetbrainsMono.ttf) automatically loaded by the engine.

**Type:** Font

**Examples:**
```python
# Use default font
text = mcrfpy.Caption("Hello", mcrfpy.default_font, 100, 100)

# Default font is pre-loaded
ui = mcrfpy.sceneUI("menu")
for i, option in enumerate(["Start", "Options", "Quit"]):
    caption = mcrfpy.Caption(option, mcrfpy.default_font, 400, 200 + i * 50)
    ui.append(caption)
```

---

### `default_texture`

The default texture (`kenney_tinydungeon.png`) with 16x16 sprites.

**Type:** Texture

**Examples:**
```python
# Use default texture
sprite = mcrfpy.Sprite(mcrfpy.default_texture, 10, 100, 100)
grid = mcrfpy.Grid(50, 50, mcrfpy.default_texture, 0, 0, 800, 600)

# Default texture info
print(f"Default texture sprites: {mcrfpy.default_texture.sprite_count}")
print(f"Sprite size: {mcrfpy.default_texture.sprite_width}x{mcrfpy.default_texture.sprite_height}")
```

---

## Common Patterns and Best Practices

### Game Loop Structure

```python
import mcrfpy
import time

# Initialize scenes
mcrfpy.createScene("menu")
mcrfpy.createScene("game")
mcrfpy.createScene("game_over")

# Game state
game_state = {
    'score': 0,
    'lives': 3,
    'level': 1
}

# Update function
def game_update():
    # Update entities
    for entity in game_grid.entities:
        if hasattr(entity, 'update'):
            entity.update()
    
    # Check win/lose conditions
    if game_state['lives'] <= 0:
        mcrfpy.setScene("game_over")
        mcrfpy.delTimer("game_loop")

# Start game loop
mcrfpy.setTimer("game_loop", game_update, 16)  # ~60 FPS
mcrfpy.setScene("menu")
```

### Entity Management Pattern

```python
class GameObject:
    """Base class for game entities"""
    
    def __init__(self, grid, x, y, sprite):
        self.entity = mcrfpy.Entity((x, y), texture, sprite)
        self.grid = grid
        grid.entities.append(self.entity)
        self.active = True
        
    def update(self):
        """Override in subclasses"""
        pass
        
    def destroy(self):
        """Remove from game"""
        if self.active:
            self.active = False
            idx = self.entity.index()
            self.grid.entities.remove(idx)

# Subclass example
class Enemy(GameObject):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y, sprite=10)
        self.hp = 10
        self.speed = 0.5
        
    def update(self):
        if not self.active:
            return
            
        # AI logic here
        self.move_towards_player()
        
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.destroy()
```

### Scene Transition Pattern

```python
def transition_scene(from_scene, to_scene, duration_ms=500):
    """Fade out, switch scene, fade in"""
    
    # Create overlay
    overlay = mcrfpy.Frame(0, 0, 1024, 768)
    overlay.fill_color = mcrfpy.Color(0, 0, 0, 0)
    
    from_ui = mcrfpy.sceneUI(from_scene)
    from_ui.append(overlay)
    
    steps = duration_ms // 32  # ~30 FPS
    
    def fade_out():
        nonlocal steps
        if steps > 0:
            alpha = int(255 * (1 - steps / (duration_ms // 32)))
            overlay.fill_color.a = alpha
            steps -= 1
        else:
            # Switch scene
            mcrfpy.setScene(to_scene)
            
            # Set up fade in
            to_ui = mcrfpy.sceneUI(to_scene)
            to_ui.append(overlay)
            overlay.fill_color.a = 255
            
            mcrfpy.delTimer("fade_out")
            mcrfpy.setTimer("fade_in", fade_in, 32)
    
    def fade_in():
        alpha = overlay.fill_color.a
        if alpha > 0:
            overlay.fill_color.a = max(0, alpha - 10)
        else:
            to_ui.remove(overlay)
            mcrfpy.delTimer("fade_in")
    
    mcrfpy.setTimer("fade_out", fade_out, 32)
```

### Input Handling Pattern

```python
# Input state tracking
input_state = {
    'keys': {},
    'mouse': {'x': 0, 'y': 0, 'buttons': {}}
}

def on_key(key):
    """Global key handler"""
    
    # Track key state
    input_state['keys'][key] = True
    
    # Handle based on scene
    scene = mcrfpy.currentScene()
    
    if scene == "menu":
        handle_menu_input(key)
    elif scene == "game":
        handle_game_input(key)
    elif scene == "inventory":
        handle_inventory_input(key)

def handle_game_input(key):
    """Game-specific input"""
    
    # Movement
    if key == ord('W'):
        player.try_move(0, -1)
    elif key == ord('S'):
        player.try_move(0, 1)
    elif key == ord('A'):
        player.try_move(-1, 0)
    elif key == ord('D'):
        player.try_move(1, 0)
    
    # Actions
    elif key == 32:  # Space
        player.interact()
    elif key == ord('I'):
        open_inventory()
    elif key == 27:  # Escape
        pause_game()

# Set up input
mcrfpy.keypressScene(on_key)
```

### Resource Management Pattern

```python
# Resource loader
class Resources:
    def __init__(self):
        self.textures = {}
        self.sounds = {}
        self.fonts = {}
        
    def load_texture(self, name, path, w, h):
        self.textures[name] = mcrfpy.Texture(path, w, h)
        
    def load_sound(self, name, path):
        self.sounds[name] = mcrfpy.createSoundBuffer(path)
        
    def load_font(self, name, path):
        self.fonts[name] = mcrfpy.Font(path)
        
    def get_texture(self, name):
        return self.textures.get(name, mcrfpy.default_texture)
        
    def play_sound(self, name):
        if name in self.sounds:
            mcrfpy.playSound(self.sounds[name])

# Initialize resources
resources = Resources()
resources.load_texture("player", "assets/player.png", 16, 16)
resources.load_texture("enemies", "assets/enemies.png", 16, 16)
resources.load_sound("coin", "assets/coin.wav")
resources.load_sound("hurt", "assets/hurt.wav")

# Use resources
player_tex = resources.get_texture("player")
resources.play_sound("coin")
```

### Error Handling Pattern

```python
def safe_scene_switch(scene_name):
    """Safely switch scenes with error handling"""
    try:
        # Check if scene exists by trying to get its UI
        ui = mcrfpy.sceneUI(scene_name)
        mcrfpy.setScene(scene_name)
        return True
    except:
        print(f"Error: Scene '{scene_name}' does not exist")
        return False

def safe_timer_create(name, callback, interval):
    """Create timer with validation"""
    if interval < 16:
        print(f"Warning: Timer '{name}' interval {interval}ms is very fast")
    
    try:
        mcrfpy.setTimer(name, callback, max(16, interval))
        return True
    except Exception as e:
        print(f"Error creating timer '{name}': {e}")
        return False

def safe_entity_remove(entity):
    """Safely remove entity from grid"""
    try:
        if hasattr(entity, 'index'):
            idx = entity.index()
            if 0 <= idx < len(entity.grid.entities):
                entity.grid.entities.remove(idx)
                return True
    except:
        pass
    return False
```

---

This completes the comprehensive API reference for McRogueFace. For more examples and tutorials, see the other documentation files in this repository.
