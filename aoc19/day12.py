from itertools import combinations
from math import gcd
import re

MOON = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")


class Moon:
    def __init__(self, pos):
        self.pos = pos
        self.vel = [0, 0, 0]

    def gravitate(self, other, i):
        if self.pos[i] < other.pos[i]:
            self.vel[i] += 1
            other.vel[i] -= 1
        elif other.pos[i] < self.pos[i]:
            self.vel[i] -= 1
            other.vel[i] += 1

    def move(self, i):
        self.pos[i] += self.vel[i]

    @property
    def energy(self):
        return sum(abs(c) for c in self.pos) * sum(abs(c) for c in self.vel)


def solve_a(moons):
    for t in range(1000):
        for a, b in combinations(moons, 2):
            for i in range(3):
                a.gravitate(b, i)
        for m in moons:
            for i in range(3):
                m.move(i)

    return sum(m.energy for m in moons)


def get_cycle(moons, i):
    t = 0
    seen = set()
    state = tuple((m.pos[i], m.vel[i]) for m in moons)
    while state not in seen:
        seen.add(state)
        for a, b in combinations(moons, 2):
            a.gravitate(b, i)
        for m in moons:
            m.move(i)
        state = tuple((m.pos[i], m.vel[i]) for m in moons)
        t += 1
    return t


def solve_b(moons):
    x = get_cycle(moons, 0)
    y = get_cycle(moons, 1)
    z = get_cycle(moons, 2)

    xy = x * y // gcd(x, y)
    return xy * z // gcd(xy, z)


def solve(lines):
    data = []
    for line in lines:
        match = MOON.match(line)
        data.append([int(match.group(i)) for i in range(1, 4)])

    moons = [Moon(d.copy()) for d in data]
    a = solve_a(moons)

    moons = [Moon(d.copy()) for d in data]
    b = solve_b(moons)

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
