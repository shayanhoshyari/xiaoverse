import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import click

# Bazel sets this. m.py is meant to run with ./bazel run //:m or ./m (which wraps it)
ROOT = Path(os.environ["BUILD_WORKSPACE_DIRECTORY"])

green: str = "\033[32m"
red: str = "\033[31m"
reset: str = "\033[00m"


def _bazel(*args: str, show_output: bool = True) -> None:
    args = [
        "./bazel",
        args[0],
        "--ui_event_filters=-INFO",
        "--noshow_progress",
        *args[1:],
    ]
    print(f"{green}Running", " ".join(args), reset)
    if show_output:
        subprocess.run(args, check=True, cwd=ROOT)
        return

    status = subprocess.run(args, cwd=ROOT, capture_output=True)
    if status.returncode != 0:
        print(f"{red}Command failed: {' '.join(args)}{reset}")
        print(f"{red}STDERR:{reset}\n{status.stderr.decode()}")
        print(f"{red}STDOUT:{reset}\n{status.stdout.decode()}")
        raise ValueError("Command failed.")


def _gazelle() -> None:
    _bazel("run", "//:gazelle")


def _buildifier() -> None:
    _bazel("run", "//:buildifier")


def _buildifier_check() -> None:
    _bazel("run", "//:buildifier.check")


def _bzl_mod_tidy() -> None:
    _bazel("mod", "tidy")


def _bzl_test(target: str, verbose: bool) -> None:
    if verbose:
        _bazel("test", target, "--test_output=streamed")
        return

    _bazel("test", target)


def _go_mod_tidy() -> None:
    _bazel("run", "@rules_go//go", "--", "mod", "tidy")


def _go_get(package: str) -> None:
    _bazel("run", "@rules_go//go", "--", "get", package)


def _go_venv() -> None:
    go_venv = Path(ROOT / ".go")

    goroot = go_venv / "goroot"
    gopath = go_venv / "gopath"

    shutil.rmtree(go_venv, ignore_errors=True)

    output_base = Path(
        subprocess.check_output(
            ["./bazel", "info", "execution_root"], cwd=ROOT, text=True
        ).strip()
    )
    targets = {
        "@go_sdk//:bin/go": {"target": goroot / "bin"},
        "@go_sdk//:tools": {
            "target": goroot / "pkg/tool/darwin_arm64"
        },  # FIXME: target is different for linux
        "@go_sdk//:srcs": {"target": goroot, "trim_prefix": 2},
        "@com_github_go_delve_delve//cmd/dlv:dlv": {"target": gopath / "bin"},
        "@org_golang_x_tools_gopls//:gopls": {"target": gopath / "bin"},
    }
    _bazel("build", *targets.keys())
    for target, spec in targets.items():
        expr = subprocess.check_output(
            [
                "./bazel",
                "cquery",
                target,
                "--output=starlark",
                "--starlark:expr",
                "[(f.path, f.short_path) for f in target.files.to_list()]",
            ],
            text=True,
            cwd=ROOT,
        )
        expr = [item for item in expr.split("\n") if item][-1]
        query = eval(expr)
        dst_root: Path = spec["target"]
        trim_prefix: int | None = spec.get("trim_prefix")

        for path, short_path in query:
            src = output_base / path

            if trim_prefix:
                trimmed_short_pth = "/".join(short_path.split("/")[trim_prefix:])
                dst = dst_root / trimmed_short_pth
            else:
                dst = dst_root / src.name

            dst.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy(src, dst)

    go_env = {
        "GOROOT": str(goroot),
        "GOPATH": str(gopath),
        "GOPROXY": "direct",
    }
    # For debugging, just source this file.
    go_env_str = "\n".join(f"export {k}={v}" for k, v in go_env.items())
    (go_venv / "go.env").write_text(go_env_str)

    # Might be slow. THis is only needed for vscode.
    # Let vscode run this lazily.
    # go = goroot / "bin/go"
    # subprocess.run(
    #     [str(go), "mod", "download"],
    #     env={**os.environ, **go_env},
    #     cwd=ROOT,
    # )


def _py_lock() -> None:
    _bazel("run", "//:ruff", "--", "format", str(ROOT), f"--config={ROOT}/ruff.toml")
    _bazel(
        "run",
        "//:ruff",
        "--",
        "check",
        "--fix",
        str(ROOT),
        f"--config={ROOT}/ruff.toml",
    )
    _bazel("run", "//:requirements.update", show_output=False)
    _bazel("run", "//:gazelle_python_manifest.update")


def _py_venv() -> None:
    _bazel("run", "//:venv")


def _wrap_cmd(name: str, func: Callable[[], None]) -> None:
    @main.command(name=name)
    def _() -> None:
        func()


@click.group()
def main() -> None:
    pass


@main.command()
def lint() -> None:
    # Order matters.

    # Format BUILD files.
    _buildifier()

    # go deps
    _go_mod_tidy()

    # MODULE.bazel use_repo() update
    _bzl_mod_tidy()

    # GZL python and other python stuff.
    _py_lock()

    # Go BUILD generation
    _gazelle()


_wrap_cmd("buildifier", _buildifier)
_wrap_cmd("buildifier.check", _buildifier_check)
_wrap_cmd("gazelle", _gazelle)

_wrap_cmd("bzl.mod.tidy", _bzl_mod_tidy)


@main.command(name="bzl.test")
@click.argument("target")
@click.option("--verbose", is_flag=True)
def bzl_test(target: str, verbose: bool) -> None:
    _bzl_test(target=target, verbose=verbose)


_wrap_cmd("go.mod.tidy", _go_mod_tidy)
_wrap_cmd("go.venv", _go_venv)


@main.command(name="go.get")
@click.argument("package")
def go_get(package: str) -> None:
    _go_get(package)


_wrap_cmd("py.lock", _py_lock)
_wrap_cmd("py.venv", _py_venv)


@main.command(name="leetcode.new")
@click.argument("name")
def leetcode_new(name: str) -> None:
    shutil.copytree(ROOT / "leetcode/template", ROOT / "leetcode" / name)


if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt) as e:
        print(f"{red}Error:{reset} {e}")
        sys.exit(-1)
