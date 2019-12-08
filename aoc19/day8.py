DRAW = {
    "01": b"\xe2\x96\x84".decode(),
    "10": b"\xe2\x96\x80".decode(),
    "11": b"\xe2\x96\x88".decode(),
}


def render(img, w, h):
    lines = []
    for y in range(0, h, 2):
        buf = ""
        for x in range(w):
            t = img[w * y + x]
            b = img[w * (y + 1) + x]
            buf += DRAW.get(t + b, " ")
        lines.append(buf)
    return "\n".join(lines)


def solve_a(data, w, h):
    area = w * h
    min_z = area
    candidate = None
    for i in range(0, len(data), area):
        layer = data[i : i + area]
        zeroes = layer.count("0")
        if zeroes < min_z:
            min_z = zeroes
            candidate = layer
    return candidate.count("1") * candidate.count("2")


def solve_b(data, w, h):
    area = w * h
    pic = ["2"] * area
    for i in range(0, len(data), area):
        for j in range(area):
            if pic[j] == "2":
                pic[j] = data[i + j]
    return render(pic, w, h)


def solve(lines):
    data = lines[0]
    return (solve_a(data, 25, 6), solve_b(data, 25, 6))


if __name__ == "__main__":
    import fileinput

    a, b = solve([l.rstrip("\r\n") for l in fileinput.input()])
    print(a)
    print(b)
