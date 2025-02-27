# https://leetcode.com/problems/diameter-of-binary-tree

import pytest
import sys
import dataclasses


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


@dataclasses.dataclass(frozen=True)
class Analysis:
    depth_l: int
    depth_r: int
    diameter: int


def analyze(root: TreeNode | None) -> Analysis:
    if root is None:
        return Analysis(0, 0, 0)

    left = analyze(root.left)
    right = analyze(root.right)

    depth_l = max(left.depth_l, left.depth_r) + 1
    depth_r = max(right.depth_l, right.depth_r) + 1
    diameter = max(left.diameter, right.diameter, depth_l + depth_r - 2)

    return Analysis(depth_l, depth_r, diameter)


def diameter(root: TreeNode | None) -> int:
    return analyze(root).diameter


def test_diameter() -> None: ...


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
