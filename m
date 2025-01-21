#!/bin/bash

# Wrapper for ./bazel run //:m -- $@

set -e

# Export so the script also sees it.
MONOREPO_PATH=$(dirname "$(realpath "$0")")
cd $MONOREPO_PATH
./bazel run --ui_event_filters=-INFO //:m -- $@

