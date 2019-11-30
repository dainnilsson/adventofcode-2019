import os
import re
import unittest

from importlib import import_module

RE_DAY = re.compile(r"(\d+)\.txt")


class TestAoc19(unittest.TestCase):

    def test_days(self):
        print()
        print()

        for fname in os.listdir("inputs"):
            m = RE_DAY.match(fname)
            day = int(m.group(1))
            with self.subTest(day=day):
                self._test_day(day)

        print()

    def _test_day(self, day):
        solve = import_module("aoc19.day{:d}".format(day)).solve
        try:
            with open("inputs/{:d}.txt".format(day)) as f:
                a, b = solve([l.rstrip("\r\n") for l in f.readlines()])
        except FileNotFoundError:
            self.skipTest("No input for day {:d}".format(day))

        print("Day {:d}".format(day))
        self._verify_solution(day, "a", a)
        self._verify_solution(day, "b", b)
        print()

    def _verify_solution(self, day, part, answer):
        with self.subTest(part=part):
            try:
                with open("outputs/{:d}{:s}.txt".format(day, part)) as f:
                    output = f.read().rstrip("\r\n")
            except FileNotFoundError:
                self.skipTest("No answer for day {:d} part {:s}".format(day, part))
            self.assertEqual(str(answer), output)
            print("  Part {:s}:".format(part), answer)
