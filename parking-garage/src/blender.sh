#!/bin/sh
# CPU construction/export does not occupy the GPU. Make's render/bake recipes
# acquire the shared lock once around their whole set before calling Blender.
set -eu
exec blender -t 2 "$@"
