def cost(m):
    return max(0, m // 3 - 2)


def full_cost(m):
    c = cost(m)
    return c + full_cost(c) if c else 0


def solve(lines):
    ms = [int(d) for d in lines]
    return (
        sum(cost(m) for m in ms),
        sum(full_cost(m) for m in ms),
    )


def optimized(lines):
    a, b = 0, 0
    for l in lines:
        m = int(l)
        c = m // 3 - 2
        a += c
        while c:
            b += c
            c = max(0, c // 3 - 2)
    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
