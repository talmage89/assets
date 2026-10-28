"""Retained compound molds, generated pebbling and original finish shaders."""
import sys,json,argparse,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,noise
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'src'))
import lookdev
p=argparse.ArgumentParser();p.add_argument('--wear',type=float,default=1)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
with bpy.data.libraries.load(str(BASE/'build/smg.blend'),link=False) as (src,dst):
 dst.objects=[n for n in src.objects if n.startswith('HIGH_')]
for dense in dst.objects:
 if not dense.get('low_target'):continue
 ob=bpy.data.objects[dense['low_target']]
 if ob.name.startswith('Grip_TexturePanel'):
  # The retained dense relief only represents the outer molded skin. Carry
  # the accepted game's hidden backing and finite rim into its bake source;
  # their cap/return normals otherwise point away from that skin entirely.
  side=-1 if '-1' in ob.name else 1
  backing=ob.copy();backing.data=ob.data.copy();backing.name=ob.name+'_Return'
  bpy.context.collection.objects.link(backing)
  bm=bmesh.new();bm.from_mesh(backing.data)
  bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.normal.x*side>.30],context='FACES')
  bm.to_mesh(backing.data);bm.free()
 ob.data=dense.data.copy();ob.vertex_groups.clear()
 if ob.name.startswith('Grip_TexturePanel'):
  side=-1 if '-1' in ob.name else 1
  for v in list(ob.data.vertices)[:97*193]:
   # Smooth the manufactured peaks where the palm works the panel. This
   # changes only the retained dense relief that transfers into the normal.
   z=v.co.z;y=v.co.y
   contact=min(1,max(0,(z+.050)/.010),max(0,(.020-z)/.010))
   relief=.00012*noise.noise(Vector((y*900,z*900,side*7.1)))
   v.co.x-=side*relief*.70*contact*a.wear
 group=ob.vertex_groups.new(name='Root');group.add(list(range(len(ob.data.vertices))),1,'REPLACE')
 bpy.data.objects.remove(dense,do_unlink=True)
from high_ammo import replace
replace()
records=lookdev.assign(a.wear)
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
(BASE/'build/delivery/finishes.json').write_text(json.dumps(records,indent=2))
