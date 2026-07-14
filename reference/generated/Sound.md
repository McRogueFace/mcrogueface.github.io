---
title: Sound
layout: default
mcrf:
  objects:
    - Sound
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Sound

{% raw %}Sound(source)

Sound effect object for short audio clips.

Args:
    source: Filename string or SoundBuffer object.

Properties:
    volume (float): Volume 0-100.
    loop (bool): Whether to loop.
    playing (bool, read-only): True if playing.
    duration (float, read-only): Duration in seconds.
    source (str, read-only): Source filename.
    pitch (float): Playback pitch (1.0 = normal).
    buffer (SoundBuffer, read-only): The SoundBuffer, if created from one.
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `buffer` | {% raw %}The SoundBuffer if created from one, else None (read-only).{% endraw %} |
| `duration` | {% raw %}Total duration of the sound in seconds (read-only).{% endraw %} |
| `loop` | {% raw %}Whether the sound loops when it reaches the end.{% endraw %} |
| `pitch` | {% raw %}Playback pitch multiplier (1.0 = normal, >1 = higher, <1 = lower).{% endraw %} |
| `playing` | {% raw %}True if the sound is currently playing (read-only).{% endraw %} |
| `source` | {% raw %}Filename path used to load this sound (read-only).{% endraw %} |
| `volume` | {% raw %}Volume level from 0 (silent) to 100 (full volume).{% endraw %} |

## Methods

### `pause() -> None`

{% raw %}pause() -> None

Pause the sound. Use play() to resume from the paused position.

{% endraw %}

### `play() -> None`

{% raw %}play() -> None

Start or resume playing the sound.

{% endraw %}

### `play_varied(pitch_range: float = 0.1, volume_range: float = 3.0) -> None`

{% raw %}play_varied(pitch_range: float = 0.1, volume_range: float = 3.0) -> None

Play with randomized pitch and volume for natural variation.

Args:
    pitch_range: Random pitch offset range (default 0.1)
    volume_range: Random volume offset range (default 3.0)
{% endraw %}

### `stop() -> None`

{% raw %}stop() -> None

Stop playing and reset to the beginning.

{% endraw %}
