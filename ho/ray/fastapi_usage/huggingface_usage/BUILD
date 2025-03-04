load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "huggingface_usage_py",
    srcs = ["huggingface_usage.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//ray",
        "@pypi//requests",
        "@pypi//starlette",
        "@pypi//torch",
        "@pypi//transformers",
    ],
)

py_binary(
    name = "huggingface_usage",
    srcs = ["huggingface_usage.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//ray",
        "@pypi//requests",
        "@pypi//starlette",
        "@pypi//torch",
        "@pypi//transformers",
    ],
)
