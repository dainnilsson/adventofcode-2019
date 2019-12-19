import re
import bisect
from collections import defaultdict
from functools import lru_cache


KEY = re.compile(r"[a-z]")


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
                for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    remaining.append(((x + dx, y + dy), m + 1))


def solve_a(data, all_keys, start):
    states = [(0, start, frozenset())]
    explored = defaultdict(lambda: float("inf"))

    @lru_cache(maxsize=None)
    def cands(pos, keys):
        return candidates(data, all_keys, pos, keys)

    while states:
        m, pos, keys = states.pop(0)
        if len(keys) == len(all_keys):
            return m
        for dm, pos, keys in cands(pos, keys):
            nm = m + dm
            if nm < explored[(pos, keys)]:
                bisect.insort(states, (nm, pos, keys))
                explored[(pos, keys)] = nm


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

    n_keys = len(all_keys)
    states = [(0, bots, frozenset())]
    explored = defaultdict(lambda: float("inf"))

    @lru_cache(maxsize=None)
    def cands(pos, keys):
        return candidates(data, all_keys, pos, keys)

    while states:
        m, bots, keys = states.pop(0)
        if len(keys) == n_keys:
            return m
        for i in range(4):
            for dm, pos, keys2 in cands(bots[i], keys):
                m2 = m + dm
                bots2 = bots[:i] + (pos,) + bots[i + 1 :]
                if m2 < explored[(bots2, keys2)]:
                    bisect.insort(states, (m2, bots2, keys2))
                    explored[(bots2, keys2)] = m2


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
