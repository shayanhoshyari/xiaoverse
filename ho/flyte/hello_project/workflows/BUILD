load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "example",
    srcs = ["example.py"],
    visibility = ["//ho/flyte/hello_project:__subpackages__"],
    deps = ["@pypi//flytekit"],
)

py_library(
    name = "workflows_py",
    srcs = [
        "__init__.py",
        "example.py",
    ],
    visibility = ["//ho/flyte/hello_project:__subpackages__"],
    deps = ["@pypi//flytekit"],
)
