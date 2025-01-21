// https://leetcode.com/problems/search-in-rotated-sorted-array/
//
// There is an integer array nums sorted in ascending order (with distinct
// values).
//
// Prior to being passed to your function, nums is possibly rotated at an
// unknown pivot index k (1 <= k < nums.length) such that the resulting array
// is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]
// (0-indexed). For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3
// and become [4,5,6,7,0,1,2].
//
// Given the array nums after the possible rotation and an integer target,
// return the index of target if it is in nums, or -1 if it is not in nums.
//
// You must write an algorithm with O(log n) runtime complexity.

package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func getMid(a int, b int) int {
	// Returns the left most when there is even number of entries.
	sum := a + b
	if sum%2 == 1 {
		return sum / 2
	}
	return sum/2 - 1
}

func findPivotImpl(nums []int, beg int, end int) int {
	// fmt.Println("[*] Operating on ", beg, end)

	// Only one left
	if end <= beg+1 {
		// fmt.Println("end <= beg + 1, return beg", beg, end)
		return beg
	}

	// Get rid of the case where beg is the pivot!
	if nums[beg] < nums[end-1] {
		// fmt.Println("nums[beg] < nums[end-1], return beg", nums[beg], nums[end-1], beg)
		return beg
	}

	mid := getMid(beg, end)

	// fmt.Println("Mid is", mid)
	if nums[mid] < nums[end-1] {
		// fmt.Println("nums[mid] < nums[beg], return find(nums, beg, mid+1)", nums[mid], nums[beg], beg, mid+1)
		return findPivotImpl(nums, beg, mid+1)
	}
	// fmt.Println("nums[mid] > nums[beg], return find(nums, mid+1, end)", nums[mid], nums[beg], mid+1, end)
	return findPivotImpl(nums, mid+1, end)
}

func findPivot(nums []int) int {
	return findPivotImpl(nums, 0, len(nums))
}

type ShiftedArray struct {
	values []int
	pivot  int
}

func (array *ShiftedArray) size() int {
	return len(array.values)
}

func (array *ShiftedArray) actualIndex(index int) int {
	return (array.pivot + index) % array.size()
}

func (array *ShiftedArray) at(index int) int {
	return array.values[array.actualIndex(index)]
}

func binarySearchImpl(array *ShiftedArray, value int, beg int, end int) int {
	// fmt.Println("[*] Operating on ", beg, end, array.values)

	if end == beg+1 {
		// fmt.Println("end = beg + 1 - ending", end, beg)
		// fmt.Println("Return value is", beg)
		return beg
	}
	mid := getMid(beg, end)
	// fmt.Println("Mid is ", mid)

	if array.at(mid) < value {
		// fmt.Println("array.at(mid) > search right", array.at(mid), value)
		return binarySearchImpl(array, value, mid+1, end)
	}
	// fmt.Println("array.at(mid) <= value -- search left", array.at(mid), value)
	return binarySearchImpl(array, value, beg, mid+1)
}

func binarySearch(array *ShiftedArray, value int) int {
	return binarySearchImpl(array, value, 0, array.size())
}

func search(nums []int, target int) int {
	pivot := findPivot(nums)
	array := ShiftedArray{values: nums, pivot: pivot}
	index := binarySearch(&array, target)

	if array.at(index) != target {
		return -1
	}
	return array.actualIndex(index)
}

// Tests

func TestGetMid(t *testing.T) {
	assert.Equal(t, getMid(0, 2), 0)
	assert.Equal(t, getMid(0, 3), 1)
}

func TestFindPivot(t *testing.T) {
	assert.Equal(t, findPivot([]int{}), 0)
	assert.Equal(t, findPivot([]int{1}), 0)
	assert.Equal(t, findPivot([]int{1, 2}), 0)
	assert.Equal(t, findPivot([]int{2, 1}), 1)
	assert.Equal(t, findPivot([]int{1, 2, 3}), 0)
	assert.Equal(t, findPivot([]int{3, 1, 2}), 1)
	assert.Equal(t, findPivot([]int{2, 3, 1}), 2)
	assert.Equal(t, findPivot([]int{4, 5, 6, 7, 0, 1, 2}), 4)
}

func TestBinarySearch(t *testing.T) {

	makeArray := func(elements ...int) *ShiftedArray {
		return &ShiftedArray{values: elements, pivot: 0}
	}

	assert.Equal(t, 0, binarySearch(makeArray(1, 2), 1))
	assert.Equal(t, 1, binarySearch(makeArray(1, 2), 2))
	assert.Equal(t, 0, binarySearch(makeArray(1, 2), 0))
	assert.Equal(t, 1, binarySearch(makeArray(1, 2), 3))
	assert.Equal(t, 0, binarySearch(makeArray(0, 1, 2, 4, 5, 6, 7), 0))
	assert.Equal(t, 0, binarySearch(&ShiftedArray{values: []int{4, 5, 6, 7, 0, 1, 2}, pivot: 4}, 0))
}

func TestSearch(t *testing.T) {

	makeArray := func(elements ...int) []int {
		return elements
	}

	assert.Equal(t, 0, search(makeArray(1, 2), 1))
	assert.Equal(t, -1, search(makeArray(1, 2), 0))
	assert.Equal(t, -1, search(makeArray(1, 2), 3))
	assert.Equal(t, 1, search(makeArray(1, 2), 2))

	assert.Equal(t, 1, search(makeArray(2, 1), 1))
	assert.Equal(t, -1, search(makeArray(2, 1), 0))
	assert.Equal(t, -1, search(makeArray(2, 1), 3))
	assert.Equal(t, 0, search(makeArray(2, 1), 2))

	assert.Equal(t, 7, search(makeArray(60, 70, 80, 90, 10, 20, 30, 50), 50))
	assert.Equal(t, 0, search(makeArray(60, 70, 80, 90, 10, 20, 30, 50), 60))
	assert.Equal(t, 3, search(makeArray(60, 70, 80, 90, 10, 20, 30, 50), 90))
	assert.Equal(t, -1, search(makeArray(60, 70, 80, 90, 10, 20, 30, 50), 91))
	assert.Equal(t, -1, search(makeArray(60, 70, 80, 90, 10, 20, 30, 50), 51))
	assert.Equal(t, -1, search(makeArray(60, 70, 80, 90, 10, 20, 30, 50), 59))

	assert.Equal(t, 4, search(makeArray(4, 5, 6, 7, 0, 1, 2), 0))
}
