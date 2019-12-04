from collections import Counter


def adjacent(pw):
    return len(set(str(pw))) < 6


def pair(pw):
    return 2 in Counter(str(pw)).values()


def increasing(pw):
    pw = str(pw)
    return pw == "".join(sorted(pw))


def solve(lines):
    parts = lines[0].split("-")
    start = int(parts[0])
    end = int(parts[1])

    a, b = 0, 0
    for pw in range(start, end):
        if increasing(pw):
            if adjacent(pw):
                a += 1
                if pair(pw):
                    b += 1

    return a, b


def parse_start(start):
    buf = start[0]
    for i in range(5):
        c = start[i + 1]
        if int(buf[i]) > int(c):
            return int(buf + (6 - len(buf)) * buf[i])
        buf += c
    return int(buf)


def count_incr(start):
    if start < 10:
        yield from range(start, 10)
    else:
        start, rem = divmod(start, 10)
        for base in count_incr(start):
            for i in range(max(base % 10, rem), 10):
                yield 10 * base + i
            rem = 0


def optimized(lines):
    parts = lines[0].split("-")
    start = parse_start(parts[0])
    end = int(parts[1])

    a, b = 0, 0
    for pw in count_incr(start):
        if pw > end:
            return a, b
        c = Counter(str(pw))
        if len(c) < 6:
            a += 1
            if 2 in c.values():
                b += 1


if __name__ == "__main__":
    import fileinput

    print(optimized([l.rstrip("\r\n") for l in fileinput.input()]))
