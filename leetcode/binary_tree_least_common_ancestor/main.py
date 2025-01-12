# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

"""
Given a binary search tree (BST), find the lowest common ancestor (LCA)
node of two given nodes in the BST.

According to the definition of LCA on Wikipedia:
“The lowest common ancestor is defined between two nodes p and q as the lowest node
 in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”
"""

import pytest
import sys
import dataclasses


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# ==== [Solution 1]
# This solution is not taking advantage that this is a binary search tree!
# Runtime is O(N)


@dataclasses.dataclass
class Analysis:
    p_reachable: bool
    q_reachable: bool
    lowest_ancestor: TreeNode | None


def analyze(root: TreeNode, p: TreeNode, q: TreeNode) -> Analysis:
    if root is None:
        return Analysis(False, False, None)

    left = analyze(root.left, p, q)
    right = analyze(root.right, p, q)

    p_reachable = left.p_reachable or right.p_reachable or root == p
    q_reachable = left.q_reachable or right.q_reachable or root == q
    lowest_ancestor = right.lowest_ancestor or left.lowest_ancestor
    if p_reachable and q_reachable and lowest_ancestor is None:
        lowest_ancestor = root

    return Analysis(
        p_reachable=p_reachable,
        q_reachable=q_reachable,
        lowest_ancestor=lowest_ancestor,
    )


def last_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    if p == q:
        return p

    result = analyze(root, p, q).lowest_ancestor
    assert result is not None

    return result


# ==== [Take advantage of the binary search tree]
# Runtime is O(logN)


def last_common_ancestor2(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    def is_common(node: TreeNode | None) -> bool:
        if node is None:
            return False
        return p.val <= node.val < q.val

    candidate = root

    while True:
        if is_common(candidate.left):
            candidate = candidate.left
        elif is_common(candidate.right):
            candidate = candidate.right
        else:
            return candidate


def test_template() -> None:
    pass


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
