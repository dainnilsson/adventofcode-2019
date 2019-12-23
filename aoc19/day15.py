from . import day9


class Program(day9.Program):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.start()
        self.value = None

    def run(self, input_fn, output_fn):
        self.start = lambda: None
        try:
            super().run(input_fn, output_fn)
        except ValueError:
            return self.value

    def fork(self):
        prog = Program(self.data)
        prog.state = self.state.copy()
        prog.pc = self.pc
        return prog


class Explorer:
    def __init__(self, m, others, moved=0, pos=(0, 0), d=1):
        self.others = others
        self.moved = moved
        self.map = m
        self.pos = pos
        self.d = d
        self.target = None

    def output(self, value):
        self.pos = self.target
        self.moved += 1
        if value == 0:
            self.map[self.pos] = -1
        elif value == 1:
            if self.pos not in self.map or self.moved < self.map[self.pos]:
                self.map[self.pos] = self.moved
                for d in range(1, 5):
                    e = Explorer(self.map, self.others, self.moved, self.pos, d)
                    e.prog = self.prog.fork()
                    self.others.append(e)
        elif value == 2:
            self.map[self.pos] = -2
            self.prog.value = self.moved
        raise ValueError()

    def input(self):
        c = self.d
        if c == 1:
            d = (0, 1)
        elif c == 2:
            d = (0, -1)
        elif c == 3:
            d = (-1, 0)
        elif c == 4:
            d = (1, 0)
        self.target = (self.pos[0] + d[0], self.pos[1] + d[1])
        return c


def render(m):
    from .day11 import bounds
    minx, miny, maxx, maxy = bounds(m)
    lines = ""
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            v = m.get((x, y), None)
            if (x, y) == (0, 0):
                lines += "S"
            elif v == -1:
                lines += b"\xe2\x96\x88".decode()
            elif v == -2:
                lines += "G"
            elif v is None:
                lines += b"\xe2\x96\x91".decode()
            else:
                lines += " "
        lines += "\n"
    print(lines)


def explore(data):
    m = {(0, 0): 0}
    bots = []
    a = None
    for d in range(1, 5):
        e = Explorer(m, bots, d=d)
        e.prog = Program(data)
        bots.append(e)
    while bots:
        e = bots.pop(0)
        ans = e.prog.run(e.input, e.output)
        if ans is not None:
            a = ans
    return m, a


def solve_b(m):
    oxygenated = set(k for k, v in m.items() if v == -2)
    missing = set(k for k, v in m.items() if v >= 0)
    t = 0
    while missing:
        t += 1
        added = set()
        for (x, y) in oxygenated:
            for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                p = (x + dx, y + dy)
                if p in missing:
                    missing.remove(p)
                    added.add(p)
        oxygenated = added
    return t


def solve(lines, do_render=False):
    data = [int(d) for d in lines[0].split(",")]

    m, a = explore(data)

    if do_render:
        render(m)

    b = solve_b(m)

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()], True))
