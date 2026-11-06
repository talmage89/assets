"""Additional real mesh budget checks beyond the four curated block plans."""
import json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from plan import generate,REGIONS
from geometry import palette
from graphics import generate as signs
from building import Building
rows=[]
for region in REGIONS:
 for seed in (17,81,193):
  p=generate(seed,region,count=4)
  for lot in p['lots']:
   bpy.ops.wm.read_factory_settings(use_empty=True);sheet,layout=signs(Path('build/signs-sweep'));root,obs,doors=Building(lot,palette(sheet),layout).build()
   n=0
   for ob in obs:ob.data.calc_loop_triangles();n+=len(ob.data.loop_triangles)
   cap=30000 if lot['stories']==3 or lot['corner'] else 20000
   assert n<=cap,(lot['id'],n,cap)
   rows.append(dict(id=lot['id'],triangles=n,budget=cap))
Path('build/mesh-sweep.json').write_text(json.dumps(dict(passed=True,buildings=rows),indent=2)+'\n');print('MESH SWEEP PASS',len(rows),'additional generated buildings')
