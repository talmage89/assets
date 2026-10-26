"""Find actual collision-free stack pitch on two re-imported delivered meshes."""
import argparse,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.assembly import distance,surface
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(a.source).resolve()))
base=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='TrafficCone')
tree=surface(base)[2];walls=[]
for z in [.067,.1,.2,.3,.4,.5,.6,.662,.67,.675,.683,.69,.697,.704]:
    for i in range(24):
        direction=Vector((math.cos(i*math.tau/24),math.sin(i*math.tau/24),0));origin=Vector((0,0,z));hits=[]
        for _ in range(4):
            hit=tree.ray_cast(origin,direction,.3)[0]
            if hit is None:break
            hits.append(hit.copy());origin=hit+direction*1e-6
        assert len(hits)==2,f'Expected inner/outer wall at z={z}, angle={i}: {len(hits)} hits'
        walls.append((hits[1]-hits[0]).length)
assert min(walls)>.002,'Shell thinner than 2 mm at sampled radial sections'
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
r['radial_wall_sections']=len(walls);r['minimum_sampled_radial_wall_m']=min(walls)
Path(a.out).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));assert r['passed']
