"""Inspect critical printed-face texels through rays on the delivered GLB.

This gates an observed failure: a source print facing inward baked a unit but
inverted normal and black AO. Unit-length normal checks alone cannot detect it.
No texture repair or filling occurs here.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--textures',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(a.source).resolve()))
ob=bpy.data.objects['HeaterBodyMesh'];me=ob.data;me.calc_loop_triangles()
verts=[ob.matrix_world@v.co for v in me.vertices];tris=[tuple(t.vertices) for t in me.loop_triangles]
tree=BVHTree.FromPolygons(verts,tris,all_triangles=True);uv=me.uv_layers['UVMap']
images={n:Image.open(Path(a.textures)/('T_PatioHeater_'+n+'.png')).convert('RGB') for n in ('BaseColor','Normal','ORM')}
rows=[]
for iz in range(29):
 z=1.660+iz*.005
 for ix in range(11):
  x=-.025+ix*.005
  if x*x+(z-1.757)**2<.025**2 or x*x+(z-1.691)**2<.013**2:continue
  hit,normal,index,distance=tree.ray_cast(Vector((x,-.10,z)),Vector((0,1,0)),.06)
  if hit is None or abs(hit.y+.0529)>.0003:continue
  tri=me.loop_triangles[index]
  mapped=barycentric_transform(hit,*(verts[i] for i in tri.vertices),*(Vector((*uv.data[i].uv,0)) for i in tri.loops))
  size=images['Normal'].width;pixel=(max(0,min(size-1,int(mapped.x*size))),max(0,min(size-1,int((1-mapped.y)*size))))
  rows.append({n:im.getpixel(pixel) for n,im in images.items()})
assert len(rows)>80,'Missing delivered control face samples'
zs=sorted(r['Normal'][2] for r in rows);ao=sorted(r['ORM'][0] for r in rows)
contrast=max(max(r['BaseColor']) for r in rows)-min(min(r['BaseColor']) for r in rows)
passed=zs[len(zs)//20]>220 and ao[len(ao)//2]>128 and contrast>80
report=dict(passed=passed,source=a.source,scope='Actual GLB surface ray hits mapped into delivered UV0/images',samples=len(rows),normal_blue_p5=zs[len(zs)//20],ao_median=ao[len(ao)//2],basecolor_byte_contrast=contrast,thresholds=dict(normal_blue_p5_min=220,ao_median_min=128,basecolor_contrast_min=80))
Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if not passed:raise RuntimeError('Delivered printed face lost orientation, exposure or label contrast')
