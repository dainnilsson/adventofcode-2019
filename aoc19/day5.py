from . import day2


class Ops(day2.Ops):
    def op_3(prog, a):
        prog.state[a] = prog.input()

    def op_4(prog, a):
        prog.output(prog.state[a])

    def op_5(prog, a, b):
        if prog.state[a]:
            prog.pc = prog.state[b]

    def op_6(prog, a, b):
        if prog.state[a] == 0:
            prog.pc = prog.state[b]

    def op_7(prog, a, b, c):
        prog.state[c] = int(prog.state[a] < prog.state[b])

    def op_8(prog, a, b, c):
        prog.state[c] = int(prog.state[a] == prog.state[b])


class Program(day2.Program):
    def __init__(self, data, input_fn, output_fn, ops=Ops):
        super().__init__(data, ops)
        self.input = input_fn
        self.output = output_fn

    def handle_mode(self, mode, pos):
        if not mode:
            pos = self.state[pos]
        return pos

    def step(self):
        code, op = divmod(self.state[self.get_pc()], 100)
        fun, n_args = self.ops.get(op)
        args = []
        for i in range(n_args):
            code, mode = divmod(code, 10)
            args.append(self.handle_mode(mode, self.get_pc()))
        fun(self, *args)
        return op


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    out = []

    program = Program(data, lambda: 1, out.append)
    program.run()
    a = out[-1]

    program = Program(data, lambda: 5, out.append)
    program.run()
    b = out[-1]

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
