"""Minimal pure-stdlib port of LZString.compressToEncodedURIComponent.

The playground (src/shell.html) loads lz-string@1.5.0 and decodes shared code
via `LZString.decompressFromEncodedURIComponent(...)` from a `#src=` URL
fragment. To emit "Open in Playground" links from build_library.py we must
produce byte-identical output to that library's *EncodedURIComponent* variant.

Only the compress side is ported (that is all the site build needs). It is
verified round-trip against the real lz-string npm package in
tools/test_lzstring.js -- if you touch this file, run that test.

Ported from the canonical pieret/lz-string algorithm (MIT). Kept deliberately
close to the reference so it is auditable against the JS source.
"""

_KEY_STR_URI_SAFE = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$"
)


def _compress(uncompressed, bits_per_char, get_char_from_int):
    if uncompressed is None:
        return ""

    context_dictionary = {}
    context_dictionary_to_create = {}
    context_c = ""
    context_wc = ""
    context_w = ""
    context_enlarge_in = 2  # compensate for the first entry which should not count
    context_dict_size = 3
    context_num_bits = 2
    context_data = []
    context_data_val = 0
    context_data_position = 0

    for cc in uncompressed:
        if cc not in context_dictionary:
            context_dictionary[cc] = context_dict_size
            context_dict_size += 1
            context_dictionary_to_create[cc] = True

        context_wc = context_w + cc
        if context_wc in context_dictionary:
            context_w = context_wc
        else:
            if context_w in context_dictionary_to_create:
                if ord(context_w[0]) < 256:
                    for _ in range(context_num_bits):
                        context_data_val = context_data_val << 1
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(get_char_from_int(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                    value = ord(context_w[0])
                    for _ in range(8):
                        context_data_val = (context_data_val << 1) | (value & 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(get_char_from_int(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value = value >> 1
                else:
                    value = 1
                    for _ in range(context_num_bits):
                        context_data_val = (context_data_val << 1) | value
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(get_char_from_int(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value = 0
                    value = ord(context_w[0])
                    for _ in range(16):
                        context_data_val = (context_data_val << 1) | (value & 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(get_char_from_int(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value = value >> 1
                context_enlarge_in -= 1
                if context_enlarge_in == 0:
                    context_enlarge_in = 2 ** context_num_bits
                    context_num_bits += 1
                del context_dictionary_to_create[context_w]
            else:
                value = context_dictionary[context_w]
                for _ in range(context_num_bits):
                    context_data_val = (context_data_val << 1) | (value & 1)
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value = value >> 1
            context_enlarge_in -= 1
            if context_enlarge_in == 0:
                context_enlarge_in = 2 ** context_num_bits
                context_num_bits += 1
            # Add wc to the dictionary.
            context_dictionary[context_wc] = context_dict_size
            context_dict_size += 1
            context_w = str(cc)

    # Output the code for w.
    if context_w != "":
        if context_w in context_dictionary_to_create:
            if ord(context_w[0]) < 256:
                for _ in range(context_num_bits):
                    context_data_val = context_data_val << 1
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                value = ord(context_w[0])
                for _ in range(8):
                    context_data_val = (context_data_val << 1) | (value & 1)
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value = value >> 1
            else:
                value = 1
                for _ in range(context_num_bits):
                    context_data_val = (context_data_val << 1) | value
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value = 0
                value = ord(context_w[0])
                for _ in range(16):
                    context_data_val = (context_data_val << 1) | (value & 1)
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value = value >> 1
            context_enlarge_in -= 1
            if context_enlarge_in == 0:
                context_enlarge_in = 2 ** context_num_bits
                context_num_bits += 1
            del context_dictionary_to_create[context_w]
        else:
            value = context_dictionary[context_w]
            for _ in range(context_num_bits):
                context_data_val = (context_data_val << 1) | (value & 1)
                if context_data_position == bits_per_char - 1:
                    context_data_position = 0
                    context_data.append(get_char_from_int(context_data_val))
                    context_data_val = 0
                else:
                    context_data_position += 1
                value = value >> 1

    context_enlarge_in -= 1
    if context_enlarge_in == 0:
        context_enlarge_in = 2 ** context_num_bits
        context_num_bits += 1

    # Mark the end of the stream.
    value = 2
    for _ in range(context_num_bits):
        context_data_val = (context_data_val << 1) | (value & 1)
        if context_data_position == bits_per_char - 1:
            context_data_position = 0
            context_data.append(get_char_from_int(context_data_val))
            context_data_val = 0
        else:
            context_data_position += 1
        value = value >> 1

    # Flush the last char.
    while True:
        context_data_val = context_data_val << 1
        if context_data_position == bits_per_char - 1:
            context_data.append(get_char_from_int(context_data_val))
            break
        else:
            context_data_position += 1

    return "".join(context_data)


def compress_to_encoded_uri_component(uncompressed: str) -> str:
    """Match lz-string's compressToEncodedURIComponent (URL-safe, 6 bits/char)."""
    if uncompressed is None:
        return ""
    return _compress(uncompressed, 6, lambda a: _KEY_STR_URI_SAFE[a])
