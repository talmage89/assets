"""Sample true home hinges and reused lot hinges on imported geometry."""
import json,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit.motion import sweep,surface


def main():
    result={}
    for stem in ('SingleWide-120','SingleWide-147','SingleWide-168','DoubleWide-245','DoubleWide-228','DoubleWide-326'):
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path('export',stem+'.gltf').resolve()))
        pivots=[o for o in bpy.context.scene.objects if o.get('pivot_axis')=='Z']
        config=dict(MOTIONS=[dict(node=o.name,axis='Z',range=list(o['range_degrees']),step=2,tolerance_m=.001) for o in pivots])
        row=sweep(config);result[stem]=row
        Path('build/motion.json').write_text(json.dumps(result,indent=2))
        assert row['passed'],(stem,row)
        print('MOTION PASS',stem,len(row['motions']),flush=True)
    Path('build/motion.json').write_text(json.dumps(result,indent=2))

if __name__=='__main__':main()
