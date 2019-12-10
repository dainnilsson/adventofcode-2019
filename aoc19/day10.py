from math import gcd, atan2, pi
import bisect


def angle(x, y):
    return (atan2(y, x) + pi / 2) % (2 * pi)


def solve(lines):
    asteroids = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                asteroids.add((x, y))

    best = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            los = {}
            for x2, y2 in asteroids:
                dx = x2 - x
                dy = y2 - y
                k = gcd(dx, dy)
                if k != 0:
                    bisect.insort(
                        los.setdefault((dx // k, dy // k), []),
                        (abs(dx) + abs(dy), (x2, y2)),
                    )
            if len(los) > len(best):
                best = los

    a = len(best)

    hits = 0
    while True:
        for coord in sorted(best, key=lambda p: angle(p[0], p[1])):
            cs = best[coord]
            target = cs.pop(0)[1]
            hits += 1
            if hits == 200:
                b = target[0] * 100 + target[1]
                return a, b
            if not cs:
                del best[coord]


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
