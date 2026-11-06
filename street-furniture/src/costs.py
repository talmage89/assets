"""Measure delivered geometry, material primitives, canonical image bytes/memory."""
import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def cost(path):
 d=json.loads(path.read_text());triangles=primitives=0;materials=set()
 for node in d.get('nodes',[]):
  if 'mesh' not in node:continue
  for p in d['meshes'][node['mesh']]['primitives']:
   assert p.get('mode',4)==4
   triangles+=d['accessors'][p['indices']]['count']//3;primitives+=1;materials.add(d['materials'][p['material']]['name'])
 images=[]
 for im in d.get('images',[]):
  p=(path.parent/im['uri']).resolve();size=Image.open(p).size;assert size[0]==size[1]
  images.append(dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,size=list(size),gpu_mib_8bpp_full_mips=size[0]*size[1]*4/3/1048576))
 return dict(path=str(path.relative_to(ROOT)),triangles=triangles,draw_primitives=primitives,materials=sorted(materials),gltf_bytes=path.stat().st_size,bin_bytes=sum((path.parent/b['uri']).stat().st_size for b in d['buffers']),images=images,gpu_mib_shared_subset=sum(i['gpu_mib_8bpp_full_mips'] for i in images))
rows={}
for folder,library in [(ROOT/'street-furniture/export','StreetFurniture'),(ROOT/'street-signs/export/set','RoadSigns')]:
 for p in sorted(folder.glob('*.gltf')):
  if p.stem!=library:rows[p.stem]=cost(p)
libs={name:cost(path) for name,path in [('StreetFurniture',ROOT/'street-furniture/export/StreetFurniture.gltf'),('RoadSigns',ROOT/'street-signs/export/set/RoadSigns.gltf')]}
images={i['path']:i for row in libs.values() for i in row['images']};report=dict(pieces=rows,libraries=libs,canonical_images=list(images.values()),unique_image_bytes=sum(i['bytes'] for i in images.values()),shared_gpu_mib=sum(i['gpu_mib_8bpp_full_mips'] for i in images.values()),scope=__doc__)
Path('build/costs.json').write_text(json.dumps(report,indent=2));lines=['# Measured final delivery costs','','GPU estimates assume 8 bpp per map with full mip chains, loaded once per canonical path. Primitives include genuinely separate moving owners. Texture PNG disk bytes are reported once below.','','| Piece | Triangles | Materials / draw primitives | glTF bytes | BIN bytes | Bound image GPU MiB |','| --- | ---: | ---: | ---: | ---: | ---: |']
for name,r in rows.items():lines.append(f"| {name} | {r['triangles']:,} | {len(r['materials'])} / {r['draw_primitives']} | {r['gltf_bytes']:,} | {r['bin_bytes']:,} | {r['gpu_mib_shared_subset']:.3f} |")
lines += ['','| Shared canonical image | Dimensions | Disk bytes | GPU MiB |','| --- | --- | ---: | ---: |']
for path,r in images.items():lines.append(f"| {path} | {r['size'][0]}² | {r['bytes']:,} | {r['gpu_mib_8bpp_full_mips']:.3f} |")
lines += ['',f"Both additions: {report['unique_image_bytes']:,} canonical image bytes; {report['shared_gpu_mib']:.6f} MiB once per scene."]
Path('build/costs.md').write_text('\n'.join(lines)+'\n');print('DELIVERY COSTS',len(rows),'pieces,',report['unique_image_bytes'],'image bytes,',report['shared_gpu_mib'],'MiB')
