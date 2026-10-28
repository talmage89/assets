"""Substitute the dense frame and author finishes on the prepared rest assembly."""
import argparse,sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
import lookdev

def main():
 p=argparse.ArgumentParser();p.add_argument('--wear',type=float,default=.72)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 with bpy.data.libraries.load(str(BASE/'build/sculpt.blend'),link=False) as (source,destination):
  destination.objects=['Frame_Grip']
 dense=destination.objects[0];mesh=dense.data.copy();bpy.data.objects.remove(dense,do_unlink=True)
 frame=bpy.data.objects['Frame_Grip'];frame.data=mesh
 frame.vertex_groups.clear();group=frame.vertex_groups.new(name='Root')
 group.add(list(range(len(mesh.vertices))),1,'REPLACE')
 lookdev.assign(a.wear)
 bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
 print('DENSE LOOKDEV FRAME',sum(len(f.vertices)-2 for f in mesh.polygons),flush=True)

if __name__=='__main__':main()
