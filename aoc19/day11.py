from .day9 import Program
from .day8 import render


def rotate(x, y, direction):
    if not direction:
        return (-y, x)
    else:
        return (y, -x)


def bounds(hull):
    min_x = max_x = min_y = max_y = float("nan")
    for x, y in hull:
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    return min_x, min_y, max_x, max_y


class Robot:
    def __init__(self, hull):
        self.direction = (0, 1)
        self.state = 1
        self.pos = (0, 0)
        self.hull = hull

    def scan(self):
        return self.pos in self.hull

    def update(self, value):
        if self.state:
            if value:
                self.hull.add(self.pos)
            else:
                self.hull.discard(self.pos)
        else:
            self.direction = rotate(self.direction[0], self.direction[1], value)
            self.pos = (
                self.pos[0] + self.direction[0],
                self.pos[1] + self.direction[1],
            )
        self.state ^= 1


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    r = Robot(set())
    painted = set()

    def counting_update(value):
        if r.state:
            painted.add(r.pos)
        r.update(value)

    p = Program(data, r.scan, counting_update)
    p.run()

    a = len(painted)

    hull = {(0, 0)}
    r = Robot(hull)
    p = Program(data, r.scan, r.update)
    p.run()

    min_x, min_y, max_x, max_y = bounds(hull)

    img = ""
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            img += "1" if (x, y) in hull else "0"
    b = render(img, max_x - min_x + 1, max_y - min_y + 1)

    return a, b


if __name__ == "__main__":
    import fileinput

    a, b = solve([l.rstrip("\r\n") for l in fileinput.input()])
    print(a)
    print(b)
