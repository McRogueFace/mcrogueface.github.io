---
layout: default
title: Roadmap & Future
nav_order: 8
---

# Roadmap & Future
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Current Status: 0.2.1-prerelease-7drl2026

<div class="status-banner">
  <h3>Preparing for 7DRL 2026!</h3>
  <p>Active development toward the Seven Day Roguelike Challenge</p>
</div>

### Recent Achievements

- **HeightMap System** - Complete procedural terrain generation toolkit
- **BSP Dungeons** - Binary Space Partitioning with room adjacency
- **Alignment System** - Reactive UI positioning (9 anchor points)
- **Dijkstra-to-HeightMap** - Pathfinding data for procgen
- **Test Modernization** - pytest integration with `mcrfpy.step()` pattern

For complete development history, see [Project History](history.md).

---

## Immediate Milestone: 7DRL 2026

**Seven Day Roguelike Challenge**
February 28 - March 8, 2026

### Goals
- Stable engine for jam participants
- Complete documentation and tutorials
- Performance validated for typical roguelike scope

### Pre-Jam Checklist
- [ ] Documentation audit complete
- [ ] All tutorials use modern API
- [ ] Quick-reference verified accurate
- [ ] Example games runnable

---

## Completed Features

The following major systems are **implemented and functional**:

### Core Engine
- **Scene System** - `mcrfpy.Scene()` with children, activation, input handling
- **Timer System** - `mcrfpy.Timer()` with `(timer, runtime)` callbacks
- **Animation System** - Property animations with easing, callbacks, locking
- **Input System** - Keyboard/Mouse classes with state queries

### Grid & Entities
- **Grid Rendering** - Chunk-based with dirty flags and RenderTexture caching
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

## Version 1.0 Target: Mid-2026

### Remaining Work

#### API Stability
- [ ] Finalize Scene/Timer/Animation APIs
- [ ] Complete deprecation of old patterns
- [ ] Comprehensive test coverage

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
| **Feb-Mar 2026** | **7DRL 2026 target** |
| Mid 2026 | Version 1.0 target |

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
