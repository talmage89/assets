"""Lossless standalone proof against full-atlas snapshots at the same bone frames."""
import hashlib,json,sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from kit import export,detachable_verify as D
from kit.gltf import GLB

def main():
 out=BASE/'build/delivery/full-atlas';out.mkdir(parents=True,exist_ok=True)
 config=out/'config.py'
 config.write_text('import runpy\nglobals().update(runpy.run_path('+repr(str(BASE/'src/export_config.py'))+'))\nDETACHABLES=[{k:v for k,v in row.items() if k not in ("texture_size","texture_clusters")} for row in DETACHABLES]\n')
 sys.argv=['blender','--','--source',str(BASE/'build/delivery/finalized.blend'),'--textures',str(BASE/'textures'),
  '--asset','Covey26','--config',str(config),'--out',str(out/'sxs.glb'),'--report',str(out/'export.json')]
 export.main();rows={}
 for name,count in [('shell',752),('hull',480)]:
  old=out/(name+'.glb');path=BASE/'export'/(name+'.glb');layout=BASE/'build/delivery/detachables'/name/'layout.json'
  g=GLB(path);triangles=sum(len(g.accessor(p['indices']))//3 for m in g.json['meshes'] for p in m['primitives'])
  assert triangles==count and len(g.json['materials'])==1
  assert sorted(g.image(i)[24] for i in range(3))==[8,8,16]
  row=dict(comparison=D.compare(old,path),audit=D.audit(path,BASE/'textures','Covey26',layout,gun=BASE/'export/sxs.glb'),
   mip_bleed=D.mip_bleed(path,BASE/'textures','Covey26',layout,gun=BASE/'export/sxs.glb'),
   triangles=triangles,bytes=path.stat().st_size,full_atlas_bytes=old.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),png_bits=[g.image(i)[24] for i in range(3)])
  assert row['audit']['size'] in (512,1024)
  rows[name]=row
 report=dict(passed=True,main_sha256=hashlib.sha256((BASE/'export/sxs.glb').read_bytes()).hexdigest(),
  scope='Full atlas versus subset: oriented geometry, tangent frames, material factors, density, surface pixels, samplers and pointwise L0-L3 mip bleed. Assembly contacts are a separate check.',items=rows)
 (BASE/'build/delivery/detachable-proof.json').write_text(json.dumps(report,indent=2));print('DETACHABLE PROOF',[(n,r['triangles'],r['audit']['size'],r['bytes']) for n,r in rows.items()])
if __name__=='__main__':main()
