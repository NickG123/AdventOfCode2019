from itertools import chain, cycle, islice, repeat
from typing import Iterator, List

INPUT = "input"


def repeating_pattern(base_pattern: List[int], repeat_count: int) -> Iterator[int]:
    return cycle(chain(*(repeat(n, repeat_count) for n in base_pattern)))


def run_phase(input: List[int], base_pattern: List[int]) -> List[int]:
    return [abs(sum(i * p for i, p in zip(input, islice(repeating_pattern(base_pattern, offset + 1), 1, None)))) % 10 for offset in range(len(input))]


def part_one(signal: List[int], base_pattern: List[int]) -> str:
    for i in range(100):
        signal = run_phase(signal, base_pattern)
    return "".join(str(i) for i in signal)[:8]


def part_two(signal: List[int]) -> str:
    start_point = int("".join(str(i) for i in signal[:7]))
    section = list(islice(cycle(signal), start_point, 10000 * len(signal)))

    for i in range(100):
        new_section = []
        total = 0
        for elem in reversed(section):
            total += elem
            new_section.append(abs(total) % 10)
        section = list(reversed(new_section))
    return "".join(str(c) for c in section[:8])


def main() -> None:
    base_pattern = [0, 1, 0, -1]

    with open(INPUT, "r") as fin:
        signal = [int(c) for c in fin.readline().strip()]

    print(part_one(signal, base_pattern))
    print(part_two(signal))


if __name__ == "__main__":
    main()
