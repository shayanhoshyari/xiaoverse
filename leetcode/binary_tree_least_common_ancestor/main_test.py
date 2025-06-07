# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

"""
Given a binary search tree (BST), find the lowest common ancestor (LCA)
node of two given nodes in the BST.

According to the definition of LCA on Wikipedia:
“The lowest common ancestor is defined between two nodes p and q as the lowest node
 in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”
"""

import dataclasses
import sys

import pytest
import pytest_timeout  # noqa: F401


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def build_bst() -> tuple[TreeNode, dict[int, TreeNode]]:
    """Create a small binary search tree used in tests.

    Returns the root node of the tree along with a mapping from node values
    to the ``TreeNode`` instances so tests can easily access arbitrary nodes.
    """

    nodes = {val: TreeNode(val) for val in [6, 2, 0, 4, 3, 5, 8, 7, 9]}

    nodes[6].left = nodes[2]
    nodes[6].right = nodes[8]

    nodes[2].left = nodes[0]
    nodes[2].right = nodes[4]

    nodes[4].left = nodes[3]
    nodes[4].right = nodes[5]

    nodes[8].left = nodes[7]
    nodes[8].right = nodes[9]

    return nodes[6], nodes


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
    if p.val > q.val:
        p, q = q, p

    candidate = root

    while candidate:
        if q.val < candidate.val:
            candidate = candidate.left
        elif p.val > candidate.val:
            candidate = candidate.right
        else:
            return candidate

    raise AssertionError("tree must contain p and q")


@pytest.mark.timeout(3)
@pytest.mark.parametrize(
    "p_val,q_val,expected",
    [
        (2, 8, 6),
        (2, 4, 2),
        (3, 5, 4),
        (0, 5, 2),
        (7, 9, 8),
        (4, 4, 4),
    ],
)
def test_last_common_ancestor(p_val: int, q_val: int, expected: int) -> None:
    root, nodes = build_bst()

    p = nodes[p_val]
    q = nodes[q_val]
    if p.val > q.val:
        p, q = q, p

    expected_node = nodes[expected]

    assert last_common_ancestor(root, p, q) is expected_node
    assert last_common_ancestor2(root, p, q) is expected_node


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
