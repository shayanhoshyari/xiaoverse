load("@rules_python//python:defs.bzl", "py_library")
load("//llm_from_scratch:notebook.bzl", "notebook_env")

py_library(
    name = "c4",
    srcs = [
        "__init__.py",
    ],
    visibility = ["//llm_from_scratch:__subpackages__"],
    deps = [
        "//llm_from_scratch/c3",
        "@pypi//torch",
    ],
)

notebook_env(
    name = "notebook",
    deps = [
        ":c4",
    ],
)
