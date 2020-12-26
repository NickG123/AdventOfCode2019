from collections import defaultdict
from enum import Enum
from intcode_computer import run_as_generator
from typing import Dict, List, Tuple

INPUT = "input"


class Direction(Enum):
    N = 0
    E = 90
    S = 180
    W = 270


MAX_COMPASS = 360

VECTORS = {
    Direction.N: (0, -1),
    Direction.E: (1, 0),
    Direction.S: (0, 1),
    Direction.W: (-1, 0)
}


class Robot:
    def __init__(self) -> None:
        self.pos = (0, 0)
        self.direction = Direction.N

    def rotate(self, clockwise: bool) -> None:
        self.direction = Direction((self.direction.value + 90 * (1 if clockwise else -1)) % MAX_COMPASS)

    def move(self) -> None:
        dx, dy = VECTORS[self.direction]
        x, y = self.pos
        self.pos = (x + dx, y + dy)


def run(program_data: List[int], white_start: bool) -> Dict[Tuple[int, int], bool]:
    robot = Robot()
    program = run_as_generator(program_data)
    tiles: Dict[Tuple[int, int], bool] = defaultdict(bool)
    if white_start:
        tiles[(0, 0)] = True

    next(program)
    try:
        while True:
            color = int(tiles[robot.pos])
            new_color = program.send(color)
            turn = next(program)
            next(program)

            tiles[robot.pos] = bool(new_color)
            robot.rotate(True if turn == 1 else False)
            robot.move()
    except StopIteration:
        return tiles


def borders(data: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    xs = [x for (x, y) in data]
    ys = [y for (x, y) in data]
    return min(xs), max(xs), min(ys), max(ys)


def print_tiles(tiles: Dict[Tuple[int, int], bool]) -> None:
    min_x, max_x, min_y, max_y = borders(list(tiles.keys()))
    for y in range(min_y, max_y + 1):
        print("".join("X" if tiles[(x, y)] else " " for x in range(min_x, max_x + 1)))


if __name__ == "__main__":
    robot = Robot()

    with open(INPUT, "r") as fin:
        program_data = [int(x) for x in fin.readline().split(",")]

    print(len(run(program_data[:], False)))
    p2_result = run(program_data[:], True)
    print_tiles(p2_result)
