"""Read-only imports and linked scene instances of the native library."""
from pathlib import Path
import math
import bpy
from mathutils import Matrix
from geo import ROOT,root
CACHE={}


def template(path):
    path=Path(path).resolve()
    if path in CACHE:return CACHE[path]
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path))
    obs=sorted(set(bpy.context.scene.objects)-before,key=lambda o:o.name)
    for ob in obs:ob.hide_render=True;ob.hide_set(True);ob['civic_template']=True
    CACHE[path]=obs;return obs


def place(path,name,p=(0,0,0),yaw=0,select=None,parent=None):
    obs=template(path);chosen=obs
    if select:
        r=next(o for o in obs if o.name.split('.')[0]==select)
        chosen=[r]+list(r.children_recursive);inv=r.matrix_world.inverted()
    else:inv=Matrix.Identity(4)
    rt=root(name,parent,p);rt.rotation_euler.z=math.radians(yaw)
    rt['library_source']=str(Path(path).resolve().relative_to(ROOT));rt['category']='vegetation' if '/trees/' in str(path) or '/shrubs/' in str(path) else 'native'
    copies={o:o.copy() for o in chosen}
    for src,cp in copies.items():
        bpy.context.collection.objects.link(cp);cp.parent=copies.get(src.parent,rt)
        cp.matrix_basis=src.matrix_basis.copy() if src.parent in copies else inv@src.matrix_world
        cp.name=name+'__'+src.name;cp.hide_render=False;cp.hide_set(False);cp.pop('civic_template',None)
    return rt


def clear():
    for obs in CACHE.values():
        for ob in obs:
            if ob.name in bpy.data.objects:bpy.data.objects.remove(ob,do_unlink=True)
    CACHE.clear()
