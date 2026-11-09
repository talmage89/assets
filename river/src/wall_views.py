"""Close wall inspections and identical-camera accepted-version controls."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from plan import generate
from package import sha,bundle
import render as current


def definitions():
    p=generate(101)
    def edge(y):return p.center(y)-p.halfwidth(y)
    return dict(
        outfall=dict(location=(edge(-36)-2.0,-36,2.30),target=(edge(-33)-4.20,-33,1.22),lens=42),
        ladder=dict(location=(edge(-56)-1.65,-56,2.30),target=(edge(-49)-4.1,-49,2.40),lens=40))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=1280);ap.add_argument('--samples',type=int,default=32)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);recipe=sha(__file__)
    accepted=Path('build/accepted-rebuild/river')
    spec=importlib.util.spec_from_file_location('_river_wall_before',accepted/'src/render.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    for before in (False,True):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        source=(accepted if before else Path('.'))/'export/RiverCrossing-101.gltf'
        bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
        module=old if before else current
        module.restore_water();module.restore_native_leaves();scene,camera=module.setup(a.width,a.samples)
        walk=bpy.data.objects['FloodwallTrailAndAccess']
        ground=BVHTree.FromPolygons([walk.matrix_world@v.co for v in walk.data.vertices],
            [list(f.vertices) for f in walk.data.polygons],all_triangles=True)
        for name,definition in definitions().items():
            path=Path('renders/wall-before' if before else 'renders/wall-details')/(name+'.png')
            meta=path.with_suffix('.json')
            if meta.exists() and json.loads(meta.read_text()).get('wall_recipe_sha256')!=recipe:meta.unlink()
            module.shot(scene,camera,definition,path,source,a.width,a.samples)
            row=json.loads(meta.read_text());row.update(wall_recipe_sha256=recipe,image_sha256=sha(path))
            eye=Vector(definition['location']);hit=ground.ray_cast(eye,Vector((0,0,-1)),5)[0]
            assert hit is not None and 1.50<eye.z-hit.z<1.85,('Wall camera has no standing floor',name,eye,hit)
            row['measured_eye_above_walk_m']=eye.z-hit.z
            if before:row['accepted_revision']='4f09582'
            assert row['bundle_sha256']==bundle(source)
            assert row['camera']==json.loads(json.dumps(definition))
            meta.write_text(json.dumps(row,indent=2)+'\n')


if __name__=='__main__':main()
