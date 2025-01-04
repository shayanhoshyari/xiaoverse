load("@bazel_skylib//rules:write_file.bzl", "write_file")
load("@buildifier_prebuilt//:rules.bzl", "buildifier")
load("@gazelle//:def.bzl", "gazelle", "gazelle_test")
load("@rules_uv//uv:pip.bzl", "pip_compile")
load("@rules_uv//uv:venv.bzl", "sync_venv")

exports_files(
    [
        "multitool.lock.json",
        "pyproject.toml",
    ],
)

# To regenerate: bazel run //:requirements.update
pip_compile(
    name = "requirements",
    requirements_in = "requirements.in",
    requirements_txt = "requirements.lock.txt",
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

sync_venv(
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

genrule(
    name = "go_tools",
    outs = [
        "go_tools/bin/dlv",
        "go_tools/bin/go",
        "go_tools/bin/gopls",
        "go_tools/bin/objdump",
    ],
    cmd = """
cp $(location @com_github_go_delve_delve//cmd/dlv:dlv) $(location :go_tools/bin/dlv)
cp $(location @go_sdk//:bin/go) $(location :go_tools/bin/go)
cp $(location @org_golang_x_tools_gopls//:gopls) $(location :go_tools/bin/gopls)
cp $(locations @go_sdk//:tools) $$(dirname $(location :go_tools/bin/objdump))
    """,
    tools = [
        "@com_github_go_delve_delve//cmd/dlv",
        "@org_golang_x_tools_gopls//:gopls",
        "@go_sdk//:bin/go",
        "@go_sdk//:tools",
    ],
)
