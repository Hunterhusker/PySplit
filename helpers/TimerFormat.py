from PySide6.QtCore import QTime


def format_wall_clock_from_ms(millis: int, full_length: bool = False):
    """
    Takes in a number of elapsed milliseconds and outputs the wallclock time as a string

    Args:
        millis: (int) the current elapsed milliseconds
        full_length: (bool) Whether the string should contain 00s or not (other than the base 00.000)

    Returns:
        (str) The wallclock time from the elapsed milliseconds as a string
    """
    result = ''

    h, m, s, ms = millis_to_wallclock_components(millis)

    if full_length:  # if we want the fully expressed time as a string then return it
        return f'{h:02}:{m:02}:{s:02}.{ms:03}'

    # else we should add only what we need
    base = f'{s:02}.{ms:03}'

    m = f'{m:02}:' if m != 0 else ''
    h = f'{h:02}:' if h != 0 else ''

    return result + "".join([h, m, base])


def millis_to_wallclock_components(millis: int):
    """
    Turns the milliseconds to wallclock time ie hours, minutes, seconds, and remaining milliseconds
    Args:
        millis: (int) the milliseconds to convert

    Returns:
        tuple[int, int, int, int]: a tuple ints in order hours, minutes, seconds, and milliseconds
    """
    if millis < 0:
        millis = millis * -1

    s, ms = divmod(millis, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)

    return h, m, s, ms


def ms_to_qtime(millis: int) -> QTime:
    """
    Turns a number of milliseconds to a QTime object

    Args:
        millis: (int) the number of milliseconds in this period

    Returns:
        (QTime) The QTime object that represents the MS duration
    """
    h, m, s, ms = millis_to_wallclock_components(millis)

    tmp = QTime()
    tmp.setHMS(h, m, s, ms)

    return tmp


def qtime_to_ms(time: QTime) -> int:
    """
    Calculates and returns the number of total milliseconds from 0 to the time defined by the QTime

    Args:
        time: (QTime) The QTime object

    Returns:
        (int) The number of milliseconds
    """
    total_time = 0

    total_time += time.msec()
    total_time += time.second() * 1000
    total_time += time.minute() * 60000
    total_time += time.hour() * 1440000

    return total_time
