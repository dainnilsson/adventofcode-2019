from functools import lru_cache


def checksum(orbits):
    @lru_cache(maxsize=None)
    def checksum_one(obj):
        return checksum_one(orbits[obj]) + 1 if obj != "COM" else 0

    return sum(checksum_one(k) for k in orbits)


def parents(orbits, node):
    return parents(orbits, orbits[node]) + [node] if node != "COM" else []


def solve(lines):
    orbits = {x[1]: x[0] for x in [o.split(")") for o in lines]}

    a = checksum(orbits)

    t1 = set(parents(orbits, orbits["YOU"]))
    t2 = set(parents(orbits, orbits["SAN"]))
    b = len(t1.symmetric_difference(t2))

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
