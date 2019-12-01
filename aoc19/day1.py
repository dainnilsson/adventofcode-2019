def solve(lines):
    ms = [[int(d) // 3 - 2] for d in lines]
    for m in ms:
        while m[-1]:
            m.append(max(0, m[-1] // 3 - 2))
    return (sum(l[0] for l in ms), sum(sum(l) for l in ms))


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
