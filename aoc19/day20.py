from .day17 import DIRS, find_state


def read_labels(data):
    labels = {}
    for y in range(len(data) - 1):
        for x in range(len(data[y]) - 1):
            if data[y][x] not in " .#":
                name = data[y][x]
                if data[y][x + 1] not in " .#":
                    name += data[y][x + 1]
                    if x == 0:
                        pos = (x + 2, y)
                    elif data[y][x - 1] == ".":
                        pos = (x - 1, y)
                    else:
                        pos = (x + 2, y)
                elif data[y + 1][x] not in " .#":
                    name += data[y + 1][x]
                    if y == 0:
                        pos = (x, y + 2)
                    elif data[y - 1][x] == ".":
                        pos = (x, y - 1)
                    else:
                        pos = (x, y + 2)
                else:
                    continue
                labels.setdefault(name, []).append(pos)

    aa = labels.pop("AA")[0]
    zz = labels.pop("ZZ")[0]
    doors = {}
    for (a, b) in labels.values():
        doors[a] = b
        doors[b] = a

    return aa, zz, doors


def solve_a(data, aa, zz, doors):
    def paths(state):
        pos, steps = state
        x, y = pos
        tile = data[y][x]
        if tile == ".":
            steps += 1
            for (dx, dy) in DIRS:
                yield (x + dx, y + dy), steps
            if pos in doors:
                yield doors[pos], steps

    return find_state([(aa, 0)], paths, lambda s: s[0] == zz, lambda s: s[0])[1]


def solve_b(data, aa, zz, doors):
    def is_outer(pos):
        x, y = pos
        return (x == 2 or x == len(data[0]) - 3) or (y == 2 or y == len(data) - 3)

    def paths(state):
        pos, level, steps = state
        x, y = pos
        tile = data[y][x]
        if tile == ".":
            steps += 1
            for (dx, dy) in DIRS:
                yield (x + dx, y + dy), level, steps
            if pos in doors:
                level += -1 if is_outer(pos) else 1
                if level >= 0:
                    yield doors[pos], level, steps

    state = find_state([(aa, 0, 0)], paths, lambda s: s[:2] == (zz, 0), lambda s: s[:2])
    return state[2]


def solve(lines):
    data = [list(line) for line in lines]
    aa, zz, doors = read_labels(data)

    return (solve_a(data, aa, zz, doors), solve_b(data, aa, zz, doors))


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
