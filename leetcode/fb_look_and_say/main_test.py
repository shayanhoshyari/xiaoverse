# https://www.facebook.com/careers/life/sample_interview_questions
# Look and say

import pytest
import sys
import os


def next_seq(digits: list[int]) -> list[int]:
    # print(f"next_seq | {digits}")
    result = []
    stack = []

    for d in digits:
        # print(f"Digit {d} - result = {result} - stack = {stack}")

        if not stack:
            # print("stack empty, adding")
            stack.append(d)
            continue

        if stack[-1] != d:
            # print("faced new digit, empty stack add to result")
            result.extend([len(stack), stack[-1]])
            stack = [d]
            continue

        # print("Same digit, record it")
        stack.append(d)

    if stack:
        # print(f"stack={stack}, adding to result")
        result.extend([len(stack), stack[-1]])

    return result


def test_next_seq() -> None:
    assert next_seq([1]) == [1, 1]
    assert next_seq([1, 1]) == [2, 1]
    assert next_seq([1, 1, 2]) == [2, 1, 1, 2]
    assert next_seq([1, 1, 2, 2, 10]) == [2, 1, 2, 2, 1, 10]


def main() -> None:
    try:
        n = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Invalid args, first arg should be number of digits")

    digits = [1]
    for i in range(n):
        print(" ".join(str(d) for d in digits))
        digits = next_seq(digits)


if __name__ == "__main__":
    if "DEMO" in os.environ:
        main()
    else:
        sys.exit(pytest.main(["-vv", __file__]))
