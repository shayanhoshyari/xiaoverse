import click
import subprocess
import click
from pathlib import Path
import os
from collections.abc import Callable


ROOT = Path(os.environ["MONOREPO_PATH"])

green: str = "\033[32m"
reset: str = "\033[00m"

def _bazel(*args: str, show_output: bool =True) -> None:
    args = ["./bazel", args[0], "--ui_event_filters=-INFO", "--noshow_progress", *args[1:]]
    print(f'{green}Running', ' '.join(args), reset)
    if show_output:
        subprocess.run(args, check=True, cwd=ROOT)
        return

    subprocess.run(args, check=True, cwd=ROOT, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


def _gazelle() -> None:
    _bazel("run", "//:gazelle")

def _buildifier() -> None:
    _bazel("run", "//:buildifier")

def _buildifier_check() -> None:
    _bazel("run", "//:buildifier.check")

def _bzl_mod_tidy() -> None:
    _bazel("mod", "tidy")

def _go_mod_tidy() -> None:
    _bazel("run", "@rules_go//go", "--", "mod", "tidy")

def _go_get(package: str) -> None:
    _bazel("run", "@rules_go//go", "--", "get", package)

def _py_lock() -> None:
    _bazel("run", "//:requirements.update", show_output=False)

def _py_venv() -> None:
    _bazel("run", "//:venv")

def _py_format() -> None:
    _bazel("run", "//:ruff", "--", "format", ".")
    _bazel("run", "//:ruff", "--", "check", "--fix")

def _wrap_cmd(name: str, func : Callable[[], None]) -> None:
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

    # Go BUILD generation
    _gazelle()

    # Python!
    _py_format()
    _py_lock()



_wrap_cmd("buildifier", _buildifier)
_wrap_cmd("buildifier.check", _buildifier_check)
_wrap_cmd("bzl.mod.tidy", _bzl_mod_tidy)
_wrap_cmd("gazelle", _gazelle)

_wrap_cmd("go.mod.tidy", _go_mod_tidy)

@main.command(name="go.get")
@click.argument("package")
def go_get(package: str) -> None:
    _go_get(package)

_wrap_cmd("py.lock", _py_lock)
_wrap_cmd("py.venv", _py_venv)
_wrap_cmd("py.format", _py_format)

if __name__ == "__main__":
    main()
