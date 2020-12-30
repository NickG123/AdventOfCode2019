from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
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


class Cell:
    def __init__(self, p: Point) -> None:
        self.p = p
        self.neighbours: List[Cell] = []

    def compute_neighbours(self, grid: Grid) -> None:
        for vector in VECTORS:
            neighbour_pos = self.p + vector
            neighbour = grid.cells.get(neighbour_pos)
            if neighbour is not None:
                self.neighbours.append(neighbour)

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
                            self.labels[anchor] = label
        self.start = self.cells[self.portals.pop(START)[0]]
        self.end = self.cells[self.portals.pop(END)[0]]

        assert all(len(p) == 2 for p in self.portals.values())

        for cell in self.cells.values():
            cell.compute_neighbours(self)

    def find_path(self) -> int:
        seen = set()
        to_visit = deque([(self.start, 0)])
        while True:
            node, distance = to_visit.popleft()
            if node in seen:
                continue
            if node == self.end:
                return distance

            to_visit.extend([(n, distance + 1) for n in node.neighbours])
            seen.add(node)

    def get_portal_exit(self, entrance: Point) -> Optional[Cell]:
        label = self.labels.get(entrance)
        if label is None:
            return None
        exits = self.portals[label]
        exit_position = next(e for e in exits if e != entrance)
        return self.cells[exit_position]


def main() -> None:
    with open(INPUT, "r") as fin:
        grid = Grid([l.strip("\n") for l in fin.readlines()])

    print(grid.find_path())


if __name__ == "__main__":
    main()
