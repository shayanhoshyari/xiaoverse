# https://leetcode.com/problems/merge-two-sorted-lists/

import pytest
import sys
import math

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def get_value(node : ListNode | None) -> float:
    if node is None:
        return math.inf
    return node.val

def pprint(*args):
    print(*args)


def mergeTwoLists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    # Handle the corner case.
    if list1 is None:
        return list2
    if list2 is None:
        return list1

    tail = head = ListNode()
    while not (list1 is None and list2 is None):
        if list1 is not None and get_value(list1) < get_value(list2):
            tail.next = list1
            list1 = list1.next
        elif list2 is not None:
            tail.next = list2
            list2 = list2.next

        if tail.next is not None:
            tail = tail.next

    return head.next

# Test

def make_list(values : list[int]) -> ListNode | None:
    iter = head = ListNode()
    for value in values:
        iter.next = ListNode(value)
        iter = iter.next
    return head.next

def infer_list(node : ListNode | None) -> list[int]:
    values = list[int]()
    iter = node
    while iter is not None:
        values.append(iter.val)
        iter = iter.next
    return values

def easy_merge(a : list[int], b : list[int]) -> list[int]:
    return infer_list(mergeTwoLists(make_list(a), make_list(b)))

def test_A() -> None:
    assert easy_merge([], []) == []
    assert easy_merge([1], []) == [1]
    assert easy_merge([], [1]) == [1]
    assert easy_merge([1], [2]) == [1,2]
    assert easy_merge([1,3], [2,3]) == [1,2,3,3]


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
