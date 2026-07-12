---
layout: default
title: Turn Manager
mcrf:
  objects: [Grid, Entity, Behavior, Trigger, DijkstraMap, AStarPath]
  diataxis: explanation
  disposition: current
  verified: "0.2.9-dev"
  verified_commit: b6720f6
---

# Turn Manager

The Turn Manager is McRogueFace's engine-native turn system. Instead of writing a Python scheduler that walks your actor list every turn, you attach a *behavior* to each entity, and a single call — `grid.step()` — advances the whole world by one round: enemies patrol, wander, sleep, chase, and report back to your code through trigger callbacks.

This page explains how a round actually unfolds and why the pieces (turn order, behaviors, labels, triggers) fit together the way they do. For a hand-rolled initiative system built in Python, see the [Turn-Based Game Loop](../cookbook/combat_turn_system) recipe — the native manager replaces it for the common case.

## Overview

Every call to `grid.step()` runs one *round*. A round is a fixed pipeline:

```
grid.step()
  ├── collect entities where turn_order != 0
  ├── sort by turn_order (ascending)
  └── for each entity:
        ├── target_label set and a labeled entity visible?
        │     └── fire TARGET trigger, skip behavior this round
        └── otherwise execute the behavior:
              ├── MOVED   → update cell + draw position
              ├── DONE    → fire DONE, revert to default_behavior
              ├── BLOCKED → fire BLOCKED
              └── no action (IDLE, CUSTOM, SLEEP mid-count)
```

The turn manager is deliberately synchronous and deterministic in structure: nothing happens between rounds unless you call `step()` again. Your game decides *when* a round happens (typically after the player acts); the engine decides *what* each entity does within it.

## Objects

| Object | Purpose |
|--------|---------|
| [Grid](../objects/Grid) | Hosts entities; `step()` drives rounds |
| [Entity](../objects/Entity) | Carries behavior, turn order, labels, callbacks |
| Behavior | Enum of built-in behavior types |
| Trigger | Enum passed to step callbacks |
| [DijkstraMap](../objects/DijkstraMap) | Pathfinder for SEEK/FLEE behaviors |

---

## Stepping the World {#step}

```python
grid.step(n=1, turn_order=None)
```

- `n`: how many full rounds to execute (default 1).
- `turn_order`: if given, only entities with **exactly** this `turn_order` value are processed — useful for running one phase of a multi-phase turn (e.g. "fast monsters" before "slow monsters").

`grid.step()` is a plain method call, so it works identically in a windowed game (call it from your `on_key` handler after the player moves) and in headless scripts. Entities whose behavior is `IDLE` are skipped entirely — they neither move nor fire triggers.

```python
def on_key(key, state):
    if state != mcrfpy.InputState.PRESSED:
        return
    if try_player_move(key):   # your movement logic
        grid.step()            # ...then the world takes its turn
scene.on_key = on_key
```

---

## Turn Order {#turn-order}

Each entity has an integer `turn_order` (default `1`):

- **`0` means skip.** The turn manager never processes the entity. This is the standard setting for the player, who is moved by your input code rather than by a behavior.
- **Higher values act later.** Within a round, entities are sorted ascending, so `turn_order=1` entities all act before `turn_order=2` entities. Entities sharing a value run in no guaranteed relative order.

```python
player.turn_order = 0   # manual control, never stepped
guard.turn_order = 1    # acts first
slime.turn_order = 2    # acts after all guards
```

Because `grid.step(turn_order=N)` filters to a single value, you can also drive phases manually — `grid.step(turn_order=1)` then, after some animation or interrupt check, `grid.step(turn_order=2)`.

---

## Behaviors {#behaviors}

A behavior is the entity's standing orders. Set one with `set_behavior()`:

```python
entity.set_behavior(type, waypoints=None, turns=0, path=None, pathfinder=None)
```

| Behavior | Arguments | What it does |
|----------|-----------|--------------|
| `Behavior.IDLE` | — | Nothing (entity is skipped) |
| `Behavior.CUSTOM` | — | No built-in action; your code drives the entity |
| `Behavior.NOISE4` | — | Random step in 4 cardinal directions |
| `Behavior.NOISE8` | — | Random step in 8 directions |
| `Behavior.PATH` | `path=[(x, y), ...]` | Follow a precomputed path, then DONE |
| `Behavior.WAYPOINT` | `waypoints=[(x, y), ...]` | A* through waypoints in order, then DONE |
| `Behavior.PATROL` | `waypoints=[...]` | Walk waypoints back and forth (never DONE) |
| `Behavior.LOOP` | `waypoints=[...]` | Cycle waypoints forever (never DONE) |
| `Behavior.SLEEP` | `turns=N` | Wait N rounds, then DONE |
| `Behavior.SEEK` | `pathfinder=...` | Move toward a target each round |
| `Behavior.FLEE` | `pathfinder=...` | Move away from a target each round |

`behavior_type` is read-only — `set_behavior()` is the only way to change it, and each call resets the behavior's internal state (waypoint progress, path index, sleep counter).

### SEEK and FLEE pathfinders

`pathfinder` accepts a [DijkstraMap](../objects/DijkstraMap), an [AStarPath](../objects/AStarPath), or a plain `(x, y)` target tuple. The Dijkstra form is the roguelike workhorse: root the map at the target, and any number of entities can descend it simultaneously.

```python
dm = grid.get_dijkstra_map(player.cell_pos)
for enemy in pack:
    enemy.set_behavior(mcrfpy.Behavior.SEEK, pathfinder=dm)
```

`get_dijkstra_map()` caches maps per root position; call `grid.clear_dijkstra_maps()` after changing walkability. When the target moves, hand the entity a freshly rooted map (see the chase example below).

---

## Trigger Callbacks {#triggers}

Behaviors report noteworthy moments through the entity's step callback:

```python
def on_trigger(trigger, data):
    ...
entity.step = on_trigger
```

Subclasses of `Entity` can define an `on_step(self, trigger, data)` method instead of assigning `entity.step` — the turn manager falls back to it when no `step` callback is set.

| Trigger | When it fires | `data` |
|---------|---------------|--------|
| `Trigger.DONE` | Behavior completed (path exhausted, sleep finished) | `None` |
| `Trigger.BLOCKED` | Movement blocked, no path found, or SEEK/FLEE cannot advance | Entity occupying the intended cell, or `None` |
| `Trigger.TARGET` | An entity matching `target_label` is visible (see [Labels](#labels)) | The spotted Entity |

Exceptions raised inside a callback are printed to stderr and swallowed; they do not abort the round.

Three ordering rules matter in practice:

1. **DONE reverts the behavior *after* your callback returns.** The engine sets `behavior_type` back to `default_behavior` (default `IDLE`) once the DONE callback finishes — so a `set_behavior()` call made inside the callback is clobbered unless `default_behavior` matches the type you set. The patrol example below shows the idiom.
2. **TARGET replaces the behavior for that round.** While `target_label` is set and a matching entity is in view, the TARGET trigger fires *instead of* running the behavior — every round. React once (e.g. switch to SEEK) and clear `target_label`, or your entity will stand still admiring its target.
3. **SEEK has no arrival trigger.** Reaching the Dijkstra root — or having nowhere better to step — reports BLOCKED. Treat "BLOCKED while seeking" as "arrived or stuck" and check positions yourself.

---

## Labels: Collision and Targeting {#labels}

`entity.labels` is a frozenset of strings. Assign any iterable to replace the whole set, or use `add_label()` / `remove_label()` / `has_label()`:

```python
player = mcrfpy.Entity((5, 5), grid=grid, labels=["player"])
orc.labels = {"hostile", "orc"}
orc.add_label("elite")
```

Labels feed two mechanisms:

- **Targeting.** Set `entity.target_label = "player"` and the turn manager scans within `entity.sight_radius` (default 10) each round. If a labeled entity is there *and* line-of-sight holds (a real FOV check — walls hide targets), the TARGET trigger fires with the spotted entity as `data`.
- **Pathfinding collision.** `grid.find_path(..., collide="hostile")` and `grid.get_dijkstra_map(..., collide="hostile")` treat cells occupied by matching entities as blocked. Behavior movement itself only respects tile walkability — entities do not physically block each other, so use `collide=` (or check `cell_pos` yourself) where it matters.

---

## Logical Position vs Draw Position {#positions}

An entity has two positions, and the turn system is built on the distinction:

- `grid_pos` (alias `cell_pos`, with `grid_x`/`grid_y`/`cell_x`/`cell_y` components) — the integer cell the entity *logically* occupies. Collision, FOV, targeting, and the turn manager all use this.
- `draw_pos` — the fractional tile position used for rendering, so a sprite can glide between cells while the logic already considers the move complete. `pos` is the same thing in pixels (`draw_pos * tile_size`).

When a behavior moves an entity, `grid.step()` updates **both**. When *you* move an entity by assigning `grid_pos`, the draw position does **not** follow — set `draw_pos` too (or animate it) if the entity should visibly move. `move_speed` (default `0.15`) is the animation duration in seconds for behavior movement; `0` means instant.

One consequence worth knowing: pathfinding methods that accept an Entity argument read its *draw* position. If you teleport the player with `grid_pos` alone, root your Dijkstra maps at `player.cell_pos` rather than passing `player` itself.

---

## Rendering Interaction {#rendering}

The renderer caches grid composition aggressively and skips redrawing an unchanged grid. `grid.step()` participates in this correctly: if any entity moved during the call, the grid's content generation is bumped and every attached view invalidates its render cache automatically. You never need to poke the grid after stepping — moves made by the turn manager appear on the next frame, exactly like moves made through the Python position setters.

---

## Example: Waypoint Patrol {#example-patrol}

A guard walks a three-point route; the DONE trigger reverses the route so it marches back. Note the `default_behavior` idiom from [rule 1](#triggers). Run it with `./mcrogueface --headless --exec patrol.py`.

```python
"""Waypoint patrol: a guard walks a route, and the DONE trigger sends it back."""
import mcrfpy
import sys

# --- Build a small walled room -------------------------------------------
scene = mcrfpy.Scene("patrol")
mcrfpy.current_scene = scene

tex = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)
grid = mcrfpy.Grid(grid_size=(12, 8), texture=tex, pos=(0, 0), size=(384, 256))
scene.children.append(grid)

for y in range(8):
    for x in range(12):
        cell = grid.at(x, y)
        wall = x == 0 or y == 0 or x == 11 or y == 7
        cell.walkable = not wall
        cell.transparent = not wall

# --- Guard: WAYPOINT route, reversed on completion ------------------------
route = [(2, 2), (9, 2), (9, 5)]

guard = mcrfpy.Entity((2, 2), grid=grid, sprite_index=84)
guard.set_behavior(mcrfpy.Behavior.WAYPOINT, waypoints=route)

# After a DONE trigger the engine reverts behavior_type to default_behavior.
# That revert happens AFTER the step callback returns, so it would clobber a
# set_behavior() call made inside the callback unless the default matches.
guard.default_behavior = mcrfpy.Behavior.WAYPOINT

def on_trigger(trigger, data):
    if trigger == mcrfpy.Trigger.DONE:
        # Route finished: walk it back the other way.
        route.reverse()
        guard.set_behavior(mcrfpy.Behavior.WAYPOINT, waypoints=route)
        print("  route complete, reversing")
    elif trigger == mcrfpy.Trigger.BLOCKED:
        print("  path blocked at", guard.cell_pos)

guard.step = on_trigger

# --- Run 24 turns ---------------------------------------------------------
for turn in range(1, 25):
    grid.step()
    print(f"turn {turn:2d}: guard at ({guard.cell_x}, {guard.cell_y})")

sys.exit(0)
```

Output (abridged):

```
turn  7: guard at (9, 2)
turn  8: guard at (9, 3)
turn  9: guard at (9, 4)
turn 10: guard at (9, 5)
  route complete, reversing
turn 11: guard at (9, 5)
turn 12: guard at (9, 4)
```

(If you only want the ping-pong, `Behavior.PATROL` does it in one line with no callback — this example uses WAYPOINT to show the DONE machinery.)

---

## Example: Detect and Chase {#example-chase}

A hound wanders randomly with `target_label` armed. When the player crosses into its FOV, the TARGET trigger fires and the hound switches to SEEK on a Dijkstra map re-rooted at the player every round. Note [rule 2](#triggers): the handler clears `target_label` so SEEK actually runs.

```python
"""Label-based detection + Dijkstra chase: a hound wanders until it spots
the player, then seeks along a refreshed DijkstraMap every turn."""
import mcrfpy
import sys

# --- Build a walled room with one obstacle wall ---------------------------
scene = mcrfpy.Scene("chase")
mcrfpy.current_scene = scene

tex = mcrfpy.Texture("assets/kenney_tinydungeon.png", 16, 16)
grid = mcrfpy.Grid(grid_size=(16, 10), texture=tex, pos=(0, 0), size=(512, 320))
scene.children.append(grid)

for y in range(10):
    for x in range(16):
        cell = grid.at(x, y)
        wall = x == 0 or y == 0 or x == 15 or y == 9
        cell.walkable = not wall
        cell.transparent = not wall

for y in range(1, 7):  # vertical wall with a gap at the bottom
    grid.at(8, y).walkable = False
    grid.at(8, y).transparent = False

# --- Player: manually controlled, skipped by step() -----------------------
player = mcrfpy.Entity((13, 5), grid=grid, sprite_index=84, labels=["player"])
player.turn_order = 0  # 0 = the turn manager never processes this entity

# --- Hound: wanders until the player enters its FOV ------------------------
hound = mcrfpy.Entity((2, 2), grid=grid, sprite_index=105)
hound.target_label = "player"  # scan for entities labeled "player"
hound.sight_radius = 6
hound.set_behavior(mcrfpy.Behavior.NOISE4)

state = {"seeking": False}

def on_trigger(trigger, data):
    if trigger == mcrfpy.Trigger.TARGET:
        # data is the spotted Entity. While target_label is set and the
        # target stays visible, TARGET fires INSTEAD of running the
        # behavior -- clear it so SEEK can actually move next round.
        hound.target_label = None
        dm = grid.get_dijkstra_map(data.cell_pos)
        hound.set_behavior(mcrfpy.Behavior.SEEK, pathfinder=dm)
        state["seeking"] = True
        print(f"  spotted {sorted(data.labels)[0]} at {data.cell_pos}")
    elif trigger == mcrfpy.Trigger.BLOCKED:
        # SEEK has no arrival trigger: reaching the Dijkstra root (or
        # having no downhill step) reports BLOCKED.
        print("  hound cannot advance from", hound.cell_pos)

hound.step = on_trigger

# --- Run: player flees left along row 8, hound pursues --------------------
for turn in range(1, 31):
    if player.cell_x > 2:  # scripted player move (a real game reads input)
        target = (player.cell_x - 1, player.cell_y if player.cell_y == 8
                  else player.cell_y + 1)
        if grid.at(target).walkable:
            player.grid_pos = target     # logical cell (collision, FOV)
            player.draw_pos = target     # render position (decoupled!)
    if state["seeking"]:
        # The player moved, so re-root the map and hand it to the hound.
        hound.set_behavior(mcrfpy.Behavior.SEEK,
                           pathfinder=grid.get_dijkstra_map(player.cell_pos))
    grid.step()
    print(f"turn {turn:2d}: hound {hound.cell_pos} player {player.cell_pos}")
    if hound.cell_pos == player.cell_pos:
        print("caught!")
        break

sys.exit(0)
```

Output (abridged):

```
turn  5: hound <Vector (2, 5)> player <Vector (8, 8)>
  spotted player at <Vector (7, 8)>
turn  6: hound <Vector (2, 5)> player <Vector (7, 8)>
turn  7: hound <Vector (3, 6)> player <Vector (6, 8)>
turn  8: hound <Vector (4, 7)> player <Vector (5, 8)>
turn  9: hound <Vector (4, 8)> player <Vector (4, 8)>
caught!
```

The wander phase is random, so the spotting turn varies between runs.

---

## Related Objects

<div class="related-objects">
<div class="object-links">
<a href="../objects/Grid" class="object-link">Grid</a>
<a href="../objects/Entity" class="object-link">Entity</a>
<a href="../objects/DijkstraMap" class="object-link">DijkstraMap</a>
<a href="../objects/AStarPath" class="object-link">AStarPath</a>
</div>
</div>
