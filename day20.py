from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

INPUT = "input"
WALL = "#"
FLOOR = "."
SPACE = " "

START = "AA"
END = "ZZ"


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)


VECTORS = [
    Point(0, 1),
    Point(0, -1),
    Point(1, 0),
    Point(-1, 0)
]


class NeighbourType(Enum):
    InnerPortal = 1
    Direct = 0
    OuterPortal = -1


class Cell:
    def __init__(self, p: Point) -> None:
        self.p = p
        self.neighbours: List[Tuple[Cell, NeighbourType]] = []

    def compute_neighbours(self, grid: Grid) -> None:
        for vector in VECTORS:
            neighbour_pos = self.p + vector
            neighbour = grid.cells.get(neighbour_pos)
            if neighbour is not None:
                self.neighbours.append((neighbour, NeighbourType.Direct))

        portal_exit = grid.get_portal_exit(self.p)
        if (portal_exit := grid.get_portal_exit(self.p)) is not None:
            self.neighbours.append(portal_exit)


def get_label(data: List[str], p: Point) -> Optional[Tuple[str, Point]]:
    for vector in VECTORS:
        anchor = p + vector
        if data[anchor.y][anchor.x] == ".":
            o = p - vector
            return data[min(p.y, o.y)][min(p.x, o.x)] + data[max(p.y, o.y)][max(p.x, o.x)], anchor
    return None


class Grid:
    def __init__(self, data: List[str]) -> None:
        self.cells = {}
        self.labels = {}
        self.portals: Dict[str, List[Point]] = defaultdict(list)
        for y, row in enumerate(data[1:-1], start=1):
            for x, cell_val in enumerate(row[1:-1], start=1):
                p = Point(x, y)
                if cell_val == FLOOR:
                    self.cells[p] = Cell(p)
                    continue
                elif cell_val in {WALL, SPACE}:
                    continue
                else:
                    result = get_label(data, p)
                    if result is not None:
                        label, anchor = result
                        self.portals[label].append(anchor)
                        if label not in {START, END}:
                            if p.x == 1 or p.x == len(row) - 2 or p.y == 1 or p.y == len(data) - 2:
                                portal_type = NeighbourType.OuterPortal
                            else:
                                portal_type = NeighbourType.InnerPortal
                            self.labels[anchor] = (label, portal_type)
        self.start = self.cells[self.portals.pop(START)[0]]
        self.end = self.cells[self.portals.pop(END)[0]]

        assert all(len(p) == 2 for p in self.portals.values())

        for cell in self.cells.values():
            cell.compute_neighbours(self)

    def find_path(self, recursive: bool) -> int:
        seen = set()
        to_visit = deque([(self.start, 0, 0)])
        while True:
            node, depth, distance = to_visit.popleft()
            if (node, depth) in seen:
                continue
            if node == self.end and depth == 0:
                return distance

            if recursive:
                to_visit.extend([(n, depth + neighbour_type.value, distance + 1) for n, neighbour_type in node.neighbours if neighbour_type != NeighbourType.OuterPortal or depth != 0])
            else:
                to_visit.extend([(n, depth, distance + 1) for n, neighbour_type in node.neighbours])
            seen.add((node, depth))

    def get_portal_exit(self, entrance: Point) -> Optional[Tuple[Cell, NeighbourType]]:
        if entrance not in self.labels:
            return None
        label, portal_type = self.labels[entrance]
        exits = self.portals[label]
        exit_position = next(e for e in exits if e != entrance)
        return self.cells[exit_position], portal_type


def main() -> None:
    with open(INPUT, "r") as fin:
        grid = Grid([l.strip("\n") for l in fin.readlines()])

    print(grid.find_path(False))
    print(grid.find_path(True))


if __name__ == "__main__":
    main()
