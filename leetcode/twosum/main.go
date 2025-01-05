package main

import (
	"fmt"
	"sort"
)

func sortedIndices(nums []int) []int {
	sorted_indices := make([]int, len(nums))
	for i := range len(nums) {
		sorted_indices[i] = i
	}
	sort.Slice(sorted_indices, func(i, j int) bool {
		return nums[sorted_indices[i]] < nums[sorted_indices[j]]
	})
	return sorted_indices
}

func twoSum(nums []int, target int) ([]int, error) {
	// Zero length array
	if len(nums) < 2 {
		return nil, fmt.Errorf("array is of small length: %d", len(nums))
	}

	sorted_indices := sortedIndices(nums)

	i := int(0)
	j := int(len(nums) - 1)
	for i < j {
		sum := nums[sorted_indices[i]] + nums[sorted_indices[j]]
		if sum == target {
			return []int{sorted_indices[i], sorted_indices[j]}, nil
		} else if sum < target {
			i = i + 1
		} else {
			j = j - 1
		}
	}

	return nil, fmt.Errorf("No result")
}

func main() {
	twoSum([]int{3, 2, 4}, 6)
}
