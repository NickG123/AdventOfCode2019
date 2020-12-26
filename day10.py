from __future__ import annotations

import itertools

from dataclasses import dataclass
from math import atan2, degrees, gcd, pi
from typing import Iterable, List, Set

INPUT = "input"


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def blockers(self, other: Point) -> Iterable[Point]:
        dx = other.x - self.x
        dy = other.y - self.y
        div = gcd(dx, dy)
        ix = dx // div
        iy = dy // div

        for i in range(1, div):
            yield Point(self.x + ix * i, self.y + iy * i)


def vaporize(station: Point, asteroids: Set[Point]) -> Iterable[Point]:
    for other in asteroids:
        if not any(blocker in asteroids for blocker in station.blockers(other)):
            yield other


def sort_asteroids(station: Point, asteroids: Iterable[Point]) -> List[Point]:
    angles = [degrees((atan2(asteroid.y - station.y, asteroid.x - station.x) + pi / 2) % (2 * pi)) for asteroid in asteroids]
    return [asteroid for angle, asteroid in sorted(zip(angles, asteroids))]


def main() -> None:
    asteroids = set()
    with open(INPUT, "r") as fin:
        for y, line in enumerate(fin):
            for x, val in enumerate(line.strip()):
                if val == "#":
                    asteroids.add(Point(x, y))

    counts = [0] * len(asteroids)
    for i, asteroid in enumerate(asteroids):
        for j, other_asteroid in enumerate(itertools.islice(asteroids, i + 1, None)):
            if not any(blocker in asteroids for blocker in asteroid.blockers(other_asteroid)):
                counts[i] += 1
                counts[i + j + 1] += 1
    print(max(counts))
    station = next(itertools.islice(asteroids, counts.index(max(counts)), None))
    asteroids.remove(station)
    total_vaporized = 0
    while True:
        vaporized = set(vaporize(station, asteroids))
        if total_vaporized + len(vaporized) > 200:
            two_hundredth = sort_asteroids(station, vaporized)[200 - total_vaporized - 1]
            break
        else:
            total_vaporized += len(vaporized)
            asteroids -= vaporized
    print(two_hundredth.x * 100 + two_hundredth.y)


if __name__ == "__main__":
    main()
