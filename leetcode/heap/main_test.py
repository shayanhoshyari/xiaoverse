"""
Heaps

Reference: https://web.stanford.edu/class/archive/cs/cs161/cs161.1168/lecture4.pdf

Left child: 2 * i + 1
Right child: 2 * i + 2
Parent: (i + 1) // 2 - 1

Reason:
  num(d, r) = 2^(d-1) + r
  left(d, r) = (d+1, 2*r)
  right(d, r) = (d+1, 2*r + 1)

Here we assume we are working with a min heap
"""

import random
import sys

import pytest


def is_heap(heap: list[int]) -> bool:
    n = len(heap)
    for idx in range(n // 2):
        left = idx * 2 + 1
        right = idx * 2 + 2
        if heap[left] < heap[idx]:
            return False
        if right < n and heap[right] < heap[idx]:
            return False
    return True


def heapify(heap: list[int], idx: int) -> None:
    n = len(heap)
    if idx >= n // 2:
        # It is a leaf
        return

    left = idx * 2 + 1
    right = idx * 2 + 2

    if heap[idx] <= heap[left] and (right == n or heap[idx] <= heap[right]):
        # All good.
        return

    if right == len(heap) or heap[right] >= heap[left]:
        min_idx = left
    else:
        min_idx = right

    heap[idx], heap[min_idx] = heap[min_idx], heap[idx]
    # sprint(f"DEBUG: idx {idx}, l={left}, r={right}, min_idx={min_idx}")
    heapify(heap, min_idx)

    return heap


def heappop(heap: list[int]) -> int:
    head = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    if heap:
        heapify(heap, 0)
    return head


def heap_sort(values: list[int]) -> list[int]:
    values = values.copy()
    n = len(values)
    for idx in reversed(range(n // 2)):
        heapify(values, idx)

    result = list[int]()
    while values:
        result.append(heappop(values))
    return result


@pytest.mark.timeout(3)
def test_is_heap() -> None:
    assert is_heap([1, 2, 3])
    assert not is_heap([2, 1, 3])
    assert is_heap([1, 1, 3])
    assert is_heap([1, 1, 3, 4, 5])


@pytest.mark.timeout(3)
def test_heapify() -> None:
    assert heapify([3, 1, 2], 0) == [1, 3, 2]
    assert heapify([10, 1, 2, 5, 7], 0) == [1, 5, 2, 10, 7]


@pytest.mark.timeout(3)
def test_heappop() -> None:
    x = [1, 2, 3]
    assert heappop(x) == 1
    assert x == [2, 3]

    x = [1, 5, 2, 10, 7]
    #
    assert heappop(x) == 1
    assert x == [2, 5, 7, 10]
    #
    assert heappop(x) == 2
    assert x == [5, 10, 7]
    #
    assert heappop(x) == 5
    assert x == [7, 10]
    #
    assert heappop(x) == 7
    assert x == [10]
    #
    assert heappop(x) == 10
    assert x == []


@pytest.mark.timeout(3)
def test_heapsort() -> None:
    assert heap_sort([2, 1]) == [1, 2]
    assert heap_sort([1, 2]) == [1, 2]
    assert heap_sort([1]) == [1]
    assert heap_sort([]) == []

    for _ in range(100):
        x = [random.randint(0, 100) for _ in range(10)]
        assert heap_sort(x) == sorted(x)


if __name__ == "__main__":
    sys.exit(pytest.main(["-svv", __file__]))
