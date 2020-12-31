from intcode_computer import Program
from itertools import chain
from typing import Set

INPUT = "input"


def main() -> None:
    with open(INPUT, "r") as fin:
        program_data = [int(x) for x in fin.readline().strip().split(",")]

    part1 = False

    computers = [Program(program_data[:], [i]) for i in range(50)]
    last_nat = None
    nat_history: Set[int] = set()
    while True:
        idle = True
        for computer in computers:
            computer.send_input(-1)
            output = chain(computer.consume_all_input(), computer.run_until_input())
            for address, x, y in zip(output, output, output):
                if address == 255:
                    if not part1:
                        print(y)
                        part1 = True
                    last_nat = (x, y)
                else:
                    computers[address].send_input(x)
                    computers[address].send_input(y)
                idle = False
        if idle:
            assert last_nat is not None
            x, y = last_nat
            if y in nat_history:
                print(y)
                break
            nat_history.add(y)
            computers[0].send_input(x)
            computers[0].send_input(y)


if __name__ == "__main__":
    main()
