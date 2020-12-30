import itertools

from intcode_computer import Program
from typing import Dict, Iterator, List, Tuple

INPUT = "input"


class TractorBeam:
    def __init__(self, program_data: List[int]) -> None:
        self.program_data = program_data
        self.beam_spaces: Dict[Tuple[int, int], bool] = {}

    def get_cell(self, x: int, y: int) -> bool:
        if (x, y) in self.beam_spaces:
            return self.beam_spaces[(x, y)]
        program = Program(self.program_data[:])
        program.send_input(x)
        program.send_input(y)
        pulled = bool(program.next_output())
        self.beam_spaces[(x, y)] = pulled
        return pulled

    def space_fits(self, start_x: int, start_y: int, size: int) -> bool:
        for y in range(start_y, start_y + size):
            for x in range(start_x, start_x + size):
                if not self.get_cell(x, y):
                    return False
        return True

    def find_space(self, size: int) -> Tuple[int, int]:
        for x, y in self.potential_bottom_left():
            if self.get_cell(x + size - 1, y - size + 1):
                top = y - size + 1
                if self.space_fits(x, top, size):
                    return (x, top)

    def potential_bottom_left(self) -> Iterator[Tuple[int, int]]:
        start_x = 0
        for y in itertools.count(5):
            for x in itertools.count(start_x):
                if self.get_cell(x, y):
                    start_x = x
                    yield (x, y)
                    break

    def __str__(self) -> str:
        result = []
        size = max(max(x, y) for x, y in self.beam_spaces) + 1
        for y in range(size):
            result.append("".join("#" if self.beam_spaces.get((x, y), False) else "." for x in range(size)))
        return "\n".join(result)


def main() -> None:
    with open(INPUT, "r") as fin:
        program_data = [int(x) for x in fin.readline().strip().split(",")]

    beam = TractorBeam(program_data)
    print(sum(beam.get_cell(x, y) for y in range(50) for x in range(50)))
    x, y = beam.find_space(100)
    print(x * 10000 + y)


if __name__ == "__main__":
    main()
