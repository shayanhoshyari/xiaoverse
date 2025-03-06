load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "hello_world",
    srcs = ["hello_world.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pypi//flytekit"],
)

py_library(
    name = "flyte_py",
    srcs = ["hello_world.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pypi//flytekit"],
)
