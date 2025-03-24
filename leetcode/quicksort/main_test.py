"""
We are sorting big -> small.
"""

import random
import sys

import pytest


def pivot(values: list[int], lo: int, hi: int, pv: int) -> int:
    """
    Pivots in place.
    Returns the index of pivot in the end.
    """
    threshold = values[pv]
    tracker = lo
    for i in range(lo, hi):
        if values[i] < threshold:
            values[tracker], values[i] = values[i], values[tracker]
            tracker += 1

    values[tracker], values[i] = values[i], values[tracker]
    # Return it for sake of tests.
    return tracker


def quick_sort(values: list[int], lo: int, hi: int) -> None:
    """
    In place.
    """
    print(f"lo={lo} high={hi}")
    if hi - lo <= 1:
        # All good.
        return

    idx = pivot(values, lo, hi, pv=hi - 1)
    quick_sort(values, lo, idx)
    quick_sort(values, idx + 1, hi)


@pytest.mark.timeout(3)
def test_pivot() -> None:
    def _pivot(values: list[int]) -> tuple[list[int], int]:
        loc = pivot(values, 0, len(values), pv=len(values) - 1)
        return values, loc

    assert _pivot([1, 2, 3, 4]) == ([1, 2, 3, 4], 3)
    assert _pivot([1, 2, 4, 3]) == ([1, 2, 3, 4], 2)
    assert _pivot([1, 3]) == ([1, 3], 1)
    assert _pivot([3, 1]) == ([1, 3], 0)


@pytest.mark.timeout(3)
def test_quicksort() -> None:
    def _qsort_incr(values: list[int]) -> list[int]:
        print(f"Qsort, values={values}")
        quick_sort(values, 0, len(values))
        return values

    assert _qsort_incr([1, 2]) == [1, 2]
    assert _qsort_incr([2, 1]) == [1, 2]
    assert _qsort_incr([1]) == [1]
    assert _qsort_incr([]) == []

    for _ in range(100):
        x = [random.randint(0, 100) for _ in range(10)]
        assert _qsort_incr(x) == sorted(x)


if __name__ == "__main__":
    sys.exit(pytest.main(["-svv", __file__]))
