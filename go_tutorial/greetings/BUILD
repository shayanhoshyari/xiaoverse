load("@rules_go//go:def.bzl", "go_library", "go_test")

go_test(
    name = "greetings_test",
    srcs = ["greetings_test.go"],
    embed = [":greetings"],
)

go_library(
    name = "greetings",
    srcs = ["greetings.go"],
    importpath = "gitlab.com/hooshi/DSA-practice/go_tutorial/greetings",
    visibility = ["//visibility:public"],
)
