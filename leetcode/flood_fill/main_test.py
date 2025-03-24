# https://leetcode.com/problems/flood-fill

import sys
from collections import deque
from collections.abc import Iterable

import pytest

Point = tuple[int, int]


def iter_neighs(p: Point, num_row: int, num_col: int) -> Iterable[Point]:
    r, c = p
    if r > 0:
        yield r - 1, c
    if c > 0:
        yield r, c - 1
    if c < num_col - 1:
        yield r, c + 1
    if r < num_row - 1:
        yield r + 1, c


def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    if color == image[sr][sc]:
        return image

    src_color = image[sr][sc]
    stack = deque([(sr, sc)])
    while stack:
        r, c = stack.pop()
        # print("[*] target ", (r, c), " = ", image[r][c])
        image[r][c] = color
        # print("image now is ", image)
        for nr, nc in iter_neighs((r, c), len(image), len(image[0])):
            # print("nei", (nr, nc), "=", image[nr][nc])
            if image[nr][nc] == src_color:
                # print("neighbour added to stack")
                stack.appendleft((nr, nc))
    return image


def test_iter() -> None:
    def get_nei(i, j, ni, nj):
        return set(iter_neighs((i, j), ni, nj))

    assert get_nei(0, 0, 1, 1) == set([])
    assert get_nei(0, 0, 2, 2) == set([(0, 1), (1, 0)])
    assert get_nei(1, 0, 2, 2) == set([(0, 0), (1, 1)])
    assert get_nei(0, 1, 2, 2) == set([(0, 0), (1, 1)])
    assert get_nei(1, 1, 2, 2) == set([(1, 0), (0, 1)])


@pytest.mark.timeout(3)
def test_template() -> None:
    assert flood_fill([[0, 0], [0, 0]], 0, 0, 1) == [[1, 1], [1, 1]]
    assert flood_fill([[0, 0], [2, 2]], 0, 0, 1) == [[1, 1], [2, 2]]
    assert flood_fill([[0, 0], [2, 2]], 0, 0, 0) == [[0, 0], [2, 2]]


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
