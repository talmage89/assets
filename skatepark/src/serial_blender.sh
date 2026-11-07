#!/bin/sh
# Model/check invocations share the same machine-wide lock as bakes/renders.
set -eu
if [ "${ASSETS_GPU_HELD:-0}" = 1 ]; then
    exec blender "$@"
fi
exec "$(dirname "$0")/../../kit/with_gpu.sh" blender "$@"
