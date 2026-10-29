"""Independent constant-material ownership audit on eroded UV interiors.

Zero ray misses do not prove that a ray hit the intended neighboring part.
At this form gate each single-material part has a known original constant
albedo. Compare the baked image with those independent target assignments.
Multi-material ammunition is excluded because its physical material edges need
separate masks; its geometry and canonical atlas are checked elsewhere.
"""
import sys,json,hashlib
from pathlib import Path
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit.image_io import read_png,srgb_to_linear

def measure(image_path=None):
 source=BASE/'build/delivery/finalized.blend'
 path=Path(image_path) if image_path else BASE/'build/baked/4k/T_Covey26_BaseColor.png'
 bpy.ops.wm.open_mainfile(filepath=str(source))
 actual=srgb_to_linear(read_png(path)[:,:,:3]);height,width=actual.shape[:2]
 labels=Image.new('L',(width,height),0);draw=ImageDraw.Draw(labels);palette=[(0,0,0)];names=[]
 for ob in sorted(bpy.context.scene.objects,key=lambda o:o.name):
  if ob.type!='MESH' or not ob.get('asset_set'):continue
  indices={f.material_index for f in ob.data.polygons}
  if len(indices)!=1:continue
  bs=ob.data.materials[indices.pop()].node_tree.nodes.get('Principled BSDF')
  assert bs and not bs.inputs['Base Color'].is_linked,'Audit only accepts original inspection constants'
  palette.append(tuple(bs.inputs['Base Color'].default_value[:3]));names.append(ob.name)
  index=len(names);assert index<255
  layer=ob.data.uv_layers['BakeUV'];ob.data.calc_loop_triangles()
  for triangle in ob.data.loop_triangles:
   draw.polygon([(float(layer.data[i].uv.x)*width,(1-float(layer.data[i].uv.y))*height) for i in triangle.loops],fill=index)
 low=np.array(labels.filter(ImageFilter.MinFilter(5)));high=np.array(labels.filter(ImageFilter.MaxFilter(5)));ids=np.array(labels)
 inside=(low==high)&(ids>0);selected=ids[inside]
 error=np.max(abs(actual[inside]-np.array(palette)[selected]),axis=1)
 counts=np.bincount(selected,minlength=len(palette));bad=np.bincount(selected[error>.01],minlength=len(palette))
 maxima=np.zeros(len(palette));np.maximum.at(maxima,selected,error)
 rows=[dict(part=name,interior_texels=int(counts[i]),wrong_constant_texels=int(bad[i]),maximum_linear_rgb_error=float(maxima[i])) for i,name in enumerate(names,1)]
 return dict(passed=not bool(bad.sum()),scope='Single-material original constants; two-pixel erosion at 4096; linear RGB tolerance .01',
  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),basecolor_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
  parts=len(names),interior_texels=int(counts.sum()),wrong_constant_texels=int(bad.sum()),records=rows)
if __name__=='__main__':
 report=measure();(BASE/'build/delivery/projection-ownership.json').write_text(json.dumps(report,indent=2))
 print('PROJECTION OWNERSHIP',report['passed'],report['parts'],report['interior_texels'],report['wrong_constant_texels'],flush=True)
 assert report['passed'],[r for r in report['records'] if r['wrong_constant_texels']]
