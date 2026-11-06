"""Prove actual external-image cache identity across buildings and a repeat."""
import json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
bpy.ops.wm.read_factory_settings(use_empty=True);paths=sorted(Path('export').glob('*.gltf'));seen={};steps=[]
assert len(paths)==28
for path in paths+[paths[0]]:
 bpy.ops.import_scene.gltf(filepath=str(path.resolve()));images=[im for im in bpy.data.images if im.source=='FILE' and im.filepath];lookup={}
 for im in images:
  key=str(Path(bpy.path.abspath(im.filepath)).resolve());assert key not in lookup,'Duplicate canonical image';lookup[key]=im
  if key in seen:assert seen[key]==im.as_pointer(),'Image identity changed'
  seen[key]=im.as_pointer()
 steps.append(dict(building=path.stem,image_datablocks=len(images)))
assert len(seen)==11
Path('build/resource-check.json').write_text(json.dumps(dict(passed=True,steps=steps,shared_images=11,rgba8_pixel_bytes=sum(im.size[0]*im.size[1]*4 for im in images),scope='Actual stock Blender import; engine compression/caching remains importer policy'),indent=2)+'\n')
print('RESOURCE PASS',len(paths),'buildings plus repeat share exactly eleven canonical image datablocks')
