"""Acquire the kit's shared flock inside a single Blender process.

The LOD builder cannot hold a second Blender parent while baking. This uses the
same advisory flock as with_gpu.sh, only around GPU work, and restores the
held-lock environment marker on success or failure.
"""
from contextlib import contextmanager
import fcntl
import os
from pathlib import Path


@contextmanager
def locked():
    if os.environ.get('ASSETS_GPU_HELD')=='1':
        yield
        return
    path=Path(os.environ['ASSETS_GPU_LOCK']);path.parent.mkdir(parents=True,exist_ok=True)
    previous=os.environ.get('ASSETS_GPU_HELD')
    with path.open('a') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        os.environ['ASSETS_GPU_HELD']='1'
        try:yield
        finally:
            if previous is None:os.environ.pop('ASSETS_GPU_HELD',None)
            else:os.environ['ASSETS_GPU_HELD']=previous
            fcntl.flock(handle,fcntl.LOCK_UN)
