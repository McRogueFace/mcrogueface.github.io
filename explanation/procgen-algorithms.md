# Procedural Generation: Choosing the Right Algorithm

*When to use BSP, WFC, Cellular Automata, or Noise—and why.*

## The Four Approaches

McRogueFace supports four procedural generation algorithms, each suited to different content types:

| Algorithm | Best For | Structure | Feel |
|-----------|----------|-----------|------|
| **BSP** | Room-based dungeons | Highly structured | Architectural |
| **WFC** | Pattern-respecting tiles | Rule-constrained | Coherent |
| **Cellular Automata** | Organic caves | Emergent | Natural |
| **Noise** | Large terrain | Smooth gradients | Landscape |

## Binary Space Partitioning (BSP)

**Use when:** You want interconnected rooms with corridors.

BSP recursively divides space into smaller regions, then places rooms within each region. The result is structured, architectural dungeons with clear room boundaries.

**How it works:**
1. Start with the full map area
2. Split at 30-70% ratios based on aspect ratio
3. Recursively split until regions are room-sized
4. Place rooms in leaf nodes
5. Connect sibling rooms with corridors

**Example use case:** Traditional roguelike dungeons (Crypt of Sokoban uses this).

**Trade-off:** Predictable structure. Rooms will feel "designed" rather than discovered.

## Wave Function Collapse (WFC)

**Use when:** You need tiles that respect adjacency rules.

WFC generates content by collapsing possibilities based on constraints. Each cell starts with all possible tiles, then collapses to specific tiles based on what neighbors allow.

**How it works:**
1. Define which tiles can be adjacent to which
2. Find the cell with minimum entropy (fewest possibilities)
3. Collapse it to one tile randomly (weighted)
4. Propagate constraints to neighbors
5. Repeat until all cells are collapsed

**Example use case:** Coherent tile patterns, puzzle rooms, structured environments.

**Trade-off:** Requires upfront rule definition. Can fail to generate if rules are too restrictive.

## Cellular Automata

**Use when:** You want organic, cave-like spaces.

Cellular automata evolve terrain through neighborhood rules. Start with random noise, then iteratively apply rules like "become wall if 5+ neighbors are walls."

**How it works:**
1. Initialize with random wall/floor distribution
2. For each cell, count wall neighbors
3. Apply rule (e.g., wall if neighbors >= 5)
4. Repeat for several generations
5. Flood-fill to remove isolated regions

**Example use case:** Natural caves, organic caverns, eroded structures.

**Trade-off:** Less controllable. May produce disconnected regions requiring post-processing.

## Noise-Based Terrain

**Use when:** You need smooth, large-scale variation.

Perlin or Simplex noise generates continuous gradients that can be mapped to terrain types. Values smoothly transition across space.

**How it works:**
1. Generate noise values for each cell (0.0 to 1.0)
2. Map ranges to terrain: water < 0.3, grass < 0.5, forest < 0.7, mountain >= 0.7
3. Optionally layer multiple noise octaves for detail

**Example use case:** Overworld maps, height-based terrain, biome distribution.

**Trade-off:** No guarantee of playability. May need post-processing for paths/connectivity.

## Hybrid Approaches

The most interesting results often combine algorithms:

- **BSP + Cellular Automata**: BSP for room layout, then CA to erode walls for organic feel
- **BSP + WFC**: BSP for structure, WFC for tile detail within rooms
- **Noise + Thresholds**: Noise for base terrain, thresholds for biome boundaries

## Performance Considerations

- **Batch cell updates** to minimize Python/C++ boundary crossings
- **Generate during scene transitions**, not real-time
- **Use deterministic seeding** for reproducible results and chunk-based streaming
