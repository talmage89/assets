"""Round-two identity audit against a saved, independently built checkpoint.

The baseline is optional review evidence, never a build dependency. All named
accepted parts, rigid owners, rest bones and complete clip F-curves are exact.
The shoulder socket alone follows the revised butt-plate surface.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path
import bpy
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon as W

ACCEPTED=('Forend','Forend_Band','Forend_Band_Screw','Muzzle_Band','Muzzle_Band_Screw',
          'Barrel','Magazine_Tube','Magazine_Cap','Magazine_CapScrew',
          'Front_Ramp','Front_Blade','Front_Bead','Ramp_Screw',
          'Bolt_Body','Bolt_Extractor','Bolt_ExtractorHook','FiringPin_Tail',
          'Locking_Block','Bolt_LockAbutment','Bolt_LockAbutment.001',
          'Carrier_Cradle','Carrier_Arm','Carrier_Hub','Carrier_Web','Carrier_Pin',
          'Lever_PivotPin','Link_Rail','Link_Rail.001','Link_RearBridge','Link_PivotPin')


def capture(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    a=bpy.data.objects['LeverArmature'];W.pose(a,None,0)
    meshes={}
    for n in ACCEPTED:
        ob=bpy.data.objects[n];m=ob.data
        data=[np.asarray([v.co[:] for v in m.vertices],dtype='<f4').tobytes(),
              np.asarray([list(p.vertices) for p in m.polygons],dtype='<i4').tobytes(),
              np.asarray([v.vector[:] for v in m.corner_normals],dtype='<f4').tobytes()]
        if n=='Front_Bead':
            # Blender's parallel sphere triangulation can reorder identical
            # faces (also documented by repeat.py). Preserve every exact
            # oriented triangle corner and normal, independent of face order.
            triangles={}
            for p in m.polygons:
                ids=list(p.vertices);j=ids.index(min(ids));key=tuple(ids[j:]+ids[:j])
                corners=[tuple(m.corner_normals[i].vector) for i in p.loop_indices]
                triangles[key]=corners[j:]+corners[:j]
            data=[data[0],np.asarray(sorted(triangles),dtype='<i4').tobytes()]
        meshes[n]=dict(sha256=hashlib.sha256(b''.join(data)).hexdigest(),bone=ob['bone'])
        if n=='Front_Bead':meshes[n]['corner_normals']=[triangles[k] for k in sorted(triangles)]
    bones={b.name:dict(matrix=[list(r) for r in b.matrix_local],parent=b.parent.name if b.parent else None) for b in a.data.bones}
    clips={act.name:sorted((fc.data_path,fc.array_index,[(list(k.co),k.interpolation) for k in fc.keyframe_points])
                         for fc in W.fcurves(act)) for act in bpy.data.actions}
    sockets={o.name:[list(r) for r in o.matrix_world] for o in bpy.context.scene.objects if o.name.startswith('Socket_')}
    return dict(meshes=meshes,bones=bones,clips=clips,sockets=sockets)


def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',default='build/lever.blend')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);old=capture(Path(a.before));new=capture(Path(a.after))
    before_normals=old['meshes']['Front_Bead'].pop('corner_normals');after_normals=new['meshes']['Front_Bead'].pop('corner_normals')
    bead_delta=float(np.max(np.abs(np.asarray(before_normals)-np.asarray(after_normals))))
    assert bead_delta<2e-6,('Front bead normal field',bead_delta)
    for k in ('meshes','bones','clips'):assert old[k]==new[k],(k,[n for n in old[k] if old[k][n]!=new[k].get(n)])
    changed=[n for n in old['sockets'] if old['sockets'][n]!=new['sockets'].get(n)]
    assert changed==['Socket_Butt'],changed
    report=dict(passed=True,accepted_meshes=len(ACCEPTED),bones=len(new['bones']),clips=len(new['clips']),
        identity=['ordered vertices','ordered triangles','corner normals','rigid owners','rest bones','all clip keys/interpolation'],
        front_bead_normal_maximum_delta=bead_delta,front_bead_topology='exact oriented triangle set; face order independent',
        changed_sockets={n:dict(before=old['sockets'][n],after=new['sockets'][n]) for n in changed})
    Path('build/preserved.json').write_text(json.dumps(report,indent=2));print('PRESERVED',report)


if __name__=='__main__':main()
