from typing import Iterable

MIN_NUM = 246540
MAX_NUM = 787419


def run_length_encode(s: str) -> Iterable[int]:
    cur_char = None
    cur_count = 0
    for c in s:
        if c == cur_char:
            cur_count += 1
        else:
            if cur_count > 0:
                yield cur_count
            cur_count = 1
            cur_char = c
    if cur_count > 0:
        yield cur_count


def test_number(num: int, exact_length: bool) -> bool:
    num_str = str(num)

    # adjacent digits
    rle = run_length_encode(num_str)
    if (exact_length) and 2 not in rle:
        return False
    elif not exact_length and not any(x > 1 for x in rle):
        return False

    # incrementing digits
    for c1, c2 in zip(num_str, num_str[1:]):
        if c1 > c2:
            return False

    return True


def main() -> None:
    print(sum(test_number(i, False) for i in range(MIN_NUM, MAX_NUM + 1)))
    print(sum(test_number(i, True) for i in range(MIN_NUM, MAX_NUM + 1)))


if __name__ == "__main__":
    main()
