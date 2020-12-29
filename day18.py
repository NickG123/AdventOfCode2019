from __future__ import annotations

import string

from collections import deque
from dataclasses import dataclass
from functools import cache
from typing import Deque, List, Set, Tuple

INPUT = "input"
KEYS = set(string.ascii_lowercase)
DOORS = set(string.ascii_uppercase)
WALL = "#"
FLOOR = "."
START = "@"


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Path:
    start: str
    end: str
    needed_keys: Set[str]
    distance: int


class Maze:
    def __init__(self, maze_data: List[str]) -> None:
        self.maze_data = [list(s) for s in maze_data]
        self.width = len(self.maze_data[0])
        self.height = len(self.maze_data)
        self.special_cells = {}
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze_data[y][x]
                if cell not in {WALL, FLOOR}:
                    self.special_cells[cell] = Point(x, y)

        keys = [cell for line in self.maze_data for cell in line if cell in KEYS]
        keys_and_start = keys + [START]

        self.paths: List[Path] = []
        for i, start in enumerate(keys_and_start):
            for end in keys_and_start[i + 1:]:
                length, blockers = self.shortest_path(self.special_cells[start], self.special_cells[end])
                self.paths.append(Path(start, end, {b.lower() for b in blockers}, length))

    def copy(self) -> Maze:
        return Maze(["".join(line) for line in self.maze_data])

    def get_start_position(self) -> Point:
        return self.special_cells[START]

    def get_cell(self, p: Point) -> str:
        return self.maze_data[p.y][p.x]

    def set_cell(self, p: Point, s: str) -> None:
        self.maze_data[p.y][p.x] = s

    def neighbours(self, p: Point) -> List[Point]:
        return [
            Point(p.x + 1, p.y),
            Point(p.x - 1, p.y),
            Point(p.x, p.y + 1),
            Point(p.x, p.y - 1),
        ]

    def shortest_path(self, start: Point, end: Point) -> Tuple[int, Set[str]]:
        seen = set()
        to_explore: Deque[Tuple[Point, List[Point]]] = deque([(start, [])])
        while to_explore:
            p, path = to_explore.popleft()
            if p in seen:
                continue
            seen.add(p)

            if p == end:
                return len(path), {self.get_cell(c) for c in path[1:] if self.get_cell(c) in DOORS.union(KEYS)}

            if not self.get_cell(p) == WALL:
                to_explore.extend((n, path + [p]) for n in self.neighbours(p))
        raise Exception("No path found")

    def options(self, start: str, keys: Set[str]) -> List[Path]:
        result = []
        for p in self.paths:
            if p.start == start:
                other = p.end
            elif p.end == start:
                other = p.start
            else:
                continue
            if other not in keys and keys.issuperset(p.needed_keys):
                result.append(p)
        return result

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.maze_data)


def read_maze() -> Maze:
    maze = []
    with open(INPUT, "r") as fin:
        for line in fin:
            maze.append(line.strip())
        return Maze(maze)


@cache
def brute_force(maze: Maze, position: str = "@", keys_held: Tuple[str, ...] = ("@",)) -> int:
    keys = set(keys_held)
    options = maze.options(position, keys)

    if len(options) == 0:
        return 0
    else:
        shortest_path_length = None
        for path in options:
            to_grab = path.start if path.start != position else path.end
            distance = path.distance + brute_force(maze, to_grab, tuple(keys | {to_grab}))
            shortest_path_length = distance if shortest_path_length is None else min(shortest_path_length, distance)

        return shortest_path_length


def main() -> None:
    maze = read_maze()
    print(brute_force(maze))


if __name__ == "__main__":
    main()
