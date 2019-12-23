from .day9 import Program


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    ans_a = None
    ans_b = None
    last_b = None

    ps = []
    idle = []
    for i in range(50):
        p = Program(data)
        p.start()
        g = p.generate()
        next(g)[1](i)
        ps.append(g)
        idle.append(False)

    act = 0
    last_xy = None
    buf = []
    while True:
        op, arg = next(ps[act])
        if op == 3:
            if buf:
                arg(buf.pop(0))
            else:
                arg(-1)
                idle[act] = True
                act = (act + 1) % len(ps)
        elif op == 4:
            buf.append(arg)
            if len(buf) == 3:
                i = buf.pop(0)
                x, y = buf
                if i == 255:
                    buf.clear()
                    last_xy = (x, y)
                    if not ans_a:
                        ans_a = y
                else:
                    act = i

        if all(idle) and last_xy:
            act = 0
            buf = list(last_xy)
            idle = [False] * len(idle)
            if ans_b is None:
                if last_xy == last_b:
                    ans_b = last_xy[1]
                    return ans_a, ans_b
                last_b = last_xy


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
