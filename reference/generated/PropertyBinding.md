---
title: PropertyBinding
layout: default
mcrf:
  objects:
    - PropertyBinding
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# PropertyBinding

{% raw %}PropertyBinding(target: UIDrawable, property: str)

A binding that reads a property value from a UI drawable.

Args:
    target: The drawable to read the property from
    property: Name of the property to read (e.g., 'x', 'opacity')

Use this to create dynamic shader uniforms that follow a drawable's
properties. The binding automatically handles cases where the target
is destroyed.

Example:
    other_frame = mcrfpy.Frame(pos=(100, 100))
    frame.uniforms['offset_x'] = mcrfpy.PropertyBinding(other_frame, 'x')
{% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `is_valid` | {% raw %}True if the binding target still exists and property is valid (bool, read-only).{% endraw %} |
| `property` | {% raw %}The property name being read (str, read-only).{% endraw %} |
| `target` | {% raw %}The drawable this binding reads from (read-only).{% endraw %} |
| `value` | {% raw %}Current value of the binding (float, read-only). Returns None if invalid.{% endraw %} |
