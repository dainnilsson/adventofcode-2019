from itertools import cycle


PHASE = (0, 1, 0, -1)


def extend(n):
    for p in cycle(PHASE):
        for _ in range(n):
            yield p


def solve_a(data):
    for _ in range(100):
        out = []
        for i in range(1, len(data) + 1):
            g = extend(i)
            next(g)
            out.append(abs(sum(a * b for a, b in zip(data, g))) % 10)
        data = out
    return "".join(str(d) for d in data[:8])


def solve_b(data):
    offset = int("".join(str(d) for d in data[:7]))
    data = data * 10000
    data = data[offset:]

    for _ in range(100):
        s = 0
        new_data = []
        for i in range(len(data), 0, -1):
            s += data[i - 1]
            new_data.append(abs(s) % 10)
        new_data.reverse()
        data = new_data

    return "".join(str(d) for d in data[:8])


def solve(lines):
    data = [int(c) for c in lines[0]]

    return solve_a(data), solve_b(data)


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
