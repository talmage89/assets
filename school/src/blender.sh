#!/bin/sh
set -eu
# Modeling and measured checks use CPU only. The Make render/matches recipes
# acquire kit/with_gpu.sh before any Cycles operation.
exec blender "$@"
