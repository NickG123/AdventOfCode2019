from __future__ import annotations
from typing import Iterable

INPUT = "input"


class Deck:
    def __init__(self, num_cards: int) -> None:
        self.cards = list(range(num_cards))

    def deal_into(self) -> None:
        self.cards = list(reversed(self.cards))

    def cut(self, n: int) -> None:
        self.cards = self.cards[n:] + self.cards[:n]

    def deal_with_increment(self, n: int) -> None:
        cards = [0] * len(self.cards)
        for i, card in enumerate(self.cards):
            cards[(i * n) % len(cards)] = card
        self.cards = cards

    def __str__(self) -> str:
        return ", ".join(str(x) for x in self.cards)


def run(deck: Deck, instructions: Iterable[str]) -> None:
    for instruction in instructions:
        command, param = instruction.rsplit(" ", 1)
        if command == "deal with increment":
            deck.deal_with_increment(int(param))
        elif command == "deal into new":
            deck.deal_into()
        else:
            deck.cut(int(param))


def part_2(instructions: Iterable[str], num_cards: int, shuffle_count: int, output_slot: int) -> int:
    # Gave up and stole a really cool solution from mcpower_ on reddit
    offset = 0
    increment = 1
    for instruction in instructions:
        command, param = instruction.rsplit(" ", 1)
        if command == "deal with increment":
            increment = (increment * pow(int(param), num_cards - 2, num_cards)) % num_cards
        elif command == "deal into new":
            increment *= -1
            offset = (offset + increment) % num_cards
        else:
            offset = (offset + increment * int(param)) % num_cards

    final_increment = pow(increment, shuffle_count, num_cards)
    final_offset = offset * (1 - pow(increment, shuffle_count, num_cards)) * pow(1 - increment, num_cards - 2, num_cards)
    return (final_offset + final_increment * output_slot) % num_cards


def main() -> None:
    deck = Deck(10007)
    with open(INPUT, "r") as fin:
        instructions = [line.strip() for line in fin]
    run(deck, instructions)
    print(deck.cards.index(2019))
    print(part_2(instructions, 119315717514047, 101741582076661, 2020))


if __name__ == "__main__":
    main()
