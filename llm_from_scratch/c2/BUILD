load("@rules_python//python:defs.bzl", "py_library")
load("//llm_from_scratch:notebook.bzl", "notebook_env")

py_library(
    name = "c2",
    data = [
        "__init__.py",
        "the-verdict.txt",
    ],
    deps = [
        "@pypi//numpy",
        "@pypi//torch",
        "@pypi//tiktoken",
        "@pypi//sentencepiece",
    ],
)

notebook_env(
    name = "notebook",
    deps = [
        ":c2",
    ],
)
