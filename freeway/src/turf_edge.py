"""Short linked sward at the mowing/paving transition, plus exposed minerals."""
import math
import bpy
from mathutils import Matrix,Vector
import geom as Q

def hit(soil,p,s,u):
 x,y,_=p.xyz(s,u)
 return soil.ray_cast(Vector((x,y,30)),Vector((0,0,-1)),60)

def add(p,parent,soil,paving,templates,rng,start):
 count=0
 # Full-width tiles cannot approach pavement without crossing it. Narrow
 # linked tiles fill that margin with progressively shorter, mown blades.
 for j in range(-140,161):
  s=j*1.3+rng.uniform(-.12,.12)
  density=max(0,min(1,(190-abs(s+35))/90))
  for side in (-1,1):
   for distance,height in ((.94,.42),(.36,.25)):
    if rng.random()>density:continue
    q,normal,_,_=hit(soil,p,s,side*(p.median/2-distance))
    if q is None:continue
    tangent=Vector((*p.frame(s)[1],0))
    xaxis=tangent.cross(normal).normalized();yaxis=normal.cross(xaxis).normalized()
    rotation=Matrix((xaxis,yaxis,normal)).transposed().to_quaternion()
    probes=[q+rotation@Vector((x,y,0)) for x,y in ((0,0),(-.32,-.75),(-.32,.75),(.32,-.75),(.32,.75))]
    if any(paving.ray_cast(v+Vector((0,0,30)),Vector((0,0,-1)),60)[0] is not None for v in probes):continue
    ob=templates[rng.randrange(8)].copy();bpy.context.collection.objects.link(ob)
    ob.name='Mown edge turf %05d'%(start+count);ob.parent=parent
    ob.location=q-Vector((0,0,.012));ob.scale=(.38,1,height)
    ob.rotation_mode='QUATERNION';ob.rotation_quaternion=rotation
    gaps=[]
    for v in probes[1:]:
     h=soil.ray_cast(v+Vector((0,0,30)),Vector((0,0,-1)),60)[0]
     if h is not None:gaps.append(v.z-h.z)
    ob.location.z-=max(0,max(gaps,default=0))
    ob['turf_card_tile']=True;count+=1
 # Salt, sweeping and tire-edge disturbance expose a narrow irregular strip.
 # Sample the existing actual terrain; do not resample or move its structure.
 batch=Q.Batch('Exposed median paving-edge soil',parent)
 stations=[-p.length/2+.001+i*(p.length-.002)/168 for i in range(169)]
 def point(s,side,inner):
  width=.12+.045*math.sin(s*.37)+.025*math.sin(s*1.19)
  q=hit(soil,p,s,side*(p.median/2-(width if inner else .008)))[0]
  return q+Vector((0,0,.0007)) if q is not None else None
 for side in (-1,1):
  for a,c in zip(stations,stations[1:]):
   pts=[point(a,side,False),point(a,side,True),point(c,side,True),point(c,side,False)]
   if all(v is not None for v in pts):batch.surface(pts,'Earth')
 batch.finish()
 return count
