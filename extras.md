---
layout: default
title: Extras & Fun
nav_order: 9
---

# Extras & Fun
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 🎮 Live Playground

<div class="playground-container">
  <h3>Try McRogueFace in Your Browser!</h3>
  <iframe src="https://mcrogueface.github.io/playground" width="100%" height="600px" frameborder="0"></iframe>
  
  <div class="playground-controls">
    <button onclick="loadExample('roguelike')">Load Roguelike</button>
    <button onclick="loadExample('platformer')">Load Platformer</button>
    <button onclick="loadExample('puzzle')">Load Puzzle Game</button>
    <button onclick="resetPlayground()">Reset</button>
  </div>
  
  <details>
    <summary>Example Code Snippets</summary>
    
```python
# Quick roguelike room
import mcrfpy

# Create a room with walls
room = mcrfpy.Grid(20, 20)
room.fill_rect(0, 0, 20, 20, WALL)
room.fill_rect(1, 1, 18, 18, FLOOR)

# Add a player
player = mcrfpy.Entity(10, 10, "@")
player.color = (0, 255, 0)

# Add some enemies
for i in range(5):
    enemy = mcrfpy.Entity(
        random.randint(2, 18),
        random.randint(2, 18),
        "g"
    )
    enemy.color = (255, 0, 0)
```
  </details>
</div>

---

## 🏆 Game Showcase Gallery

<div class="showcase-grid">
  <div class="showcase-item">
    <img src="assets/games/crypt-of-sokoban.gif" alt="Crypt of Sokoban">
    <h4>Crypt of Sokoban</h4>
    <p>The original 7DRL entry that started it all!</p>
    <div class="showcase-tags">
      <span class="tag">Puzzle</span>
      <span class="tag">Roguelike</span>
    </div>
    <a href="https://github.com/user/crypt-of-sokoban" class="showcase-link">View Source</a>
  </div>
  
  <div class="showcase-item">
    <img src="assets/games/dungeon-merchant.gif" alt="Dungeon Merchant">
    <h4>Dungeon Merchant</h4>
    <p>Run a shop in a dangerous dungeon!</p>
    <div class="showcase-tags">
      <span class="tag">Economy</span>
      <span class="tag">Strategy</span>
    </div>
    <a href="https://github.com/user/dungeon-merchant" class="showcase-link">View Source</a>
  </div>
  
  <div class="showcase-item">
    <img src="assets/games/ascii-garden.gif" alt="ASCII Garden">
    <h4>ASCII Garden</h4>
    <p>Peaceful gardening with procedural plants</p>
    <div class="showcase-tags">
      <span class="tag">Simulation</span>
      <span class="tag">Relaxing</span>
    </div>
    <a href="https://github.com/user/ascii-garden" class="showcase-link">View Source</a>
  </div>
  
  <div class="showcase-item">
    <img src="assets/games/robot-escape.gif" alt="Robot Escape">
    <h4>Robot Escape</h4>
    <p>Program robots to solve puzzles</p>
    <div class="showcase-tags">
      <span class="tag">Programming</span>
      <span class="tag">Puzzle</span>
    </div>
    <a href="https://github.com/user/robot-escape" class="showcase-link">View Source</a>
  </div>
</div>

<div class="submit-game">
  <h3>Made something cool?</h3>
  <a href="https://github.com/mcrogueface/showcase/issues/new" class="btn btn-primary">
    Submit Your Game!
  </a>
</div>

---

## 📦 Asset Packs & Resources

### Official Asset Packs

<div class="asset-grid">
  <div class="asset-pack">
    <h4>🎨 Classic Roguelike Pack</h4>
    <p>Traditional ASCII tileset with 256 glyphs</p>
    <ul>
      <li>Multiple font styles</li>
      <li>Color palettes</li>
      <li>UI elements</li>
    </ul>
    <a href="https://github.com/mcrogueface/assets-classic" class="btn">Download</a>
  </div>
  
  <div class="asset-pack">
    <h4>🏰 Dungeon Tileset</h4>
    <p>16x16 pixel art for dungeon crawlers</p>
    <ul>
      <li>Walls and floors</li>
      <li>Doors and furniture</li>
      <li>Treasure and items</li>
    </ul>
    <a href="https://github.com/mcrogueface/assets-dungeon" class="btn">Download</a>
  </div>
  
  <div class="asset-pack">
    <h4>👾 Sci-Fi Terminal</h4>
    <p>Futuristic fonts and UI elements</p>
    <ul>
      <li>Glowing effects</li>
      <li>Tech borders</li>
      <li>Holographic colors</li>
    </ul>
    <a href="https://github.com/mcrogueface/assets-scifi" class="btn">Download</a>
  </div>
  
  <div class="asset-pack">
    <h4>🎵 Sound Effects Library</h4>
    <p>200+ game-ready sound effects</p>
    <ul>
      <li>Combat sounds</li>
      <li>UI feedback</li>
      <li>Ambient loops</li>
    </ul>
    <a href="https://github.com/mcrogueface/assets-audio" class="btn">Download</a>
  </div>
</div>

### Community Resources

- [Awesome McRogueFace](https://github.com/community/awesome-mcrogueface) - Curated list of resources
- [Tileset Converter](https://tools.mcrogueface.dev/converter) - Convert tilesets from other engines
- [Palette Generator](https://tools.mcrogueface.dev/palette) - Create cohesive color schemes
- [ASCII Art Tool](https://tools.mcrogueface.dev/ascii) - Design sprites and logos

---

## 🛠️ Community Tools & Utilities

### Development Tools

<div class="tools-list">
  <div class="tool-item">
    <h4>McRogueFace VSCode Extension</h4>
    <p>Syntax highlighting, snippets, and debugging</p>
    <code>ext install mcrogueface.vscode</code>
  </div>
  
  <div class="tool-item">
    <h4>Level Editor Plugin</h4>
    <p>Visual level design with live preview</p>
    <code>pip install mcrogueface-editor</code>
  </div>
  
  <div class="tool-item">
    <h4>Sprite Sheet Packer</h4>
    <p>Optimize your game's graphics</p>
    <code>npm install -g mcrogue-pack</code>
  </div>
  
  <div class="tool-item">
    <h4>Performance Profiler</h4>
    <p>Find bottlenecks in your game</p>
    <code>cargo install mcrogue-prof</code>
  </div>
</div>

### Game Templates

```bash
# Install the template generator
pip install mcrogueface-templates

# Create a new game from template
mcrogue new my-game --template roguelike
mcrogue new my-game --template puzzle
mcrogue new my-game --template action
```

---

## 🥚 Easter Eggs & Secrets

### Hidden Features

<div class="easter-eggs">
  <details>
    <summary>🔍 The Konami Code</summary>
    <p>Press ↑↑↓↓←→←→BA in any McRogueFace game to unlock developer mode!</p>
  </details>
  
  <details>
    <summary>🎭 Secret Color Mode</summary>
    <p>Set <code>mcrfpy.SECRET_COLORS = True</code> for psychedelic rendering!</p>
  </details>
  
  <details>
    <summary>🐉 Hidden Boss</summary>
    <p>Name your player "MCROGUEFACE" to spawn a special boss in any dungeon!</p>
  </details>
  
  <details>
    <summary>🎪 Party Mode</summary>
    <p>Run <code>import mcrfpy.party</code> on your birthday for a surprise!</p>
  </details>
</div>

### Dev Team Signatures

Find these hidden messages in the source code:
- `// Here be dragons` - marks particularly complex code
- `/* TCB was here */` - original author's signature
- `# TODO: Make this less hacky` - appears 42 times!

---

## 🎉 Fun Facts

<div class="fun-facts">
  <div class="fact-card">
    <h4>📊 By the Numbers</h4>
    <ul>
      <li>7 days to create original game</li>
      <li>42,000+ lines of code</li>
      <li>300+ commits in first month</li>
      <li>17 cups of coffee per feature</li>
    </ul>
  </div>
  
  <div class="fact-card">
    <h4>🎨 Design Inspirations</h4>
    <ul>
      <li>Dwarf Fortress (ASCII aesthetics)</li>
      <li>Pico-8 (simplicity)</li>
      <li>Love2D (Lua influence)</li>
      <li>Pygame (Python focus)</li>
    </ul>
  </div>
  
  <div class="fact-card">
    <h4>🏗️ Development Stories</h4>
    <ul>
      <li>First version had no save feature</li>
      <li>Python integration took 3 rewrites</li>
      <li>The grid system was inspired by spreadsheets</li>
      <li>Sound support added due to one user request</li>
    </ul>
  </div>
</div>

### Community Achievements

- 🏆 **First Community Game Jam** - 50 entries in 48 hours!
- 🌟 **1000th GitHub Star** - Reached in just 3 months
- 🎮 **Most Complex Game** - "Infinite Dungeon" with 10k lines of Python
- 🤝 **Largest Contribution** - Complete French translation by @pierredev

---

## 👏 Credits & Acknowledgments

### Core Team

<div class="credits-grid">
  <div class="credit-card">
    <img src="assets/avatars/john.png" alt="John">
    <h4>John</h4>
    <p>Project Creator & Lead Developer</p>
    <div class="social-links">
      <a href="https://github.com/john">GitHub</a>
      <a href="https://twitter.com/john">Twitter</a>
    </div>
  </div>
  
  <div class="credit-card">
    <img src="assets/avatars/contributor1.png" alt="Contributor">
    <h4>Sarah Chen</h4>
    <p>Python API Design</p>
    <div class="social-links">
      <a href="https://github.com/schen">GitHub</a>
    </div>
  </div>
  
  <div class="credit-card">
    <img src="assets/avatars/contributor2.png" alt="Contributor">
    <h4>Alex Rivera</h4>
    <p>Documentation & Tutorials</p>
    <div class="social-links">
      <a href="https://github.com/arivera">GitHub</a>
    </div>
  </div>
</div>

### Special Thanks

- **7DRL Community** - For the inspiration and feedback
- **SFML Team** - For the excellent graphics library
- **Python Software Foundation** - For the best scripting language
- **Our Families** - For understanding the late night coding sessions

### Open Source Libraries

McRogueFace stands on the shoulders of giants:

- [SFML](https://www.sfml-dev.org/) - Simple and Fast Multimedia Library
- [libtcod](https://github.com/libtcod/libtcod) - The Doryen Library
- [Dear ImGui](https://github.com/ocornut/imgui) - Immediate Mode GUI
- [CPython](https://github.com/python/cpython) - Python interpreter

### Community Contributors

Thank you to our [100+ contributors](https://github.com/mcrogueface/mcrogueface/graphs/contributors) who have made McRogueFace what it is today!

---

<div class="final-message">
  <h2>🚀 Ready to Start Your Adventure?</h2>
  <p>Join thousands of developers creating amazing roguelike games!</p>
  <div class="cta-buttons">
    <a href="quickstart.html" class="btn btn-primary btn-lg">Get Started</a>
    <a href="https://github.com/jmccardle/McRogueFace" class="btn btn-secondary btn-lg">View Source</a>
  </div>
</div>

<style>
.playground-container {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 10px;
  margin: 2rem 0;
}

.playground-controls {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  justify-content: center;
}

.showcase-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.showcase-item {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.showcase-item:hover {
  transform: translateY(-5px);
}

.showcase-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.showcase-item h4 {
  padding: 1rem 1rem 0;
  margin: 0;
}

.showcase-item p {
  padding: 0.5rem 1rem;
  color: #666;
}

.showcase-tags {
  padding: 0 1rem;
  display: flex;
  gap: 0.5rem;
}

.tag {
  background: #e0e0e0;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
}

.showcase-link {
  display: block;
  padding: 1rem;
  text-align: center;
  background: #667eea;
  color: white;
  text-decoration: none;
  transition: background 0.3s;
}

.showcase-link:hover {
  background: #5a67d8;
}

.submit-game {
  text-align: center;
  margin: 3rem 0;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 10px;
}

.asset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.asset-pack {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.asset-pack h4 {
  margin-top: 0;
  color: #667eea;
}

.tools-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin: 2rem 0;
}

.tool-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 10px;
  border-left: 4px solid #667eea;
}

.tool-item h4 {
  margin-top: 0;
}

.tool-item code {
  background: #e0e0e0;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  display: inline-block;
  margin-top: 0.5rem;
}

.easter-eggs {
  margin: 2rem 0;
}

.easter-eggs details {
  background: #f8f9fa;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 10px;
  cursor: pointer;
}

.easter-eggs summary {
  font-weight: bold;
  font-size: 1.1rem;
}

.fun-facts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.fact-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 10px;
}

.fact-card h4 {
  margin-top: 0;
}

.fact-card ul {
  margin: 0;
  padding-left: 1.5rem;
}

.credits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.credit-card {
  text-align: center;
  padding: 1.5rem;
}

.credit-card img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 1rem;
}

.social-links {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 0.5rem;
}

.social-links a {
  color: #667eea;
  text-decoration: none;
}

.final-message {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
  border-radius: 10px;
  margin: 3rem 0;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .showcase-grid,
  .asset-grid,
  .fun-facts,
  .credits-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>

<script>
// Placeholder functions for demo
function loadExample(type) {
  console.log(`Loading ${type} example...`);
  // In production, this would load actual examples
}

function resetPlayground() {
  console.log('Resetting playground...');
  // In production, this would reset the iframe
}
</script>