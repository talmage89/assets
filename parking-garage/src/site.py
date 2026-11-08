"""Complete placeable town sites, with shared native meshes and images.

Garage meshes, context and actors remain named hierarchies. All photographic
review consumes these exports; the source model scene is never rendered.
"""
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
from build import export
from setting import town


def main():
    receipts=[]
    for seed in (101,202):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        p=json.loads(Path(f'build/garage-{seed}.json').read_text())
        bpy.ops.import_scene.gltf(filepath=str(Path(f'export/ParkingGarage-{seed}.gltf').resolve()))
        rt=next(o for o in bpy.context.scene.objects if o.parent is None)
        print('ASSEMBLE SITE',seed,flush=True);context=town(p,rt)
        report={k:v for k,v in context.items() if k!='root'}
        Path(f'build/actors-{seed}.json').write_text(json.dumps(report,indent=2)+'\n')
        path=Path(f'export/sites/ParkingGarageSite-{seed}.gltf')
        delivery=export(path,list(bpy.context.scene.objects))
        doc=json.loads(path.read_text());unique=sum(doc['accessors'][p['indices']]['count']//3 for m in doc['meshes'] for p in m['primitives'])
        receipts.append(dict(seed=seed,garage_triangles=p['garage_triangles'],**report,delivery=delivery,
            unique_mesh_triangles=unique,expanded_scene_triangles=G.triangles(bpy.context.scene.objects)))
        Path('build/sites.json').write_text(json.dumps(receipts,indent=2)+'\n')
        print('SITE EXPORTED',seed,unique,delivery['gltf_bytes']+delivery['bin_bytes'],flush=True)


if __name__=='__main__':main()
