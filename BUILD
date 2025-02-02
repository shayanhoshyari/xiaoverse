load("@bazel_skylib//rules:write_file.bzl", "write_file")
load("@buildifier_prebuilt//:rules.bzl", "buildifier")
load("@gazelle//:def.bzl", "gazelle", "gazelle_test")
load("@rules_python//python:defs.bzl", "py_binary")
load("@rules_uv//uv:pip.bzl", "pip_compile")
load("@rules_uv//uv:venv.bzl", "create_venv")

exports_files(
    [
        "multitool.lock.json",
        "pyproject.toml",
    ],
)

py_binary(
    name = "m",
    srcs = ["m.py"],
    main = "m.py",
    deps = [
        "@pypi//click",
    ],
)

# To regenerate: bazel run //:requirements.update
pip_compile(
    name = "requirements",
    requirements_in = "requirements.in",
    requirements_txt = "requirements.lock.txt",
    universal = True,
)

write_file(
    name = "py_env_pth",
    out = "py_env.pth",
    content = [
        "# Add root of workspace to .vscode so picks up all python",
        "# files via intellisense",
        "../../../..",
    ],
)

create_venv(
    name = "venv",
    destination_folder = ".venv",
    requirements_txt = "//:requirements.lock.txt",
    site_packages_extra_files = [":py_env_pth"],
)

# Buildifier

buildifier(
    name = "buildifier",
    lint_mode = "fix",
    mode = "fix",
)

# Target used by aspect workflows `buildifier` step to check starlark formatting and lint errors.
buildifier(
    name = "buildifier.check",
    lint_mode = "warn",
    mode = "diff",
)

# Gazelle auto-file generator.
# gazelle:prefix gitlab.com/hooshi/DSA-practice
# gazelle:go_naming_convention import
gazelle(name = "gazelle")

gazelle_test(
    name = "gazelle_test",
    workspace = "//:BUILD",
)

alias(
    name = "ruff",
    actual = "@multitool//tools/ruff",
)

alias(
    name = "go",
    actual = "@rules_go//go",
)
