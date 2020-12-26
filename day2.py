from typing import List
from intcode_computer import run

INPUT = "input"
TARGET = 19690720


def run_program_with_args(program: List[int], noun: int, verb: int) -> int:
    program[1] = noun
    program[2] = verb
    program_copy = program[:]
    run(program_copy)
    return program_copy[0]


def main() -> None:
    with open(INPUT, "r") as fin:
        program = [int(x) for x in fin.readline().split(",")]
    print(run_program_with_args(program, 12, 2))

    for noun in range(100):
        for verb in range(100):
            if run_program_with_args(program, noun, verb) == TARGET:
                print(noun * 100 + verb)
                return


if __name__ == "__main__":
    main()
