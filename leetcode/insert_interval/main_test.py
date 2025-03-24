# https://leetcode.com/problems/insert-interval/description/

import sys

import pytest

Interval = tuple[int, int]


def is_overlapping(x: Interval, y: Interval) -> bool:
    return (
        y[0] <= x[0] <= y[1]
        or y[0] <= x[1] <= y[1]
        or x[0] <= y[1] <= x[1]
        or x[0] <= y[1] <= x[1]
    )


def insert(intervals: list[Interval], newInterval: Interval) -> list[Interval]:
    if not intervals:
        return [newInterval]

    if newInterval[1] < intervals[0][0]:
        return [newInterval] + intervals

    if newInterval[0] > intervals[-1][1]:
        return intervals + [newInterval]

    min_value, max_value = newInterval
    remove = list[int]()
    for idx, interval in enumerate(intervals):
        if is_overlapping(interval, newInterval):
            remove.append(idx)
            min_value = min(min_value, interval[0])
            max_value = max(max_value, interval[1])

    if remove:
        beg = remove[0]
        end = remove[-1] + 1
    else:
        for idx, interval in enumerate(intervals):
            if newInterval[0] > interval[1]:
                beg = idx + 1
                end = idx + 1

    return intervals[:beg] + [(min_value, max_value)] + intervals[end:]


@pytest.mark.timeout(3)
def test_insert() -> None:
    assert insert([], (0, 1)) == [(0, 1)]
    assert insert([(0, 1)], (0, 1)) == [(0, 1)]
    assert insert([(0, 2)], (0, 1)) == [(0, 2)]
    assert insert([(0, 2), (3, 4)], (-1, 1)) == [(-1, 2), (3, 4)]
    assert insert([(-2, -1), (0, 2), (3, 4)], (-1, 1)) == [(-2, 2), (3, 4)]
    assert insert([(1, 5)], (2, 3)) == [(1, 5)]
    assert insert([(3, 5), (12, 15)], (6, 6)) == [(3, 5), (6, 6), (12, 15)]


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
