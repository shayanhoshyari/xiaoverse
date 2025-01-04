//go:build tools

// Use for telling go these are tools and don't strip them.

package main

import (
	_ "github.com/go-delve/delve/cmd/dlv"
	_ "golang.org/x/tools/gopls"
)
