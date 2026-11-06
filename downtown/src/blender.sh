#!/bin/sh
# Serialize this family's Blender work with the shared machine's GPU work.
set -eu
if [ "${ASSETS_GPU_HELD:-0}" = 1 ]; then
    exec blender "$@"
fi
DOWNTOWN_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
exec "$DOWNTOWN_ROOT/kit/with_gpu.sh" blender "$@"
