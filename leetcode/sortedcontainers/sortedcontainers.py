# https://www.facebook.com/careers/life/sample_interview_questions
# Spiral array

import pytest
import sys
from sortedcontainers import SortedList, SortedDict


@pytest.mark.timeout(3)
def test_sorted_list() -> None:
    c = SortedList([1, 10, 12])
    assert c.bisect_left(0) == 0
    assert c.bisect_left(1) == 0
    assert c.bisect_left(2) == 1
    assert c.bisect_left(100) == 3

    assert c.bisect_right(0) == 0
    assert c.bisect_right(1) == 1
    assert c.bisect_right(2) == 1
    assert c.bisect_right(100) == 3

    c = SortedList([1, 10, 10, 12])
    assert c.bisect_left(10) == 1
    assert c.bisect_right(10) == 3


@pytest.mark.timeout(3)
def test_sorted_dict() -> None:
    c = SortedDict(
        {
            0: "shayan",
            10: "nan",
            12: "molly",
        }
    )
    assert c.bisect_left(0) == 0
    assert c.bisect_right(0) == 1

    assert c.bisect_left(9) == 1
    assert c.bisect_right(9) == 1

    assert c.bisect_left(10) == 1
    assert c.bisect_right(10) == 2

    assert c.bisect_left(12) == 2
    assert c.bisect_right(12) == 3

    assert c.bisect_left(13) == 3
    assert c.bisect_right(13) == 3


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", *sys.argv[1:], __file__]))
