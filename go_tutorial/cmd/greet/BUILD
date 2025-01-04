load("@rules_go//go:def.bzl", "go_binary", "go_library")

go_library(
    name = "greet_lib",
    srcs = ["greet.go"],
    importpath = "gitlab.com/hooshi/DSA-practice/go_tutorial/cmd/greet",
    visibility = ["//visibility:private"],
    deps = ["//go_tutorial"],
)

go_binary(
    name = "greet",
    embed = [":greet_lib"],
    visibility = ["//visibility:public"],
)
