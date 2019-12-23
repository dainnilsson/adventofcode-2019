from . import day2


class Ops(day2.Ops):
    def op_3(prog, a):
        prog.io = a

    def op_4(prog, a):
        prog.io = prog.state[a]

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
    def __init__(self, data, ops=Ops):
        super().__init__(data, ops)
        self.io = None

    def _set_io(self, value):
        if self.io is not None:
            raise ValueError("Unhandled IO data!")
        self.io = value

    def _get_io(self):
        if self.io is None:
            raise ValueError("IO missing data!")
        v = self.io
        self.io = None
        return v

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

    def generate(self):
        op = None
        while op != 99:
            op = self.step()
            if op == 3:
                reg = self._get_io()
                yield (3, self._set_io)
                self.state[reg] = self._get_io()
            elif op == 4:
                yield (4, self._get_io())
        yield (99, None)

    def run(self, in_fn, out_fn):
        self.start()
        for op, arg in self.generate():
            if op == 3:
                arg(in_fn())
            elif op == 4:
                out_fn(arg)


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    out = []

    program = Program(data)
    program.run(lambda: 1, out.append)
    a = out[-1]

    program = Program(data)
    program.run(lambda: 5, out.append)
    b = out[-1]

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
