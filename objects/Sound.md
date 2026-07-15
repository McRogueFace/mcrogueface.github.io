---
layout: default
title: Sound
mcrf:
  objects: [Sound]
  diataxis: reference
  disposition: current
  verified: "0.2.8-dev"
  verified_commit: 3a85dd8
---

# Sound

Sound effect object for short audio clips.

## Overview

The `Sound` class handles short audio effects that load entirely into memory. Sounds can be played multiple times simultaneously and have low latency, making them ideal for game effects like footsteps, UI clicks, and combat sounds.

## Quick Reference

```python
# Load and play a sound effect
hit_sound = mcrfpy.Sound("assets/audio/hit.wav")
hit_sound.volume = 75
hit_sound.play()

# Looping ambient sound
ambient = mcrfpy.Sound("assets/audio/wind.ogg")
ambient.loop = True
ambient.play()

# Check status
print(f"Duration: {hit_sound.duration}s")
```

## Constructor

```python
mcrfpy.Sound(filename: str)
```

| Argument | Type | Description |
|----------|------|-------------|
| `filename` | str | Filename string or SoundBuffer object |

Supported formats: OGG, WAV, FLAC

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `duration` | float | Total duration in seconds (read-only) |
| `loop` | bool | Whether to loop when reaching the end |
| `pitch` | float | Playback pitch multiplier (1.0 = normal) |
| `playing` | bool | Whether sound is currently playing (read-only) |
| `source` | str | Path to the source file (read-only) |
| `buffer` | SoundBuffer or None | Underlying sound buffer (read-only) |
| `volume` | float | Volume level (0-100) |

## Methods

| Method | Description |
|--------|-------------|
| `play()` | Start or resume playback |
| `pause()` | Pause playback (keeps position) |
| `stop()` | Stop playback (resets position) |
| `play_varied(pitch_range=0.1, volume_range=3.0)` | Play with randomized pitch/volume |

## Usage Notes

- Sounds load entirely into memory - use for short clips (under 10 seconds)
- Multiple Sound instances can play simultaneously
- Use `Music` for longer background tracks
- Low latency makes sounds ideal for responsive game feedback

## Related

<div class="related-objects">
<div class="object-links">
<a href="Music" class="object-link">Music</a>
</div>
</div>
