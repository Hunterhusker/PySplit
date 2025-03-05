def format_wall_clock_from_ms(millis: int, full_length: bool = False):
    """
    Takes in a number of elapsed milliseconds and outputs the wallclock time as a string

    Args:
        millis: (int) the current elapsed milliseconds
        full_length: (bool) Whether the string should contain 00s or not (other than the base 00.000)

    Returns:
        (str) The wallclock time from the elapsed milliseconds as a string
    """
    s, ms = divmod(millis, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)

    if full_length:  # if we want the fully expressed time as a string then return it
        return f'{h:02}:{m:02}:{s:02}.{ms:03}'

    # else we should add 
