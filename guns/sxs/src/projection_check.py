"""Independent 4K surface-identity witness for variable procedural finishes.

The same selected-to-active projection bakes an independently assigned part ID
into a temporary alpha channel. The GPU witness is checked against UV-triangle
ownership, then omitted from the delivered RGB base color. This catches wrong
neighbors even when their material colors happen to be similar.
"""
import sys,json,hashlib
from pathlib import Path
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path.insert(0,str(ROOT))
from kit.image_io import read_png

def measure(image_path=None):
 source=BASE/'build/delivery/finalized.blend';path=Path(image_path) if image_path else BASE/'build/baked/4k/projection-owner.png'
 bpy.ops.wm.open_mainfile(filepath=str(source));actual=np.rint(read_png(path)[:,:,0]*255).astype(np.uint8)
 height,width=actual.shape;labels=Image.new('L',(width,height));draw=ImageDraw.Draw(labels)
 parts=sorted([o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')],key=lambda o:o.name)
 for index,ob in enumerate(parts,1):
  ob.data.calc_loop_triangles();uv=ob.data.uv_layers['BakeUV']
  for triangle in ob.data.loop_triangles:
   draw.polygon([(uv.data[j].uv.x*width,(1-uv.data[j].uv.y)*height) for j in triangle.loops],fill=index)
 ids=np.asarray(labels);lo=np.asarray(labels.filter(ImageFilter.MinFilter(5)));hi=np.asarray(labels.filter(ImageFilter.MaxFilter(5)))
 inside=(lo==hi)&(ids>0);bad=inside&(actual!=ids)
 rows=[dict(part=ob.name,interior_texels=int(np.count_nonzero(inside&(ids==i))),
  wrong_owner_texels=int(np.count_nonzero(bad&(ids==i)))) for i,ob in enumerate(parts,1)]
 return dict(passed=not bool(bad.any()),scope='Independent source-part emission witness against target UV triangles; two-pixel erosion at 4096; exact 8-bit identity',
  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),witness_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
  parts=len(parts),interior_texels=int(inside.sum()),wrong_owner_texels=int(bad.sum()),records=rows)
if __name__=='__main__':
 report=measure();(BASE/'build/delivery/projection-ownership.json').write_text(json.dumps(report,indent=2))
 print('PROJECTION OWNERSHIP',report['passed'],report['parts'],report['interior_texels'],report['wrong_owner_texels'])
 assert report['passed'],[r for r in report['records'] if r['wrong_owner_texels']]
