from __future__ import annotations
from collections import defaultdict
from typing import Dict, List

INPUT = "input"


def get_ancestor_tree(parents: Dict[str, str], node: str) -> List[str]:
    ancestor_tree = []
    while node in parents:
        node = parents[node]
        ancestor_tree.append(node)
    return ancestor_tree[::-1]


def get_transfers(source: str, dest: str, parents: Dict[str, str]) -> int:
    src_ancestor_tree = get_ancestor_tree(parents, source)
    dest_ancestor_tree = get_ancestor_tree(parents, dest)
    for i, (a, b) in enumerate(zip(get_ancestor_tree(parents, source), get_ancestor_tree(parents, dest))):
        if a != b:
            break
    return len(src_ancestor_tree) - i + len(dest_ancestor_tree) - i


def main() -> None:
    orbits = defaultdict(list)
    parents = {}
    with open(INPUT, "r") as fin:
        for line in fin:
            target, orbiting = line.strip().split(")")
            orbits[target].append(orbiting)
            parents[orbiting] = target

    nodes = ["COM"]
    total_orbits = 0
    depth = 0
    while nodes:
        total_orbits += depth * len(nodes)
        nodes = [orbiting for node in nodes for orbiting in orbits[node]]
        depth += 1

    print(total_orbits)
    print(get_transfers("YOU", "SAN", parents))


if __name__ == "__main__":
    main()
