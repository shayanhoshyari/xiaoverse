load("@rules_python//python:defs.bzl", "py_library")
load("//llm_from_scratch:notebook.bzl", "notebook_env")

py_library(
    name = "c5",
    srcs = [
        "__init__.py",
    ],
    deps = [
        "@pypi//torch",
        "@pypi//tiktoken",
        "//llm_from_scratch/c4",
    ],
    visibility = ["//:__subpackages__"],
)

notebook_env(
    name = "notebook",
    deps = [
        ":c5",
    ],
)
