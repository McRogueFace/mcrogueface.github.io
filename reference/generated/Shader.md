---
title: Shader
layout: default
mcrf:
  objects:
    - Shader
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Shader

{% raw %}Shader(fragment_source: str, dynamic: bool = False)

A GPU shader program for visual effects.

Args:
    fragment_source: GLSL fragment shader source code
    dynamic: If True, shader uses time-varying effects and will
             invalidate parent caches each frame

Shaders enable GPU-accelerated visual effects like glow, distortion,
color manipulation, and more. Assign to drawable.shader to apply.

Engine-provided uniforms (automatically available):
    - float time: Seconds since engine start
    - float delta_time: Seconds since last frame
    - vec2 resolution: Texture size in pixels
    - vec2 mouse: Mouse position in window coordinates

Example:
    shader = mcrfpy.Shader('''
        uniform sampler2D texture;
        uniform float time;
        void main() {
            vec2 uv = gl_TexCoord[0].xy;
            vec4 color = texture2D(texture, uv);
            color.rgb *= 0.5 + 0.5 * sin(time);
            gl_FragColor = color;
        }
    ''', dynamic=True)
    frame.shader = shader
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `dynamic` | {% raw %}Whether this shader uses time-varying effects (bool). Dynamic shaders invalidate parent caches each frame.{% endraw %} |
| `is_valid` | {% raw %}True if the shader compiled successfully (bool, read-only).{% endraw %} |
| `source` | {% raw %}The GLSL fragment shader source code (str, read-only).{% endraw %} |

## Methods

### `set_uniform(name: str, value: float|tuple) -> None`

{% raw %}set_uniform(name: str, value: float|tuple) -> None

Set a custom uniform value on this shader.

Args:
    name: Uniform variable name in the shader
    value: Float, vec2 (2-tuple), vec3 (3-tuple), or vec4 (4-tuple)

Raises:
    ValueError: If uniform type cannot be determined

Note:
    Engine uniforms (time, resolution, etc.) are set automatically
{% endraw %}
