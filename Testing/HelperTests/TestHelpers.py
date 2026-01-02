import unittest
from sys import intern

from helpers.TimerFormat import *


class TestHelpers(unittest.TestCase):
    def test_format_wall_clock_from_ms(self):
        # < 1 second
        self.assertEqual(format_wall_clock_from_ms(0), "00.000")
        self.assertEqual(format_wall_clock_from_ms(5), "00.005")
        self.assertEqual(format_wall_clock_from_ms(15), "00.015")
        self.assertEqual(format_wall_clock_from_ms(250), "00.250")
        self.assertEqual(format_wall_clock_from_ms(999), "00.999")

        # >= 1 second
        self.assertEqual(format_wall_clock_from_ms(1000), "01.000")
        self.assertEqual(format_wall_clock_from_ms(10000), "10.000")
        self.assertEqual(format_wall_clock_from_ms(59999), "59.999")

        # >= 1 minute
        self.assertEqual(format_wall_clock_from_ms(60000), "01:00.000")
        self.assertEqual(format_wall_clock_from_ms(600000), "10:00.000")
        self.assertEqual(format_wall_clock_from_ms(3599999), "59:59.999")

        # >= 1 hour
        self.assertEqual(format_wall_clock_from_ms(3600000), "01:00:00.000")
        self.assertEqual(format_wall_clock_from_ms(36000000), "10:00:00.000")
        self.assertEqual(format_wall_clock_from_ms(360000000), "100:00:00.000")
        self.assertEqual(format_wall_clock_from_ms(3600000000), "1000:00:00.000")

    def test_format_wall_clock_from_ms_negative(self):
        # < 1 second
        self.assertEqual(format_wall_clock_from_ms(-5), "-00.005")
        self.assertEqual(format_wall_clock_from_ms(-15), "-00.015")
        self.assertEqual(format_wall_clock_from_ms(-250), "-00.250")
        self.assertEqual(format_wall_clock_from_ms(-999), "-00.999")

        # >= 1 second
        self.assertEqual(format_wall_clock_from_ms(-1000), "-01.000")
        self.assertEqual(format_wall_clock_from_ms(-10000), "-10.000")
        self.assertEqual(format_wall_clock_from_ms(-59999), "-59.999")

        # >= 1 minute
        self.assertEqual(format_wall_clock_from_ms(-60000), "-01:00.000")
        self.assertEqual(format_wall_clock_from_ms(-600000), "-10:00.000")
        self.assertEqual(format_wall_clock_from_ms(-3599999), "-59:59.999")

        # >= 1 hour
        self.assertEqual(format_wall_clock_from_ms(-3600000), "-01:00:00.000")
        self.assertEqual(format_wall_clock_from_ms(-36000000), "-10:00:00.000")
        self.assertEqual(format_wall_clock_from_ms(-360000000), "-100:00:00.000")
        self.assertEqual(format_wall_clock_from_ms(-3600000000), "-1000:00:00.000")

    def test_millis_to_wallclock_components(self):
        self.assertEqual(millis_to_wallclock_components(0), (0, 0, 0, 0))
        self.assertEqual(millis_to_wallclock_components(5), (0, 0, 0, 5))
        self.assertEqual(millis_to_wallclock_components(15), (0, 0, 0, 15))
        self.assertEqual(millis_to_wallclock_components(250), (0, 0, 0, 250))
        self.assertEqual(millis_to_wallclock_components(999), (0, 0, 0, 999))

        # >= 1 second
        self.assertEqual(millis_to_wallclock_components(1000), (0, 0, 1, 0))
        self.assertEqual(millis_to_wallclock_components(10000), (0, 0, 10, 0))
        self.assertEqual(millis_to_wallclock_components(59999), (0, 0, 59, 999))

        # >= 1 minute
        self.assertEqual(millis_to_wallclock_components(60000), (0, 1, 0, 0))
        self.assertEqual(millis_to_wallclock_components(600000), (0, 10, 0, 0))
        self.assertEqual(millis_to_wallclock_components(3599999), (0, 59, 59, 999))

        # >= 1 hour
        self.assertEqual(millis_to_wallclock_components(3600000), (1, 0, 0, 0))
        self.assertEqual(millis_to_wallclock_components(36000000), (10, 0, 0, 0))
        self.assertEqual(millis_to_wallclock_components(360000000), (100, 0, 0, 0))
        self.assertEqual(millis_to_wallclock_components(3600000000), (1000, 0, 0, 0))

    def test_ms_to_qtime(self):
        for i in range(0, 35999999, 250):
            interesting_time = ms_to_qtime(i)
            h, m, s, ms = millis_to_wallclock_components(i)

            self.assertEqual(interesting_time.msec(), ms)
            self.assertEqual(interesting_time.second(), s)
            self.assertEqual(interesting_time.minute(), m)
            self.assertEqual(interesting_time.hour(), h)

    def test_ms_to_qtime_to_ms(self):
        # increment through a wide range of possible milliseconds that could be used as times and check they go in and out of QTime safely
        for i in range(0, 35999999, 250):
            interesting_time = ms_to_qtime(i)
            interesting_ms = qtime_to_ms(interesting_time)

            self.assertEqual(interesting_ms, i)
