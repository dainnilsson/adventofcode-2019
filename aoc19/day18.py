import re
import bisect
from functools import lru_cache
from .day17 import DIRS, find_state


KEY = re.compile(r"[a-z]")


class SortedList(list):
    def append(self, value):
        bisect.insort(self, value)


def candidates(data, all_keys, pos, keys):
    explored = set()
    remaining = [(pos, 0)]
    while remaining:
        (x, y), m = remaining.pop(0)
        if (x, y) not in explored:
            explored.add((x, y))
            target = data[y][x]
            if target in all_keys and target not in keys:
                yield m, (x, y), keys | {target}
            if target == "." or target.lower() in keys:
                for (dx, dy) in DIRS:
                    remaining.append(((x + dx, y + dy), m + 1))


def solve_a(data, all_keys, start):
    @lru_cache(maxsize=None)
    def cands(pos, keys):
        return candidates(data, all_keys, pos, keys)

    def paths(state):
        steps, keys, pos = state
        for s, p, k in cands(pos, keys):
            yield (steps + s, k, p)

    return find_state(
        SortedList([(0, frozenset(), start)]),
        paths,
        lambda s: len(s[1]) == len(all_keys),
        lambda s: s[1:],
    )[0]


def solve_b(data, all_keys, start):
    x, y = start
    data[y - 1][x] = "#"
    data[y + 1][x] = "#"
    data[y][x - 1] = "#"
    data[y][x + 1] = "#"

    bots = (
        (start[0] - 1, start[1] - 1),
        (start[0] + 1, start[1] - 1),
        (start[0] - 1, start[1] + 1),
        (start[0] + 1, start[1] + 1),
    )

    @lru_cache(maxsize=None)
    def cands(pos, keys):
        return candidates(data, all_keys, pos, keys)

    def paths(state):
        steps, keys, bots = state
        for i in range(4):
            for s, p, k in cands(bots[i], keys):
                bots2 = bots[:i] + (p,) + bots[i + 1 :]
                yield (steps + s, k, bots2)

    return find_state(
        SortedList([(0, frozenset(), bots)]),
        paths,
        lambda s: len(s[1]) == len(all_keys),
        lambda s: s[1:],
    )[0]


def solve(lines):
    data = [list(line) for line in lines]

    keys = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            c = data[y][x]
            if c == "@":
                data[y][x] = "."
                start = (x, y)
            elif KEY.match(c):
                keys[c] = (x, y)

    return (solve_a(data, keys, start), solve_b(data, keys, start))


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
