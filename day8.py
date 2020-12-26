from collections import Counter
from enum import Enum
from typing import Iterable, List, TextIO

INPUT = "input"
WIDTH = 25
HEIGHT = 6


class Pixel(Enum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2


def read_frames(fin: TextIO) -> Iterable[List[int]]:
    frame_size = WIDTH * HEIGHT
    line = [int(c) for c in fin.readline()]

    for i in range(0, len(line), frame_size):
        yield line[i:i + frame_size]


def merge_image(dest: List[Pixel], src: List[Pixel]) -> None:
    for i, (d, s) in enumerate(zip(dest, src)):
        if d == Pixel.TRANSPARENT:
            dest[i] = s


def display_image(image: List[Pixel]) -> None:
    for i in range(0, len(image), WIDTH):
        print("".join("X" if x == Pixel.WHITE else " " for x in image[i:i + WIDTH]))


def main() -> None:
    with open(INPUT, "r") as fin:
        min_0_frame = None
        image = [Pixel.TRANSPARENT] * (WIDTH * HEIGHT)
        for frame in read_frames(fin):
            frame_counts = Counter(frame)
            layer = [Pixel(i) for i in frame]
            merge_image(image, layer)
            if min_0_frame is None or min_0_frame.get(0, 0) > frame_counts.get(0, 0):
                min_0_frame = frame_counts
        print(min_0_frame.get(1, 0) * min_0_frame.get(2, 0))
        print()
        display_image(image)


if __name__ == "__main__":
    main()
