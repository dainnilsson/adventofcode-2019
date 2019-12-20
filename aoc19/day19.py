from .day9 import Program


def check(data, x, y):
    pos = [y, x]
    out = []
    p = Program(data, pos.pop, out.append)
    p.run()
    return out.pop()


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]

    a = sum(1 for y in range(50) for x in range(50) if check(data, x, y))

    x, y = 0, 0
    while True:
        if check(data, x + 99, y):
            if check(data, x, y + 99):
                break
            x += 1
        else:
            y += 1

    b = x * 10000 + y

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
