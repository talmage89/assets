"""Actual serialized construction, optional native landscape and shared-image costs."""
import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def component(path):
 doc=json.loads(path.read_text());counts=[sum(doc['accessors'][p['indices']]['count']//3 for p in m['primitives']) for m in doc['meshes']];draws=[len(m['primitives']) for m in doc['meshes']]
 return dict(path=str(path),unique_mesh_triangles=sum(counts),placed_triangles=sum(counts[n['mesh']] for n in doc['nodes'] if 'mesh' in n),placed_primitive_draws=sum(draws[n['mesh']] for n in doc['nodes'] if 'mesh' in n),materials=len(doc['materials']),gltf_bytes=path.stat().st_size,bin_bytes=sum((path.parent/q['uri']).stat().st_size for q in doc['buffers']),images=[(path.parent/q['uri']).resolve() for q in doc['images']])

def main():
 rows=[];all_maps={}
 for seed in (71,92):
  core=component(Path(f'export/Minigolf-{seed}.gltf'));plants=component(Path(f'export/Minigolf-{seed}-landscape.gltf'));maps={}
  for path in set(core['images']+plants['images']):
   w,h=Image.open(path).size;row=dict(uri=str(path.relative_to(ROOT)),size=[w,h],bytes=path.stat().st_size,compressed_full_mip_mib=w*h*4/3/1048576);maps[row['uri']]=row;all_maps[row['uri']]=row
  for part in (core,plants):part['images']=[str(p.relative_to(ROOT)) for p in part['images']]
  rows.append(dict(seed=seed,construction=core,landscape=plants,complete_placed_triangles=core['placed_triangles']+plants['placed_triangles'],geometry_json_bytes=sum(p['gltf_bytes']+p['bin_bytes'] for p in (core,plants)),shared_image_bytes=sum(q['bytes'] for q in maps.values()),shared_gpu_mib=sum(q['compressed_full_mip_mib'] for q in maps.values()),images=list(maps.values())))
 out=dict(scope='8-bpp block compression and full mips; URI-based caching across pieces and seeds. Core construction and optional native plants remain separate, co-located glTF components. Draws are unbatched placed primitives, not an engine performance promise.',courses=rows,union_images=list(all_maps.values()),union_gpu_mib=sum(q['compressed_full_mip_mib'] for q in all_maps.values()))
 Path('build/costs.json').write_text(json.dumps(out,indent=2));print([(r['seed'],r['construction']['placed_triangles'],r['landscape']['placed_triangles'],r['geometry_json_bytes'],r['shared_gpu_mib']) for r in rows])
if __name__=='__main__':main()
