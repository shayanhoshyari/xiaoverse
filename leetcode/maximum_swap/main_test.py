# https://leetcode.com/problems/maximum-swap

import sys

import pytest


def get_digits(value: int) -> list[int]:
    digits = list[int]()
    while value:
        digits.append(value % 10)
        value = value // 10
    return list(reversed(digits))


def stitch(digits: list[int]) -> int:
    result = 0
    for digit in digits:
        result = result * 10 + digit
    return result


def swap(values: list[int], x: int, y: int) -> None:
    values[x], values[y] = values[y], values[x]


def get_rightmost_location(values: list[int]) -> dict[int, int]:
    result = dict[int, int]()
    for idx, value in enumerate(values):
        result[value] = max(idx, result.get(value, -1))
    return result


def maximum_swap(value: int) -> int:
    digits = get_digits(value)
    digit2loc = get_rightmost_location(digits)
    large_digits = sorted(digits, reverse=True)

    # Find the swap
    swap: tuple[int, int] | None = None
    for idx, large_digit in enumerate(large_digits):
        digit = digits[idx]
        if digit != large_digit:
            swap = (digit2loc[large_digit], idx)
            break

    if swap is None:
        return value

    digits[swap[0]], digits[swap[1]] = digits[swap[1]], digits[swap[0]]
    return stitch(digits)


def test_get_digits() -> None:
    assert get_digits(12) == [1, 2]
    assert get_digits(0) == []
    assert get_digits(1) == [1]


def test_stich() -> None:
    assert stitch([1, 2]) == 12


def test_get_rightmost_location() -> None:
    assert get_rightmost_location([1, 1]) == {1: 1}
    assert get_rightmost_location([1, 1, 1]) == {1: 2}
    assert get_rightmost_location([1, 1, 1, 3]) == {1: 2, 3: 3}


def test_swap() -> None:
    x = [1, 2, 3]
    swap(x, 0, 2)
    assert x == [3, 2, 1]


def test_maximum_swap() -> None:
    assert maximum_swap(12) == 21
    assert maximum_swap(321) == 321
    assert maximum_swap(312) == 321
    assert maximum_swap(4312) == 4321
    assert maximum_swap(3124) == 4123
    assert maximum_swap(1993) == 9913
    assert maximum_swap(98368) == 98863


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
