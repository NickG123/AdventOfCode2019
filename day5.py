from intcode_computer import run

INPUT = "input"


def main() -> None:
    with open(INPUT, "r") as fin:
        program = [int(x) for x in fin.readline().split(",")]
    print(run(program[:], [1]))
    print(run(program[:], [5]))


if __name__ == "__main__":
    main()
