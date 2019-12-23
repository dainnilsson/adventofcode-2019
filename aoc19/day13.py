from .day9 import Program
from .day11 import bounds
from time import sleep


TILES = {
    0: " ",
    1: b"\xe2\x96\x92".decode(),
    2: b"\xe2\x96\x84".decode(),
    3: b"\xe2\x96\x80".decode(),
    4: "o",
}


class Game:
    def __init__(self):
        self.screen = {}
        self.score = 0
        self.buf = []
        self.ball_x = 0
        self.paddle_x = 0

    def output(self, value):
        if len(self.buf) == 2:
            x, y = self.buf
            self.buf.clear()
            if (x, y) == (-1, 0):
                self.score = value
            else:
                self.screen[(x, y)] = value
                if value == 3:
                    self.paddle_x = x
                elif value == 4:
                    self.ball_x = x
        else:
            self.buf.append(value)

    def input(self):
        if self.ball_x < self.paddle_x:
            return -1
        if self.ball_x > self.paddle_x:
            return 1
        return 0

    def render(self):
        print("\x1b[2J\x1b[H")
        minx, miny, maxx, maxy = bounds(self.screen)
        lines = "SCORE:  {:28d}\n".format(self.score)
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                lines += TILES[self.screen[(x, y)]]
            lines += "\n"
        print(lines)


def solve(lines, render=False):
    data = [int(d) for d in lines[0].split(",")]

    game = Game()

    Program(data).run(lambda: None, game.output)

    a = len([t for t in game.screen.values() if t == 2])

    data[0] = 2
    game = Game()
    if render:
        def f():
            game.render()
            sleep(0.05)
            return game.input()
    else:
        f = game.input
    Program(data).run(f, game.output)

    b = game.score
    if render:
        game.render()

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()], True))
