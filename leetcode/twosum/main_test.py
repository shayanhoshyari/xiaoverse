import sys

import pytest


def twoSum(nums: list[int], target: int) -> list[int]:
    mapping = {}
    for i, value in enumerate(nums):
        # See if we have a friend already
        sibling_value = int(target - value)
        sibling = mapping.get(sibling_value)
        if sibling is not None:
            return [i, sibling]

        # Record for future
        mapping[int(value)] = i

    return []


def sortedTwoSum(nums: list[int], target: int) -> list[int]:
    return sorted(twoSum(nums, target))


def test_twosum() -> None:
    assert sortedTwoSum([0, 1], 1) == [0, 1]
    assert sortedTwoSum([12, 0, 1], 1) == [1, 2]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
