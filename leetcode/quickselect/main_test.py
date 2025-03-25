# https://leetcode.com/problems/template

import random
import sys
from typing import Any

import pytest
import pytest_timeout  # noqa


def pivot(values: list[int], lo: int, hi: int, pivot_index: int | None = None) -> int:
    """
    Runs pivot on the values in the [lo hi) range.
    Will not do anything if hi - lo <= 1
    Returns the final index where the pivot ends up.
    """
    if hi <= lo + 1:
        return hi - 1

    # Pick a random pivot
    if pivot_index is None:
        pivot_index = random.randint(lo, hi - 1)

    pivot_value = values[pivot_index]
    tracker = lo

    # First pass - people who are smaller than pivot
    for i in range(lo, hi):
        if values[i] < pivot_value:
            values[tracker], values[i] = values[i], values[tracker]
            tracker += 1

    # Second pass, add the pivot values themselves
    for i in range(tracker, hi):
        if values[i] == pivot_value:
            values[tracker], values[i] = values[i], values[tracker]
            tracker += 1

    return tracker - 1


def _quickselect_impl(values: list[int], lo: int, hi: int, k: int) -> int:
    mid = pivot(values, lo, hi)
    n_right = hi - mid  # including mid

    if n_right == k:
        # We found the exact value we were looking for.
        return values[mid]

    if n_right > k:
        # Look in right side
        return _quickselect_impl(values, mid + 1, hi, k)

    # Look in left side
    return _quickselect_impl(values, lo, mid, k - n_right)


def quickselect(values: list[int], k: int) -> int:
    """
    Returns the k-th largest value in an array. It does not deal with
    duplication, so if the input is [1,2,2,3,3,3, 5] and k=4, returns 3.
    """
    return _quickselect_impl(values, 0, len(values), k)


@pytest.mark.timeout(3)
def test_pivot() -> None:
    def _pivot_test(values: list[int], pivot_index: int) -> list[int]:
        values = values.copy()
        pivot(values, 0, len(values), pivot_index)
        return values

    assert _pivot_test([1, 2, 3, 4], 3) == [1, 2, 3, 4]
    assert _pivot_test([4, 3, 2, 1], 3) == [1, 3, 2, 4]

    # Try non last pivot.
    assert _pivot_test([4, 3, 2, 1], 2) == [1, 2, 3, 4]


@pytest.mark.timeout(3)
def test_quickselect() -> None:
    assert quickselect([1, 2, 3, 4], 2) == 3
    assert quickselect([1, 2, 3, 4], 4) == 1
    assert quickselect([2, 1, 4, 3], 4) == 1
    assert quickselect([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert quickselect([3, 2, 1, 5, 6, 4], 2) == 5


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
