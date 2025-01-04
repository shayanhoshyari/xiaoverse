"""
This script is a shim that allows running bazel python targets by vscode debugger.
"""

import os
import runpy
import shlex
import subprocess
from pathlib import Path
from typing import cast

BAZEL_WORKSPACE = Path(__file__).resolve().parents[1]
BAZEL_BIN = "bazel"


def run_bazel_target(target: str) -> None:
    # Make sure the target is built.
    subprocess.check_call([BAZEL_BIN, "build", target], cwd=BAZEL_WORKSPACE)

    # What we could put together to get the binary and CWD it should run from.
    query = subprocess.check_output(
        [
            BAZEL_BIN,
            "cquery",
            "--ui_event_filters=-info,-debug",
            "--noshow_progress",
            "--output=starlark",
            "--starlark:expr=[target.files_to_run.executable.path, target.files_to_run.runfiles_manifest.path]",
            target,
        ],
        text=True,
        cwd=BAZEL_WORKSPACE,
    )

    execroot = subprocess.check_output([BAZEL_BIN, "info", "execution_root"], text=True, cwd=BAZEL_WORKSPACE)
    execroot = execroot.strip()

    
    # Not sure how to properly deal with this, but if the target is used as a tool, it might
    # return multiple values (on in out/...-fastabuild one in out/...opt-exec)
    # This is just a heuristic to get the last line
    last_query = [item for item in query.split("\n") if item][-1]

    binary, runfiles_manifest = cast(tuple[str, str], eval(last_query))

    binary_abs = BAZEL_WORKSPACE / binary
    runfiles_manifest_abs = BAZEL_WORKSPACE / runfiles_manifest

    # Bazel runs things in execroot.
    os.chdir(execroot)
    # Set the runfile manifest, in case the binary uses runfiles
    os.environ["RUNFILES_MANIFEST_FILE"] = str(runfiles_manifest_abs)
    # Run the binary!
    runpy.run_path(str(binary_abs), run_name="__main__")


if __name__ == "__main__":
    import sys

    # For vscode to be able to pass arguments in one go from command line, we need to
    # read them as one string :(
    if len(sys.argv) != 2:
        raise ValueError(
            'Expected only and only one argument, syntax: "<bazel target> <args>" as a single bash argument.'
        )

    args = shlex.split(sys.argv[1])

    target = args.pop(0)
    # Modify sys.argv, so when we transition to run the actual executable, it will have
    # all the arguments, minus the one that belongs to this script.
    sys.argv[1:] = args

    run_bazel_target(target)