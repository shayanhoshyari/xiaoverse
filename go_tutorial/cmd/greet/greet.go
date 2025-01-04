package main

import (
	"fmt"

	greetings "gitlab.com/hooshi/DSA-practice/go_tutorial"
)

func main() {
	message := greetings.HelloBasic("My dear darlings!")
	fmt.Println(message)
}
