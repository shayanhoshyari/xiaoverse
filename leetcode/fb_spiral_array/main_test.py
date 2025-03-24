# https://www.facebook.com/careers/life/sample_interview_questions
# Spiral array

import dataclasses
import enum
import sys

import pytest

NOT_FILLED = -1


class Direction(enum.Enum):
    up = enum.auto()
    right = enum.auto()
    down = enum.auto()
    left = enum.auto()


ROTATE_CLOCKWISE = {
    Direction.up: Direction.right,
    Direction.right: Direction.down,
    Direction.down: Direction.left,
    Direction.left: Direction.up,
}

STEP_DIRECTION = {
    Direction.up: (-1, 0),
    Direction.right: (0, 1),
    Direction.down: (1, 0),
    Direction.left: (0, -1),
}

Position = tuple[int, int]


@dataclasses.dataclass
class State:
    direction: Direction
    pos: Position
    n: int
    counter: int
    array: list[list[int]]
    on_going: bool = True


def step(state: State) -> State:
    """
    Returns:
        Next state, or None. None means we are done.
    """
    print(f"Iteration {state.counter} Started")

    def is_valid(p: Position) -> bool:
        result = (
            0 <= p[0] < state.n
            and 0 <= p[1] < state.n
            and array[p[0]][p[1]] == NOT_FILLED
        )
        print(f"trying {p}, result = {result}")
        return result

    def maybe_valid_direction(direction: Direction) -> Position | None:
        step_direction = STEP_DIRECTION[direction]
        maybe_next = (
            state.pos[0] + step_direction[0],
            state.pos[1] + step_direction[1],
        )
        return maybe_next if is_valid(maybe_next) else None

    array = state.array
    direction = state.direction

    # First set the array
    array[state.pos[0]][state.pos[1]] = state.counter

    # Find next location - try one
    print(f"Trying direction {direction}")
    if next_pos := maybe_valid_direction(direction):
        print("[*] Direction worked, moving on")
        return dataclasses.replace(
            state,
            pos=next_pos,
            direction=direction,
            array=array,
            counter=state.counter + 1,
        )

    # Find next try 2
    print(f"Trying direction {direction}")
    direction = ROTATE_CLOCKWISE[direction]
    if next_pos := maybe_valid_direction(direction):
        print("[*] Direction worked, moving on")
        return dataclasses.replace(
            state,
            pos=next_pos,
            direction=direction,
            array=array,
            counter=state.counter + 1,
        )

    print("[*] finished")
    return dataclasses.replace(state, array=array, on_going=False)


def spiral(n: int) -> list[list[int]]:
    state = State(
        direction=Direction.right,
        pos=(0, 0),
        n=n,
        counter=1,
        array=[[NOT_FILLED] * n for _ in range(n)],
    )
    while state.on_going:
        state = step(state)

    return state.array


def print_spiral(n: int) -> None:
    pass


@pytest.mark.timeout(3)
def test_template() -> None:
    assert spiral(1) == [[1]]
    assert spiral(2) == [[1, 2], [4, 3]]
    assert spiral(3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
