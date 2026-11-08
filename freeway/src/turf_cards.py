"""Dense, rooted crossed grass cards; deterministic spatial density falloff.

Only the near ROW needs geometric parallax. The whole alignment retains its
textured base; small repeated glTF meshes are shared across spatial batches.
"""
import math,random
import bpy
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
import geom as Q
from textures import rect

def plant(p,parent):
 vertices=[];faces=[]
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  root=ob
  while root.parent:root=root.parent
  if root.get('module_kind') not in ('roadway','ramp','arterial'):continue
  if root.name in ('RoadStraight','RoadCurve','RoadBankTransition','RampBranch'):continue
  offset=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
  ob.data.calc_loop_triangles()
  for face in ob.data.loop_triangles:
   if ob.data.materials[face.material_index] not in (Q.M['Asphalt'],Q.M['Concrete'],Q.M.get('WheelPolish'),Q.M.get('AsphaltPolish')):continue
   pts=[vertices[offset+i] for i in face.vertices]
   if (pts[1]-pts[0]).cross(pts[2]-pts[0]).z>0:faces.append(tuple(offset+i for i in face.vertices))
 paving=BVHTree.FromPolygons(vertices,faces,all_triangles=True)
 # The curved scene's median is a separate graded skin, above its far field.
 # Sampling only the cut-slope mesh would bury all median cards underneath it.
 vertices=[];faces=[]
 bpy.context.view_layer.update()
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or not ob.name.startswith(('Cut slopes and drainage','WideMedian__Mesh')):continue
  offset=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
  ob.data.calc_loop_triangles();faces.extend(tuple(offset+i for i in f.vertices) for f in ob.data.loop_triangles)
 soil=BVHTree.FromPolygons(vertices,faces,all_triangles=True)
 rng=random.Random(p.seed+919);groups={};count=0
 # Tiles contain many clumps, avoiding one object/draw for each tuft. Eight
 # tile patterns repeat as linked meshes; rotations break their local rhythm.
 templates=[]
 for pattern in range(8):
  b=Q.Batch('Grass clump tile %02d'%pattern)
  for j in range(16):
   x=rng.uniform(-.65,.65);y=rng.uniform(-.65,.65);h=rng.uniform(.10,.23)
   shade=1 if pattern<4 else .80
   tint=(rng.uniform(.78,1)*shade,rng.uniform(.83,1)*shade,rng.uniform(.65,.87)*shade,1)
   for angle in (rng.uniform(0,math.pi),rng.uniform(math.pi,math.tau)):
    d=Vector((math.cos(angle),math.sin(angle),0))*.16;v=Vector((x,y,0))
    pts=[v-d,v+d,v+d+Vector((.035,0,h)),v-d+Vector((.035,0,h))]
    u0,v0,u1,v1=rect('weed');b.face(pts,'GrassCard',uv=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)],tint=tint)
  ob=b.finish();templates.append(ob)
 # A high-density inspected area fades over 120m into the textured base.
 # No geometry is spent in distant lots or beyond the principal corridor.
 for sindex in range(-140,161):
  s=sindex*1.30+rng.uniform(-.45,.45)
  for uindex in range(-65,66):
   u=uindex*1.30+rng.uniform(-.45,.45)
   if p.kind=='diamond' and abs(u)<p.edge+.5:continue
   if p.kind=='soundwall' and not (abs(u)<p.median/2-.35 or p.edge+.5<abs(u)<30):continue
   dist=abs(s+35);density=max(0,min(1,(190-dist)/90))
   if rng.random()>density:continue
   x,y,_=p.xyz(s,u);q,normal,_,_=soil.ray_cast(Vector((x,y,30)),Vector((0,0,-1)),60)
   if q is None:continue
   probes=((0,0),(1.1,0),(-1.1,0),(0,1.1),(0,-1.1),(.9,.9),(.9,-.9),(-.9,.9),(-.9,-.9))
   if any(paving.ray_cast(Vector((x+dx,y+dy,30)),Vector((0,0,-1)),60)[0] is not None for dx,dy in probes):continue
   limit=43 if p.kind=='diamond' else 28
   tall=abs(u)>limit
   # Height follows the mowing boundary, with unmown seed drifts rather
   # than a dotted row of isolated stems. Mown median stays close-cropped.
   h=(1.7+.8*math.sin(s*.19+u*.43)**2) if tall else .52+.28*rng.random()
   if tall and math.sin(s*.23+u*.39)<-.6:h*=.5
   pattern=rng.randrange(8) if tall else (4*(math.floor(abs(u)/1.8)%2)+rng.randrange(4))
   ob=templates[pattern].copy();bpy.context.collection.objects.link(ob)
   ob.name='ROW turf tile %05d'%count;ob.parent=parent;ob.location=q+Vector((0,0,-.025))
   ob.rotation_mode='QUATERNION';ob.rotation_quaternion=normal.to_track_quat('Z','Y')@Quaternion(Vector((0,0,1)),rng.uniform(0,math.tau));ob.scale=(1,1,h)
   # A linked tile is planar at its roots. At a ditch/crest crease, lower it
   # onto the measured earth rather than leaving its downhill edge floating.
   gaps=[]
   for dx,dy in ((-.9,-.9),(-.9,.9),(.9,-.9),(.9,.9)):
    v=ob.location+ob.rotation_quaternion@Vector((dx,dy,0))
    hit=soil.ray_cast(Vector((v.x,v.y,30)),Vector((0,0,-1)),60)[0]
    if hit is not None:gaps.append(v.z-hit.z)
   lowering=max(0,max(gaps,default=0)+.005)
   ob.location.z-=lowering;ob['terrain_root_lowering_m']=lowering
   ob['turf_card_tile']=True;count+=1
 if p.kind=='diamond':
  for j in range(-32,33):
   s=j*6.096
   if abs(s)<20 or rng.random()<.22:continue
   for side in (-1,1):
    ob=templates[rng.randrange(len(templates))].copy();bpy.context.collection.objects.link(ob)
    ob.name='Rooted barrier-joint weeds %04d'%count;ob.parent=parent
    ob.location=p.xyz(s,side*.58,-.012);ob.scale=(.32,.65,.65)
    ob['turf_card_tile']=True;count+=1
 for ob in templates:bpy.data.objects.remove(ob,do_unlink=True)
 parent['turf_tiles']=count;parent['turf_triangles']=sum(len(ob.data.loop_triangles) for ob in parent.children_recursive if ob.type=='MESH' and ob.get('turf_card_tile'))
 return count
