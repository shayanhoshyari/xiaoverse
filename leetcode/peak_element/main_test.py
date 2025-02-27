# https://leetcode.com/problems/find-peak-element

import pytest
import sys
import math


def get(values: list[int], idx: int) -> float:
    if idx < 0 or idx >= len(values):
        return -math.inf
    return values[idx]


def is_max(values: list[int], idx: int) -> bool:
    if get(values, idx) > get(values, idx - 1) and get(values, idx) > get(
        values, idx + 1
    ):
        return True
    return False


def _peak_element(values: list[int], beg: int, end: int) -> int:
    if is_max(values, beg):
        return beg

    if is_max(values, end):
        return end

    mid = (beg + end) // 2

    if is_max(values, mid):
        return mid

    if get(values, mid) > get(values, mid + 1):
        return _peak_element(values, mid, end)

    return _peak_element(values, beg, mid)


def peak_element(values: list[int]) -> int:
    return _peak_element(values, 0, len(values))


def test_peak_element() -> None:
    pass


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
