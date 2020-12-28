from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from intcode_computer import run_as_generator
from typing import Deque, Iterable, List, Optional, Tuple

INPUT = "input"


class Movement(Enum):
    North = 1
    South = 2
    West = 3
    East = 4


class Status(Enum):
    Wall = 0
    Moved = 1
    Oxygen = 2


class Cell(Enum):
    Wall = 0
    Floor = 1
    Oxygen = 2
    Unknown = 3

    def __str__(self) -> str:
        return CELL_CHARS[self]


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


CELL_CHARS = {
    Cell.Wall: "#",
    Cell.Floor: ".",
    Cell.Oxygen: "O",
    Cell.Unknown: " "
}
VECTORS = {
    Movement.North: Point(0, -1),
    Movement.South: Point(0, 1),
    Movement.West: Point(-1, 0),
    Movement.East: Point(1, 0)
}


def borders(data: Iterable[Point]) -> Tuple[int, int, int, int]:
    xs = [p.x for p in data]
    ys = [p.y for p in data]
    return min(xs), max(xs), min(ys), max(ys)


def neighbours(pos: Point) -> List[Tuple[Point, Movement]]:
    return [(pos + vector, movement) for movement, vector in VECTORS.items()]


class Robot:
    def __init__(self, program: List[int]) -> None:
        self.position = Point(0, 0)
        self.program = run_as_generator(program)
        self.status: Optional[Status] = None
        self.grid = defaultdict(lambda: Cell.Unknown, {Point(0, 0): Cell.Floor})
        self.to_explore = deque([p for p, m in neighbours(self.position)])

        next(self.program)

    def move(self, move: Movement) -> None:
        vector = VECTORS[move]
        self.status = Status(self.program.send(move.value))
        next(self.program)
        if self.status == Status.Wall:
            self.grid[self.position + vector] = Cell.Wall
        else:
            self.position += vector
            self.grid[self.position] = Cell.Floor if self.status == Status.Moved else Cell.Oxygen

    def search(self) -> Point:
        while self.to_explore:
            print(self)
            to_explore = self.to_explore.popleft()
            for movement in self.shortest_path(self.position, to_explore):
                self.move(movement)
            if self.status != Status.Wall:
                self.to_explore.extend([p for p, m in neighbours(self.position) if self.grid[p] == Cell.Unknown])
                if self.status == Status.Oxygen:
                    oxygen_position = self.position
        return oxygen_position

    def shortest_path(self, start: Point, end: Point) -> List[Movement]:
        visited = set()
        to_visit: Deque[Tuple[Point, List[Movement]]] = deque([(start, [])])

        while True:
            pos, path = to_visit.popleft()
            if pos == end:
                return path
            if pos not in visited and self.grid[pos] in {Cell.Floor, Cell.Oxygen}:
                for neighbour, movement in neighbours(pos):
                    to_visit.append((neighbour, path + [movement]))
            visited.add(pos)

    def spread_oxygen(self, start: Point) -> int:
        turn_count = 0
        to_visit = {start}

        while True:
            print(self)
            to_visit = {n for p in to_visit for n, m in neighbours(p) if self.grid[n] == Cell.Floor}
            self.grid.update({n: Cell.Oxygen for n in to_visit})
            if not to_visit:
                break
            turn_count += 1

        return turn_count

    def __str__(self) -> str:
        min_x, max_x, min_y, max_y = borders(self.grid.keys())
        result = []
        for y in range(min_y, max_y + 1):
            result.append("".join(str(self.grid[Point(x, y)]) if Point(x, y) != self.position else "D" for x in range(min_x, max_x + 1)))
        return "\n".join(result)


def main() -> None:
    with open(INPUT, "r") as fin:
        program_data = [int(x) for x in fin.readline().strip().split(",")]
    robot = Robot(program_data)

    oxygen_position = robot.search()
    spread_time = robot.spread_oxygen(oxygen_position)
    print(len(robot.shortest_path(Point(0, 0), oxygen_position)))
    print(spread_time)


if __name__ == "__main__":
    main()
