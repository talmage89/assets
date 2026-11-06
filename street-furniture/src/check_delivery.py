"""Final atlas/image/channel audit, independent of the source recipe."""
import hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import uv
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path('export/StreetFurniture.gltf').resolve()))
objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
# Importers call the first exported channel UVMap. It is the baked atlas,
# independently verified from the actual external glTF's TEXCOORD_0 binding.
r=uv.report(objects,2048,layer='UVMap');assert r['degenerate_uv_triangles']==0 and r['outside_triangles']==0 and r['overlap_fraction']<1e-5,r
assert r['density_px_m']['5']>55 and r['density_px_m']['50']>75,r['density_px_m']
doc=json.loads(Path('export/StreetFurniture.gltf').read_text());images=[]
for im in doc['images']:
 p=Path('export')/im['uri'];image=Image.open(p);expected=1024 if 'Graphics' in im['uri'] else 2048
 assert image.size==(expected,expected),(p,image.size)
 images.append(dict(uri=im['uri'],bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),dimensions=image.size,gpu_mib_full_mips_8bpp=expected**2*4/3/1048576))
assert len(images)==4
for mat in doc['materials']:
 p=mat['pbrMetallicRoughness'];assert 'baseColorTexture' in p and 'metallicRoughnessTexture' in p and 'normalTexture' in mat
 if 'GraphicsGlazing' in mat['name']:
  assert 'occlusionTexture' not in mat
  tr=mat['extensions']['KHR_materials_transmission'];assert 'transmissionTexture' in tr
  assert doc['textures'][tr['transmissionTexture']['index']]['source']==doc['textures'][p['metallicRoughnessTexture']['index']]['source']
  assert tr['transmissionTexture'].get('texCoord',0)==0
  assert p['baseColorTexture'].get('texCoord',0)==1
 else:assert mat['occlusionTexture']['index']==p['metallicRoughnessTexture']['index']
# The actual lower plate is measured from imported front plate vertices.
rt=bpy.data.objects['BusStop'];pts=[rt.matrix_world.inverted()@o.matrix_world@v.co for o in rt.children_recursive if o.type=='MESH' for v in o.data.vertices]
route=[p.z for p in pts if abs(p.x)>.22 and 2.10<p.z<2.37];bottom=min(route);assert abs(bottom-2.1336)<1e-5,bottom
receipt=ROOT/'build/street-furniture-preservation.json';baseline=json.loads(receipt.read_text()) if receipt.exists() else {};changed=[p for p,h in baseline.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed,changed
report=dict(passed=True,atlas={k:v for k,v in r.items() if k!='island_measurements'},images=images,shared_gpu_mib=sum(i['gpu_mib_full_mips_8bpp'] for i in images),measured_route_plate_bottom_m=bottom,preserved_files=len(baseline),scope=__doc__)
Path('build/delivery-check.json').write_text(json.dumps(report,indent=2));print('FINAL DELIVERY PASSED',report['shared_gpu_mib'],'MiB; route bottom',bottom)
