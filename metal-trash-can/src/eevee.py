"""The exported metal uses a procedural studio reflection capture in Eevee."""
import sys,json
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import studio
original=studio.add_studio

def captured_studio():
 camera=original()
 probe=bpy.data.lightprobes.new('Procedural studio sphere capture','SPHERE')
 probe.influence_distance=5;probe.clip_start=.06;probe.clip_end=30
 ob=bpy.data.objects.new('Studio reflection capture',probe);bpy.context.collection.objects.link(ob);ob.location=(0,-.70,.60);ob['studio']=True
 return camera

if __name__=='__main__':
 studio.add_studio=captured_studio;studio.main()
 args=sys.argv[sys.argv.index('--')+1:];folder=Path(args[args.index('--out')+1]);path=folder/'shots.json';meta=json.loads(path.read_text())
 for row in meta.values():row['reflection_lighting']='Procedural studio SPHERE capture; no external environment image'
 path.write_text(json.dumps(meta,indent=2))
