INPUT = "input"


def compute_fuel(mass: int) -> int:
    return mass // 3 - 2


def main() -> None:
    part1_total = 0
    part2_total = 0
    with open(INPUT, "r") as fin:
        for line in fin:
            fuel = compute_fuel(int(line))
            part1_total += fuel
            while fuel >= 0:
                part2_total += fuel
                fuel = compute_fuel(fuel)

    print(part1_total)
    print(part2_total)


if __name__ == "__main__":
    main()
