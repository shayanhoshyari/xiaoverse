load("@rules_python//python:defs.bzl", "py_library")
load("//llm_from_scratch:notebook.bzl", "notebook_env")

py_library(
    name = "c2",
    data = [
        "__init__.py",
        "the-verdict.txt",
    ],
    visibility = ["//llm_from_scratch:__subpackages__"],
    deps = [
        "@pypi//numpy",
        "@pypi//tiktoken",
        "@pypi//torch",
    ],
)

notebook_env(
    name = "notebook",
    deps = [
        ":c2",
    ],
)

py_library(
    name = "c2_py",
    srcs = ["__init__.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//tiktoken",
        "@pypi//torch",
    ],
)
