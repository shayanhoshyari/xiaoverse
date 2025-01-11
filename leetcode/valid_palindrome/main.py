# https://leetcode.com/problems/valid-palindrome

import pytest
import sys


def is_valid(c: str) -> bool:
    return (ord("a") <= ord(c) <= ord("z")) or (ord("0") <= ord(c) <= ord("9"))


def sanitize(value: str) -> str:
    return "".join([c for c in value.lower() if is_valid(c)])


def is_palindrome(value: str) -> bool:
    value = sanitize(value)
    # Way 1
    # leet code ran out of time.
    # if len(value) < 1:
    #     return True
    # return value[0] == value[-1] and is_palindrome(value[1:-1])

    # Way 2
    for idx in range(len(value) // 2):
        c1 = value[idx]
        c2 = value[len(value) - 1 - idx]
        if c1 != c2:
            return False
    return True


def test_is_valid() -> None:
    assert is_valid("0")
    assert is_valid("9")
    assert is_valid("z")
    assert is_valid("a")
    assert is_valid("b")
    assert not is_valid("X")
    assert not is_valid("\n")


def test_sanitize() -> None:
    assert sanitize("A man, a plan, a canal: Panama") == "amanaplanacanalpanama"


def test_is_palindrome() -> None:
    assert is_palindrome("")
    assert is_palindrome("s")
    assert is_palindrome("ss")
    assert not is_palindrome("sxy")
    assert is_palindrome("sxs")


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
