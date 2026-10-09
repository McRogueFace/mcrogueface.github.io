---
layout: default
title: Roadmap & Future
nav_order: 8
mcrf:
  objects: []
  diataxis: meta
  disposition: rewrite-pending
  verified: "0.3.0-dev"
  verified_commit: 73acab0
---

# Roadmap & Future
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Current Status: 0.2.8 released, 0.3.0 in preparation

<div class="status-banner">
  <h3>0.3.0: Python 3.15</h3>
  <p>The current release is 0.2.8. The next release, 0.3.0, embeds CPython 3.15 and is being prepared now.</p>
</div>

### What shipped since 0.2.8 (on master, headed for 0.3.0)

- **Python 3.15** - CPython 3.15.0 is embedded on Linux, Windows and the web build. `mcrfpy` refuses to import in subinterpreters, and release builds keep frame pointers so `perf` and gdb can unwind from Python through the engine.
- **Grid type split** - `GridData` (the map: cells, layers, entities, FOV, pathfinding) is now public and separate from `GridView` (the drawable camera). `mcrfpy.Grid` is the same type as `GridView`. `entity.grid` now returns a `GridData`.
- **Grid input works again** - cell callbacks, hover, clickable overlay children, and several views over one map.
- **About 33% faster** overall than 0.2.8 on the headless Crucible benchmark, with dense grid storage, O(1) `grid.entities` indexing and idle-view render caching.
- **Zero-copy numpy views** - `with layer.edit() as view:` on color and tile layers, and the buffer protocol on `DiscreteMap`.
- **Deterministic headless simulation** - `mcrfpy.step()` is a full simulation frame, `mcrfpy.advance(ms)` advances simulation time, and `mcrfpy.set_random_seed()` seeds the engine's random streams.
- **`GridData.observe()`** - snapshot what an observer sees through a field of view (experimental).
- **Fixes** - `DijkstraMap.path_from()` no longer returns its path reversed, `.parent` and `find()` keep Python subclass identity, and `mcrfpy.lock()` deadlocks in headless and multi-thread use are gone.
- **Docs are tests** - the site's code samples run in the engine's test suite.

The full list, including breaking changes, is in the 0.3.0 release notes in the engine repository (`docs/release-notes-0.3.0.md`). Progress is tracked on the [0.3.0 release board](https://dev.ffwf.net/forgejo/john/McRogueFace/projects/8).

### Still being finished for 0.3.0

- Bug fixes: leaks in position setters and `get_metrics()`, `--exec` tracebacks, a flaky audio teardown in the test suite, and project scaffolding for the new Python version.
- `Sound.play_varied()` will play on a separate voice so the variation is actually heard.
- Timers will catch up across a wide step, so an interval of T over a long span fires the expected number of times.
- `clear()` will be added to `UICollection` and `EntityCollection`.
- `VisibilityMask` will get value equality and hashing.
- `--audio-off` / `config.audio_enabled` will be made to work.

For complete development history, see [Project History](history.md).

---

## Completed Features

The following major systems are **implemented and functional**:

### Core Engine
- **Scene System** - `mcrfpy.Scene()` with children, activation, input handling
- **Timer System** - `mcrfpy.Timer()` with `(timer, runtime)` callbacks
- **Animation System** - Property animations with easing, callbacks, locking
- **Input System** - Keyboard/Mouse classes with state queries

### Grid & Entities
- **Grid Rendering** - `GridView` cameras over a shared `GridData`, with dirty tracking and RenderTexture caching
- **Entity System** - SpatialHash for O(1) queries, 5000+ entity benchmarks
- **FOV System** - Thread-safe field-of-view with configurable algorithms
- **Pathfinding API** - A* and Dijkstra with HeightMap integration

### Procedural Generation
- **HeightMap** - Terrain generation, noise, thresholds, kernel transforms
- **BSP** - Binary Space Partitioning for dungeon layouts
- **Noise Algorithms** - Multiple algorithms with parameter control

### Developer Tools
- **Debug Console** - ImGui-based Python REPL overlay (press `)
- **Performance Profiler** - F3 overlay with frame timing and metrics
- **Headless Mode** - `mcrfpy.step()` for synchronous testing
- **Benchmark Logging** - Performance analysis system

### Documentation
- **API Reference** - Complete Python API documentation
- **Tutorials** - Multi-part roguelike tutorial series
- **Cookbook** - Practical recipes with screenshots

---

## Version 1.0 Target

### Remaining Work

#### API Stability
- [ ] Finalize Scene/Timer/Animation APIs (the public surface is already locked behind a snapshot test, and breaking changes are being bundled)
- [x] Complete deprecation of old patterns (camelCase module functions, `sprite_number`, string enum comparisons removed)
- [ ] Comprehensive test coverage (the suite is at 639 tests, up from about 300 at 0.2.8)

#### Documentation
- [ ] All docs using modern API patterns
- [ ] Tutorial code verified runnable
- [ ] Video tutorials (stretch goal)

#### Polish
- [ ] Example games updated
- [ ] Error messages improved
- [ ] Edge cases handled

### Success Criteria

Per the [Strategic Direction](https://dev.ffwf.net/forgejo/john/McRogueFace/wiki/Strategic-Direction):

> v1.0 readiness is measured through performance targets, API stability, complete documentation, and tutorial completion—not feature completeness.

---

## Post-v1.0: Deferred Features

These features are intentionally deferred until after v1.0 stabilization:

- **Python Wheel Packaging** - pip-installable distribution
- **Shader Support** - Custom GLSL effects
- **Particle Systems** - Visual effects
- **Multi-window Support** - Multiple render targets

---

## Not Planned

The following have been evaluated and deemed misaligned with McRogueFace's beginner-focused mission:

- Living world MMO features
- Full ECS architecture rewrites
- 50,000-tile ecosystem simulations
- Network/multiplayer support (removed from v1.0 scope)

---

## Development Philosophy

### Target Audiences

1. **Newcomers** to game development
2. **Game jam** participants
3. **Researchers** using games as environments

### Core Values

1. **Simplicity First** - Easy things should be easy
2. **Power When Needed** - Complex things should be possible
3. **Batteries Included** - Useful defaults, removable when needed
4. **Open Source Forever** - Free as in freedom

### Design Principles

- **Minimal Boilerplate** - Start coding game logic immediately
- **Pythonic API** - Feels natural to Python developers
- **Performance Conscious** - Fast by default, optimizable when needed
- **Foundation First** - Fix core systems before expanding features

---

## Project Timeline

| Date | Milestone |
|------|-----------|
| Feb 2023 | Initial proof-of-concept |
| Mar 2024 | 7DRL 2024 - First complete games |
| Oct 2024 | Tutorial implementation, documentation system |
| Nov 2024 | Python 3.14, Grid layers, drawing primitives |
| Dec 2025 | Performance optimizations, LLM research features |
| Jan 2026 | HeightMap, BSP, Alignment, test modernization |
| Feb-Mar 2026 | 7DRL 2026 |
| Mar-Jul 2026 | 0.2.8, API freeze work, fuzz-driven bug sweep, Grid type split |
| **Oct 2026** | **0.3.0 in preparation (Python 3.15)** |
| TBD | Version 1.0 |

For detailed month-by-month history, see [Project History](history.md).

---

## Contributing

McRogueFace development happens at:
- **Upstream**: [dev.ffwf.net/forgejo/john/McRogueFace](https://dev.ffwf.net/forgejo/john/McRogueFace)
- **GitHub Mirror**: [github.com/jasons-gh/McRogueFace](https://github.com/jasons-gh/McRogueFace)

We welcome:
- Bug reports and feature requests
- Documentation improvements
- Tutorial contributions
- Example games

<style>
.status-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
  margin: 2rem 0;
}

.status-banner h3 {
  margin: 0 0 0.5rem 0;
}

.status-banner p {
  margin: 0;
  opacity: 0.9;
}
</style>
