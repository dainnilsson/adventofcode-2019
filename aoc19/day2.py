from itertools import count
from inspect import signature
from functools import lru_cache


class Ops:
    def op_1(prog, a, b, c):
        prog.state[c] = prog.state[a] + prog.state[b]

    def op_2(prog, a, b, c):
        prog.state[c] = prog.state[a] * prog.state[b]

    def op_99(prog):
        pass

    @classmethod
    @lru_cache(maxsize=None)
    def get(cls, op):
        fun = getattr(cls, f"op_{op}")
        return fun, len(signature(fun).parameters) - 1


class Program:
    def __init__(self, data, ops=Ops):
        self.data = data
        self.ops = ops

    def get_pc(self):
        self.pc += 1
        return self.pc - 1

    def step(self):
        op = self.state[self.get_pc()]
        fun, n_args = self.ops.get(op)
        fun(self, *[self.state[self.get_pc()] for _ in range(n_args)])
        return op

    def run(self):
        self.pc = 0
        self.state = self.data.copy()
        while self.step() != 99:
            pass
        return self.state[0]


def candidates():
    """Generates noun, verb pairs in a growing search space."""
    for s in count(0):
        for x in range(s):
            yield (x, s)
            yield (s, x)
        yield (s, s)


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    program = Program(data)

    program.data[1] = 12
    program.data[2] = 2

    a = program.run()

    for noun, verb in candidates():
        program.data[1] = noun
        program.data[2] = verb
        if program.run() == 19690720:
            return (a, 100 * noun + verb)


def run(data, noun, verb):
    data = data.copy()
    data[1] = noun
    data[2] = verb
    pc = 0
    op = 0
    while op != 99:
        op = data[pc]
        if op == 1:
            data[data[pc + 3]] = data[data[pc + 1]] + data[data[pc + 2]]
        elif op == 2:
            data[data[pc + 3]] = data[data[pc + 1]] * data[data[pc + 2]]
        pc += 4
    return data[0]


def optimized(lines):
    data = [int(d) for d in lines[0].split(",")]

    a = run(data, 12, 2)

    for noun, verb in candidates():
        if run(data, noun, verb) == 19690720:
            return (a, 100 * noun + verb)


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
