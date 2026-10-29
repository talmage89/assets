"""Original 12-gauge exterior visual shells, shared without a gun dependency.

The accepted pump shell proportions and six folded petals are retained. Units
are millimeters, head center origin, +Y toward the mouth. No ballistic or
manufacturing data. Caller supplies materials; returned mesh is not registered.
"""
import math
import bpy
from mathutils import Vector
from kit import model as M, weapon as W

RIM=22.4
LOADED_LENGTH=57.5
FIRED_LENGTH=69.8

def bridge(a,b):
 if len(a)==1:return [(a[0],b[(j+1)%len(b)],b[j]) for j in range(len(b))]
 if len(b)==1:return [(a[i],a[(i+1)%len(a)],b[0]) for i in range(len(a))]
 faces=[];i=j=0;n,m=len(a),len(b)
 while i<n or j<m:
  aa=(i+1)/n;bb=(j+1)/m
  if abs(aa-bb)<1e-9:
   faces.append((a[i%n],b[j%m],b[(j+1)%m],a[(i+1)%n]));i+=1;j+=1
  elif aa<bb:faces.append((a[i%n],b[j%m],a[(i+1)%n]));i+=1
  else:faces.append((a[i%n],b[j%m],b[(j+1)%m]));j+=1
 return faces

def shell(name,materials,*,base=(0,0,0),fired=False):
 n=28 if fired else 32;pn=12 if fired else 16
 # One closed connected surface, including the actual primer seat, preserves
 # the accepted exterior without hidden overlapping backing disks.
 specs=([(.75,0,pn,'primer',0),(.15,.65,pn,'primer',0),(.12,2.7,pn,'primer',0)] if fired else
  [(.12,0,pn,'primer',0),(.12,2.7,pn,'primer',0)])
 specs += [(0,2.7,pn,'primer',0),(0,11.2,n,'brass',0),(1.4,11.2,n,'brass',0),
  (1.8,10.1,n,'brass',0),(10.5,10.1,n,'brass',0),(10.5,10.05,n,'hull',0)]
 if fired:
  specs += [(69.8,10.12,n,'hull',-.18),(69.8,9.55,n,'mouth',-.18),
   (10.5,9.35,8,'mouth',0),(10.5,0,1,'mouth',0)]
 else:
  specs += [(57.5,9.8,n,'hull',0),(57.5,9.3,n,'hull',0),(57.25,9.3,24,'hull',0),
   (56.95,7.3,24,'hull',.35),(56.35,4.8,24,'hull',.6),(55.7,.65,24,'hull',.14),
   (55.1,.6,16,'mouth',0),(10.5,.6,8,'mouth',0),(10.5,0,1,'mouth',0)]
 vertices=[];rings=[];faces=[];slots=[];keys=['primer','brass','hull','mouth']
 for a,r,sides,mat,warp in specs:
  ring=[]
  for i in range(sides if r else 1):
   t=i*math.tau/sides
   offset=warp*(.5+.5*math.cos(6*t)) if fired else warp*math.cos(6*t)
   ring.append(len(vertices));vertices.append((base[0]+r*math.cos(t),base[1]+a+offset,base[2]+r*math.sin(t)))
  rings.append(ring)
 for i,(a,b) in enumerate(zip(rings,rings[1:])):
  ff=bridge(a,b);faces+=ff;slots += [keys.index(specs[i+1][3])]*len(ff)
 ob=M.mesh(name,vertices,faces,materials['primer'])
 for key in keys[1:]:ob.data.materials.append(materials[key])
 for f,slot in zip(ob.data.polygons,slots):f.material_index=slot
 # Normals are outward for a single continuous closed skin.
 import bmesh
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
 M.smooth(ob,60);tri=ob.modifiers.new('Shell triangles','TRIANGULATE');M.apply(ob)
 normals=[v.vector.copy() for v in ob.data.corner_normals]
 for f in ob.data.polygons:
  for j in f.loop_indices:
   p=ob.data.vertices[ob.data.loops[j].vertex_index].co-Vector(base)
   if abs(f.normal.y)<.12:
    nn=Vector((p.x,0,p.z)).normalized();normals[j]=nn if nn.dot(f.normal)>0 else -nn
   elif abs(f.normal.y)>.995:normals[j]=Vector((0,math.copysign(1,f.normal.y),0))
 ob.data.normals_split_custom_set(normals)
 ob['ammo_visual']='12-gauge fired hull' if fired else '12-gauge live shell'
 ob['source_proportions']='shared original pump exterior; connected hidden joins'
 return ob
