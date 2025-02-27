load("@rules_go//go:def.bzl", "go_binary", "go_library")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "helloworld_py",
    srcs = ["helloworld.py"],
    visibility = ["//:__subpackages__"],
)

go_library(
    name = "helloworld_lib",
    srcs = ["helloworld.go"],
    importpath = "gitlab.com/hooshi/DSA-practice/helloworld",
    visibility = ["//visibility:private"],
)

go_binary(
    name = "helloworld",
    embed = [":helloworld_lib"],
    visibility = ["//visibility:public"],
)
