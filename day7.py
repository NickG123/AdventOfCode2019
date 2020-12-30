import itertools
from intcode_computer import run, Program

INPUT = "input"


def main() -> None:
    with open(INPUT, "r") as fin:
        program = [int(x) for x in fin.readline().strip().split(",")]

    max_output = None
    for order in itertools.permutations(range(5)):
        signal = 0
        for phase_setting in order:
            result = run(program[:], [phase_setting, signal])
            if result is None:
                raise Exception("No return value")
            signal = result
        max_output = signal if max_output is None else max(signal, max_output)
    print(max_output)

    max_output = None
    for order in itertools.permutations(range(5, 10)):
        signal = 0
        current_amplifier = 0
        amplifiers = []
        for phase_setting in order:
            p = Program(program[:], [phase_setting])
            amplifiers.append(p)

        while True:
            amplifiers[current_amplifier].send_input(signal)
            new_signal = amplifiers[current_amplifier].next_output_or_end()
            if new_signal is None:
                break
            signal = new_signal
            current_amplifier = (current_amplifier + 1) % len(amplifiers)
        max_output = signal if max_output is None else max(signal, max_output)
    print(max_output)


if __name__ == "__main__":
    main()
