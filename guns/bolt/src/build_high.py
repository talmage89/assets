"""Apply original finish fields to the accepted sculpt and relief sources."""
import argparse,sys,json,hashlib
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'src'))
import lookdev
p=argparse.ArgumentParser();p.add_argument('--wear',type=float,default=.85)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
# Mesh-only loading cannot introduce an armature, socket, clip or foreign asset.
names=[o.name for o in bpy.context.scene.objects if o.type=='MESH' and o.parent and o.parent.type=='ARMATURE' and o.get('bone')]
with bpy.data.libraries.load(str(BASE/'build/sculpt.blend'),link=False) as (src,dst):
 dst.objects=list(names)
for part,dense in zip(names,dst.objects):
 target=bpy.data.objects[part]
 target.data=dense.data.copy();target.vertex_groups.clear()
 group=target.vertex_groups.new(name=target['bone']);group.add(list(range(len(target.data.vertices))),1,'REPLACE')
 bpy.data.objects.remove(dense,do_unlink=True)
records=lookdev.assign(a.wear)
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
(BASE/'build/delivery/finishes.json').write_text(json.dumps(records,indent=2))
print('B24 HIGH FINISHES',len(records),flush=True)
