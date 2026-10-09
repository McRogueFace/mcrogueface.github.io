---
layout: default
title: Project History
nav_order: 9
mcrf:
  objects: []
  diataxis: meta
  disposition: rewrite-pending
  verified: "0.3.0-dev"
  verified_commit: 73acab0
---

# McRogueFace Project History
{: .no_toc }

A chronological record of McRogueFace development from inception to present.

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Origins (February 2023)

McRogueFace began as an experimental proof-of-concept combining SFML graphics with embedded Python and libtcod roguelike utilities.

**Initial Commit:** February 23, 2023
- Combined rendering proof-of-concept
- Linux-only, experimental architecture

---

## Foundation Year (2024)

### Q1 2024: 7DRL Game Jam

The 7-Day Roguelike Challenge 2024 transformed McRogueFace from experiment to engine.

**February 2024:**
- Major refactor to Python 3.12
- CMake build system
- libtcod and SFML built from source

**March 2024 (7DRL Week):**
- UIGrid tilemap rendering
- Entity system implementation
- Scene switching API
- Mouse and keyboard input
- Timer system
- Caption text rendering
- Window scaling
- **Crypt of Sokoban** - first complete game built with McRogueFace

**Post-7DRL Stabilization:**
- RAII memory management for Python objects
- Standardized handling: Texture, Color, Vector, Font

### Q2-Q3 2024

Incremental improvements and API refinement between jam events.

### Q4 2024: Roguelike Tutorial Implementation

**October 2024:**
- Complete API reference documentation
- Tutorial Python implementations (Parts 0-6)
- Documentation macro system (MCRF_* macros)
- Profiling system with F3 overlay
- Headless mode with `--headless --exec`

**November 2024:**
- **Python 3.14 migration**
- UI hierarchy foundations (parent/child relationships)
- Drawing primitives: UILine, UICircle, UIArc
- Geometry module for orbital mechanics
- Grid layer system with dirty flags
- Chunk-based rendering for large grids
- RenderTexture caching
- Developer console (ImGui overlay)
- Self-contained venv support for pip packages
- libtcod-headless fork integration

---

## Recent Development (Last 6 Months)

### December 2025

**Performance & Architecture:**
- EntityCollection iterator optimization: O(n²) → O(n), 100× speedup
- SpatialHash for O(1) entity spatial queries
- Animation property locking (prevents conflicts)
- Benchmark extended to 5000 entities

**API Improvements:**
- Scene API with module-level properties
- `click` → `on_click` rename for consistency
- Sound/Music classes
- Keyboard state queries
- Version info exposure

**Research Features:**
- TurnOrchestrator for multi-turn LLM simulation
- Action parser/executor for LLM agents
- WorldGraph for deterministic room descriptions
- VLLM integration demos

**Quality of Life:**
- `mcrfpy.step()` for synchronous headless execution
- Grid camera defaults and `center_camera()` method
- 14-part tutorial Python files

### January 2026 (Current Month)

**Week 1 (Jan 1-5):**
- Timer refactor: stopwatch semantics, `mcrfpy.timers` collection
- Scene transitions via Scene object
- Animation fixes (0-duration edge case, integer values)
- Easing functions as enum
- `.animate` helper method
- Vector improvements (indexing, tuple comparison, floor)
- Position handling: always `mcrfpy.Vector`, accepts tuples/iterables

**Week 2 (Jan 6-10):**
- Code editor window with lockable positions
- `mcrfpy.Mouse` class (symmetry with `mcrfpy.Keyboard`)
- Timer background execution
- Scene object as Python parent support
- Grid.at() segfault fix
- Windows build (mingw cross-compilation)
- Version bump: 0.2.1-prerelease-7drl2026
- Input enums (replacing strings)
- Pathfinding separation: A* and Dijkstra

**Week 3 (Jan 11-14):**
- **HeightMap system** - complete procedural generation toolkit:
  - Core class with scalar operations
  - Query methods, threshold operations
  - Terrain generation (dig_hill, dig_bezier)
  - Kernel transforms, combination operations
  - Noise algorithms with parameters
- **BSP (Binary Space Partitioning):**
  - Procedural dungeon generation
  - Room adjacency graphs
  - Safety features and API improvements
- **Dijkstra-to-HeightMap conversion**
- **Alignment system** - reactive UI positioning
- Test suite modernization with pytest and `mcrfpy.step()` pattern

---

## 0.2.8 and the 0.3.0 Cycle (2026)

**0.2.8** was tagged on June 30, 2026. The 0.3.0 cycle that followed (in development as of October 2026) is the Python 3.15 release. The draft release notes in the engine repo (`docs/release-notes-0.3.0.md`) are the full list; the highlights:

- **Python 3.15**: CPython 3.15.0 is embedded on Linux, Windows and WebAssembly. The `mcrfpy` module uses multi-phase initialization and refuses to load in subinterpreters. Release builds keep frame pointers (PEP 831), so `perf` and gdb can unwind from Python through the engine.
- **Grid type split**: `UIGrid` was removed. `GridData` (the map: cells, layers, entities, FOV, pathfinding) is now public and not drawable; `GridView` (the drawable camera) carries position, size, zoom and cell callbacks. `mcrfpy.Grid` is the same type as `GridView`.
- **Faster and leaner**: the chunk system was replaced by dense walkable/transparent arrays, idle grid views no longer re-render, and the new Crucible benchmark measures about 33% faster than 0.2.8.
- **Headless simulation**: `mcrfpy.step()` is now a full simulation frame, `mcrfpy.advance()` and `set_random_seed()` were added, and `GridData.observe()` snapshots what an observer sees.
- **Threading**: `mcrfpy.lock()` is a tested frame barrier for background threads.
- **Docs as tests**: the site's code samples run in the engine test suite (639 tests).

---

## Version History

| Version | Date | Milestone |
|---------|------|-----------|
| Initial | Feb 2023 | Proof of concept |
| 7DRL 2024 | Mar 2024 | First playable games |
| 0.2.0-prerelease | Jan 2026 | 7DRL 2026 preparation |
| 0.2.1-prerelease | Jan 2026 | Development build |
| 0.2.8 | Jun 2026 | Released |
| 0.3.0 | In development | Python 3.15, Grid type split |

---

## Features Completed (vs Original Roadmap)

The following features from the original roadmap are **now complete**:

- ✅ **Pathfinding API** - A* and Dijkstra with HeightMap integration
- ✅ **Animation System** - Property animations with easing, callbacks, locking
- ✅ **Performance Profiler** - F3 overlay, benchmark logging, dirty flags
- ✅ **Debug Console** - ImGui-based Python REPL overlay
- ✅ **FOV System** - Thread-safe with configurable algorithms

---

## Development Philosophy Evolution

From the [Strategic Direction](https://dev.ffwf.net/forgejo/john/McRogueFace/wiki/Strategic-Direction) wiki:

> "Fix foundation systems before expanding features."

The project evolved from feature-focused development to a **foundation-first approach**:

1. **Target Audience**: Beginners, game jam participants, researchers
2. **Core Principle**: "Batteries included but removable"
3. **v1.0 Criteria**: Performance, stability, and documentation—not feature count

### What Was Deferred

Per strategic direction, these are intentionally deferred until after v1.0:
- Python wheel packaging
- Shader support
- Particle systems
- Multi-window support

### What Was Abandoned

These ambitious features were deemed misaligned with the beginner-focused mission:
- Living world MMO features
- Full ECS rewrites
- 50,000-tile ecosystems

---

## Contributing to History

This document is maintained by the GoblinCorps team. For corrections or additions, please file an issue at the [GoblinCorps fork](https://github.com/GoblinCorps/mcrogueface.github.io).
