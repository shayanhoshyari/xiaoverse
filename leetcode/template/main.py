# https://leetcode.com/problems/template

import pytest
import sys
from typing import Any


def template(*args: Any) -> Any:
    pass


@pytest.mark.timeout(3)
def test_template() -> None:
    pass


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
