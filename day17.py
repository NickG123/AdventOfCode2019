from intcode_computer import Program
from typing import Iterator, List, Tuple

INPUT = "input"


def find_intersections(image: str) -> Iterator[Tuple[int, int]]:
    rows = image.split("\n")
    for y, (prev_row, row, next_row) in enumerate(zip(rows, rows[1:], rows[2:]), start=1):
        for x, cells in enumerate(zip(row, row[1:], row[2:], prev_row[1:], next_row[1:]), start=1):
            if all(cell == "#" for cell in cells):
                yield x, y


def readlines(program: Program) -> Iterator[str]:
    while True:
        line = []
        while (c := chr(next(program))) != "\n":
            line.append(c)
        yield "".join(line)


def read_image(program: Program) -> str:
    result: List[str] = []
    for line in readlines(program):
        if not line.strip():
            return "\n".join(result)
        result.append(line)
    raise Exception("Expected blank line")


def write_text(program: Program, s: str) -> None:
    for c in s + "\n":
        program.send_input(ord(c))


def main() -> None:
    with open(INPUT, "r") as fin:
        program_data = [int(c) for c in fin.readline().strip().split(",")]

    program_data[0] = 2
    program = Program(program_data[:])
    image = read_image(program)
    print(image)
    intersections = find_intersections(image)
    print(sum(x * y for x, y in intersections))
    next(readlines(program))
    write_text(program, "A,A,B,C,C,A,C,B,C,B")
    next(readlines(program))
    write_text(program, "L,4,L,4,L,6,R,10,L,6")
    next(readlines(program))
    write_text(program, "L,12,L,6,R,10,L,6")
    next(readlines(program))
    write_text(program, "R,8,R,10,L,6")
    next(readlines(program))
    write_text(program, "n")
    next(program)

    image = read_image(program)
    print(image)
    print(next(program))


if __name__ == "__main__":
    main()
