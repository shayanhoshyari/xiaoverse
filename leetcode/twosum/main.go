package main

import (
	"fmt"
	"slices"
)

func twoSum(nums []int, target int) ([]int, error) {
	// Zero length array
	if len(nums) < 2 {
		return nil, fmt.Errorf("array is of small length: %d", len(nums))
	}

	i := int(0)
	j := int(len(nums) - 1)
	slices.Sort(nums)
	for i < j {
		sum := nums[i] + nums[j]
		if sum == target {
			return []int{i, j}, nil
		} else if sum < target {
			i = i + 1
		} else {
			j = j - 1
		}
	}

	return nil, fmt.Errorf("No result")
}

func main() {
	twoSum([]int{2, 7, 11, 15}, 9)
}
