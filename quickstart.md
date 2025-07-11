# McRogueFace Quickstart Guide

**Make 2D games with Python** - No C++ required!

---

[**Source Code**](https://github.com/jmccardle/McRogueFace) • [**Downloads**](https://github.com/jmccardle/McRogueFace/releases) • **[Quickstart](https://mcrogueface.github.io/quickstart)** • [**Tutorials**](https://mcrogueface.github.io/tutorials) • [**API Reference**](https://mcrogueface.github.io/api) • [**Cookbook**](https://mcrogueface.github.io/cookbook) • [**C++ Extensions**](https://mcrogueface.github.io/extending-cpp)

---

## Get Started in 5 Minutes

This guide will have you running games and making changes in just a few minutes. No compilation needed!

### 1. Download McRogueFace

1. Go to the [latest release](https://github.com/jmccardle/McRogueFace/releases/latest)
2. Download the right version for your system:
   - **Windows**: `mcrogueface-windows.zip`
   - **Mac**: `mcrogueface-macos.zip`
   - **Linux**: `mcrogueface-linux.tar.gz`
3. Extract the archive to a folder (e.g., `C:\Games\McRogueFace` or `~/McRogueFace`)

### 2. Run the Demo Game

Open a terminal/command prompt in the McRogueFace folder and run:

**Windows:**
```cmd
mcrogueface.exe
```

**Mac/Linux:**
```bash
./mcrogueface
```

You should see the demo game start up! Use arrow keys to move around, click buttons, and explore what's possible.

### 3. Switch to a Different Game

McRogueFace comes with multiple example games. Let's switch from the demo to the full "Crypt of Sokoban" game:

1. Open `scripts/game.py` in a text editor
2. Change the content to:
```python
import crypt_of_sokoban as game
game.run()
```
3. Save and run McRogueFace again

Now you're playing a complete roguelike with enemies, items, and puzzle mechanics!

### 4. Make Your First Change

Let's add a custom button to the main menu. Open `scripts/game.py` and replace it with:

```python
import mcrfpy

# Create a scene
scene = mcrfpy.Scene("main_menu")
mcrfpy.setScene("main_menu")

# Add a background
bg = mcrfpy.Frame(0, 0, 1920, 1080, fill_color=(20, 20, 40))
scene.ui.append(bg)

# Add a title
title = mcrfpy.Caption(760, 100, 400, 100, "My Awesome Game")
title.font_size = 48
title.color = (255, 255, 100)
scene.ui.append(title)

# Add a custom button
def start_game():
    print("Starting the game!")
    # Load the actual game
    import crypt_of_sokoban as game
    game.run()

button = mcrfpy.Button(810, 400, 300, 80, "Start Adventure")
button.bg_color = (50, 150, 50)
button.hover_color = (70, 200, 70)
button.click_color = (40, 100, 40)
button.onclick = start_game
scene.ui.append(button)

# Add a quit button
def quit_game():
    mcrfpy.quit()

quit_btn = mcrfpy.Button(810, 500, 300, 80, "Quit")
quit_btn.bg_color = (150, 50, 50)
quit_btn.onclick = quit_game
scene.ui.append(quit_btn)
```

Save and run - you now have a custom main menu!

### 5. Add a Game Item

Let's create a custom item for Crypt of Sokoban. Create a new file `scripts/my_items.py`:

```python
from cos_entities import Item

class MagicWand(Item):
    def __init__(self, x, y):
        # Use sprite position 123 from the sprite sheet
        super().__init__(x, y, sprite_index=123)
        self.name = "Magic Wand"
        self.description = "Casts fireballs at enemies"
        
    def use(self, user, target=None):
        if target and hasattr(target, 'take_damage'):
            print(f"{user.name} zaps {target.name} with the {self.name}!")
            target.take_damage(25)
            return True
        return False
```

To add it to the game, you'd modify the level generation to spawn your item!

### 6. Load a Custom Sprite Sheet

Want to use your own graphics? Here's how:

```python
import mcrfpy

# Load your sprite sheet (32x32 pixel tiles)
mcrfpy.loadTexture("sprites", "assets/my_sprites.png", 32, 32)

# Use it in the game
scene = mcrfpy.Scene("game")
grid = mcrfpy.Grid(50, 50, 20, 15, "sprites", 32, 32)

# Set specific tiles
grid.at(5, 5).sprite = 10  # Tree sprite at position 10
grid.at(6, 5).sprite = 11  # Rock sprite at position 11

scene.ui.append(grid)
mcrfpy.setScene("game")
```

## What's Next?

### Learn by Doing
- **[McRogueFace Does The Entire Roguelike Tutorial](https://mcrogueface.github.io/tutorials)** - Build a complete game step-by-step
- **[Cookbook](https://mcrogueface.github.io/cookbook)** - Copy/paste solutions for common tasks

### Reference Material  
- **[Complete API Reference](https://mcrogueface.github.io/api)** - Every function and class documented
- **[Example Games](https://github.com/jmccardle/McRogueFace/tree/main/examples)** - Full source code to learn from

### Advanced Topics
- **[C++ Extension Guide](https://mcrogueface.github.io/extending-cpp)** - Add new engine features (requires compilation)

## Troubleshooting

### "mcrogueface: command not found"
You need to be in the McRogueFace directory, or add it to your PATH.

### "No module named mcrfpy"
Make sure you're running `mcrogueface`, not `python`. McRogueFace is a complete Python environment.

### Black screen on startup
Check that the `assets/` and `scripts/` folders are in the same directory as the mcrogueface executable.

### Can't load my sprites
- Ensure your sprite sheet uses 32x32 pixel tiles (or adjust the size in loadTexture)
- Use PNG format with transparency
- Check the file path is relative to the mcrogueface executable

## Get Help

- **Discord**: [Join our community](https://discord.gg/mcrogueface)
- **Issues**: [Report bugs](https://github.com/jmccardle/McRogueFace/issues)
- **Discussions**: [Ask questions](https://github.com/jmccardle/McRogueFace/discussions)

---

Ready to make games? Download McRogueFace and start creating!
