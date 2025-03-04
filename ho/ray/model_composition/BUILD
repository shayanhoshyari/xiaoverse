load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "model_composition_py",
    srcs = ["model_composition.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//debugpy",
        "@pypi//ray",
        "@pypi//requests",
        "@pypi//starlette",
    ],
)

py_binary(
    name = "model_composition",
    srcs = ["model_composition.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//debugpy",
        "@pypi//ray",
        "@pypi//requests",
        "@pypi//starlette",
    ],
)
