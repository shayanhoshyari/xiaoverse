# https://leetcode.com/problems/binary-search

import sys

import pytest


def search_impl(nums: list[int], target: int, beg: int, end: int) -> int:
    size = end - beg
    if size == 0:
        return -1
    if size == 1:
        return beg if nums[beg] == target else -1
    mid = (beg + end) // 2

    if target >= nums[mid]:
        return search_impl(nums, target, mid, end)
    else:
        return search_impl(nums, target, 0, mid)


def search(nums: list[int], target: int) -> int:
    return search_impl(nums, target, 0, len(nums))


def test_search() -> None:
    assert search([], 1) == -1
    assert search([1], 1) == 0
    assert search([1], 2) == -1

    assert search([1, 2], -1) == -1
    assert search([1, 2], 1) == 0
    assert search([1, 2], 2) == 1
    assert search([1, 2], 4) == -1

    assert search([1, 2, 3, 4], 4) == 3
    assert search([1, 2, 3, 4], 3) == 2
    assert search([1, 2, 3, 4], 2) == 1
    assert search([1, 2, 3, 4], 1) == 0


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
