---
title: SoundBuffer
layout: default
mcrf:
  objects:
    - SoundBuffer
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# SoundBuffer

{% raw %}SoundBuffer(filename: str)
SoundBuffer.from_samples(data: bytes, channels: int, sample_rate: int)
SoundBuffer.tone(frequency: float, duration: float, waveform: str = 'sine', ...)
SoundBuffer.sfxr(preset: str, seed: int = None)

Audio sample buffer for procedural audio generation and effects.

Holds PCM sample data that can be created from files, raw samples,
tone synthesis, or sfxr presets. Effect methods return new SoundBuffer
instances (copy-modify pattern).

Properties:
    duration (float, read-only): Duration in seconds.
    sample_count (int, read-only): Total number of samples.
    sample_rate (int, read-only): Samples per second (e.g. 44100).
    channels (int, read-only): Number of audio channels.
    sfxr_params (dict or None, read-only): sfxr parameters if sfxr-generated.
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `channels` | {% raw %}Number of audio channels (read-only).{% endraw %} |
| `duration` | {% raw %}Total duration in seconds (read-only).{% endraw %} |
| `sample_count` | {% raw %}Total number of samples (read-only).{% endraw %} |
| `sample_rate` | {% raw %}Sample rate in Hz (read-only).{% endraw %} |
| `sfxr_params` | {% raw %}Dict of sfxr parameters if sfxr-generated, else None (read-only).{% endraw %} |

## Methods

### `bit_crush(bits: int, rate_divisor: int) -> SoundBuffer`

{% raw %}bit_crush(bits: int, rate_divisor: int) -> SoundBuffer

Reduce bit depth and sample rate for lo-fi effect.

{% endraw %}

### `concat(buffers: list[SoundBuffer], overlap: float = 0.0) -> SoundBuffer`

*classmethod*

{% raw %}concat(buffers: list[SoundBuffer], overlap: float = 0.0) -> SoundBuffer

Concatenate multiple SoundBuffers with optional crossfade overlap.

Args:
    buffers: List of SoundBuffer objects to concatenate
    overlap: Crossfade overlap duration in seconds
{% endraw %}

### `distortion(drive: float) -> SoundBuffer`

{% raw %}distortion(drive: float) -> SoundBuffer

Apply tanh soft clipping distortion.

{% endraw %}

### `echo(delay_ms: float, feedback: float, wet: float) -> SoundBuffer`

{% raw %}echo(delay_ms: float, feedback: float, wet: float) -> SoundBuffer

Apply echo effect with delay, feedback, and wet/dry mix.

{% endraw %}

### `from_samples(data: bytes, channels: int, sample_rate: int) -> SoundBuffer`

*classmethod*

{% raw %}from_samples(data: bytes, channels: int, sample_rate: int) -> SoundBuffer

Create a SoundBuffer from raw int16 PCM sample data.

Args:
    data: Raw PCM data as bytes (int16 little-endian)
    channels: Number of audio channels (1=mono, 2=stereo)
    sample_rate: Sample rate in Hz (e.g. 44100)
{% endraw %}

### `gain(factor: float) -> SoundBuffer`

{% raw %}gain(factor: float) -> SoundBuffer

Multiply all samples by a scalar factor. Use for volume/amplitude control before mixing.

Args:
    factor: Amplitude multiplier (0.5 = half volume, 2.0 = double). Clamps to int16 range.
{% endraw %}

### `high_pass(cutoff_hz: float) -> SoundBuffer`

{% raw %}high_pass(cutoff_hz: float) -> SoundBuffer

Apply single-pole IIR high-pass filter.

{% endraw %}

### `low_pass(cutoff_hz: float) -> SoundBuffer`

{% raw %}low_pass(cutoff_hz: float) -> SoundBuffer

Apply single-pole IIR low-pass filter.

{% endraw %}

### `mix(buffers: list[SoundBuffer]) -> SoundBuffer`

*classmethod*

{% raw %}mix(buffers: list[SoundBuffer]) -> SoundBuffer

Mix multiple SoundBuffers together (additive, clamped).

Args:
    buffers: List of SoundBuffer objects to mix
{% endraw %}

### `normalize() -> SoundBuffer`

{% raw %}normalize() -> SoundBuffer

Scale samples to 95%% of int16 max.

{% endraw %}

### `pitch_shift(factor: float) -> SoundBuffer`

{% raw %}pitch_shift(factor: float) -> SoundBuffer

Resample to shift pitch. factor>1 = higher+shorter.

{% endraw %}

### `reverb(room_size: float, damping: float, wet: float) -> SoundBuffer`

{% raw %}reverb(room_size: float, damping: float, wet: float) -> SoundBuffer

Apply simplified Freeverb-style reverb.

{% endraw %}

### `reverse() -> SoundBuffer`

{% raw %}reverse() -> SoundBuffer

Reverse the sample order.

{% endraw %}

### `sfxr(preset: str = None, seed: int = None, **params) -> SoundBuffer`

*classmethod*

{% raw %}sfxr(preset: str = None, seed: int = None, **params) -> SoundBuffer

Generate retro sound effects using sfxr synthesis.

Args:
    preset: One of: coin, laser, explosion, powerup, hurt, jump, blip
    seed: Random seed for deterministic generation

Returns:
    SoundBuffer with sfxr_params set for later mutation
{% endraw %}

### `sfxr_mutate(amount: float = 0.05, seed: int = None) -> SoundBuffer`

{% raw %}sfxr_mutate(amount: float = 0.05, seed: int = None) -> SoundBuffer

Jitter sfxr params and re-synthesize. Only works on sfxr-generated buffers.

{% endraw %}

### `slice(start: float, end: float) -> SoundBuffer`

{% raw %}slice(start: float, end: float) -> SoundBuffer

Extract a time range in seconds.

{% endraw %}

### `tone(frequency: float, duration: float, waveform: str = 'sine', ...) -> SoundBuffer`

*classmethod*

{% raw %}tone(frequency: float, duration: float, waveform: str = 'sine', ...) -> SoundBuffer

Generate a tone with optional ADSR envelope.

Args:
    frequency: Frequency in Hz
    duration: Duration in seconds
    waveform: One of: sine, square, saw, triangle, noise
    attack: ADSR attack time in seconds (default 0.01)
    decay: ADSR decay time in seconds (default 0.0)
    sustain: ADSR sustain level 0.0-1.0 (default 1.0)
    release: ADSR release time in seconds (default 0.01)
{% endraw %}
