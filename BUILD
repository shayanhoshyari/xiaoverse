load("@bazel_skylib//rules:write_file.bzl", "write_file")
load("@buildifier_prebuilt//:rules.bzl", "buildifier")
load("@gazelle//:def.bzl", "gazelle", "gazelle_binary", "gazelle_test")
load("@pypi//:requirements.bzl", "all_whl_requirements")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@rules_python_gazelle_plugin//manifest:defs.bzl", "gazelle_python_manifest")
load("@rules_python_gazelle_plugin//modules_mapping:def.bzl", "modules_mapping")
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
    visibility = ["//:__subpackages__"],
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
# gazelle:python_library_naming_convention $package_name$_py
# gazelle:python_binary_naming_convention $package_name$_pybin
# gazelle:python_test_naming_convention $package_name$_pytest

gazelle_binary(
    name = "gazelle_bin",
    languages = [
        "@rules_python_gazelle_plugin//python",
        "@gazelle//language/go",
        "@gazelle//language/proto",
    ],
)

gazelle(
    name = "gazelle",
    gazelle = ":gazelle_bin",
)

gazelle_test(
    name = "gazelle_test",
    gazelle = ":gazelle_bin",
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

# This rule fetches the metadata for python packages we depend on. That data is
# required for the gazelle_python_manifest rule to update our manifest file.
modules_mapping(
    name = "modules_map",
    wheels = all_whl_requirements,
)

# Docs: https://github.com/bazelbuild/rules_python/blob/main/gazelle/README.md
# Gazelle python extension needs a manifest file mapping from
# an import to the installed package that provides it.
# This macro produces two targets:
# - //:gazelle_python_manifest.update can be used with `bazel run`
#   to recalculate the manifest
# - //:gazelle_python_manifest.test is a test target ensuring that
#   the manifest doesn't need to be updated
gazelle_python_manifest(
    name = "gazelle_python_manifest",
    modules_mapping = ":modules_map",
    pip_repository_name = "pypi",
    requirements = "//:requirements.lock.txt",
)

py_library(
    name = "DSA-practice_pybin",
    srcs = ["m.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pypi//click"],
)
