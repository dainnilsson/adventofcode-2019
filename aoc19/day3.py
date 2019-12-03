DIRS = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}


def travel(steps):
    x, y = 0, 0
    visited = [(x, y)]
    for s in steps:
        direction, distance = s[0], int(s[1:])
        dx, dy = DIRS[direction]
        for _ in range(distance):
            x += dx
            y += dy
            p = (x, y)
            visited.append(p)

    return visited


def solve(lines):
    path_a = travel(lines[0].split(","))
    path_b = travel(lines[1].split(","))

    collisions = set(path_a).intersection(set(path_b))
    collisions.remove((0, 0))

    return (
        min(abs(p[0]) + abs(p[1]) for p in collisions),
        min(path_a.index(p) + path_b.index(p) for p in collisions),
    )


def optimized(lines):
    visited = {}
    x, y, c = 0, 0, 0
    for step in reversed(lines[0].split(",")):
        (dx, dy), distance = DIRS[step[0]], int(step[1:])
        for _ in range(distance):
            x -= dx
            y -= dy
            c += 1
            visited[(x, y)] = c
    ex, ey, = x, y

    a, b = float("NaN"), float("NaN")
    for step in lines[1].split(","):
        (dx, dy), distance = DIRS[step[0]], int(step[1:])
        for _ in range(distance):
            x += dx
            y += dy
            c += 1
            p = (x, y)
            if p in visited:
                a = min(abs(ex - x) + abs(ey - y), a)
                b = min(c - visited[p], b)

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
