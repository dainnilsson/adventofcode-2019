from . import day5


class Ops(day5.Ops):
    def op_9(prog, a):
        prog.rb += prog.state[a]


class Program(day5.Program):
    def __init__(self, *args, ops=Ops):
        super().__init__(*args, ops)

    def start(self):
        self.rb = 0
        super().start()

    def handle_mode(self, mode, pos):
        if mode != 1:
            pos = self.state[pos]
            if mode == 2:
                pos += self.rb
        if len(self.state) <= pos:
            self.state.extend([0] * (pos - len(self.state) + 1))
        return pos


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    out = []
    p = Program(data)

    p.run(lambda: 1, out.append)
    p.run(lambda: 2, out.append)

    return tuple(out)


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
