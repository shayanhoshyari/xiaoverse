package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

type Node struct {
	prev  *Node
	next  *Node
	value int
	key   int
}

type CacheMeory = map[int]*Node

type LRUCache struct {
	capacity int

	memory CacheMeory

	head *Node // recently used
	tail *Node // least recently used
}

func Constructor(capacity int) LRUCache {
	return LRUCache{capacity: capacity, memory: make(CacheMeory), head: nil, tail: nil}
}

func (this *LRUCache) Print() {
	printKey := func(node *Node) string {
		if node != nil {
			return fmt.Sprintf("%d", node.key)
		}
		return "nil"
	}

	fmt.Println("Memory Keys with Prev and Next:")
	for key, node := range this.memory {
		prevKey := printKey(node.prev)
		nextKey := printKey(node.next)
		fmt.Printf("Key: %d, Prev: %s, Next: %s\n", key, prevKey, nextKey)
	}

	fmt.Printf("Head Key: %s\n", printKey(this.head))
	fmt.Printf("Tail Key: %s\n", printKey(this.tail))
}

func (this *LRUCache) MoveFront(item *Node) {
	fmt.Println("Moving", item.key, "to front")
	this.Print()

	// Store info
	exHead := this.head
	exPrev := item.prev
	exNext := item.next

	// LRU
	this.head = item
	// Me -> Neighbours
	item.next = exHead
	if exHead != nil {
		exHead.prev = item
	}
	item.prev = nil
	// Neighbors -> Me
	if exPrev != nil {
		exPrev.next = exNext
	}
	if exNext != nil {
		exNext.prev = exPrev
	}

	if this.tail == item && exPrev != nil {
		// If exPrev is nil we only have one item, do nothing!
		fmt.Println("Key ", item.key, "was also marked as tail, updating to ", exPrev)
		this.tail = exPrev
	}
}

func (this *LRUCache) Get(key int) int {
	fmt.Println("[*] Getting key at", key)
	item, exists := this.memory[key]
	if exists {
		fmt.Println("Key found - moving to front", item)
		this.MoveFront(item)
		return item.value
	}
	fmt.Println("Key not found")
	return -1
}

func (this *LRUCache) Put(key int, value int) {
	// Check if exists
	// No:
	//  Check if len is exceeding
	//    Yes: Evit LRU
	//  Add to map
	// Move to front

	fmt.Println("[*] Putting key at:", key)

	item, exists := this.memory[key]
	if !exists {
		fmt.Println("Key does not exist:", key)
		if len(this.memory) == this.capacity {
			exTail := this.tail
			exPrev := exTail.prev

			fmt.Println("Capacity breached, evicting, len=", len(this.memory), "target=", exTail.key)

			this.tail = exPrev
			if exPrev != nil {
				exPrev.next = nil
			}

			delete(this.memory, exTail.key)
		}
		item = &Node{value: value, prev: nil, next: nil, key: key}
		// Add behind tail
		this.memory[key] = item

		fmt.Println("Added item to map, len=", len(this.memory), "map=", this.memory)
	} else {
		fmt.Println("Item already in map with prev value", item.value, "changing value to", value)
		item.value = value
	}

	// Move item to front.
	this.MoveFront(item)

	// If first time, need to init tail too
	if this.tail == nil {
		fmt.Println("Setting tail to be the head - first run", this.head, this.tail)
		this.tail = this.head
	}

}

/**
 * Your LRUCache object will be instantiated and called as such:
 * obj := Constructor(capacity);
 * param_1 := obj.Get(key);
 * obj.Put(key,value);
 */

func (cache *LRUCache) GetSilent(key int) int {
	item, exists := cache.memory[key]
	if !exists {
		return -1
	}
	return item.value
}

func TestCaseA(t *testing.T) {
	cache := Constructor(12)
	cache.Put(1, 12)
	assert.Equal(t, cache.Get(1), 12)
	assert.Equal(t, cache.Get(2), -1)
	fmt.Println("Case A passed")

	cache.Put(2, 20)
	assert.Equal(t, cache.Get(1), 12)
	assert.Equal(t, cache.Get(2), 20)
	fmt.Println("Case B passed")

	cache.Put(1, 10)
	assert.Equal(t, cache.Get(1), 10)
	assert.Equal(t, cache.Get(2), 20)
	fmt.Println("Case C passed")
}

func TestCaseB(t *testing.T) {
	cache := Constructor(1)

	cache.Put(1, 12)
	assert.Equal(t, cache.Get(1), 12)

	cache.Put(1, 11)
	assert.Equal(t, cache.Get(1), 11)

	cache.Put(2, 13)
	assert.Equal(t, cache.Get(1), -1)
	assert.Equal(t, cache.Get(2), 13)

	cache.Put(2, 14)
	assert.Equal(t, cache.Get(1), -1)
	assert.Equal(t, cache.Get(2), 14)

	cache.Put(3, 15)
	assert.Equal(t, cache.Get(2), -1)
	assert.Equal(t, cache.Get(3), 15)
}

func TestCaseC(t *testing.T) {
	cache := Constructor(2)

	cache.Put(1, 12)
	cache.Put(2, 14)
	assert.Equal(t, cache.GetSilent(1), 12)
	assert.Equal(t, cache.GetSilent(2), 14)

	// Now 1 should be evicted
	cache.Put(3, 15)
	assert.Equal(t, cache.GetSilent(1), -1)
	assert.Equal(t, cache.GetSilent(2), 14)
	assert.Equal(t, cache.GetSilent(3), 15)

	// Now 2 should be evicted
	cache.Put(4, 16)
	assert.Equal(t, cache.GetSilent(2), -1)
	assert.Equal(t, cache.GetSilent(3), 15)
	assert.Equal(t, cache.GetSilent(4), 16)

	// Now do get on 3, so 4 should be evicted
	cache.Get(3)
	cache.Put(5, 17)
	assert.Equal(t, cache.GetSilent(3), 15)
	assert.Equal(t, cache.GetSilent(4), -1)
	assert.Equal(t, cache.GetSilent(5), 17)
}

func TestCaseD(t *testing.T) {
	cache := Constructor(2)

	cache.Put(1, 1)
	cache.Put(2, 2)
	assert.Equal(t, cache.Get(1), 1)
	cache.Put(3, 3)
	assert.Equal(t, cache.Get(2), -1)
	cache.Put(4, 4)
	assert.Equal(t, cache.Get(1), -1)
	assert.Equal(t, cache.Get(3), 3)
	assert.Equal(t, cache.Get(4), 4)
}

func TestCaseE(t *testing.T) {
	cache := Constructor(1)

	assert.Equal(t, cache.Get(1), -1)
	cache.Put(2, 1)
	assert.Equal(t, cache.Get(2), 1)
	cache.Put(3, 1)
	assert.Equal(t, cache.Get(2), -1)
	assert.Equal(t, cache.Get(3), 1)
}
