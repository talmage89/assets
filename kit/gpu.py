"""Cycles device discovery with an explicit CPU fallback and the flock wrapper."""
import os
import warnings
import bpy


def enable():
    if os.environ.get('ASSETS_GPU_HELD')!='1':
        raise RuntimeError('Cycles requires kit/with_gpu.sh (GPU lock not held)')
    prefs=bpy.context.preferences.addons['cycles'].preferences
    for kind in ('OPTIX','CUDA'):
        try:
            prefs.compute_device_type=kind;prefs.refresh_devices()
            devices=[d for d in prefs.devices if d.type==kind]
            if devices:
                for d in prefs.devices:d.use=d.type==kind
                bpy.context.scene.cycles.device='GPU'
                print('ASSETS_GPU',kind,[d.name for d in devices]);return kind
        except (TypeError,RuntimeError) as e:print('GPU probe:',kind,e)
    bpy.context.scene.cycles.device='CPU'
    warnings.warn('No Cycles OptiX/CUDA device available; falling back to CPU (slower).',
                  RuntimeWarning, stacklevel=2)
    return 'CPU'
