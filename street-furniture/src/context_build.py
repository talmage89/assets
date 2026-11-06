"""Presentation-only library utility run, generated inside this family's build.

Imports the library's actual pole construction and catenary functions; never
opens any existing delivery for writing. Procedural materials need no utility
family rebuild or duplicate shipped texture allocation.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'utility/src')]
from kit import model as G
import surfaces as U
U.material=lambda:None
U.uv_object=lambda *a,**k:None
from construction import palette,pole,M
from plan import pole_spec
from span import sample
bpy.ops.wm.read_factory_settings(use_empty=True);palette()
# Stock library albedos survive glTF. Procedural source nodes would otherwise
# become an unsupported white material when exported solely for context.
poles=[]
for i,x in enumerate((23,65,107,149,191,233,275)):
    s=pole_spec(kind='transformer' if i in (1,4) else 'tangent',seed=1010+i);s.update(comm_count=2,bank=1,light=False)
    a=pole('ContextUtility_'+str(i),s);a.root.location=(x,5.65,.04);a.root.rotation_euler.z=math.pi/2;poles.append(a)
bpy.context.view_layer.update()
for i,(a,b) in enumerate(zip(poles,poles[1:])):
    for key in a.sockets:
        if not (key.startswith('Primary_') or key in ('Neutral','CommDrop')) or key not in b.sockets:continue
        p=a.sockets[key].matrix_world.translation;q=b.sockets[key].matrix_world.translation
        diameter=.0101 if key.startswith('Primary') else .012 if key=='Neutral' else .016
        points,_=sample(p,q,.70 if key.startswith('Primary') else .95,max_step=1.5)
        G.smooth(G.tube('Library utility catenary '+str(i)+' '+key,points,diameter/2,M['Aluminum'] if key.startswith('Primary') else M['Cable'],6),180)
out=Path('build/context');out.mkdir(parents=True,exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str((out/'UtilityContext.glb').resolve()),export_format='GLB',export_animations=False)
