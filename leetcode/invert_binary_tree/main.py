# https://leetcode.com/problems/invert-binary-tree

from __future__ import annotations

import pytest
import sys
from collections import deque

def eq(r: TreeNode | None, l : TreeNode | None) -> bool:
    if r is None and l is None:
        return True
    if r is None or l is None:
        return False
    return r.val == l.val and eq(l.left, r.left) and eq(l.right, r.right)

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert_tree(root : TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    return TreeNode(
        val = root.val,
        left = invert_tree(root.right),
        right = invert_tree(root.left),
    )

def vec2tree(values : list[int]) -> TreeNode | None:
    if not values:
        return None

    def init_node(depth: int, row : int) -> TreeNode | None:
        idx = (2**depth) + row 
        if idx >= len(values):
            return None
        if values[idx] is None:
            return None

        return TreeNode(
            values[idx],
            init_node(depth+1, row),
            init_node(depth+1, row+1),
        )

    return init_node(0, 0)

def tree2vec(root : TreeNode | None) -> list[int]:
    # FIXME
    return []

def test_template() -> None: ...


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
