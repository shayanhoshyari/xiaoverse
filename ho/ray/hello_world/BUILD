load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "hello_world_py",
    srcs = ["hello_world.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pypi//ray"],
)

py_binary(
    name = "hello_world",
    srcs = ["hello_world.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pypi//ray"],
)
