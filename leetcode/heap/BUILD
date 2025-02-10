load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "heap",
    srcs = ["main.py"],
    main = "main.py",
    deps = [
        "@pypi//pytest",
        "@pypi//pytest_timeout",
    ],
)
