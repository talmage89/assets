"""Byte-exact delivery geometry/rig/layout comparison for the three-fix review.

Run in Blender with --before pointing at a saved accepted export directory.
Image payloads and the intentionally revised standalone case are excluded.
Every rifle/magazine accessor (including normals, UVs, animation and skin data),
node, skin layout, mesh primitive layout and material assignment must agree.
"""
import argparse,json,sys,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.gltf import GLB
p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True);p.add_argument('--out',type=Path,default=BASE/'build/correction-identity.json');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
rows={}
for name in ('bolt','magazine_loaded','magazine_empty'):
 old=GLB(a.before/(name+'.glb'));new=GLB(BASE/'export'/(name+'.glb'))
 for key in ('nodes','meshes','skins','animations','scenes','scene','materials','textures','samplers'):
  assert old.json.get(key)==new.json.get(key),(name,key,'delivery layout changed')
 assert len(old.json['accessors'])==len(new.json['accessors'])
 for i in range(len(old.json['accessors'])):
  assert old.accessor(i).tobytes()==new.accessor(i).tobytes(),(name,'accessor',i)
 rows[name]=dict(passed=True,identical_accessors=len(old.json['accessors']),scope='All geometry, normals, UVs, indices, weights, bind matrices, clips, nodes, materials and layout; image bytes intentionally excluded')
case=GLB(BASE/'export/case.glb');tri=sum(len(case.accessor(p['indices']))//3 for m in case.json['meshes'] for p in m['primitives']);assert tri<=800
rows['case']=dict(triangles=tri,intentional_change='round shoulder, 40-sided mouth, same 14 axial profile stations and physical dimensions')
a.out.write_text(json.dumps(dict(passed=True,comparisons=rows),indent=2));print(a.out.read_text())
