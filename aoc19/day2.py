import fileinput

"""Day 2 from AOC 2017 as a sample."""


def solve(lines):
    data = [[int(x) for x in row.split()] for row in lines]

    return (
        sum(max(r) - min(r) for r in data),
        sum(x // y for r in data for x in r for y in r if x != y and x % y == 0),
    )


if __name__ == "__main__":
    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
