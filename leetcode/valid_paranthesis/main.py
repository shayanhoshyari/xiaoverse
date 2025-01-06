import pytest
from collections import deque

OPEN_TO_CLOSE = {
    "{" : "}",
    "[" : "]",
    "(" : ")",
}

CLOSE_TO_OPEN = {v : k for k, v in OPEN_TO_CLOSE.items()}

def peek(values : deque[str]) -> str | None:
    if not values:
        return None
    result = values.pop()
    values.append(result)
    return result


def is_valid(s : str) -> bool:
    open_parans = deque[str]()
    for char in s:
        # Case 1 : closing
        if char in CLOSE_TO_OPEN:
            sibling = CLOSE_TO_OPEN[char]
            opened = peek(open_parans)
            if opened != sibling:
                return False
            # All good proceed
            open_parans.pop()
        # Case 2: open paran
        elif char in OPEN_TO_CLOSE:
            open_parans.append(char)

    if open_parans:
        # if still values left some opens are not closed.
        return False

    return True


def test_is_valid() -> None:
    assert is_valid("shayan")
    assert is_valid("{}")
    assert is_valid("{[]}")
    assert is_valid("[{}]")
    assert is_valid("[{}()]")

    assert not is_valid("[{()]")
    assert not is_valid("[")

if __name__ == "__main__":
    pytest.main([__file__])
