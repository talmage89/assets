#!/bin/sh
# Child inherits lock FD 9; callers cannot accidentally release it before Blender exits.
set -eu
: "${ASSETS_GPU_LOCK:?Set ASSETS_GPU_LOCK to the shared GPU lock path}"
mkdir -p "$(dirname "$ASSETS_GPU_LOCK")"
exec 9>"$ASSETS_GPU_LOCK"
flock 9
export ASSETS_GPU_HELD=1
exec "$@"
