"""Sample actual exported solids with kit.motion; alpha sheets are not solids."""
import sys,json,math
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils import Vector
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
from kit import model as G,motion as K


def split(ob):
    """Separate connected closed components for intended-bearing identification.

    This is derived from the exported indices, never regenerated construction.
    Zero-thickness leaf/wire/fabric surfaces are explicitly omitted.
    """
    # glTF splits coincident vertices at shading/UV seams; weld only the audit
    # copy within .2 micrometres before testing manifold solid components.
    ob.data=ob.data.copy();bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=2e-7)
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    me=ob.data;verts=list(me.vertices);adj={v.index:set() for v in verts};faces=[]
    for f in me.polygons:
        ma=me.materials[f.material_index]
        if any(s in ma.name for s in ('ChainLink','GardenPlants')):continue
        faces.append(f)
        for i,j in zip(f.vertices,list(f.vertices)[1:]+[f.vertices[0]]):adj[i].add(j);adj[j].add(i)
    remaining={i for i,n in adj.items() if n};components=[]
    while remaining:
        stack=[remaining.pop()];c=set(stack)
        while stack:
            for j in adj[stack.pop()]:
                if j in remaining:remaining.remove(j);c.add(j);stack.append(j)
        fs=[f for f in faces if f.vertices[0] in c];used=sorted(c);idx={old:i for i,old in enumerate(used)}
        edge={}
        for f in fs:
            for a,b in zip(f.vertices,list(f.vertices)[1:]+[f.vertices[0]]):k=tuple(sorted((a,b)));edge[k]=edge.get(k,0)+1
        if any(n!=2 for n in edge.values()):continue
        new=G.mesh(ob.name+'_solid_'+str(len(components)),[me.vertices[i].co[:] for i in used],[[idx[i] for i in f.vertices] for f in fs]);new.parent=ob.parent;new.matrix_basis=ob.matrix_basis.copy();new['asset_set']='MotionAudit';components.append(new)
    bpy.data.objects.remove(ob,do_unlink=True);return components


def main():
    reports={}
    for seed in (117,229,341):
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(f'export/checkpoint/Garden_{seed}.gltf').resolve()))
        gate=next(o for o in bpy.context.scene.objects if o.name.startswith('GateLeaf'));gate.rotation_mode='XYZ';gate.rotation_euler.z=0;bpy.context.view_layer.update()
        # Include placed shed doors as well as the gate. An isolated native
        # assembly test cannot prove clearance from this garden's plots/tools.
        pivots=[gate]+[o for o in bpy.context.scene.objects if o.name.startswith('Door_') and o.type=='EMPTY']
        # Include nearby exported fixed pieces, not only the matching prefab.
        selected=[]
        for ob in list(bpy.context.scene.objects):
            if ob.type!='MESH':continue
            pts=[ob.matrix_world@v.co for v in ob.data.vertices]
            if any(K.owned(ob,pivot) or any((v-pivot.matrix_world.translation).length<2.5 for v in pts) for pivot in pivots):selected.extend(split(ob))
        config=dict(MOTIONS=[dict(node=pivot.name,axis='Z',range=list(pivot['range_degrees']),step=5,tolerance_m=.0004,allow=[]) for pivot in pivots])
        reports[str(seed)]=K.sweep(config)
        assert reports[str(seed)]['passed'],reports[str(seed)]
    # Native shed doors: closed exported components, real bores and pins.
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path('build/context/shed.glb').resolve()));bpy.context.view_layer.update()
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH':split(ob)
    specs=[]
    for pivot in [o for o in bpy.context.scene.objects if o.name.startswith('Door_') and o.type=='EMPTY']:
        specs.append(dict(node=pivot.name,axis='Z',range=list(pivot['range_degrees']),step=5,tolerance_m=.0005,allow=[]))
    reports['shed']=K.sweep(dict(MOTIONS=specs));assert reports['shed']['passed'],reports['shed']
    result=dict(passed=True,scope='exported solids; gate and placed shed-door neighbourhoods, plus native shed assembly',reports=reports,
                limitation='5 degree sampled sweep; intentional alpha sheets omitted; no continuous-time certification')
    Path('build/motion.json').write_text(json.dumps(result,indent=2));print('MOTION CHECK PASSED',flush=True)


if __name__=='__main__':main()
