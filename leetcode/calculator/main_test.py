"""
https://leetcode.com/problems/basic-calculator
https://blog.darrien.dev/posts/writing-calc-parser/
"""

import sys
from typing import Literal

import pytest
import pytest_timeout  # noqa

Token = int | Literal["+", "-", "*", "/"]


def evalualte(v1: int, v2: int, op: str) -> int:
    if op == "+":
        return v1 + v2
    if op == "-":
        return v1 - v2
    if op == "*":
        return v1 * v2
    if op == "/":
        return v1 / v2
    raise ValueError()


def calculate_basic(tokens: list[Token]) -> int:
    """
    Given a set of clean tokens, like [-, 1, +, 2, *, 1, 2, 3], returns the answer
    Assumes the input does not have any parentheses
    """
    # If starts with char add a trailing 0
    if not isinstance(tokens[0], int):
        tokens.insert(0, 0)

    # Pass 1: make numbers
    pass1 = list[Token]()
    for t in tokens:
        if isinstance(t, int) and pass1 and isinstance(pass1[-1], int):
            pass1[-1] = pass1[-1] * 10 + t
        else:
            pass1.append(t)

    print("After pass 1: ", pass1)

    # Pass 2: compute * or /
    pass2 = list[Token]()
    for t in pass1:
        if (
            isinstance(t, int)
            and len(pass2) >= 2
            and pass2[-1] in ("*", "/")
            and isinstance(pass2[-2], int)
        ):
            pass2[-2] = evalualte(pass2[-2], t, pass2[-1])
            pass2.pop()
        else:
            pass2.append(t)

    print("After pass 2: ", pass2)

    # pass 3: compute the rest
    pass3 = list[Token]()
    for t in pass2:
        if len(pass3) >= 2:
            pass3[-2] = evalualte(pass3[-2], t, pass3[-1])
            pass3.pop()
        else:
            pass3.append(t)

    print("After pass 3: ", pass3)

    return pass3[0]


def calculate(expr: str) -> int:
    """
    Given a math expression, compute the result
    """

    # Ensure that the expression starts and ends with parens.
    # This was our algo will terminate with a single token.
    expr = f"({expr})"

    token_stack = list[list[str]]()
    for char in expr:
        if char == " ":
            pass
        elif char == "(":
            # Start a new sub operation
            token_stack.append([])
        elif char == ")":
            # Compute the value that this paranthesis was tracking, and
            # add it to the previous stack of tokens
            value = calculate_basic(token_stack[-1])
            token_stack.pop()
            if not token_stack:
                token_stack.append([value])
            else:
                token_stack[-1].append(value)
        elif char in ("+", "-", "*", "/"):
            token_stack[-1].append(char)
        elif char.isdigit():
            token_stack[-1].append(int(char))
        else:
            raise ValueError(f"Not supported char {char}")

    assert len(token_stack) == 1
    assert len(token_stack[0]) == 1
    result = token_stack[0][0]
    assert isinstance(result, int)
    return result


@pytest.mark.timeout(3)
def test_calculate_basic() -> None:
    # no / +
    assert calculate_basic([1, 2, 3]) == 123
    assert calculate_basic(["-", 1, 2, 3]) == -123
    assert calculate_basic([2, "-", 1, 2, 3]) == -121
    assert calculate_basic([1, 2, 3, "+", 1, 2]) == 135
    assert calculate_basic([2, "-", 1, 2, 3, "+", 1, 3]) == -108
    # with / +
    assert calculate_basic([1, 2, 3, "/", 1, 2, 3]) == 1
    assert calculate_basic([1, 2, 3, "*", 1, 2, 3]) == 123 * 123
    assert calculate_basic([2, "-", 3, "*", 4, "/", 2, "+", 1]) == -3


@pytest.mark.timeout(3)
def test_calculate() -> None:
    assert calculate("(1+(4+5+2)-3)+(6+8)") == 23
    assert calculate("2-1 + 2") == 3
    assert calculate("1 + 1") == 2
    assert calculate("1 + 1") == 2


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
