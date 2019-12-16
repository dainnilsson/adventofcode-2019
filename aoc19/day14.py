from collections import Counter
from math import ceil


def produce(reactions, inventory, elem, amount):
    amount -= inventory[elem]
    if amount <= 0:
        return 0

    if elem == "ORE":
        inventory[elem] += amount
        return amount

    produced, needed = reactions[elem]
    times = ceil(amount / produced)
    c = 0
    for (n, elem2) in needed:
        c += produce(reactions, inventory, elem2, times * n)
        inventory[elem2] -= times * n

    inventory[elem] += times * produced
    return c


def solve(lines):
    reactions = {}
    for line in lines:
        lh, rh = line.split(" => ", 1)

        needed = []
        for pair in lh.split(", "):
            amount, elem = pair.split()
            needed.append((int(amount), elem))
        amount, key = rh.split()
        reactions[key] = (int(amount), needed)

    inventory = Counter()
    a = produce(reactions, inventory, "FUEL", 1)

    ore = 1000000000000 - a

    n = 0
    while ore // a > 1:
        n += ore // a
        ore -= produce(reactions, inventory, "FUEL", n)
    while ore > 0:
        n += 1
        ore -= produce(reactions, inventory, "FUEL", n)
    return a, n - 1


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
