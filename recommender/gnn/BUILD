load("@rules_python//python:defs.bzl", "py_library")
load("//llm_from_scratch:notebook.bzl", "notebook_env")

py_library(
    name = "gnn",
    srcs = [
        "__init__.py",
    ],
    deps = [
        "@pypi//torch",
        "@pypi//torch_geometric",
    ],
)

notebook_env(
    name = "notebook",
    deps = [
        ":gnn",
    ],
)
