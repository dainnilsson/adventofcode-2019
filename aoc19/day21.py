from .day9 import Program
from inspect import cleandoc


def solve(lines):
    data = [int(d) for d in lines[0].split(",")]
    program = Program(data)

    def springcode(script):
        code = bytearray((cleandoc(script) + "\n").encode())
        code.reverse()

        out = []
        program.run(code.pop, out.append)

        return out.pop()

    a = springcode(
        """
        NOT A T
        OR T J
        NOT B T
        OR T J
        NOT C T
        OR T J
        AND D J
        WALK
        """
    )

    b = springcode(
        """
        NOT A T
        OR T J
        NOT B T
        OR T J
        NOT C T
        OR T J
        AND D J
        NOT E T
        NOT T T
        OR H T
        AND T J
        RUN
        """
    )

    return a, b


if __name__ == "__main__":
    import fileinput

    print(solve([l.rstrip("\r\n") for l in fileinput.input()]))
