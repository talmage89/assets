"""The additional library audit is separate from the existing final sign gate."""
import json,sys,math
from pathlib import Path
import bpy
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'street-furniture/src'))
from check import audit
report=audit(Path('export/set/RoadSigns.gltf'),json.loads(Path('build/set/manifest.json').read_text()),True)
# Independently fit the imported perforation centers below the blank. This
# catches a bend applied in a joined child's frame while extras claim 3deg.
root=bpy.data.objects['RoadSign_speed25'];points=[]
for ob in root.children_recursive:
    if ob.type=='MESH':
        matrix=root.matrix_world.inverted()@ob.matrix_world
        points += [tuple(matrix@v.co) for v in ob.data.vertices if .5<(matrix@v.co).z<2.0]
points=np.asarray(points);slope=float(np.polyfit(points[:,2],points[:,0],1)[0])
angle=math.degrees(math.atan(slope));assert abs(angle-3.0)<.03,angle
report['measured_bent_post_angle_degrees']=angle
Path('build/set/check.json').write_text(json.dumps(report,indent=2));print('SIGN CHECKPOINT PASSED',len(report['rows']),'assemblies')
