load("@rules_python//python:defs.bzl", "py_library")
load("//llm_from_scratch:notebook.bzl", "notebook_env")

py_library(
    name = "c3",
    srcs = [
        "__init__.py",
    ],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//torch",
    ],
)

notebook_env(
    name = "notebook",
    deps = [
        ":c3",
    ],
)
