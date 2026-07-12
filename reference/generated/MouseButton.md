---
title: MouseButton
layout: default
mcrf:
  objects:
    - MouseButton
  diataxis: reference
  source: generated
  verified: 0.2.8-dev
  verified_commit: b6720f6
---

# MouseButton

{% raw %}Enum representing mouse buttons and scroll wheel.

Values:
    LEFT: Left mouse button
    RIGHT: Right mouse button
    MIDDLE: Middle mouse button / scroll wheel click
    X1: Extra mouse button 1
    X2: Extra mouse button 2
    SCROLL_UP: Scroll wheel up
    SCROLL_DOWN: Scroll wheel down
{% endraw %}

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
