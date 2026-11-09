"""Exact construction parameters for the X220/H120 regular subdivision cage.

These cages author UVs as integer grid coordinates, with straight boundaries.
After n subdivisions every parameter is an exact multiple of 2**-n. Blender's
threaded face-varying evaluation introduces small, process-dependent rounding
errors; using those errors as geometry changes later clipping and reduction.
Restore the known lattice, checking its premise before changing any coordinate.
This does not quantize positions, normals, or the eventual delivery atlas.
"""
import numpy as np


def restore(ob, levels):
    if not isinstance(levels, int) or not 0 <= levels <= 8:
        raise ValueError('Expected an authored subdivision depth from 0 to 8')
    layer = ob.data.uv_layers.active
    if layer is None:
        raise ValueError('Missing regular construction chart: ' + ob.name)
    values = np.empty(len(layer.data) * 2, dtype=np.float32)
    layer.data.foreach_get('uv', values)
    if not np.all(np.isfinite(values)):
        raise ValueError('Nonfinite construction parameters: ' + ob.name)
    scale = 2 ** levels
    exact = np.rint(values * scale) / scale
    error = float(np.max(np.abs(values - exact), initial=0))
    # Observed native drift is below 0.00002 chart units. A changed cage or
    # nonregular UV chart must fail rather than silently snapping its design.
    if error > .0001:
        raise ValueError(f'{ob.name}: construction chart is off its lattice by {error}')
    layer.data.foreach_set('uv', exact)
    return error
