"""Use Ground's own sod-fringe builder and alpha sheet, without a new texture."""
import importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
_CACHE=None


def modules():
    global _CACHE
    if _CACHE:return _CACHE
    old=sys.path[:];names=('dimensions','textures','organic');saved={n:sys.modules.pop(n,None) for n in names}
    sys.path.insert(0,str(ROOT/'ground/src'))
    try:
        def load(name,path):
            spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
        base=load('_trailer_native_ground',ROOT/'ground/src/build.py')
        additions=load('_trailer_native_ground_additions',ROOT/'ground/src/additions.py');additions.b=base
        _CACHE=base,additions;return _CACHE
    finally:
        sys.path[:]=old
        for n,value in saved.items():
            sys.modules.pop(n,None)
            if value:sys.modules[n]=value


def edges(parent,paths,seed,lib):
    from site import getsitepackages
    from geometry import ROOT
    objects=lib.load(ROOT/'ground/export/Ground.glb');mats={ma.name.split('.')[0]:ma for ob in objects if ob.type=='MESH' for ma in ob.data.materials}
    base,additions=modules();base.MATS['GroundTrim']=mats['GroundTrim'];base.MATS['GroundFoliage']=mats['GroundFoliage']
    ob=additions.grass_edges(parent,paths,seed);ob['library_source']='ground/src/additions.py::grass_edges';return ob
