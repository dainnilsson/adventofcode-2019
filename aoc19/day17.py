from .day9 import Program

DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))


def solve_a(m):
    a = 0
    for (x, y), v in m.items():
        if v == "#" and all(m.get((x + dx, y + dy)) == "#" for (dx, dy) in DIRS):
            a += x * y
    return a


def format_func(value):
    steps = []
    s = 0
    for c in value:
        if c in "LR":
            if s:
                steps.append(str(s))
                s = 0
            steps.append(c)
        else:
            s += 1
    if s:
        steps.append(str(s))
    return ",".join(steps)


def trace_path(data, pos, facing):
    path = []
    while True:
        x, y = pos
        dx, dy = facing
        if data.get((x + dx, y + dy)) == "#":
            path.append("S")
            pos = (x + dx, y + dy)
        else:
            rx = dy
            ry = -dx
            if data.get((x + rx, y + ry)) == "#":
                path.append("L")
                facing = (rx, ry)
            elif data.get((x - rx, y - ry)) == "#":
                path.append("R")
                facing = (-rx, -ry)
            else:
                return path


def find_state(states, paths, goal, explored):
    seen = set()
    while states:
        state = states.pop(0)
        if goal(state):
            return state
        e_state = explored(state)
        if e_state not in seen:
            seen.add(e_state)
            for next_state in paths(state):
                states.append(next_state)


def find_parts(path):
    def paths(state):
        subpaths, n, rem = state
        for i in range(len(rem) - 1, 0, -1):
            subpath = rem[:i]
            if len(format_func(subpath)) <= 20:
                parts = rem.split(subpath)
                n2 = n + len(parts) - 1
                if n2 <= 10:
                    yield subpaths + (subpath,), n2, "".join(parts)

    return find_state(
        [(tuple(), 0, path)], paths, lambda s: len(s[0]) == 3 and not s[2], lambda s: s
    )[0]


def get_instructions(data, pos, facing):
    p = "".join(trace_path(data, pos, facing))
    subpaths = find_parts(p)
    program = (
        p.replace(subpaths[0], "A,")
        .replace(subpaths[1], "B,")
        .replace(subpaths[2], "C,")
    )[:-1]
    functions = [format_func(fn) for fn in find_parts(p)]

    return bytearray("\n".join([program] + functions + ["n", ""]).encode())


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    buf = bytearray()
    Program(data).run(None, buf.append)

    lines = buf.decode().split()

    m = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            m[(x, y)] = c
            i = "v^><".find(c)
            if i >= 0:
                facing = DIRS[i]
                pos = (x, y)

    a = solve_a(m)

    instructions = get_instructions(m, pos, facing)
    buf = []
    data[0] = 2
    Program(data).run(lambda: instructions.pop(0), buf.append)

    return a, buf.pop()


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
