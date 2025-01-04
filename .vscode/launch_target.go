// This is work in progress
// Does not work now.

package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

var (
	bazelWorkspace = getWorkspaceRoot()
	bazelBin       = "./bazel"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Expected exactly one argument: '<bazel target> <args>' as a single string.")
		os.Exit(1)
	}

	args := strings.Fields(os.Args[1])
	if len(args) == 0 {
		fmt.Println("No target specified.")
		os.Exit(1)
	}

	target := args[0]
	os.Args = append([]string{os.Args[0]}, args[1:]...)

	err := runBazelTarget(target)
	if err != nil {
		fmt.Printf("Failed to run bazel target: %v\n", err)
		os.Exit(1)
	}
}

func runBazelTarget(target string) error {
	// Build the target
	fmt.Println("Building target:", target)
	cmd := exec.Command(bazelBin, "build", target)
	cmd.Dir = bazelWorkspace
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("bazel build failed: %w", err)
	}

	// Query the target to get executable and runfiles
	queryCmd := exec.Command(
		bazelBin, "cquery",
		"--ui_event_filters=-info,-debug",
		"--noshow_progress",
		"--output=starlark",
		"--starlark:expr=[target.files_to_run.executable.path, target.files_to_run.runfiles_manifest.path]",
		target,
	)
	queryCmd.Dir = bazelWorkspace

	var out bytes.Buffer
	queryCmd.Stdout = &out
	queryCmd.Stderr = os.Stderr

	if err := queryCmd.Run(); err != nil {
		return fmt.Errorf("bazel cquery failed: %w", err)
	}

	// Get the execution root
	execRootCmd := exec.Command(bazelBin, "info", "execution_root")
	execRootCmd.Dir = bazelWorkspace
	execRoot, err := execRootCmd.Output()
	if err != nil {
		return fmt.Errorf("failed to get execroot: %w", err)
	}

	execRootStr := strings.TrimSpace(string(execRoot))

	// Parse the last line of the query output
	queryOutput := strings.TrimSpace(out.String())
	lines := strings.Split(queryOutput, "\n")
	if len(lines) == 0 {
		return errors.New("no output from cquery")
	}
	lastLine := lines[len(lines)-1]

	// Extract binary and runfiles manifest
	var binary, runfilesManifest string
	var result []string
	err = json.Unmarshal([]byte(lastLine), &result)
	if err != nil {
		return fmt.Errorf("failed to parse cquery output: %w", err)
	}
	if len(result) != 2 {
		return errors.New("unexpected cquery output format")
	}
	binary, runfilesManifest = result[0], result[1]

	binary = strings.Trim(binary, "\"")
	runfilesManifest = strings.Trim(runfilesManifest, "\"")

	binaryAbs := filepath.Join(bazelWorkspace, binary)
	runfilesManifestAbs := filepath.Join(bazelWorkspace, runfilesManifest)

	// Set environment variables and change directory to execroot
	os.Setenv("RUNFILES_MANIFEST_FILE", runfilesManifestAbs)
	err = os.Chdir(execRootStr)
	if err != nil {
		return fmt.Errorf("failed to change directory to execroot: %w", err)
	}

	// Execute the binary
	fmt.Println("Running binary:", binaryAbs)
	execCmd := exec.Command(binaryAbs, os.Args[1:]...)
	execCmd.Stdout = os.Stdout
	execCmd.Stderr = os.Stderr

	return execCmd.Run()
}

// getWorkspaceRoot finds the Bazel workspace root by walking up the directory tree.
func getWorkspaceRoot() string {
	dir, err := os.Getwd()
	if err != nil {
		fmt.Println("Failed to get current directory:", err)
		os.Exit(1)
	}

	for {
		if _, err := os.Stat(filepath.Join(dir, "MODULE.bazel")); err == nil {
			return dir
		}
		parent := filepath.Dir(dir)
		if parent == dir {
			break
		}
		dir = parent
	}

	fmt.Println("Bazel WORKSPACE file not found.")
	os.Exit(1)
	return ""
}
