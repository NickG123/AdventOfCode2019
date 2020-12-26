from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

INPUT = "input"


class Direction(Enum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


@dataclass(frozen=True, eq=True)
class Pair:
    x: int
    y: int

    def __add__(self, other: Pair) -> Pair:
        return Pair(self.x + other.x, self.y + other.y)


vectors = {
    Direction.Up: Pair(0, 1),
    Direction.Down: Pair(0, -1),
    Direction.Right: Pair(1, 0),
    Direction.Left: Pair(-1, 0)
}


class Wire:
    def __init__(self, path_str: str) -> None:
        self.path = [(Direction(s[0]), int(s[1:])) for s in path_str.split(",")]

    def positions(self) -> Iterable[Pair]:
        position = Pair(0, 0)
        for (direction, distance) in self.path:
            for _ in range(distance):
                position += vectors[direction]
                yield position


def main() -> None:
    with open(INPUT, "r") as fin:
        wire1 = Wire(fin.readline())
        wire2 = Wire(fin.readline())

        grid = {}
        for i, pos in enumerate(wire1.positions()):
            if pos not in grid:
                grid[pos] = i + 1
        min_part_1_distance = None
        min_part_2_distance = None
        for i, pos in enumerate(wire2.positions()):
            if pos in grid:
                part_1_distance = abs(pos.x) + abs(pos.y)
                part_2_distance = i + 1 + grid[pos]
                min_part_1_distance = part_1_distance if min_part_1_distance is None else min(part_1_distance, min_part_1_distance)
                min_part_2_distance = part_2_distance if min_part_2_distance is None else min(part_2_distance, min_part_2_distance)
        print(min_part_1_distance)
        print(min_part_2_distance)


if __name__ == "__main__":
    main()
