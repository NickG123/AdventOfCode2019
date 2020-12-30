from intcode_computer import Program

from typing import List, Optional

INPUT = "input"

part1 = [
    # If B or C is a hole and D is ground jump to D
    "NOT B J",
    "NOT C T",
    "OR T J",
    "AND D J",

    # If A is a hole, jump
    "NOT A T",
    "OR T J",

    "WALK"
]

part2 = [
    # If B or C is a hole and D and E are ground jump to D
    "NOT B J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "AND H J",

    # If A is a hole, jump
    "NOT A T",
    "OR T J",

    "RUN"
]


def run(program: Program, commands: List[str]) -> Optional[int]:
    print(program.read_line())
    for c in commands:
        program.write_string(c)
    print(program.read_line())
    print(program.read_line())
    print(program.read_line())
    ret = next(program)
    if ret == 10:
        for line in program.read_lines():
            print(line)
        return None

    return ret


def main() -> None:
    with open(INPUT, "r") as fin:
        program_data = [int(x) for x in fin.readline().strip().split(",")]
    print(run(Program(program_data[:]), part1))
    print(run(Program(program_data[:]), part2))


if __name__ == "__main__":
    main()
