from enum import Enum
from intcode_computer import Program
from typing import Dict, Tuple

INPUT = "input"


class Tile(Enum):
    Empty = 0
    Wall = 1
    Block = 2
    Paddle = 3
    Ball = 4


SYMBOLS = {
    Tile.Empty: " ",
    Tile.Wall: "☐",
    Tile.Block: "X",
    Tile.Paddle: "-",
    Tile.Ball: "O"
}


class Board:
    def __init__(self) -> None:
        self.board: Dict[Tuple[int, int], Tile] = {}
        self.score = 0
        self.block_count = 0
        self.paddle_x = 0
        self.ball_x = 0

    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        self.board[(x, y)] = tile
        if tile == Tile.Block:
            self.block_count += 1
        elif tile == Tile.Paddle:
            self.paddle_x = x
        elif tile == Tile.Ball:
            self.ball_x = x

    def next_move(self) -> int:
        if self.paddle_x > self.ball_x:
            return -1
        if self.paddle_x < self.ball_x:
            return 1
        return 0

    def __str__(self) -> str:
        width = max(x for x, y in self.board.keys())
        height = max(y for x, y in self.board.keys())
        board = "\n".join("".join(SYMBOLS[self.board[(x, y)]] for x in range(width + 1)) for y in range(height + 1))
        return f"{self.score}\n{board}\n"


def main() -> None:
    with open(INPUT, "r") as fin:
        program_data = [int(x) for x in fin.readline().split(",")]
    program_data[0] = 2
    program = Program(program_data)

    board = Board()
    for x, y, tile in zip(program, program, program):
        if x == -1:
            break
        board.set_tile(x, y, Tile(tile))
    print(board)

    while True:
        output = program.run_until_input()
        for x, y, val in zip(output, output, output):
            if x == -1 and y == 0:
                board.score = val
            else:
                board.set_tile(x, y, Tile(val))
        print(board)
        if program.ended:
            break
        program.send_input(board.next_move())
        program.next_command()
    print(board)


if __name__ == "__main__":
    main()
