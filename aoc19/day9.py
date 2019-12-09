from . import day5


class Ops(day5.Ops):
    def op_9(prog, a):
        prog.rb += prog.state[a]


class Program(day5.Program):
    def run(self):
        self.rb = 0
        super().run()

    def step(self):
        code, op = divmod(self.state[self.get_pc()], 100)
        fun, n_args = Ops.get(op)
        args = []
        for i in range(n_args):
            code, mode = divmod(code, 10)
            pos = self.get_pc()
            if mode != 1:
                pos = self.state[pos]
                if mode == 2:
                    pos += self.rb
            args.append(pos)
        ln = max(args, default=0)
        if len(self.state) <= ln:
            self.state.extend([0] * (ln - len(self.state) + 1))
        fun(self, *args)
        return op


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    inp = [2, 1]
    out = []
    p = Program(data, inp.pop, out.append)

    p.run()
    p.run()

    return tuple(out)


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
