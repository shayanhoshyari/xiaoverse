package main

import (
	"fmt"

	"gitlab.com/hooshi/DSA-practice/go_tutorial/greetings"
)

func main() {
	message := greetings.HelloBasic("My dear darlings!")
	fmt.Println(message)
}
