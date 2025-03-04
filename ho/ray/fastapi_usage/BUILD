load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "fastapi_usage",
    srcs = ["fastapi_usage.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//fastapi",
        "@pypi//ray",
        "@pypi//requests",
    ],
)

py_library(
    name = "fastapi_usage_py",
    srcs = ["fastapi_usage.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//fastapi",
        "@pypi//ray",
        "@pypi//requests",
    ],
)
