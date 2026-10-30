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
from forms import receiver, receiver_field, barrel_magazine, furniture, sights, bands
from mechanism import lever, bolt_lock_carrier, hammer_trigger_gate, ammunition, hammer_inlet
from dimensions import HEADS, PARENTS, SOCKETS, RIDING
from clips import build_clips
import interface


def source_hash():
    names=('build.py','clips.py','dimensions.py','forms.py','geometry.py','mechanism.py','interface.py','feed.py')
    paths=[Path(__file__).parent/name for name in names]+[ROOT/'guns/common/ammo_3030.py',ROOT/'guns/common/interface_v1_5.py']
    return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in paths)).hexdigest()


def finish_normals(ob):
    normals=[v.vector.copy() for v in ob.data.corner_normals]
    for f in ob.data.polygons:
        for i in f.loop_indices:
            if ob.name=='Receiver':
                p=ob.data.vertices[ob.data.loops[i].vertex_index].co
                distance,normal=receiver_field(p)
                if abs(distance)<.15 and normal.dot(f.normal)>.3:normals[i]=normal
            if ob.name in ('Receiver','Lever_FingerLoop') and abs(f.normal.x)>.999:
                normals[i]=__import__('mathutils').Vector((1 if f.normal.x>0 else -1,0,0))
            if ob.name=='Upper_Tang' and abs(f.normal.z)>.995:
                normals[i]=__import__('mathutils').Vector((0,0,1 if f.normal.z>0 else -1))
            if ob.name=='Rear_Buckhorn' and abs(f.normal.y)>.999:
                normals[i]=__import__('mathutils').Vector((0,1 if f.normal.y>0 else -1,0))
            if normals[i].dot(f.normal)<.08:normals[i]=f.normal.copy()
    ob.data.normals_split_custom_set(normals)


def repair_float_normals(ob):
    """Check the actual meter-space triangle winding after float conversion.

    A nanometer-wide Boolean sliver can change its normal after millimeter
    scaling. Do not let an old split normal point through that actual face.
    """
    from mathutils import Vector
    normals=[row.vector.copy() for row in ob.data.corner_normals];count=0
    for face in ob.data.polygons:
        if len(face.vertices)!=3:continue
        a,b,c=[ob.data.vertices[i].co for i in face.vertices]
        actual=(b-a).cross(c-a)
        if actual.length<1e-15:continue
        actual.normalize()
        for i in face.loop_indices:
            if normals[i].dot(actual)<.08:normals[i]=actual.copy();count+=1
    if count:ob.data.normals_split_custom_set(normals)
    return count


def finish(ob):
    tri=ob.modifiers.new('Export triangles','TRIANGULATE');tri.keep_custom_normals=True
    if ob.name in ('Upper_Tang','Stock'):tri.ngon_method='CLIP'
    M.apply(ob);finish_normals(ob)
    ob.data.transform(Matrix.Scale(.001,4));ob.matrix_world=Matrix.Identity(4)
    repair_float_normals(ob)


def transfer_carved_normals(target, reference, mapping):
    # M.apply evaluates and clears the whole modifier stack. Retain the rigid
    # binding when this also runs on the already-rigged dense stock source.
    bindings=[(m.name,m.object) for m in target.modifiers if m.type=='ARMATURE']
    for modifier in list(target.modifiers):
        if modifier.type=='ARMATURE':target.modifiers.remove(modifier)
    high=bpy.data.objects.new('Dense normal reference',reference);bpy.context.collection.objects.link(high)
    M.smooth(high,42)
    mod=target.modifiers.new('Carved source normal field','DATA_TRANSFER');mod.object=high
    mod.use_loop_data=True;mod.data_types_loops={'CUSTOM_NORMAL'}
    mod.loop_mapping=mapping;mod.use_max_distance=True;mod.max_distance=.8
    M.apply(target);bpy.data.objects.remove(high,do_unlink=True)
    for name,armature in bindings:
        modifier=target.modifiers.new(name,'ARMATURE');modifier.object=armature


def sculpt_normals():
    # Transfer the original cage's smooth normal field without adding vertices
    # or textures. This prevents reduction's irregular triangle areas from
    # making the compound walnut read as a collection of flat shaded patches.
    for name in ('Stock','Forend'):
        target=bpy.data.objects[name]
        transfer_carved_normals(target,G.NORMAL_HIGH.get(name,G.HIGH[name]),
            'POLYINTERP_NEAREST' if name=='Stock' else 'POLYINTERP_LNORPROJ')


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/lever.blend')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    G.palette();receiver();barrel_magazine();furniture();bands();sights();lever();bolt_lock_carrier();hammer_trigger_gate();hammer_inlet();ammunition()
    sculpt_normals()
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
        ob=bpy.data.objects[name];old[name]=ob.data;ob.data=mesh
        if name=='Stock':transfer_carved_normals(ob,G.NORMAL_HIGH[name],'POLYINTERP_NEAREST')
        mesh=ob.data
        finish_normals(ob);mesh.transform(Matrix.Scale(.001,4))
        ob.vertex_groups.clear();vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(mesh.vertices))),1,'REPLACE')
    bpy.ops.wm.save_as_mainfile(filepath=str(out.parent/'sculpt.blend'))
    for name,mesh in old.items():
        ob=bpy.data.objects[name];ob.data=mesh;ob.vertex_groups.clear()
        vg=ob.vertex_groups.new(name=ob['bone']);vg.add(list(range(len(mesh.vertices))),1,'REPLACE')
    # Preserve named source parts in the inspection GLB so both source and
    # imported surfaces can be independently audited at this gate. The accepted
    # rig will later use kit/export.py's atlas + EXPORT_SKIN_NAMES path.
    from guns.common.feed_sampling import export as feed_export
    from feed import BONES
    feed_export(out.with_suffix('.glb'),[arm]+G.PARTS+sockets,BONES)
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
