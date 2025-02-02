"""
Utilities for working with jupyter.
"""

load("@rules_python//python:defs.bzl", "py_binary")

def notebook_env(name, deps):
    """
    Create a jupyter environment.

    Args:
        name (str): The name of the py_binary target.
        deps (list): The dependencies. Any python file or data you want to load should be added as a py_library dependency.
    """
    py_binary(
        name = name,
        srcs = [Label("notebook.py")],
        main = Label("notebook.py"),
        deps = [
            "@pypi//jupyter",
            "@pypi//ipykernel",
            "@pypi//notebook",
        ] + deps,
    )
