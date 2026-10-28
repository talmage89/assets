"""Measure the actual exported-source surfaces used by the display-value audit."""
import sys,json
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit import weapon as W,motion
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
W.pose(bpy.data.objects['B24Armature'],None,0)
queries={
 'stock':('Stock_Mold',[(.265,.047),(.315,.047),(.315,.055),(.265,.055)]),
 'steel':('Receiver',[(.050,.067),(.076,.067),(.076,.075),(.050,.075)]),
 'steel_barrel':('Barrel',[(.620,.064),(.720,.064),(.720,.069),(.620,.069)]),
 'steel_barrel_lit':('Barrel',[(.620,.070),(.720,.070),(.720,.075),(.620,.075)]),
 'steel_barrel_full':('Barrel',[(.620,.054),(.720,.054),(.720,.076),(.620,.076)]),
 'steel_receiver_full':('Receiver',[(.050,.058),(.076,.058),(.076,.079),(.050,.079)]),
 'scope_dark':('Scope_Body',[(.005,.108),(.033,.108),(.033,.113),(.005,.113)]),
 'scope':('Scope_Body',[(.005,.121),(.033,.121),(.033,.126),(.005,.126)])}
rows={}
for name,(part,yz) in queries.items():
 tree=motion.surface(bpy.data.objects[part])['tree'];points=[]
 for y,z in yz:
  hit,normal,index,distance=tree.ray_cast(Vector((.06,y,z)),Vector((-1,0,0)),.12)
  assert hit is not None,(name,y,z)
  points.append(list(hit))
 rows[name]=dict(part=part,points_m=points,method='actual finalized triangle BVH, +X to -X surface rays at declared Y/Z stations')
(BASE/'build/value-loci.json').write_text(json.dumps(rows,indent=2))
print('B24 VALUE SURFACE LOCI',rows,flush=True)
