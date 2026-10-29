"""Accepted game shapes, rest frames and every half-frame pose stay unchanged.

Only the requested front retainer and its seated sling-loop endpoints differ.
Fingerprints are recorded from the accepted pre-round source, never from the
revised source during an ordinary build. This proves preservation, not fit.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,weapon_verify as V
from interface import CLIPS
CHANGED={'Handguard_Retainer363','Handguard_SlingLoop'}
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default=str(BASE/'build/ak.blend'));p.add_argument('--record',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 bpy.ops.wm.open_mainfile(filepath=str(Path(args.source).resolve()));arm=bpy.data.objects['R39Armature'];W.pose(arm,None,0)
 meshes={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or not ob.get('asset_set') or ob.get('bake_only') or ob.name in CHANGED:continue
  meshes[ob.name]=dict(bone=ob['bone'],vertices=len(ob.data.vertices),triangles=len(ob.data.polygons),
   geometry=digest([[list(v.co) for v in ob.data.vertices],[list(f.vertices) for f in ob.data.polygons]]),
   normals=digest([list(row.vector) for row in ob.data.corner_normals]))
 bones={b.name:dict(parent=b.parent.name if b.parent else None,rest=[list(row) for row in b.matrix_local]) for b in arm.data.bones}
 sockets={o.name:[list(row) for row in o.matrix_world] for o in bpy.context.scene.objects if o.name.startswith('Socket_')}
 # Actual affine matrices at all accepted verification samples, not clip labels.
 samples=[(c,i*.5) for c,s in CLIPS.items() for i in range(s['frames']*2+1)]
 captured=V.capture(arm,samples,list(sockets));poses=digest(captured)
 row=dict(meshes=meshes,bones=bones,sockets=sockets,affine_samples=len(samples),poses=poses,
          allowed_changed_parts=sorted(CHANGED),scope='Accepted source meshes/normals, bone/socket frames and sampled animation affine matrices; fit and appearance checked separately.')
 accepted=BASE/'src/accepted_look_round2.json'
 if args.record:
  assert not accepted.exists(),'Do not replace an accepted baseline during a revision'
  accepted.write_text(json.dumps(row,indent=2));print('RECORDED',len(meshes),'accepted meshes',flush=True)
 else:
  expected=json.loads(accepted.read_text());assert row==expected,'Accepted geometry, normals, frames or sampled clips changed'
  result=dict(passed=True,unchanged_meshes=len(meshes),unchanged_mesh_names=sorted(meshes),affine_samples=len(samples),allowed_changed_parts=sorted(CHANGED),scope=row['scope'])
  (BASE/'build/round2-preservation.json').write_text(json.dumps(result,indent=2));print('PRESERVED',len(meshes),'meshes;',len(samples),'affine poses',flush=True)
if __name__=='__main__':main()
