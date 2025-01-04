#!/bin/bash

# Main task runner.

yellow="\033[33m"
reset="\033[00m"
green="\033[32m"
magenta="\033[35m"
red="\033[31m"
cyan="\033[36m"

function bazel() {
    echo  -e "Running ${green}\"./bazel $@\"${reset}"
    ./bazel $1 --ui_event_filters=-INFO --noshow_progress ${@:2}
}

function main() {
    action=$1
    args=${@:2}

    if [[ $action = "lint" ]]; then
        bazel run @rules_go//go -- mod tidy
        bazel mod tidy
        bazel run //:buildifier
        bazel run //:ruff -- format . && bazel run //:ruff -- check --fix .
        return
    fi

    if [[ $action = "buildifier" ]]; then
        bazel run //:buildifier
        return
    fi

    if [[ $action = "buildifier.check" ]]; then
        bazel run //:buildifier.check
        return
    fi

    if [[ $action = "bzl.mod.tidy" ]]; then
        bazel mod tidy
        return
    fi

    if [[ $action = "go.mod.tidy" ]]; then
        bazel run @rules_go//go -- mod tidy
        return
    fi

    if [[ $action = "gazelle" ]]; then
        bazel run //:gazelle
        return
    fi

    if [[ $action = "py.lock" ]]; then
        bazel run  //:requirements.update
        return
    fi

    if [[ $action = "py.venv" ]]; then
        bazel run //:venv
        return
    fi

    if [[ $action = "py.lint" ]]; then
        bazel run //:ruff -- format . && bazel run //:ruff -- check --fix .
        return
    fi

    echo -e "${red}Invalid command: $@${reset}"
    exit -1
}


main "$@"