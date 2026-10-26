"""Minnow Petal 60: original thin molded shell and optional 140 mm water."""
import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import bpy,bmesh
from mathutils import Vector
from kit.motion import surface
from kit import model as G,materials as M
from kit.prop import arguments,Build
import finishes

a=arguments();b=Build('KiddiePool',a.quality,a.wear);N=48;FILL=.140
plastic=finishes.plastic(a.wear)
# Outside -> curl -> free return -> inside -> floor. This is a solid gauge,
# with an actual open underside under the roll, not a thick torus on a bucket.
profile=[(0,0),(0,.625),(.006,.644),(.020,.654),(.150,.6998),(.287,.748),
 (.298,.762),(.3028,.762),(.3048,.755),(.3028,.749),(.299,.748),
 (.299,.750),(.3015,.751),(.3028,.755),(.3015,.759),(.287,.7462),
 (.150,.6980),(.020,.6522),(.0024,.625),(.0024,0)]
body=G.lathe('Thin molded basin and curled rim',profile,plastic,N)
# Twelve broad molded flutes stiffen the thin wall without reproducing a product pattern.
for v in body.data.vertices:
 if abs(v.co.z-.150)<1e-6:
  theta=math.atan2(v.co.y,v.co.x);rr=math.hypot(v.co.x,v.co.y)
  target=rr-.0048*(.5+.5*math.cos(12*theta));v.co.x*=target/rr;v.co.y*=target/rr
def triangulate(ob):
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY');bm.to_mesh(ob.data);bm.free();return ob
# Small sun/molding warp in the unsupported upper lip; cardinal diameter and
# flat floor remain at the measured dimensions. Water remains horizontal.
for v in body.data.vertices:
 if v.co.z>.25:
  theta=math.atan2(v.co.y,v.co.x);weight=min(1,(v.co.z-.25)/.037)
  v.co.z-=.0055*(.5+.5*math.sin(3*theta))*weight
  rr=math.hypot(v.co.x,v.co.y);dr=.0025*math.sin(2*theta)**2*(.5+.5*math.sin(3*theta+.4))*weight
  v.co.x*=1-dr/rr;v.co.y*=1-dr/rr
G.smooth(body,65);b.add(triangulate(body));rim_tree=surface(body)['tree']
# Optional separate open surface. The active water area stays within the actual
# polygonal inside wall; it is not a cylinder intersecting the plastic shell.
waterroot=G.pivot('Water',(0,0,0));waterroot.parent=b.root;waterroot['static_root']=True
R=.689;vs=[(0,0,FILL)]+[(R*math.cos(i*math.tau/N),R*math.sin(i*math.tau/N),FILL) for i in range(N)]
ob=G.mesh('Water surface / optional',vs,[(0,1+i,1+(i+1)%N) for i in range(N)],finishes.water());ob['allow_boundary']=True;b.add(ob,waterroot)
# Five damp fescue clippings: closed, thin tapered strips lying on the actual rim.
grass=M.surface('Damp grass clippings','plastic',a.wear,color=(.018,.065,.006),roughness=.31)
for j,(angle,length,width) in enumerate([(-1.16,.039,.0025),(-1.10,.027,.0022),(-.99,.045,.003),(-2.15,.031,.0025),(-2.07,.024,.002)]):
 theta=angle;rad=.755;cx=rad*math.cos(theta);cy=rad*math.sin(theta)
 # Tangential blades follow the crown arc; tiny curved tips remain attached.
 vs=[]
 for k,t in enumerate((-.5,0,.5)):
  tangent=t*length
  for side in (-1,0,1):
   w=width*(.30 if k==2 else 1)*side/2
   xx=cx-math.sin(theta)*tangent+math.cos(theta)*w;yy=cy+math.cos(theta)*tangent+math.sin(theta)*w
   hit=rim_tree.ray_cast(Vector((xx,yy,.35)),Vector((0,0,-1)),.10)
   assert hit[0] is not None,'Grass must lie on the actual rim'
   vs.append((xx,yy,hit[0].z+.00009))
 fs=[(j*3+i,j*3+i+1,(j+1)*3+i+1,(j+1)*3+i) for j in range(2) for i in range(2)]
 ob=G.mesh(f'Wet rim grass clipping {j+1}',vs,fs,grass)
 sol=ob.modifiers.new('Actual blade thickness','SOLIDIFY');sol.thickness=.00020;sol.offset=0;sol.use_even_offset=True
 triangulate(b.add(ob))
# Matching high/game main surfaces avoid thin-shell projection rays crossing layers.
b.save(a.out,a.quality)
