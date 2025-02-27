load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "sortedcontainers",
    srcs = ["sortedcontainers.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//pytest",
        "@pypi//sortedcontainers",
    ],
)

py_library(
    name = "sortedcontainers_py",
    srcs = ["sortedcontainers.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//pytest",
        "@pypi//sortedcontainers",
    ],
)
