#!/bin/sh
# Full presentations use a CPU controller and one Blender process per set.
# Model/check calls and explicitly selected views execute Blender directly.
set -eu
render=0
filtered=0
previous=''
for argument do
    if [ "$previous" = '--python' ] && [ "$argument" = 'src/render.py' ]; then render=1; fi
    case "$argument" in --shots|--sheet) filtered=1;; esac
    previous="$argument"
done
if [ "$render" = 1 ] && [ "$filtered" = 0 ]; then
    exec python3 "$(dirname "$0")/render_driver.py" "$@"
fi
exec "${BLENDER_REAL:-blender}" "$@"
