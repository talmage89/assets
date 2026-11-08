"""Fresh-import verification of actual earth/edge return surface contacts."""
import json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check import bvh
rows={}
for seed in (101,202):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(f'export/Freeway-{seed}.gltf').resolve()));bpy.context.view_layer.update()
 soil=bvh([o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Cut slopes and drainage')]);edges=bvh([o for o in bpy.context.scene.objects if o.type=='MESH' and '__SeatedEdges' in o.name]);samples=json.loads(Path(f'build/edge-support-{seed}.json').read_text());burial=[];serialization=[]
 for sample in samples:
  p=Vector(sample['foot']);nearest=edges.find_nearest(p)[0];assert nearest is not None;serialization.append((nearest-p).length)
  q=soil.ray_cast(Vector((p.x,p.y,30)),Vector((0,0,-1)),60)[0];assert q is not None;burial.append(p.z-q.z)
 assert max(serialization)<.00004,(seed,max(serialization));assert max(burial)<.00004,(seed,max(burial))
 rows[str(seed)]=dict(samples=len(samples),measured_edge_foot_to_soil_max_gap_m=max(burial),minimum_burial_m=min(burial),source_to_imported_edge_max_discrepancy_m=max(serialization),scope='Each sampled exterior edge foot lies on/in actual soil; source-to-imported distance separately proves serialization. This does not certify a compacted geotechnical subgrade.')
Path('build/edge-audit.json').write_text(json.dumps(rows,indent=2));print('EDGE AUDIT PASSED',rows)
