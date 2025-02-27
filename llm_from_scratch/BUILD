load("@rules_python//python:defs.bzl", "py_binary", "py_library")

exports_files(["notebook.py"])

py_binary(
    name = "notebook",
    srcs = ["notebook.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pypi//jupyter_server"],
)

py_library(
    name = "llm_from_scratch_pybin",
    srcs = ["notebook.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pypi//jupyter_server"],
)
