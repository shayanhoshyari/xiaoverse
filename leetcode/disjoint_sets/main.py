# Union find, or Disjoint sets

import pytest
import sys
from typing import Any

class DisjointSet:
    def __init__(self, size : int) -> None:
        """Initialize the disjoint set with a given size."""
        self.parent = [i for i in range(size)]  # Each element is its own parent initially
        self.rank = [0] * size  # Rank is used for union by rank

    def find(self, x : int) -> int:
        """Find the representative of the set containing x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x : int, y : int) -> None:
        """Union the sets containing x and y using union by rank."""
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return
        
        if self.rank[x] == self.rank[y]:
            # eqaul rank, merge and increment.
            self.parent[y] = x
            self.rank[x] += 1
        elif self.rank[x] > self.rank[y]:
            # the one with larger rank becomes parent.
            self.parent[y] = x
        else:
            self.parent[x] = y

    def connected(self, x : int, y : int) -> None:
        """Check if x and y are in the same set."""
        return self.find(x) == self.find(y)



@pytest.mark.timeout(3)
def test_disjoint_tests_1() -> None:
    s = DisjointSet(4)
    s.union(0, 1)
    assert s.connected(0, 1)
    assert not s.connected(0, 2)
    assert not s.connected(0, 3)
    assert not s.connected(2, 3)

    s.union(2, 3)
    assert s.connected(0, 1)
    assert not s.connected(0, 2)
    assert not s.connected(0, 3)
    assert s.connected(2, 3)

    s.union(1, 2)
    assert s.connected(0, 1)
    assert s.connected(0, 2)
    assert s.connected(0, 3)
    assert s.connected(2, 3)


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
