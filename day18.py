from __future__ import annotations

import string

from collections import deque
from dataclasses import dataclass
from functools import cache
from typing import Deque, List, Set, Optional, Tuple

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
    def __init__(self, maze_data: List[str], part2: bool) -> None:
        self.maze_data = [list(s) for s in maze_data]
        self.width = len(self.maze_data[0])
        self.height = len(self.maze_data)
        self.special_cells = {}
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze_data[y][x]
                if cell not in {WALL, FLOOR}:
                    self.special_cells[cell] = Point(x, y)

        if part2:
            p = self.special_cells[START]
            self.maze_data[p.y][p.x] = WALL
            self.maze_data[p.y - 1][p.x] = WALL
            self.maze_data[p.y + 1][p.x] = WALL
            self.maze_data[p.y][p.x - 1] = WALL
            self.maze_data[p.y][p.x + 1] = WALL
            self.maze_data[p.y - 1][p.x - 1] = "1"
            self.maze_data[p.y - 1][p.x + 1] = "2"
            self.maze_data[p.y + 1][p.x + 1] = "3"
            self.maze_data[p.y + 1][p.x - 1] = "4"
            del self.special_cells[START]
            self.special_cells["1"] = Point(p.x - 1, p.y - 1)
            self.special_cells["2"] = Point(p.x - 1, p.y + 1)
            self.special_cells["3"] = Point(p.x + 1, p.y + 1)
            self.special_cells["4"] = Point(p.x + 1, p.y - 1)

        keys = [cell for line in self.maze_data for cell in line if cell in KEYS]
        if part2:
            keys_and_start = keys + ["1", "2", "3", "4"]
        else:
            keys_and_start = keys + [START]

        self.paths: List[Path] = []
        for i, start in enumerate(keys_and_start):
            for end in keys_and_start[i + 1:]:
                result = self.shortest_path(self.special_cells[start], self.special_cells[end])
                if result is not None:
                    length, blockers = result
                    self.paths.append(Path(start, end, {b.lower() for b in blockers}, length))

    def get_cell(self, p: Point) -> str:
        return self.maze_data[p.y][p.x]

    def neighbours(self, p: Point) -> List[Point]:
        return [
            Point(p.x + 1, p.y),
            Point(p.x - 1, p.y),
            Point(p.x, p.y + 1),
            Point(p.x, p.y - 1),
        ]

    def shortest_path(self, start: Point, end: Point) -> Optional[Tuple[int, Set[str]]]:
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
        return None

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


def read_maze(part2: bool) -> Maze:
    maze = []
    with open(INPUT, "r") as fin:
        for line in fin:
            maze.append(line.strip())
        return Maze(maze, part2)


@cache
def brute_force(maze: Maze, positions: Tuple[str, ...] = ("@",), keys_held: Optional[Tuple[str, ...]] = None) -> int:
    if keys_held is None:
        keys = set(positions)
    else:
        keys = set(keys_held)
    options = [(i, op) for i, p in enumerate(positions) for op in maze.options(p, keys)]

    if len(options) == 0:
        return 0
    else:
        shortest_path_length = None
        for position_index, path in options:
            to_grab = path.start if path.start != positions[position_index] else path.end
            new_positions = list(positions)
            new_positions[position_index] = to_grab
            distance = path.distance + brute_force(maze, tuple(new_positions), tuple(keys | {to_grab}))
            shortest_path_length = distance if shortest_path_length is None else min(shortest_path_length, distance)

        return shortest_path_length


def main() -> None:
    print(brute_force(read_maze(False)))
    print(brute_force(read_maze(True), ("1", "2", "3", "4")))


if __name__ == "__main__":
    main()
