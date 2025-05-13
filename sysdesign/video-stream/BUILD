load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "video-stream",
    srcs = ["__main__.py"],
    data = ["static/index.html"],
    main = "__main__.py",
    visibility = ["//:__subpackages__"],
    deps = [
        "@pypi//fastapi",
        "@pypi//requests",
        "@pypi//uvicorn",
    ],
)
