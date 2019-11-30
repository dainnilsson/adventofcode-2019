import fileinput

"""Day 1 from AOC 2017 as a sample."""


def solve(lines):
    ds = [int(d) for d in lines[0]]
    n = len(ds)

    return (
        sum(d for i, d in enumerate(ds) if d == ds[(i + 1) % n]),
        sum(d for i, d in enumerate(ds) if d == ds[(i + n // 2) % n]),
    )


if __name__ == "__main__":
    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
