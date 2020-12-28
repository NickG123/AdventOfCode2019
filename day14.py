from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from math import ceil
from typing import Dict, List, Iterable, Tuple

INPUT = "input"


@dataclass(frozen=True)
class Chemical:
    amount: int
    name: str

    @staticmethod
    def from_string(s: str) -> Chemical:
        amount, name = s.split(" ")
        return Chemical(int(amount), name)


@dataclass(frozen=True)
class Reaction:
    inputs: List[Chemical]
    output: Chemical

    @staticmethod
    def from_string(s: str) -> Reaction:
        inputs, output = s.split(" => ")
        return Reaction([Chemical.from_string(c) for c in inputs.split(", ")], Chemical.from_string(output))


def read_reactions() -> Iterable[Reaction]:
    with open(INPUT, "r") as fin:
        for line in fin:
            yield Reaction.from_string(line.strip())


def run_reactions(reactions_by_output: Dict[str, Reaction], requirements: Dict[str, int], reverse: bool = False) -> Tuple[int, Dict[str, int]]:
    ore_required = 0
    extra_resources: Dict[str, int] = defaultdict(int)

    while requirements:
        requirement, amount = requirements.popitem()

        if not reverse:
            existing_extra = extra_resources[requirement]
            if existing_extra != 0:
                if amount > existing_extra:
                    amount -= existing_extra
                    extra_resources[requirement] = 0
                else:
                    extra_resources[requirement] -= amount
                    continue

        reaction = reactions_by_output[requirement]
        if reverse:
            reactions_needed, extra = divmod(amount, reaction.output.amount)
        else:
            reactions_needed = ceil(amount / reaction.output.amount)
            extra = reaction.output.amount * reactions_needed - amount

        if extra != 0:
            extra_resources[requirement] += extra

        for chem in reaction.inputs:
            required_amount = chem.amount * reactions_needed
            if chem.name == "ORE":
                ore_required += required_amount
            else:
                requirements[chem.name] += required_amount
    return ore_required, extra_resources


def main() -> None:
    reactions_by_output = {r.output.name: r for r in read_reactions()}

    ore_required, extra_resources = run_reactions(reactions_by_output, defaultdict(int, {"FUEL": 1}))
    print(ore_required)

    ore_available = 1000000000000
    total_reactions = 0
    leftover_resources: Dict[str, int] = defaultdict(int)

    while True:
        possible_reactions, ore_leftover = divmod(ore_available, ore_required)
        total_reactions += possible_reactions

        for name, count in extra_resources.items():
            leftover_resources[name] += count * possible_reactions

        ore_available, leftover_resources = run_reactions(reactions_by_output, defaultdict(int, leftover_resources), reverse=True)
        if ore_available == 0:
            break
        ore_available += ore_leftover

    print(total_reactions)


if __name__ == "__main__":
    main()
