def op_add(data, a, b, c):
    data[c] = data[a] + data[b]


def op_mul(data, a, b, c):
    data[c] = data[a] * data[b]


OPS = {1: (3, op_add), 2: (3, op_mul)}


def run(data, noun, verb):
    data = data.copy()
    data[1] = noun
    data[2] = verb

    pc = 0
    try:
        op = data[pc]
        while op != 99:
            n_args, fun = OPS[op]
            fun(data, *data[pc + 1 : pc + 1 + n_args])
            pc += 1 + n_args
            op = data[pc]
    except Exception:
        return None
    return data[0]


def candidates():
    """Generates noun, verb pairs in a growing search space."""
    s = 0
    while True:
        s += 1
        for x in range(s):
            yield (x, s)
            yield (s, x)
        yield (s, s)


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    a = run(data, 12, 2)

    for noun, verb in candidates():
        if run(data, noun, verb) == 19690720:
            return (a, 100 * noun + verb)


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
