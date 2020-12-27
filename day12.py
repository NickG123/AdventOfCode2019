from __future__ import annotations

import itertools

from math import lcm
from typing import Iterable, List, Optional, Tuple

INPUT = "input"


class Vector(Tuple[int, int, int]):
    def __new__(cls, x: int, y: int, z: int) -> Vector:
        return tuple.__new__(Vector, (x, y, z))

    @staticmethod
    def from_list(xyz: List[int]) -> Vector:
        x, y, z = xyz
        return Vector(x, y, z)

    def __add__(self, other: Vector) -> Vector:
        return Vector(*(a + b for a, b in zip(self, other)))


class Moon:
    def __init__(self, position: Vector) -> None:
        self.position = position
        self.initial_position = position
        self.velocity = Vector(0, 0, 0)

    def compute_velocity(self, moons: List[Moon]) -> None:
        new_vector = []
        for i in range(3):
            new_vector.append(sum(compute_1d_velocity(self.position[i], moon.position[i]) for moon in moons))
        self.velocity += Vector.from_list(new_vector)

    def move(self) -> None:
        self.position += self.velocity

    def energy(self) -> int:
        pot = sum(abs(x) for x in self.position)
        kin = sum(abs(x) for x in self.velocity)
        return pot * kin

    def reset(self) -> None:
        self.position = self.initial_position
        self.velocity = Vector(0, 0, 0)


def compute_1d_velocity(a: int, b: int) -> int:
    diff = b - a
    return diff // abs(diff) if diff != 0 else 0


def read_moons() -> Iterable[Moon]:
    with open(INPUT, "r") as fin:
        for line in fin:
            assignments = line.strip("\n><").split(", ")
            yield Moon(Vector(*(int(assignment.split("=")[-1]) for assignment in assignments)))


def print_moons(moons: List[Moon]) -> None:
    for moon in moons:
        print(moon.position, moon.velocity)


def step(moons: List[Moon]) -> None:
    for moon in moons:
        moon.compute_velocity(moons)

    for moon in moons:
        moon.move()


def main() -> None:
    moons = list(read_moons())
    for _ in range(1000):
        step(moons)
    print(sum(moon.energy() for moon in moons))

    for moon in moons:
        moon.reset()

    cycles: List[Optional[int]] = [None] * 3
    for step_num in itertools.count(1):
        step(moons)
        for i, cycle in enumerate(cycles):
            if cycle is None:
                for moon in moons:
                    if moon.position[i] != moon.initial_position[i]:
                        break
                else:
                    cycles[i] = step_num + 1
        if not any(cycle is None for cycle in cycles):
            print(lcm(*cycles))
            break


if __name__ == "__main__":
    main()
