load("@rules_python//python:defs.bzl", "py_library")
load("//llm_from_scratch:notebook.bzl", "notebook_env")

py_library(
    name = "c5",
    srcs = [
        "__init__.py",
    ],
    visibility = ["//llm_from_scratch:__subpackages__"],
    deps = [
        "//llm_from_scratch/c2:c2_py",
        "//llm_from_scratch/c4",
        "@pypi//tensorflow",
        "@pypi//tiktoken",
        "@pypi//torch",
    ],
)

notebook_env(
    name = "notebook",
    deps = [
        ":c5",
    ],
)
