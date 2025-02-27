load("@rules_go//go:def.bzl", "go_binary", "go_library", "go_test")
load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "main_test",
    srcs = ["main_test.py"],
    deps = ["@pypi//pytest"],
)

go_library(
    name = "twosum_lib",
    srcs = ["main.go"],
    importpath = "gitlab.com/hooshi/DSA-practice/leetcode/twosum",
    visibility = ["//visibility:private"],
)

go_binary(
    name = "twosum",
    embed = [":twosum_lib"],
    visibility = ["//visibility:public"],
)

go_test(
    name = "twosum_test",
    srcs = ["main_test.go"],
    embed = [":twosum_lib"],
    deps = ["@com_github_stretchr_testify//assert"],
)
