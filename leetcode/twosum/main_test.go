package main

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test1(t *testing.T) {
	var indices []int
	var err error

	indices, err = twoSum([]int{3, 2, 4}, 6)
	assert.NoError(t, err)
	assert.Equal(t, indices, []int{1, 2})

	indices, err = twoSum([]int{11, 15, 2, 7}, 9)
	assert.NoError(t, err)
	assert.Equal(t, indices, []int{2, 3})

	indices, err = twoSum([]int{2, 7, 11, 15}, 9)
	assert.NoError(t, err)
	assert.Equal(t, indices, []int{0, 1})

	indices, err = twoSum([]int{2, 7, 11, 15}, 16)
	assert.Error(t, err)
	assert.Equal(t, err.Error(), "No result")

	indices, err = twoSum([]int{}, 16)
	assert.Error(t, err)
	assert.True(t, strings.HasPrefix(err.Error(), "array is of small length"))

	indices, err = twoSum([]int{16}, 16)
	assert.Error(t, err)
	assert.True(t, strings.HasPrefix(err.Error(), "array is of small length"))

}
