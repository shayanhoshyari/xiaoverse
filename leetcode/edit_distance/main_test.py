# https://leetcode.com/problems/edit-distance/

# I messed up indexing e :(

import sys
from collections.abc import Iterable

import pytest

VERBOSE = False


def revrange(n: int) -> Iterable[int]:
    yield from reversed(range(n))


def print_matrix(e: list[list[int]], prefix: str = "") -> None:
    if not VERBOSE:
        return

    n2 = len(e)
    n1 = len(e[0])
    if prefix:
        print(prefix)
    print("[")
    for j in range(n2):
        for i in range(n1):
            print(e[j][i], end=" ")
        print()
    print("]")


def minDistance(word1: str, word2: str) -> int:
    print("[*]Compute")
    n1 = len(word1)
    n2 = len(word2)

    e = [[-1] * (n1 + 1) for _ in range(n2 + 1)]

    e[-1][-1] = 0

    # Start iteration
    print_matrix(e, "First matrx")

    for i in revrange(n1):
        e[-1][i] = e[-1][i + 1] + 1

    print_matrix(e, "Handled last row")

    for j in revrange(n2):
        e[j][-1] = e[j + 1][-1] + 1

    print_matrix(e, "Handled last column")

    for i in revrange(n1):
        for j in revrange(n2):
            print_matrix(e, f"Handling entry {i} {j}")
            offset = 0 if word1[i] == word2[j] else 1
            e[j][i] = min(
                e[j][i + 1] + 1,
                e[j + 1][i] + 1,
                e[j + 1][i + 1] + offset,
            )

    # Print
    print_matrix(e, "final result")

    return e[0][0]


@pytest.mark.timeout(3)
def test_cases_1() -> None:
    assert minDistance("", "") == 0
    assert minDistance("h", "") == 1
    assert minDistance("h", "o") == 1
    assert minDistance("", "o") == 1


@pytest.mark.timeout(3)
def test_cases_2() -> None:
    assert minDistance("horse", "ros") == 3


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
