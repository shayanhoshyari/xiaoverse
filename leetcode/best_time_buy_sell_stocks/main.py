# https://leetcode.com/problems/best-time-to-buy-and-sell-stock

import pytest
import sys


def max_profit(prices: list[float]) -> float:
    if not prices:
        return 0

    min_price = prices[0]
    max_profit = 0.
    for price in prices[1:]:
        max_profit = max(max_profit, price - min_price)
        min_price = min(min_price, price)

    return max_profit

def test_template() -> None:
    assert max_profit([0,1]) == 1
    assert max_profit([0,1,2]) == 2
    assert max_profit([1,0]) == 0
    assert max_profit([1,0,-1,2]) == 3


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
