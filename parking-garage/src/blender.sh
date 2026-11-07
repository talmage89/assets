#!/bin/sh
# Serialize Blender work on the shared machine; inherited render locks are kept.
set -eu
if [ "${ASSETS_GPU_HELD:-0}" = 1 ]; then
    exec blender -t 4 "$@"
fi
exec "$(dirname "$0")/../../kit/with_gpu.sh" blender -t 4 "$@"
