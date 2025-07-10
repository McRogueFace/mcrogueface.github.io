---
layout: default
title: Quickstart Guide
nav_order: 2
---

# From Zero to Roguelike in 5 Minutes ⚡

Build your first roguelike game with McRogueFace in just 5 minutes! This guide will take you from installation to a playable game with step-by-step instructions.

<div class="progress-tracker">
  <div class="step active">1. Check Prerequisites</div>
  <div class="step">2. Install McRogueFace</div>
  <div class="step">3. Create Your Game</div>
  <div class="step">4. Run & Play</div>
  <div class="step">5. Customize</div>
</div>

---

## 🔍 Step 1: Prerequisites Check

Before we begin, let's make sure you have everything needed. Copy and run this command:

<div class="code-block">
```bash
# Check all prerequisites at once
python3 --version && echo "✓ Python $(python3 --version | cut -d' ' -f2)" || echo "✗ Python 3.8+ required"
g++ --version > /dev/null 2>&1 && echo "✓ C++ compiler found" || echo "✗ C++ compiler required"
cmake --version > /dev/null 2>&1 && echo "✓ CMake found" || echo "✗ CMake 3.10+ required"
```
<button class="copy-btn" onclick="copyCode(this)">📋 Copy</button>
</div>

**You need:**
- ✅ Python 3.8 or higher
- ✅ C++ compiler (g++ or clang++)
- ✅ CMake 3.10 or higher
- ✅ 200MB free disk space

<details>
<summary>📦 Missing something? Click here for installation commands</summary>

<div class="tabs">
  <button class="tab-btn active" onclick="showTab('ubuntu')">Ubuntu/Debian</button>
  <button class="tab-btn" onclick="showTab('macos')">macOS</button>
  <button class="tab-btn" onclick="showTab('windows')">Windows</button>
</div>

<div id="ubuntu" class="tab-content active">
```bash
sudo apt update
sudo apt install python3 python3-dev g++ cmake libsfml-dev
```
</div>

<div id="macos" class="tab-content">
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python cmake sfml
```
</div>

<div id="windows" class="tab-content">
1. Install [Python 3.8+](https://www.python.org/downloads/)
2. Install [Visual Studio 2019+](https://visualstudio.microsoft.com/downloads/) with C++ tools
3. Install [CMake](https://cmake.org/download/)
4. Install [Git Bash](https://git-scm.com/downloads)
</div>
</details>

---

## 🚀 Step 2: Install McRogueFace

Choose your installation method:

<div class="install-options">
  <div class="option recommended">
    <h3>🎯 Quick Install (Recommended)</h3>
    <div class="code-block">
    ```bash
    pip install mcrogueface
    ```
    <button class="copy-btn" onclick="copyCode(this)">📋 Copy</button>
    </div>
    <p class="install-time">⏱️ ~30 seconds</p>
  </div>

  <div class="option">
    <h3>🔧 From Source</h3>
    <div class="code-block">
    ```bash
    git clone https://github.com/mcrogueface/mcrogueface
    cd mcrogueface
    ./build.sh
    ```
    <button class="copy-btn" onclick="copyCode(this)">📋 Copy</button>
    </div>
    <p class="install-time">⏱️ ~2 minutes</p>
  </div>
</div>

<div class="verify-install">
<h4>✅ Verify Installation:</h4>
<div class="code-block">
```bash
python3 -c "import mcrfpy; print('✓ McRogueFace installed successfully!')"
```
<button class="copy-btn" onclick="copyCode(this)">📋 Copy</button>
</div>
</div>

---

## 🎮 Step 3: Your First Game

Let's create a simple dungeon crawler! Create a new file called `my_first_game.py`:

<div class="code-block">
```python
# my_first_game.py - A complete roguelike in 50 lines!
import mcrfpy
import random

# Game state
player_pos = [5, 5]
enemies = [[8, 3], [2, 7], [9, 9]]
treasure = [7, 7]
game_won = False

def create_game():
    """Set up the game window and map"""
    # Create a game scene
    scene = mcrfpy.Scene("game", 800, 600)
    scene.set_background_color(20, 20, 30)
    
    # Create the dungeon map (10x10 grid)
    grid = scene.add_grid(100, 50, 10, 10, 50, 50)
    grid.set_default_tile("floor", (100, 100, 100))
    
    # Add walls around the edges
    for i in range(10):
        grid.set_tile(i, 0, "wall", (50, 50, 50))
        grid.set_tile(i, 9, "wall", (50, 50, 50))
        grid.set_tile(0, i, "wall", (50, 50, 50))
        grid.set_tile(9, i, "wall", (50, 50, 50))
    
    # Add some random walls for obstacles
    for _ in range(10):
        x, y = random.randint(1, 8), random.randint(1, 8)
        if [x, y] not in [player_pos, treasure] + enemies:
            grid.set_tile(x, y, "wall", (50, 50, 50))
    
    update_display(scene)
    return scene

def update_display(scene):
    """Update the display with current game state"""
    grid = scene.get_grid(0)
    
    # Draw player (green @)
    grid.set_entity(player_pos[0], player_pos[1], "@", (0, 255, 0))
    
    # Draw enemies (red E)
    for enemy in enemies:
        grid.set_entity(enemy[0], enemy[1], "E", (255, 0, 0))
    
    # Draw treasure (yellow $)
    if not game_won:
        grid.set_entity(treasure[0], treasure[1], "$", (255, 255, 0))
    
    # Update status
    status = "You won! Press R to restart" if game_won else "Arrow keys to move, collect the treasure!"
    scene.set_caption(0, status)

def handle_input(key):
    """Handle player movement"""
    global player_pos, game_won
    
    if key == "R" and game_won:
        restart_game()
        return
    
    # Calculate new position
    new_pos = player_pos.copy()
    if key == "UP": new_pos[1] -= 1
    elif key == "DOWN": new_pos[1] += 1
    elif key == "LEFT": new_pos[0] -= 1
    elif key == "RIGHT": new_pos[0] += 1
    else: return
    
    # Check boundaries and walls
    if 0 < new_pos[0] < 9 and 0 < new_pos[1] < 9:
        scene = mcrfpy.get_current_scene()
        grid = scene.get_grid(0)
        
        if grid.get_tile(new_pos[0], new_pos[1]) != "wall":
            # Check for enemy collision
            if new_pos not in enemies:
                # Clear old position
                grid.clear_entity(player_pos[0], player_pos[1])
                player_pos = new_pos
                
                # Check for treasure
                if player_pos == treasure and not game_won:
                    game_won = True
                
                # Move enemies randomly
                move_enemies(grid)
                update_display(scene)

def move_enemies(grid):
    """Simple enemy movement"""
    for enemy in enemies:
        # Clear old position
        grid.clear_entity(enemy[0], enemy[1])
        
        # Random movement
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        new_x = enemy[0] + direction[0]
        new_y = enemy[1] + direction[1]
        
        # Check if valid move
        if (0 < new_x < 9 and 0 < new_y < 9 and 
            grid.get_tile(new_x, new_y) != "wall" and
            [new_x, new_y] != player_pos):
            enemy[0], enemy[1] = new_x, new_y

def restart_game():
    """Reset the game"""
    global player_pos, enemies, game_won
    player_pos = [5, 5]
    enemies = [[8, 3], [2, 7], [9, 9]]
    game_won = False
    scene = create_game()

# Start the game!
if __name__ == "__main__":
    scene = create_game()
    mcrfpy.set_scene(scene)
    mcrfpy.bind_keys(handle_input)
    mcrfpy.run()
```
<button class="copy-btn" onclick="copyCode(this)">📋 Copy All</button>
</div>

<div class="preview-section">
<h3>🖼️ What You'll Build:</h3>
<div class="game-preview">
  <img src="assets/quickstart-game-preview.png" alt="Game Preview" />
  <div class="preview-features">
    <div class="feature">👤 Play as @ symbol</div>
    <div class="feature">👹 Avoid red enemies</div>
    <div class="feature">💰 Collect the treasure</div>
    <div class="feature">🏃 Enemies chase you</div>
  </div>
</div>
</div>

---

## ▶️ Step 4: Run Your Game

<div class="code-block">
```bash
python3 my_first_game.py
```
<button class="copy-btn" onclick="copyCode(this)">📋 Copy</button>
</div>

**Controls:**
- ⬆️⬇️⬅️➡️ **Arrow Keys**: Move your character
- **R**: Restart after winning
- **ESC**: Quit the game

<div class="success-banner">
🎉 **Congratulations!** You've just created your first roguelike game!
</div>

---

## 🎨 Step 5: Quick Customizations

Try these simple modifications to make the game your own:

<div class="customization-grid">
  <div class="custom-option">
    <h4>🎨 Change Characters</h4>
    <div class="code-block">
    ```python
    # In update_display(), change:
    grid.set_entity(player_pos[0], player_pos[1], "🧙", (0, 255, 0))
    grid.set_entity(enemy[0], enemy[1], "👾", (255, 0, 0))
    grid.set_entity(treasure[0], treasure[1], "💎", (255, 255, 0))
    ```
    </div>
  </div>

  <div class="custom-option">
    <h4>🗺️ Bigger Map</h4>
    <div class="code-block">
    ```python
    # Change grid creation:
    grid = scene.add_grid(100, 50, 20, 15, 30, 30)
    # Update boundary checks to match!
    ```
    </div>
  </div>

  <div class="custom-option">
    <h4>⚡ Add Power-ups</h4>
    <div class="code-block">
    ```python
    # Add to game state:
    power_ups = [[4, 4], [6, 8]]
    player_speed = 1

    # In update_display():
    for power in power_ups:
        grid.set_entity(power[0], power[1], "⚡", (0, 255, 255))
    ```
    </div>
  </div>

  <div class="custom-option">
    <h4>🎵 Add Sounds</h4>
    <div class="code-block">
    ```python
    # After treasure collection:
    mcrfpy.play_sound("assets/coin.wav")
    
    # On enemy collision:
    mcrfpy.play_sound("assets/hit.wav")
    ```
    </div>
  </div>
</div>

---

## 🚦 What's Next?

Choose your adventure path:

<div class="next-steps">
  <a href="/tutorial" class="path-card tutorial">
    <h3>📚 Tutorial Path</h3>
    <p>Learn McRogueFace step-by-step</p>
    <ul>
      <li>Core concepts explained</li>
      <li>Build a complete game</li>
      <li>Best practices</li>
    </ul>
    <span class="path-time">2-3 hours</span>
  </a>

  <a href="/cookbook" class="path-card cookbook">
    <h3>🍳 Cookbook Path</h3>
    <p>Quick recipes for common features</p>
    <ul>
      <li>Copy-paste solutions</li>
      <li>Common patterns</li>
      <li>Quick wins</li>
    </ul>
    <span class="path-time">5-10 min each</span>
  </a>

  <a href="/api" class="path-card api">
    <h3>📖 API Reference</h3>
    <p>Complete documentation</p>
    <ul>
      <li>All classes & methods</li>
      <li>Parameters & returns</li>
      <li>Code examples</li>
    </ul>
    <span class="path-time">As needed</span>
  </a>

  <a href="/examples" class="path-card examples">
    <h3>🎮 Example Games</h3>
    <p>Full games with source code</p>
    <ul>
      <li>Classic roguelike</li>
      <li>Puzzle dungeons</li>
      <li>Action RPG</li>
    </ul>
    <span class="path-time">Explore freely</span>
  </a>
</div>

---

## ❓ Troubleshooting

<details>
<summary>🔴 "Module 'mcrfpy' not found"</summary>

Make sure you've installed McRogueFace:
```bash
pip install mcrogueface
# or
pip3 install mcrogueface
```

If using virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install mcrogueface
```
</details>

<details>
<summary>🔴 "No display found" or window doesn't appear</summary>

**On Linux (SSH/headless):**
```bash
# Install virtual display
sudo apt install xvfb
# Run with virtual display
xvfb-run python3 my_first_game.py
```

**On macOS:**
Make sure you're running from Terminal.app, not SSH.

**On Windows:**
Run from Command Prompt or PowerShell, not WSL.
</details>

<details>
<summary>🔴 Game runs but no characters appear</summary>

Check your font support:
```python
# Add after imports
mcrfpy.set_font("assets/fonts/DejaVuSansMono.ttf")
```

Or use ASCII instead of Unicode:
```python
# Use @ instead of 🧙
grid.set_entity(player_pos[0], player_pos[1], "@", (0, 255, 0))
```
</details>

<details>
<summary>🔴 "Segmentation fault" or crash</summary>

1. Check Python version (3.8+ required):
   ```bash
   python3 --version
   ```

2. Rebuild from source:
   ```bash
   git clone https://github.com/mcrogueface/mcrogueface
   cd mcrogueface
   ./build.sh clean
   ./build.sh
   ```

3. Enable debug mode:
   ```python
   mcrfpy.debug_mode(True)
   ```
</details>

<details>
<summary>💡 More help needed?</summary>

- 💬 [Discord Community](https://discord.gg/mcrogueface)
- 🐛 [Report an Issue](https://github.com/mcrogueface/mcrogueface/issues)
- 📧 [Email Support](mailto:support@mcrogueface.com)
- 📺 [Video Tutorials](https://youtube.com/mcrogueface)
</details>

---

<div class="congratulations">
  <h2>🎊 Ready to Build Amazing Roguelikes!</h2>
  <p>You've completed the quickstart and have a working game. The adventure begins now!</p>
  <div class="share-buttons">
    <a href="https://twitter.com/intent/tweet?text=I%20just%20built%20my%20first%20roguelike%20with%20%40mcrogueface%20in%205%20minutes!%20%23gamedev%20%23roguelike" class="share-btn twitter">Share on Twitter</a>
    <a href="https://discord.gg/mcrogueface" class="share-btn discord">Join our Discord</a>
  </div>
</div>

<style>
.progress-tracker {
  display: flex;
  justify-content: space-between;
  margin: 2rem 0;
  padding: 0;
}

.progress-tracker .step {
  flex: 1;
  text-align: center;
  padding: 1rem;
  background: #f0f0f0;
  border-radius: 8px;
  margin: 0 0.5rem;
  font-weight: bold;
  color: #666;
  position: relative;
}

.progress-tracker .step.active {
  background: #4CAF50;
  color: white;
}

.code-block {
  position: relative;
  margin: 1rem 0;
}

.copy-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 0.5rem 1rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.copy-btn:hover {
  background: #45a049;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tab-btn {
  padding: 0.5rem 1rem;
  background: #f0f0f0;
  border: none;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
}

.tab-btn.active {
  background: #333;
  color: white;
}

.tab-content {
  display: none;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 0 4px 4px 4px;
}

.tab-content.active {
  display: block;
}

.install-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.option {
  padding: 1.5rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  position: relative;
}

.option.recommended {
  border-color: #4CAF50;
  background: #f0fff0;
}

.option.recommended::before {
  content: "RECOMMENDED";
  position: absolute;
  top: -12px;
  left: 20px;
  background: #4CAF50;
  color: white;
  padding: 0.2rem 0.8rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.install-time {
  text-align: center;
  color: #666;
  margin-top: 0.5rem;
}

.verify-install {
  background: #e8f5e9;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.preview-section {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.game-preview {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
}

.game-preview img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.preview-features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature {
  padding: 0.8rem;
  background: white;
  border-radius: 4px;
  font-size: 1.1rem;
}

.success-banner {
  background: #4CAF50;
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.2rem;
  margin: 2rem 0;
}

.customization-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin: 2rem 0;
}

.custom-option {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
}

.custom-option h4 {
  margin-top: 0;
  color: #333;
}

.next-steps {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin: 2rem 0;
}

.path-card {
  display: block;
  padding: 2rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  position: relative;
}

.path-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}

.path-card.tutorial { border-color: #2196F3; }
.path-card.cookbook { border-color: #FF9800; }
.path-card.api { border-color: #9C27B0; }
.path-card.examples { border-color: #4CAF50; }

.path-card h3 {
  margin-top: 0;
}

.path-card ul {
  padding-left: 1.5rem;
  margin: 1rem 0;
}

.path-time {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  background: #f0f0f0;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #666;
}

.congratulations {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  margin: 3rem 0;
}

.congratulations h2 {
  margin-top: 0;
}

.share-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.share-btn {
  padding: 0.8rem 1.5rem;
  background: white;
  color: #333;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: transform 0.2s;
}

.share-btn:hover {
  transform: scale(1.05);
}

.share-btn.twitter {
  background: #1DA1F2;
  color: white;
}

.share-btn.discord {
  background: #5865F2;
  color: white;
}

details {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
}

details summary {
  cursor: pointer;
  font-weight: bold;
  padding: 0.5rem;
}

details[open] summary {
  margin-bottom: 1rem;
}
</style>

<script>
function copyCode(button) {
  const codeBlock = button.previousElementSibling;
  const code = codeBlock.textContent;
  navigator.clipboard.writeText(code).then(() => {
    const originalText = button.textContent;
    button.textContent = '✓ Copied!';
    setTimeout(() => {
      button.textContent = originalText;
    }, 2000);
  });
}

function showTab(tabName) {
  // Hide all tabs
  document.querySelectorAll('.tab-content').forEach(tab => {
    tab.classList.remove('active');
  });
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  
  // Show selected tab
  document.getElementById(tabName).classList.add('active');
  event.target.classList.add('active');
}

// Update progress tracker as user scrolls
window.addEventListener('scroll', () => {
  const sections = ['prerequisites', 'install', 'create', 'run', 'customize'];
  const scrollPosition = window.scrollY;
  
  // Update progress based on scroll position
  // Implementation depends on your specific needs
});
</script>