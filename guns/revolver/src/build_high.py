"""Dense sculpted grip/hammer and procedural look; all coordinates are original."""
import argparse,sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'src'))
import lookdev
p=argparse.ArgumentParser();p.add_argument('--wear',type=float,default=.85)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
with bpy.data.libraries.load(str(BASE/'build/sculpt.blend'),link=False) as (source,destination):
 destination.objects=['Grip_RubberMold','Hammer_Body']
for dense in destination.objects:
 name=dense.get('part_name',dense.name).split('.')[0]
 ob=bpy.data.objects[name];ob.data=dense.data.copy()
 ob.vertex_groups.clear();g=ob.vertex_groups.new(name=ob['bone']);g.add(list(range(len(ob.data.vertices))),1,'REPLACE')
 bpy.data.objects.remove(dense,do_unlink=True)
lookdev.assign(a.wear)
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
