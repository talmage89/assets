"""Rebuild read-only library fence/light construction into playground-local products.

Adapters select quick review finishes only. Existing deliveries are never opened
for writing. No copied geometry implementation or second fence/light design.
"""
import importlib.util,sys,math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def fences(parent,plan,F):
    saved={k:sys.modules.get(k) for k in ('dimensions','modular','mesh_tile')};oldpath=list(sys.path)
    try:
        folder=ROOT/'fences/chain-link/src';sys.path[:0]=[str(folder),str(ROOT/'fences/src')]
        sys.modules['dimensions']=load('fence_dimensions',folder/'dimensions.py')
        sys.modules['modular']=load('fence_modular',ROOT/'fences/src/modular.py')
        sys.modules['mesh_tile']=load('fence_tile',folder/'mesh_tile.py')
        C=load('playground_library_chain',folder/'build.py');b=C.Chain(False,.35)
        x0,y0,x1,y1=plan['surface']
        for i in range(4):
            before=set(bpy.context.scene.objects);b.section('Chain_Section');obs=set(bpy.context.scene.objects)-before;rt=next(o for o in obs if o.get('static_root'))
            b.post(rt,'Library fence line post',-1.524,False)
            if i==3:b.post(rt,'Library fence last post',1.524,False)
            for o in list(rt.children_recursive):
                if o.type=='MESH' and not o.get('allow_boundary'):F.own(o,o.parent,'zinc')
            F.finish(rt);rt.parent=parent;rt.location=(x0+2+i*3.048,y1+.75,0);rt['library_source']='fences/chain-link/src/build.py'
    finally:
        sys.path[:]=oldpath
        for k,v in saved.items():
            if v is None:sys.modules.pop(k,None)
            else:sys.modules[k]=v

def light(parent,plan,F):
    saved=sys.modules.get('dimensions');oldpath=list(sys.path)
    try:
        folder=ROOT/'street-light/src';sys.modules['dimensions']=load('light_dimensions',folder/'dimensions.py');sys.path[:0]=[str(folder)]
        L=load('playground_library_light',folder/'build.py')
        # Main's own argument function normally clears the scene. Supply the
        # equivalent requested quality with no reset so the assembly can be reused.
        from types import SimpleNamespace
        L.arguments=lambda:SimpleNamespace(quality='game',wear=.2,out='build/context/LibraryLight.blend')
        class ReuseBuild(L.Build):
            def save(self,*args):pass
        L.Build=ReuseBuild
        L.finish=lambda wear,kind:F.M['Frame'];L.thread_finish=lambda *args:F.M['Frame']
        before=set(bpy.context.scene.objects);L.main();added=set(bpy.context.scene.objects)-before
        rt=next(o for o in added if o.name.startswith('StreetLight') and o.type=='EMPTY')
        for o in list(rt.children_recursive):
            if o.type=='MESH':F.own(o,o.parent,'zinc')
        F.finish(rt);rt.parent=parent;rt.location=(plan['surface'][2]+1.4,plan['walk_y']+1.3,0);rt['library_source']='street-light/src/build.py'
    finally:
        sys.path[:]=oldpath
        if saved is None:sys.modules.pop('dimensions',None)
        else:sys.modules['dimensions']=saved
