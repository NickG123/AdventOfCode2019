import itertools
from collections import deque
from intcode_computer import Program
from typing import Deque, Iterable


INPUT = "input"

START_COMMANDS = [
    "north",
    "north",
    "take sand",
    "south",
    "south",
    "south",
    "take space heater",
    "west",
    "take wreath",
    "south",
    "south",
    "take pointer",
    "north",
    "north",
    "east",
    "north",
    "west",
    "south",
    "take planetoid",
    "north",
    "west",
    "take festive hat",
    "west",
    "south",
    "west",
    "drop sand",
    "drop space heater",
    "drop wreath",
    "drop pointer",
    "drop festive hat",
    "drop planetoid"
]

ITEMS = ["sand", "space heater", "wreath", "pointer", "festive hat", "planetoid"]


def brute_force_door() -> Iterable[str]:
    for size in range(1, len(ITEMS)):
        for combination in itertools.combinations(ITEMS, size):
            for item in combination:
                yield f"take {item}"
            yield "north"
            for item in combination:
                yield f"drop {item}"


def run(program: Program, input_data: Deque[str]) -> None:
    bf_door = brute_force_door()
    for line in program.read_lines():
        print(line)
        if line == "Command?":
            if input_data:
                command = input_data.popleft()
            else:
                command = next(bf_door)
            print(command)
            program.write_string(command)


def main() -> None:
    with open(INPUT, "r") as fin:
        program_data = [int(x) for x in fin.readline().strip().split(",")]
    run(Program(program_data), deque(START_COMMANDS))


if __name__ == "__main__":
    main()
