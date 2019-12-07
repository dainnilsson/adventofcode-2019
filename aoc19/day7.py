from .day5 import Program

from queue import Queue
from itertools import permutations
from concurrent.futures import ThreadPoolExecutor


def solve_a(data):
    qs = [Queue() for _ in range(6)]
    ps = [Program(data, qs[i].get, qs[i + 1].put) for i in range(5)]

    a = 0
    for seqs in permutations(range(5), 5):
        for i, s in enumerate(seqs):
            qs[i].put(s)
        qs[0].put(0)

        for p in ps:
            p.run()
        a = max(a, qs[-1].get())
    return a


def solve_b(data):
    qs = [Queue() for _ in range(5)]
    qs.append(qs[0])
    ps = [Program(data, qs[i].get, qs[i + 1].put) for i in range(5)]

    b = 0
    for seqs in permutations(range(5, 10), 5):
        for i, s in enumerate(seqs):
            qs[i].put(s)
        qs[0].put(0)

        with ThreadPoolExecutor() as e:
            for p in ps:
                e.submit(p.run)

        b = max(b, qs[0].get())
    return b


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    return (
        solve_a(data),
        solve_b(data)
    )


def solve_b_opt(data):
    qs = [Queue() for _ in range(5)]
    qs.append(qs[0])
    ps = [Program(data, qs[i].get, qs[i + 1].put) for i in range(5)]

    b = 0
    for seqs in permutations(range(5, 10), 5):
        for i, s in enumerate(seqs):
            qs[i].put(s)
        qs[0].put(0)

        for p in ps:
            p.state = p.data.copy()
            p.pc = 0

        act = 0  # Do our own scheduling
        op = ps[0].step()
        while op != 99:
            if op == 4:
                act = (act + 1) % 5
            op = ps[act].step()

        b = max(b, qs[0].get())
    return b


def optimized(lines):
    data = [int(d) for d in lines[0].split(",")]

    return (
        solve_a(data),
        solve_b_opt(data)
    )


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
