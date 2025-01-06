# https://leetcode.com/problems/merge-sorted-array

import pytest
import sys


class Subarray:
    def __init__(self, storage: list[int], beg: int, end: int) -> None:
        self.storage = storage
        self.beg = beg
        self.end = end

    def get(self, index: int) -> int:
        return self.storage[self.beg + index]

    def set(self, index: int, value: int) -> None:
        self.storage[self.beg + index] = value

    def size(self) -> int:
        return self.end - self.beg

    def max_size(self) -> int:
        return len(self.storage) - self.beg

    def repr(self) -> str:
        return f"beg={self.beg}, end={self.end}, values=" + str(
            self.storage[self.beg : self.end]
        )


def pprint(*args):
    print(*args)


def merge(
    nums1: Subarray,
    nums2: Subarray,
) -> None:
    pprint("[*] merge\n", nums1.repr(), "\n", nums2.repr())
    # Input assumptions
    assert nums1.max_size() >= nums1.size() + nums2.size()
    assert nums2.size() == nums2.max_size()

    # 1 is finished, put 2 inside it
    if nums1.size() == 0:
        pprint("Case 1: 1 is empty")
        for index in range(nums2.size()):
            nums1.set(index, nums2.get(index))
        return

    # 2 is finished, nothing to do.
    if nums2.size() == 0:
        pprint("Case 2: 2 is empty\n")
        return

    # First array has smaller value
    if nums1.get(0) <= nums2.get(0):
        pprint("Case 3: 1 has the smaller member")
        merge(Subarray(nums1.storage, nums1.beg + 1, nums1.end), nums2)
        return

    pprint("Case 4: 2 has smaller member")

    # Second array has smaller value
    # Find first value that is bigger
    nums2_shift = nums2.size()
    for index in range(nums2.size()):
        value = nums2.get(index)
        if value > nums1.get(0):
            pprint(f"Detected index {index} because {value} > {nums1.get(0)}")
            nums2_shift = index
            break

    # First do the merge
    if nums2_shift != nums2.size():
        merge(nums1, Subarray(nums2.storage, nums2.beg + nums2_shift, nums2.end))

    upper_end = nums1.end + nums2.size() - nums2_shift
    # Shift upper according to uppershift
    nums1.storage[nums1.beg + nums2_shift : upper_end + nums2_shift] = nums1.storage[
        nums1.beg : upper_end
    ]
    # Copy the lower to the openned area.
    nums1.storage[nums1.beg : nums1.beg + nums2_shift] = nums2.storage[
        nums2.beg : nums2.beg + nums2_shift
    ]

    pprint("Merged so far: ", nums2.storage)


def merge_simple(x: list[int], y: list[int]) -> list[int]:
    x_extended = x + [0] * len(y)
    merge(
        Subarray(x_extended, 0, len(x)),
        Subarray(y, 0, len(y)),
    )
    return x_extended


def test_merge_a() -> None:
    assert merge_simple([], []) == []
    assert merge_simple([1], []) == [1]
    assert merge_simple([], [1]) == [1]
    assert merge_simple([1], [1]) == [1, 1]
    assert merge_simple([1], [2]) == [1, 2]
    assert merge_simple([2], [1]) == [1, 2]
    assert merge_simple([2, 3], [1, 4]) == [1, 2, 3, 4]
    assert merge_simple([20, 20, 30], [10, 11, 40]) == [10, 11, 20, 20, 30, 40]


def test_merge_b() -> None:
    assert merge_simple(
        [0, 0, 3],
        [-1, 1, 1, 1, 2, 3],
    ) == [-1, 0, 0, 1, 1, 1, 2, 3, 3]


def test_merge_c() -> None:
    assert merge_simple(
        [0, 2],
        [-1, 1, 1, 2, 2, 3],
    ) == [-1, 0, 1, 1, 2, 2, 2, 3]


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
