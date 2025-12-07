"""
A simple set of helper scripts to deal with the fact that I like RBGA format and for some reason the QColor only does ARGB??
"""


def hex_rgba_to_argb(rgba_string: str):
    """
    Converts hex in rgba to argb

    Args:
        rgba_string: (str) The hex code in rgba format

    Returns:
        (str) The hex color as an argb string, eg "#AARRGGBB" or "#ARGB"
    """
    tagged = False

    if '#' in rgba_string:
        rgba_string = rgba_string.strip('#')
        tagged = True

    hex_code = '00000000'

    code_len = len(rgba_string)
    if code_len > 6:
        hex_code = rgba_string[6:9] + rgba_string[:6]

    elif code_len == 6:
        hex_code = f'ff{rgba_string}'

    elif code_len == 4:
        hex_code = rgba_string[3] + rgba_string[:3]

    elif code_len == 3:
        hex_code = f'f{rgba_string}'

    if tagged:
        return f'#{hex_code}'

    return hex_code


def hex_argb_to_rgba(argb_string: str):
    """
    Converts hex in argb to rgba

    Args:
        argb_string: (str) The hex code in argb format

    Returns:
        (str) The hex color as an argb string, aka "#RRGGBBAA" or "#RGBA"
    """
    tagged = False

    if '#' in argb_string:
        argb_string = argb_string.strip('#')
        tagged = True

    hex_code = '00000000'

    code_len = len(argb_string)
    if code_len > 6:
        hex_code = argb_string[2:9] + argb_string[:2]

    elif code_len == 6:
        hex_code = f'{argb_string}ff'

    elif code_len == 4:
        hex_code = argb_string[1:4] + argb_string[0]

    elif code_len == 3:
        hex_code = f'{argb_string}f'

    if tagged:
        return f'#{hex_code}'

    return hex_code


def to_full_rgba(hex_code: str, argb: bool = False):
    """
    Converts from any hex to a full 8 character rgba hex code

    Args:
        hex_code: (str) the starting hex code
        argb: (bool) whether this string is actually argb and needs converted

    Returns:
        (str) The desired fully qualified hex code as a string, w/ the leading # iff it was given with one
    """
    tagged = False

    if '#' in hex_code:
        hex_code = hex_code.strip('#')
        tagged = True

    if argb:
        hex_code = hex_argb_to_rgba(hex_code)

    code_len = len(hex_code)

    if code_len == 6:
        hex_code += 'ff'

    elif code_len == 4:
        new_code = ''

        new_code += hex_code[0] * 2
        new_code += hex_code[1] * 2
        new_code += hex_code[2] * 2
        new_code += hex_code[3] * 2

        hex_code = new_code

    elif code_len == 3:
        new_code = ''

        new_code += hex_code[0] * 2
        new_code += hex_code[1] * 2
        new_code += hex_code[2] * 2
        new_code += 'ff'

        hex_code = new_code

    elif code_len != 8:
        hex_code = '00000000'

    if tagged:
        return f'#{hex_code}'

    return hex_code


def to_full_argb(hex_code: str, rgba: bool = False):
    """
    Converts from any hex to a full 8 character argb hex code

    Args:
        hex_code: (str) the starting hex code
        rgba: (bool) whether this string is actually rgba and needs converted

    Returns:
        (str) The desired fully qualified hex code as a string, w/ the leading # iff it was given with one
    """
    tagged = False

    if '#' in hex_code:
        hex_code = hex_code.strip('#')
        tagged = True

    if rgba:
        hex_code = hex_rgba_to_argb(hex_code)

    code_len = len(hex_code)

    if code_len == 6:
        hex_code = f'ff{hex_code}'

    elif code_len == 4:
        new_code = ''

        new_code += hex_code[0] * 2
        new_code += hex_code[1] * 2
        new_code += hex_code[2] * 2
        new_code += hex_code[3] * 2

        hex_code = new_code

    elif code_len == 3:
        new_code = ''

        new_code += 'ff'
        new_code += hex_code[0] * 2
        new_code += hex_code[1] * 2
        new_code += hex_code[2] * 2

        hex_code = new_code

    elif code_len != 8:
        hex_code = '00000000'

    if tagged:
        return f'#{hex_code}'

    return hex_code

