---
title: Music
layout: default
mcrf:
  objects:
    - Music
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Music

{% raw %}Streaming music object for longer audio tracks{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `duration` | {% raw %}Total duration of the music in seconds (read-only).{% endraw %} |
| `loop` | {% raw %}Whether the music loops when it reaches the end.{% endraw %} |
| `playing` | {% raw %}True if the music is currently playing (read-only).{% endraw %} |
| `position` | {% raw %}Current playback position in seconds. Can be set to seek.{% endraw %} |
| `source` | {% raw %}Filename path used to load this music (read-only).{% endraw %} |
| `volume` | {% raw %}Volume level from 0 (silent) to 100 (full volume).{% endraw %} |

## Methods

### `pause() -> None`

{% raw %}pause() -> None

Pause the music. Use play() to resume from the paused position.

{% endraw %}

### `play() -> None`

{% raw %}play() -> None

Start or resume playing the music.

{% endraw %}

### `stop() -> None`

{% raw %}stop() -> None

Stop playing and reset to the beginning.

{% endraw %}
