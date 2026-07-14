---
title: Alignment
layout: default
mcrf:
  objects:
    - Alignment
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: a46667d
---

# Alignment

{% raw %}Alignment enum for positioning UI elements relative to parent bounds.

Values:
    TOP_LEFT, TOP_CENTER, TOP_RIGHT
    CENTER_LEFT, CENTER, CENTER_RIGHT
    BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT

Margin Validation Rules:
    Margins define distance from parent edge when aligned.

    - CENTER: No margins allowed (raises ValueError if margin != 0)
    - TOP_CENTER, BOTTOM_CENTER: Only vert_margin applies (horiz_margin raises ValueError)
    - CENTER_LEFT, CENTER_RIGHT: Only horiz_margin applies (vert_margin raises ValueError)
    - Corner alignments (TOP_LEFT, etc.): All margins valid

Properties:
    align: Alignment value or None to disable
    margin: General margin for all applicable edges
    horiz_margin: Override for horizontal edge (0 = use general margin)
    vert_margin: Override for vertical edge (0 = use general margin)

Example:
    # Center a panel in the scene
    panel = Frame(size=(200, 100), align=Alignment.CENTER)
    scene.children.append(panel)

    # Place button in bottom-right with 10px margin
    button = Frame(size=(80, 30), align=Alignment.BOTTOM_RIGHT, margin=10)
    panel.children.append(button){% endraw %}

## Properties

| Property | Description |
| --- | --- |
| `denominator` | {% raw %}the denominator of a rational number in lowest terms{% endraw %} |
| `imag` | {% raw %}the imaginary part of a complex number{% endraw %} |
| `numerator` | {% raw %}the numerator of a rational number in lowest terms{% endraw %} |
| `real` | {% raw %}the real part of a complex number{% endraw %} |

## Methods

### `as_integer_ratio($self, /)`

{% raw %}Return a pair of integers, whose ratio is equal to the original int.

The ratio is in lowest terms and has a positive denominator.

>>> (10).as_integer_ratio()
(10, 1)
>>> (-10).as_integer_ratio()
(-10, 1)
>>> (0).as_integer_ratio()
(0, 1){% endraw %}

### `bit_count($self, /)`

{% raw %}Number of ones in the binary representation of the absolute value of self.

Also known as the population count.

>>> bin(13)
'0b1101'
>>> (13).bit_count()
3{% endraw %}

### `bit_length($self, /)`

{% raw %}Number of bits necessary to represent self in binary.

>>> bin(37)
'0b100101'
>>> (37).bit_length()
6{% endraw %}

### `conjugate($self, /)`

{% raw %}Returns self, the complex conjugate of any int.{% endraw %}

### `from_bytes($type, /, bytes, byteorder='big', *, signed=False)`

*classmethod*

{% raw %}Return the integer represented by the given array of bytes.

  bytes
    Holds the array of bytes to convert.  The argument must either
    support the buffer protocol or be an iterable object producing bytes.
    Bytes and bytearray are examples of built-in objects that support the
    buffer protocol.
  byteorder
    The byte order used to represent the integer.  If byteorder is 'big',
    the most significant byte is at the beginning of the byte array.  If
    byteorder is 'little', the most significant byte is at the end of the
    byte array.  To request the native byte order of the host system, use
    sys.byteorder as the byte order value.  Default is to use 'big'.
  signed
    Indicates whether two's complement is used to represent the integer.{% endraw %}

### `is_integer($self, /)`

{% raw %}Returns True. Exists for duck type compatibility with float.is_integer.{% endraw %}

### `to_bytes($self, /, length=1, byteorder='big', *, signed=False)`

{% raw %}Return an array of bytes representing an integer.

  length
    Length of bytes object to use.  An OverflowError is raised if the
    integer is not representable with the given number of bytes.  Default
    is length 1.
  byteorder
    The byte order used to represent the integer.  If byteorder is 'big',
    the most significant byte is at the beginning of the byte array.  If
    byteorder is 'little', the most significant byte is at the end of the
    byte array.  To request the native byte order of the host system, use
    sys.byteorder as the byte order value.  Default is to use 'big'.
  signed
    Determines whether two's complement is used to represent the integer.
    If signed is False and a negative integer is given, an OverflowError
    is raised.{% endraw %}
