---
title: CallableBinding
layout: default
mcrf:
  objects:
    - CallableBinding
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# CallableBinding

{% raw %}CallableBinding(callable: Callable[[], float])

A binding that calls a Python function to get its value.

Args:
    callable: A function that takes no arguments and returns a float

The callable is invoked every frame when the shader is rendered.
Keep the callable lightweight to avoid performance issues.

Example:
    player_health = 100
    frame.uniforms['health_pct'] = mcrfpy.CallableBinding(
        lambda: player_health / 100.0
    )
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `callable` | {% raw %}The Python callable (read-only).{% endraw %} |
| `is_valid` | {% raw %}True if the callable is still valid (bool, read-only).{% endraw %} |
| `value` | {% raw %}Current value from calling the callable (float, read-only). Returns None on error.{% endraw %} |
