"""Find actual collision-free stack pitch on two re-imported delivered meshes."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.assembly import distance
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(a.source).resolve()))
base=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='TrafficCone')
upper=base.copy();bpy.context.collection.objects.link(upper);rest=base.matrix_world.copy()
def measure(pitch):
    upper.matrix_world=rest.copy();upper.matrix_world.translation+=Vector((0,0,pitch));bpy.context.view_layer.update()
    return distance(base,upper)
lo=.04;hi=.16
assert measure(lo)[1]=='triangle-surface intersection','Search lower bound does not intersect'
assert measure(hi)[1]!='triangle-surface intersection','Search upper bound still intersects'
for _ in range(19):
    middle=(lo+hi)/2
    if measure(middle)[1]=='triangle-surface intersection':lo=middle
    else:hi=middle
pitch=hi+.0001;gap,method=measure(pitch)
r=dict(passed=method!='triangle-surface intersection',source=a.source,first_collision_free_pitch_m=hi,demonstrated_pitch_m=pitch,measured_sampled_surface_gap_m=gap,method=method,search_resolution_m=(.16-.04)/2**19,safety_margin_m=.0001,scope='physical evaluated triangle surfaces of two imported GLB instances; not nominal bore arithmetic or serialization')
Path(a.out).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));assert r['passed']
