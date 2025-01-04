load("@rules_go//go:def.bzl", "go_binary", "go_library")

go_library(
    name = "greet_error_lib",
    srcs = ["greet_error.go"],
    importpath = "gitlab.com/hooshi/DSA-practice/go_tutorial/cmd/greet_error",
    visibility = ["//visibility:private"],
    deps = ["//go_tutorial/greetings"],
)

go_binary(
    name = "greet_error",
    embed = [":greet_error_lib"],
    visibility = ["//visibility:public"],
)
