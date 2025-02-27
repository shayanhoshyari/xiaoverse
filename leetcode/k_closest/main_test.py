# https://leetcode.com/problems/k-closest-points-to-origin

import pytest
import sys
import heapq


Point = tuple[int, int]


def make_item(point: Point) -> tuple[int, Point]:
    x, y = point
    return -(x * x + y * y), point


def kClosest(points: list[Point], k: int) -> list[Point]:
    items = list[(int, Point)]()
    for point in points:
        if len(items) < k:
            heapq.heappush(items, make_item(point))
            continue

        maybe_gone = heapq.heappop(items)
        item = make_item(point)
        keep = item if item[0] > maybe_gone[0] else maybe_gone
        heapq.heappush(items, keep)

    return [point for _, point in items]


@pytest.mark.timeout(3)
def test_queue() -> None:
    queue = list[tuple[int, str]]()
    heapq.heappush(queue, (12, "s"))
    heapq.heappush(queue, (13, "w"))
    heapq.heappush(queue, (11, "z"))

    assert heapq.heappop(queue) == (11, "z")
    assert heapq.heappop(queue) == (12, "s")
    assert heapq.heappop(queue) == (13, "w")


@pytest.mark.timeout(3)
def test_template() -> None:
    assert sorted(kClosest([(0, 0), (1, 1)], 1)) == sorted([(0, 0)])
    assert sorted(kClosest([(0, 0), (1, 1)], 2)) == sorted([(0, 0), (1, 1)])
    assert sorted(kClosest([(1, 1), (0, 0)], 1)) == sorted([(0, 0)])
    assert sorted(kClosest([(1, 3), (-2, 2)], 1)) == sorted([(-2, 2)])


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
