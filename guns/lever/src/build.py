"""PD Bracken L20: reproducible visual form checkpoint. Blender 5.2."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
import bpy
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as M, weapon as W
from guns.common import ammo_3030
import geometry as G
from forms import receiver, barrel_magazine, furniture, sights, bands
from mechanism import lever, bolt_lock_carrier, hammer_trigger_gate, ammunition, hammer_inlet
from dimensions import HEADS, PARENTS, SOCKETS, RIDING
from clips import build_clips
import interface


def source_hash():
    names=('build.py','clips.py','dimensions.py','forms.py','geometry.py','mechanism.py','interface.py')
    paths=[Path(__file__).parent/name for name in names]+[ROOT/'guns/common/ammo_3030.py',ROOT/'guns/common/interface_v1_5.py']
    return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in paths)).hexdigest()


def finish(ob):
    tri=ob.modifiers.new('Export triangles','TRIANGULATE');tri.keep_custom_normals=True;M.apply(ob)
    # Resolve only normals opposing triangle winding. Small Boolean patches
    # cannot carry a broad inherited smooth fan across a machining corner.
    normals=[v.vector.copy() for v in ob.data.corner_normals]
    for f in ob.data.polygons:
        for i in f.loop_indices:
            if ob.name=='Receiver' and abs(f.normal.x)>.94 and f.area>1:
                normals[i]=__import__('mathutils').Vector((1 if f.normal.x>0 else -1,0,0))
            if normals[i].dot(f.normal)<.08:normals[i]=f.normal.copy()
    ob.data.normals_split_custom_set(normals)
    ob.data.transform(Matrix.Scale(.001,4));ob.matrix_world=Matrix.Identity(4)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/lever.blend')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    G.palette();receiver();barrel_magazine();furniture();bands();sights();lever();bolt_lock_carrier();hammer_trigger_gate();hammer_inlet();ammunition()
    for ob in G.PARTS:finish(ob)
    arm=W.armature('LeverArmature',{k:tuple(v*.001 for v in pos) for k,pos in HEADS.items()},PARENTS)
    arm['base_interface_version']=interface.VERSION;arm['interface_version']=interface.SUPPLEMENT_VERSION
    arm['capabilities']=json.dumps(interface.CAPABILITIES,sort_keys=True)
    for ob in G.PARTS:W.rigid_bind(ob,arm,ob['bone'])
    sockets=W.sockets(arm,{k:tuple(v*.001 for v in pos) for k,pos in SOCKETS.items()},RIDING)
    build_clips(arm)
    sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.render.fps=60
    sc['stage']='FORM CHECKPOINT: constant materials; no finish/UV/bake acceptance'
    sc['generator_sha256']=source_hash()
    W.pose(arm,'Idle',0)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    counts={ob.name:len(ob.data.polygons) for ob in G.PARTS}
    W.pose(arm,None,0)
    # Dense cages remain original, separately rebuildable sources, ready for
    # the later kit selected-to-active bake. This gate does not bake them.
    old={}
    for name,mesh in G.HIGH.items():
        ob=bpy.data.objects[name];old[name]=ob.data;mesh.transform(Matrix.Scale(.001,4));ob.data=mesh
        ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(mesh.vertices))),1,'REPLACE')
    bpy.ops.wm.save_as_mainfile(filepath=str(out.parent/'sculpt.blend'))
    for name,mesh in old.items():
        ob=bpy.data.objects[name];ob.data=mesh;ob.vertex_groups.clear()
        vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(mesh.vertices))),1,'REPLACE')
    # Preserve named source parts in the inspection GLB so both source and
    # imported surfaces can be independently audited at this gate. The accepted
    # rig will later use kit/export.py's atlas + EXPORT_SKIN_NAMES path.
    W.export(out.with_suffix('.glb'),[arm]+G.PARTS+sockets)
    for fired,name in [(False,'cartridge'),(True,'case')]:
        parts=ammo_3030.build(name,(0,0,0),G.MAT,G.reg,fired=fired,headstamp=True)
        for ob in parts:finish(ob)
        ob=W.joined_copy(parts,'Bracken_'+name);ob.parent=None
        W.export(out.parent/(name+'.glb'),[ob],animations=False)
        counts[name]=len(ob.data.polygons)
        bpy.data.objects.remove(ob,do_unlink=True)
        for ob in parts:bpy.data.objects.remove(ob,do_unlink=True)
    data=dict(total=sum(v for k,v in counts.items() if k not in ('cartridge','case')),
              parts={k:v for k,v in counts.items() if k not in ('cartridge','case')},
              cartridge=counts['cartridge'],case=counts['case'])
    (out.parent/'triangles.json').write_text(json.dumps(data,indent=2))
    (out.parent/'interface.json').write_text(json.dumps(dict(version=interface.SUPPLEMENT_VERSION,base_version=interface.VERSION,
        fps=60,capabilities=interface.CAPABILITIES,states=interface.STATES,clips=interface.CLIPS,sockets_mm=SOCKETS),indent=2))
    print('LEVER TRIANGLES',data['total'],'CARTRIDGE',data['cartridge'],'CASE',data['case'],flush=True)


if __name__=='__main__':main()
