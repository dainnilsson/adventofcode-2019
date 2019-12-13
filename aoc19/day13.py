from .day9 import Program


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


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    game = Game()

    p = Program(data, lambda: None, game.output)
    p.run()

    a = len([t for t in game.screen.values() if t == 2])

    data[0] = 2
    game = Game()
    p = Program(data, game.input, game.output)
    p.run()

    b = game.score

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
