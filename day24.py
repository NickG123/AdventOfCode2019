from __future__ import annotations

from collections import defaultdict
from typing import List, Set, Tuple

INPUT = "input"
BUG = "#"
EMPTY = "."

INNER_EDGES = {
    (2, 1): [(x, 0) for x in range(0, 5)],
    (2, 3): [(x, 4) for x in range(0, 5)],
    (1, 2): [(0, y) for y in range(0, 5)],
    (3, 2): [(4, y) for y in range(0, 5)],
}

OUTER_EDGES = {
    (0, 0): [(2, 1), (1, 2)],
    (4, 0): [(2, 1), (3, 2)],
    (0, 4): [(1, 2), (2, 3)],
    (4, 4): [(2, 3), (3, 2)]
}
for i in range(1, 4):
    OUTER_EDGES[(0, i)] = [(1, 2)]
    OUTER_EDGES[(4, i)] = [(3, 2)]
    OUTER_EDGES[(i, 0)] = [(2, 1)]
    OUTER_EDGES[(i, 4)] = [(2, 3)]


def new_grid() -> List[List[str]]:
    return [[EMPTY for x in range(5)] for y in range(5)]


class Grid:
    def __init__(self, data: List[List[str]], recursive: bool) -> None:
        self.data = defaultdict(new_grid, {0: data})
        self.recursive = recursive
        self.to_update = set()
        for y, row in enumerate(self.data[0]):
            for x in range(len(row)):
                if not recursive or x != 2 or y != 2:
                    self.to_update.add((0, x, y))
                    self.to_update.update(self.neighbours(0, x, y))

    def neighbours(self, depth: int, x: int, y: int) -> Set[Tuple[int, int, int]]:
        neighbour_pos = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        if self.recursive:
            result: Set[Tuple[int, int, int]] = set()
            for nx, ny in neighbour_pos:
                if (not 0 <= ny < len(self.data[depth])) or (not 0 <= nx < len(self.data[depth][y])):
                    result.update((depth - 1, sx, sy) for sx, sy in OUTER_EDGES[(x, y)])
                elif nx == 2 and ny == 2:
                    result.update((depth + 1, sx, sy) for sx, sy in INNER_EDGES[(x, y)])
                else:
                    result.add((depth, nx, ny))
            return result
        else:
            return {(0, x, y) for x, y in neighbour_pos if 0 <= y < len(self.data[0]) and 0 <= x < len(self.data[0][y])}

    def tick(self) -> None:
        updates = []
        to_update = set()
        for depth, x, y in self.to_update:
            cell = self.data[depth][y][x]
            neighbours = self.neighbours(depth, x, y)
            num_bugs = sum(self.data[d][y][x] == BUG for d, x, y in neighbours)
            if (cell == BUG and num_bugs != 1) or (cell == EMPTY and num_bugs in {1, 2}):
                updates.append((depth, x, y))
                to_update.add((depth, x, y))
                to_update.update(neighbours)
        for d, x, y in updates:
            self.data[d][y][x] = BUG if self.data[d][y][x] == EMPTY else EMPTY
        self.to_update = to_update

    def biodiversity(self) -> int:
        result = 0
        for y, row in enumerate(self.data[0]):
            for x, cell in enumerate(row):
                if cell == BUG:
                    result += 2 ** (len(row) * y + x)
        return result

    def bug_count(self) -> int:
        bugs = 0
        for data in self.data.values():
            for row in data:
                bugs += sum(c == BUG for c in row)
        return bugs

    def __str__(self) -> str:
        result = []
        for depth in range(min(self.data), max(self.data) + 1):
            result.append(f"Depth: {depth}")
            result.extend(("".join(l) for l in self.data[depth]))
        return "\n".join(result) + "\n"

    def print_neighbours(self, cx: int, cy: int) -> None:
        neighbours = self.neighbours(0, cx, cy)
        depths = [depth for depth, x, y in neighbours]
        for depth in range(min(depths), max(depths) + 1):
            print(f"Depth: {depth}")
            for y in range(0, 5):
                for x in range(0, 5):
                    if (depth, x, y) in neighbours:
                        print("X", end="")
                    elif depth == 0 and x == cx and y == cy:
                        print("O", end="")
                    else:
                        print(".", end="")
                print()


def main() -> None:
    with open(INPUT, "r") as fin:
        lines = fin.readlines()
        grid = Grid([list(l.strip()) for l in lines], False)
        grid2 = Grid([list(l.strip()) for l in lines], True)
    history = set()
    while str(grid) not in history:
        history.add(str(grid))
        grid.tick()
    print(grid.biodiversity())

    for i in range(200):
        grid2.tick()

    print(grid2.bug_count())


if __name__ == "__main__":
    main()
