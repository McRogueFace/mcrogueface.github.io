---
layout: default
title: Music
---

# Music

Streaming music object for longer audio tracks.

## Overview

The `Music` class handles streaming audio playback for longer audio files like background music. Unlike `Sound` which loads entirely into memory, Music streams from disk making it ideal for longer tracks.

## Quick Reference

```python
# Load and play background music
music = mcrfpy.Music("assets/audio/theme.ogg")
music.volume = 50  # 50% volume
music.loop = True
music.play()

# Control playback
music.pause()
music.position = 30.0  # Jump to 30 seconds
music.play()

# Check status
print(f"Duration: {music.duration}s")
print(f"Playing: {music.playing}")
```

## Constructor

```python
mcrfpy.Music(filename: str)
```

| Argument | Type | Description |
|----------|------|-------------|
| `filename` | str | Path to the audio file |

Supported formats: OGG, WAV, FLAC

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `duration` | float | Total duration in seconds (read-only) |
| `loop` | bool | Whether to loop when reaching the end |
| `playing` | bool | Whether music is currently playing (read-only) |
| `position` | float | Current playback position in seconds |
| `source` | str | Path to the source file (read-only) |
| `volume` | float | Volume level (0-100) |

## Methods

| Method | Description |
|--------|-------------|
| `play()` | Start or resume playback |
| `pause()` | Pause playback (keeps position) |
| `stop()` | Stop playback (resets position) |

## Usage Notes

- Only one Music instance should play at a time for best performance
- Use `Sound` for short effects that may overlap
- Streaming means lower memory usage but slight CPU overhead
- Set `loop = True` before calling `play()` for seamless looping

## Related

<div class="related-objects">
<div class="object-links">
<a href="Sound" class="object-link">Sound</a>
</div>
</div>
