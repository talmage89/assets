"""Orbit 14: original tubular frame, sewn pad and analytic tiled fabrics."""
import sys,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G
from kit.prop import Build,arguments
from kit.materials import surface
from kit.export import atlas_material
from dimensions import *
from finishes import zinc,pad,foam
import fabric_tile

class Trampoline(Build):
 def __init__(self,a):
  super().__init__('Trampoline',a.quality,a.wear)
  self.zinc=zinc(a.wear);self.pad=pad(a.wear);self.foam=foam(a.wear)
  self.black=surface('Binding and molded buckles','rubber',a.wear,color=(.009,.012,.013),roughness=.86,dust=.15)
  self.tape=surface('Faded entry zipper binding','plastic',a.wear,color=(.029,.072,.101),roughness=.81,dust=.1)
  folder=Path('build/fabric-source');fabric_tile.apply(folder,wear=a.wear)
  self.alpha=atlas_material('Trampoline',folder.resolve(),.4,True,alpha_mode='BLEND')
  for n in self.alpha.node_tree.nodes:
   if hasattr(n,'uv_map'):n.uv_map='BakeUV'
 def box(self,n,p,s,m=None,pa=None):return self.add(G.box(n,p,s,m or self.zinc,.0004 if self.high else 0,2),pa)
 def tube(self,n,path,r,m=None,sides=8,pa=None):return self.add(G.tube(n,path,r,m or self.zinc,sides),pa)
 def rod(self,n,a,b,r,m=None,sides=8,pa=None):return self.add(G.cylinder(n,a,b,r,m or self.zinc,sides),pa)
 def fabric(self,name,verts,faces,uvs):
  ob=self.add(G.mesh(name,verts,faces,self.alpha));ob['allow_boundary']=True;ob['export_part']='FabricAssembly'
  layer=ob.data.uv_layers.new(name='BakeUV')
  by_vertex={vi:co for face,coords in zip(faces,uvs) for vi,co in zip(face,coords)}
  for face in ob.data.polygons:
   for li in face.loop_indices:layer.data[li].uv=by_vertex[ob.data.loops[li].vertex_index]
  return ob

def ribbon(b,name,points,width,mat):
 vs=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
  side=tangent.cross(Vector((0,0,1)))
  if side.length<1e-6:side=Vector((1,0,0))
  side.normalize();vs.extend([tuple(Vector(p)-side*width/2),tuple(Vector(p)+side*width/2)])
 ob=b.add(G.mesh(name,vs,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(len(points)-1)],mat));ob['allow_boundary']=True
 return ob

def polar(r,a,z):return (r*math.cos(a),r*math.sin(a),z)
def sweep_closed(b,name,profile,mat,N=96):
 loops=[[polar(r,math.tau*j/N,z) for z,r in profile] for j in range(N)]
 k=len(profile);steps=N//12;result=[]
 for panel in range(12):
  vs=sum([loops[j%N] for j in range(panel*steps,(panel+1)*steps+1)],[])
  fs=[(j*k+i,j*k+(i+1)%k,(j+1)*k+(i+1)%k,(j+1)*k+i) for j in range(steps) for i in range(k)]
  fs += [tuple(reversed(range(k))),tuple(range(steps*k,(steps+1)*k))]
  result.append(b.add(G.smooth(G.mesh(name+' '+str(panel),vs,fs,mat),85)))
 return result

def leg_tube(b,name,path,rad):
 # The known vertical bending plane fixes section clocking. Generic parallel
 # transport can rotate an octagon just enough to leave its flats above grade.
 points=list(map(Vector,path));loops=[]
 for i,p in enumerate(points):
  tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();v=tangent.cross(rad).normalized()
  loops.append([p+TUBE/2*(rad*math.cos(j*math.tau/8)+v*math.sin(j*math.tau/8)) for j in range(8)])
 return b.add(G.smooth(G.loft(name,loops,b.zinc),47))

def frame(b):
 # Continuous tubular hoop is formed from twelve swaged sections. Rings mark
 # the actual joints while avoiding hidden internal tube surfaces.
 profile=[(MAT_Z+TUBE/2*math.sin(i*math.tau/6),FRAME_R+TUBE/2*math.cos(i*math.tau/6)) for i in range(6)]
 sweep_closed(b,'Twelve section galvanized hoop',profile,b.zinc,84)
 for j in range(6):
  a=A0+math.pi/12+j*math.tau/6;rad=Vector((math.cos(a),math.sin(a),0));t=Vector((-math.sin(a),math.cos(a),0))
  chord=FRAME_R*math.cos(math.pi/12);w=FRAME_R*math.sin(math.pi/12)
  def point(u,z):return tuple(rad*chord+t*u+Vector((0,0,z)))
  # A real 38 mm bent W brace with two loaded flats on grade, not wire legs.
  path=[point(-w,MAT_Z),point(-w,.14),point(-w+.024,.055),point(-w+.08,.019),point(-.30,.019),point(-.16,.019),point(0,.057),point(.16,.019),point(.30,.019),point(w-.08,.019),point(w-.024,.055),point(w,.14),point(w,MAT_Z)]
  leg_tube(b,'Leg extension '+str(j)+' L',path[:2],rad)
  leg_tube(b,'W leg '+str(j),path[1:-1],rad)
  leg_tube(b,'Leg extension '+str(j)+' R',path[-2:],rad)
  for side in (-1,1):
   aa=a+side*math.pi/12;pt=polar(FRAME_R,aa,MAT_Z)
   # Cylindrical pressed sockets extend below the hoop over the leg spigot.
   b.rod('Leg socket %d %d'%(j,side),(pt[0],pt[1],.81),(pt[0],pt[1],MAT_Z),.0225)
   if b.high:b.rod('Leg retaining bolt %d %d'%(j,side),polar(FRAME_R-.026,aa,.845),polar(FRAME_R+.027,aa,.845),.004,sides=6)
  # Six enclosure poles attach to the hoop and continue below it to a clamp.
  a-=math.pi/12
  pole_r=FRAME_R+.040
  points=[polar(pole_r,a,.65),polar(pole_r,a,1.82),polar(pole_r-.020,a,2.21),polar(pole_r-.09,a,2.51),polar(1.95,a,2.66)]
  b.tube('Enclosure pole '+str(j),points,.0127,sides=8)
  # Foam covers the steel pole above the pad. Same macro bend stations in high/game.
  covered=[polar(pole_r,a,.96)]+points[1:]
  b.tube('Pole foam sleeve '+str(j),covered,.026,b.foam,8)
  b.rod('Pole upper cap '+str(j),polar(1.95,a,2.654),polar(1.95,a,POLE_TOP),.027,b.black,8)
  for z in (.71,.84):
   # Stamped clamping ears bridge pole to its socket; bolt faces are visible.
   p=Vector(polar(FRAME_R+.020,a,z));ob=G.box('Pole clamp '+str(j),p,(.080,.036,.020),b.zinc,0);ob.rotation_euler.z=a;b.add(ob)
   if b.high:b.rod('Pole clamp bolt '+str(j),polar(FRAME_R-.036,a,z),polar(FRAME_R+.059,a,z),.004,b.zinc,6)
  # Top strap connects net hem to foam-covered pole, under the cap.
  b.tube('Net pole top attachment '+str(j),[polar(NET_R1,a,NET_TOP),polar(1.947,a,NET_TOP),polar(1.953,a,NET_TOP-.022)],.004,b.black,6)
 # Swage witness seams at all twelve frame joints, baked where small.
 for j in range(12):
  a=A0+j*math.tau/12;rad=Vector((math.cos(a),math.sin(a),0));t=Vector((-math.sin(a),math.cos(a),0));p=rad*FRAME_R+Vector((0,0,MAT_Z))
  if b.high:b.rod('Hoop swage seam '+str(j),p-t*.002,p+t*.002,.0205,b.zinc,8)

def mat(b):
 # A grid of clipped cells preserves physical weave pitch and an unloaded sag.
 # Intersections use a mathematical circle, not a sampled photograph.
 verts=[];faces=[];uvs=[];u0,v0,u1,v1=MAT_RECT
 N=math.ceil(2*MAT_R/TILE)
 def clip_circle(poly):
  for j in range(96):
   a=(j+.5)*math.tau/96;nx,ny=math.cos(a),math.sin(a);lim=MAT_R*math.cos(math.pi/96);out=[]
   for A,B in zip(poly,poly[1:]+poly[:1]):
    da=A[0]*nx+A[1]*ny-lim;db=B[0]*nx+B[1]*ny-lim
    if da<=1e-9:out.append(A)
    if (da<0)!=(db<0):t=da/(da-db);out.append((A[0]+t*(B[0]-A[0]),A[1]+t*(B[1]-A[1])))
   poly=out
   if not poly:break
  clean=[]
  for v in poly:
   if not clean or math.dist(v,clean[-1])>1e-7:clean.append(v)
  if len(clean)>1 and math.dist(clean[0],clean[-1])<1e-7:clean.pop()
  poly=clean
  while len(poly)>3:
   remove=next((i for i in range(len(poly)) if abs((poly[i][0]-poly[i-1][0])*(poly[(i+1)%len(poly)][1]-poly[i][1])-(poly[i][1]-poly[i-1][1])*(poly[(i+1)%len(poly)][0]-poly[i][0]))<1e-10),None)
   if remove is None:break
   poly.pop(remove)
  return poly
 for i in range(N):
  x0=-MAT_R+i*TILE;x1=min(MAT_R,x0+TILE)
  for j in range(N):
   y0=-MAT_R+j*TILE;y1=min(MAT_R,y0+TILE);poly=clip_circle([(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
   if len(poly)<3:continue
   k=len(verts);verts +=[(x,y,MAT_Z-.018*(1-(x*x+y*y)/(MAT_R*MAT_R))) for x,y in poly];faces.append(tuple(range(k,k+len(poly))))
   uvs.append([(u0+(x-x0)/TILE*(u1-u0),v0+(y-y0)/TILE*(v1-v0)) for x,y in poly])
 b.fabric('Jump mat alpha',verts,faces,uvs)
 for panel in range(12):
  ring=[]
  for j in range(panel*6,panel*6+7):
   a=j*math.tau/72;ring.extend([polar(MAT_R-.016,a,MAT_Z+.002),polar(MAT_R+.006,a,MAT_Z+.002)])
  ob=b.add(G.mesh('Sewn mat perimeter webbing '+str(panel),ring,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(6)],b.black));ob['allow_boundary']=True

def springs(b):
 verts=[];faces=[];uvs=[];u0,v0,u1,v1=SPRING_RECT
 for j in range(SPRINGS):
  a=math.tau*j/SPRINGS;rad=Vector((math.cos(a),math.sin(a),0));t=Vector((-math.sin(a),math.cos(a),0))
  start=rad*(MAT_R+.004)+Vector((0,0,MAT_Z))
  for across in (t,Vector((0,0,1))):
   k=len(verts);verts += [tuple(start+rad*x+across*y) for x,y in [(0,-SPRING_WIDTH/2),(SPRING_LENGTH,-SPRING_WIDTH/2),(SPRING_LENGTH,SPRING_WIDTH/2),(0,SPRING_WIDTH/2)]]
   faces.append((k,k+1,k+2,k+3));uvs.append([(u0,v0),(u1,v0),(u1,v1),(u0,v1)])
 b.fabric('Spring coil alpha',verts,faces,uvs)

def padding(b):
 # The inner edge rolls back locally, exposing a little spring below the sewn
 # skirt. Top and underside differ in both exposure and material normal.
 N=72;loops=[]
 for j in range(N):
  a=j*math.tau/N;pucker=math.sin(6*a)**2;lift=.004*math.sin(3*a+1)**2
  front=abs(math.atan2(math.sin(a+math.pi/2),math.cos(a+math.pi/2)))
  roll=.105*math.exp(-(front/.42)**4);inner=PAD_IN+roll
  section=[(.904+roll*.12,inner),(.933+lift+roll*.15,inner+.012),(PAD_TOP+.006*pucker,(inner+PAD_OUT)/2),(.933,PAD_OUT-.012),(.892,PAD_OUT),(.886+roll*.12,inner+.016)]
  loops.append([polar(r,a,z) for z,r in section])
 k=6
 for panel in range(12):
  stations=[loops[j%N] for j in range(panel*6,panel*6+7)];verts=sum(stations,[])
  faces=[(j*k+i,j*k+(i+1)%k,(j+1)*k+(i+1)%k,(j+1)*k+i) for j in range(6) for i in range(k)]
  faces += [tuple(reversed(range(k))),tuple(range(6*k,7*k))]
  b.add(G.smooth(G.mesh('Sewn safety pad panel '+str(panel),verts,faces,b.pad),45))
 for j in range(12):
  a=j*math.tau/12
  front=abs(math.atan2(math.sin(a+math.pi/2),math.cos(a+math.pi/2)));inner=PAD_IN+.105*math.exp(-(front/.42)**4)
  # Small bound stitched radial seams, physically supported on the cover.
  ribbon(b,'Pad radial sewn seam '+str(j),[polar(inner+.018,a,.938+(inner-PAD_IN)*.15),polar((inner+PAD_OUT)/2,a,PAD_TOP),polar(PAD_OUT-.012,a,.935)],.003,b.tape)
 for j in range(12):
  a=math.tau*j/12
  ribbon(b,'Pad underside retaining tie '+str(j),[polar(2.02,a,.887),polar(FRAME_R,a,.85),polar(FRAME_R+.018,a,.874)],.006,b.black)

def net(b):
 # Nine cloth cells per 60-degree panel, eight vertically: very inexpensive
 # double-sided cards. Shared nodes at each edge prevent geometric cracks.
 verts=[];faces=[];uvs=[];u0,v0,u1,v1=NET_RECT;cols=10;rows=8
 def at(sector,q,t):
  a=A0+(sector+q)*math.tau/6;sag=.055*math.sin(math.pi*q)**2
  # Disable radial bagging at the front zip line so its slider has a true axis.
  front=abs(math.atan2(math.sin(a+math.pi/2),math.cos(a+math.pi/2)))
  envelope=min(1,front/.14)
  r=NET_R0+(NET_R1-NET_R0)*t+.026*math.sin(math.pi*t)*math.sin(math.pi*q)**2*envelope
  return polar(r,a,NET_BOTTOM+(NET_TOP-sag-NET_BOTTOM)*t)
 for sector in range(6):
  for j in range(cols):
   q0=j/cols;q1=(j+1)/cols
   for i in range(rows):
    t0=i/rows;t1=(i+1)/rows;k=len(verts)
    ps=[at(sector,q0,t0),at(sector,q1,t0),at(sector,q1,t1),at(sector,q0,t1)];verts+=ps;faces.append((k,k+1,k+2,k+3))
    # Physical cell dimensions vary slightly with cloth sag, within report bands.
    width=.200;height=.224  # whole weave periods; continuous phase at card joins
    uvs.append([(u0,v0),(u0+width/TILE*(u1-u0),v0),(u0+width/TILE*(u1-u0),v0+height/TILE*(v1-v0)),(u0,v0+height/TILE*(v1-v0))])
 b.fabric('Enclosure net alpha',verts,faces,uvs)
 # Sewn top and bottom hems carry the fabric, including sag between supports.
 for t,name in [(0,'Net lower binding'),(1,'Net sagged upper binding')]:
  for panel in range(12):
   points=[at(j//cols,(j%cols)/cols,t) for j in range(panel*5,panel*5+6)]
   vs=[]
   for p in points:vs.extend([(p[0],p[1],p[2]-.008),(p[0],p[1],p[2]+.008)])
   ob=b.add(G.mesh(name+' '+str(panel),vs,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(5)],b.black));ob['allow_boundary']=True
 for j in range(6):
  a=A0+j*math.tau/6
  ribbon(b,'Net panel seam '+str(j),[polar(NET_R0+(NET_R1-NET_R0)*t,a,NET_BOTTOM+(NET_TOP-NET_BOTTOM)*t) for t in (0,.5,1)],.005,b.black)
 # Bottom lacing runs to the mat binding, supported by the mat's sewn edge.
 for j in range(42):
  a=j*math.tau/42
  ribbon(b,'Net to mat lace '+str(j),[polar(NET_R0,a,NET_BOTTOM),polar(MAT_R-.004,a,MAT_Z-.003),polar(NET_R0,a+.01,NET_BOTTOM)],.0036,b.black)
 # Blue vertical entry tape and a short horizontal foot seam, no brand copied.
 for x in (-.012,.012):
  pts=[(x,-zip_radius(z)-.004,z) for z in (ZIP_BOTTOM,ZIP_TOP)]
  ob=G.mesh('Entry zipper tape',[(x-.011,pts[0][1],ZIP_BOTTOM),(x+.011,pts[0][1],ZIP_BOTTOM),(x+.011,pts[1][1],ZIP_TOP),(x-.011,pts[1][1],ZIP_TOP)],[(0,1,2,3)],b.tape);ob['allow_boundary']=True;b.add(ob)
  # A narrow raised teeth line bakes onto the tape without a second texture.
 b.tube('Entry zipper teeth line',[(0,-zip_radius(z)-.006,z) for z in (ZIP_BOTTOM,ZIP_TOP)],.0018,b.black,4)
 for z in (1.03,1.46,1.94):
  for sign in (-1,1):
   b.box('Entry buckle webbing',(sign*.075,-zip_radius(z)-.012,z),(.09,.006,.019),b.black)
   b.box('Entry molded buckle open',(sign*.036,-zip_radius(z)-.020,z),(.027,.012,.026),b.black)
 slider=G.pivot('ZipSlider',(0,-zip_radius(ZIP_TOP)-.012,ZIP_TOP));slider.parent=b.root;slider.rotation_euler.x=ZIP_ANGLE;slider['slide_axis']='Z';slider['range_m']=[-1.28,0]
 yy=-zip_radius(ZIP_TOP)
 cross=[(-.009,-.003),(-.009,-.029),(.009,-.029),(.009,-.003),(.004,-.003),(.004,-.018),(-.004,-.018),(-.004,-.003)]
 b.add(G.profile('Zipper slider body',[(x,yy+y) for x,y in cross],ZIP_TOP-.012,ZIP_TOP+.012,b.zinc,'Z'),slider)
 b.tube('Zipper pull tab',[(-.006,-zip_radius(ZIP_TOP)-.027,ZIP_TOP),(0,-zip_radius(ZIP_TOP)-.035,ZIP_TOP-.037),(.006,-zip_radius(ZIP_TOP)-.027,ZIP_TOP)],.002,b.zinc,4,slider)

def main():
 a=arguments();b=Trampoline(a);frame(b);mat(b);springs(b);padding(b);net(b)
 # Lock both representations to the same diagonal on nonplanar cloth quads.
 # Blender's implicit render tessellation differs from finalize's BEAUTY split.
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':
   bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY');bm.to_mesh(ob.data);bm.free()
 b.save(a.out,a.quality)
if __name__=='__main__':main()
