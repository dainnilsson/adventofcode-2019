import os
import re
import time
import unittest

from importlib import import_module

RE_DAY = re.compile(r"(\d+)\.txt")


class TestAoc19(unittest.TestCase):
    def test_days(self):
        print()
        print()

        for fname in sorted(os.listdir("inputs")):
            m = RE_DAY.match(fname)
            day = int(m.group(1))
            with self.subTest(day=day):
                self._test_day(day)

        print()

    def _test_day(self, day):
        mod = import_module("aoc19.day{:d}".format(day))
        try:
            with open("inputs/{:d}.txt".format(day)) as f:
                lines = [l.rstrip("\r\n") for l in f.readlines()]
        except FileNotFoundError:
            self.skipTest("No input for day {:d}".format(day))

        a, b, s = self._run_test(day, mod.solve, lines)
        print("Day {:d} (completed in {:f} ms)".format(day, s * 1000))
        self._verify_solution(day, "a", a)
        self._verify_solution(day, "b", b)

        if hasattr(mod, "optimized"):
            opt_a, opt_b, opt_s = self._run_test(day, mod.optimized, lines)
            with self.subTest(part="optimized"):
                self.assertEqual(a, opt_a, "Optimized answer A doesn't match!")
                self.assertEqual(b, opt_b, "Optimized answer B doesn't match!")
            print(
                "  Optimized: {:f} ms ({:.2%} of non-optimized version)".format(
                    opt_s * 1000, opt_s / s
                )
            )

        print()

    def _run_test(self, day, solve, lines):
        start_time = time.time()
        a, b = solve(lines)
        end_time = time.time()
        return a, b, end_time - start_time

    def _verify_solution(self, day, part, answer):
        with self.subTest(part=part):
            try:
                with open("outputs/{:d}{:s}.txt".format(day, part)) as f:
                    output = f.read().rstrip("\r\n")
            except FileNotFoundError:
                self.skipTest("No answer for day {:d} part {:s}".format(day, part))
            self.assertEqual(str(answer), output)

            if "\n" in output:
                print("  Part {:s}:".format(part))
                print(answer)
            else:
                print("  Part {:s}:".format(part), answer)
