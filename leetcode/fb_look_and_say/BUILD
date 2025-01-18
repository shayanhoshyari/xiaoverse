load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "fb_look_and_say",
    srcs = ["main.py"],
    main = "main.py",
    deps = [
        "@pypi//pytest",
        "@pypi//pytest_timeout",
    ],
)
