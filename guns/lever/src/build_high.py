"""Original retained carved source and procedural finishes; no photo input."""
import argparse,sys,json
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'src'))
import lookdev
def main():
 p=argparse.ArgumentParser();p.add_argument('--wear',type=float,default=1)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 names=[o.name for o in bpy.context.scene.objects if o.type=='MESH' and not o.name.startswith('Standalone_')]
 with bpy.data.libraries.load(str(BASE/'build/sculpt.blend'),link=False) as (source,dest):dest.objects=names
 for high in dest.objects:
  if high is None:continue
  name=high.get('part_name',high.name.rsplit('.',1)[0]);target=bpy.data.objects.get(name)
  if target and len(high.data.polygons)>len(target.data.polygons):
   target.data=high.data.copy();target.vertex_groups.clear()
   group=target.vertex_groups.new(name=target['bone']);group.add(list(range(len(target.data.vertices))),1,'REPLACE')
  bpy.data.objects.remove(high,do_unlink=True)
 records=lookdev.assign(a.wear)
 bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
 (BASE/'build/delivery/finishes.json').write_text(json.dumps(records,indent=2))
 print('BRACKEN FINISHES',len(records),flush=True)
if __name__=='__main__':main()
