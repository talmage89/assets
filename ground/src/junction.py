"""Additive parametric arterial pieces, independent of Ground's delivery graph.

Widths, corner returns, raised medians with bay tapers/noses, and channelizing
islands. Only the canonical library's materials are read, never modified.
"""
import math,sys,json,argparse
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit import model as G
from kit.tiling import world_uv

def build(spec,rootpath):
 from mathutils import Vector
 before=set(bpy.context.scene.objects)
 bpy.ops.import_scene.gltf(filepath=str((rootpath/'ground/export/Ground.glb').resolve()))
 old=set(bpy.context.scene.objects)-before
 mats={k:next(m for m in bpy.data.materials if m.name==k) for k in ('Asphalt','Concrete','Lawn')}
 for o in old:bpy.data.objects.remove(o,do_unlink=True)
 def material(n,c):
  m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.88;return m
 white=material('Arterial aged white',(.55,.55,.50));yellow=material('Arterial faded yellow',(.52,.32,.012));seal=material('Arterial loop seal',(.012,.012,.011))
 L=3.3528;hx=spec['ns']*L/2+spec['median']/2;hy=spec['ew']*L/2;R=spec['radius'];extent=spec.get('extent',350)
 rt=G.pivot('ParametricJunction',(0,0,0));rt['presentation_only']=True
 def mesh(n,vs,fs,ma):
  o=G.mesh(n,vs,fs,ma)
  for face in o.data.polygons:
   zz=[o.data.vertices[i].co.z for i in face.vertices]
   if max(zz)-min(zz)<1e-7 and face.normal.z<0:face.flip()
  o.data.update();o.parent=rt;coverage=6.096 if ma==mats['Asphalt'] else 1.524 if ma==mats['Concrete'] else 3.048
  world_uv(o,coverage)
  uv=o.data.uv_layers.active
  for f in o.data.polygons:
   if abs(f.normal.z)>.5:continue
   axes=(1,2) if abs(f.normal.x)>.5 else (0,2)
   for li in f.loop_indices:
    v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]/coverage,v[axes[1]]/coverage)
  if ma in mats.values():
   ca=o.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
   for v in ca.data:v.color=(1,1,1,1)
  return o
 def poly(n,pts,z,ma):return mesh(n,[(x,y,z) for x,y in pts],[tuple(range(len(pts)))],ma)
 def slab(n,pts,ma=mats['Concrete'],z=.1524):
  # Closed perimeter with curb face, walking top.
  vs=[(x,y,h) for h in (.004,z) for x,y in pts];N=len(pts)
  return mesh(n,vs,[tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],ma)
 def rect(n,x0,x1,y0,y1,z,ma):return poly(n,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z,ma)
 def xy(x,y,t):
  c,s=math.cos(t*math.pi/2),math.sin(t*math.pi/2);return (x*c-y*s,x*s+y*c)
 def strip(n,x0,x1,y0,y1,t,z,ma):return poly(n,[xy(x,y,t) for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]],z,ma)
 rect('Town underlay',-extent,extent,-extent,extent,-.02,mats['Lawn'])
 rect('Intersection asphalt',-hx,hx,-hy,hy,.012,mats['Asphalt'])
 for t in spec['approaches']:
  h=hx if t%2==0 else hy;fh=hy if t%2==0 else hx;core=fh+.4572+R;stop=core+3.9624
  strip('Continuing crowned road',-h,h,fh,extent,t,.012,mats['Asphalt'])
  for side in (-1,1):
   # Gutter / full-width unscaled sidewalk / planting strip.
   strip('Concrete gutter',side*h,side*(h+.4572),core,extent,t,.008,mats['Concrete'])
   pts=[xy(side*x,y,t) for x,y in [(h+.4572,core),(h+.6096,core),(h+.6096,extent),(h+.4572,extent)]];slab('Straight curb',pts)
   strip('Planted verge',side*(h+.6096),side*(h+2.286),core,extent,t,.151,mats['Lawn'])
   strip('Continuing sidewalk',side*(h+2.286),side*(h+3.81),core,extent,t,.1524,mats['Concrete'])
   # Walking paving has joints, generated in geometry.
   for y in range(math.ceil(core/1.524),99):
    yy=y*1.524
    strip('Sidewalk expansion joint',side*(h+2.286),side*(h+3.81),yy-.004,yy+.004,t,.153,seal)
  # Lane lines. Right side inbound from the opposing approach.
  centers=(-L/2,L/2) if spec['ns']==5 and t%2==0 else (0,)
  if spec['median'] and t%2==0:centers=()
  for center in centers:
   for x in (center-.085,center+.085):strip('Double yellow center',x-.05,x+.05,stop,extent,t,.016,yellow)
  if (spec['ns'] if t%2==0 else spec['ew'])>=4:
   for side in (-1,1):
    x=side*((L if spec['median'] else L*1.5)+(spec['median']/2 if spec['median'] else 0))
    for y in range(round(stop+3),348,9):strip('White lane dash',x-.05,x+.05,y,y+3.048,t,.016,white)
  strip('Stop bar',-h,(L/2 if spec['ns']==5 and t%2==0 else -.1),stop-.3048,stop+.3048,t,.017,white)
  for i in range(math.floor(2*h/.76)):
   x=-h+.3+i*.76;strip('Crosswalk bar',x,x+.4572,core+.6,core+2.4288,t,.017,white)
  for x in ([-L,-2*L,0] if spec['ns']==5 and t%2==0 else [-L/2]):
   if abs(x)>h-.5:continue
   y=stop+3
   pts=[(x-.9144,y-.70),(x-.70,y-.9144),(x+.70,y-.9144),(x+.9144,y-.70),(x+.9144,y+.70),(x+.70,y+.9144),(x-.70,y+.9144),(x-.9144,y+.70)]
   for a,b in zip(pts,pts[1:]+pts[:1]):
    dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);ox,oy=-dy/l*.005,dx/l*.005
    poly('Sealed detector sawcut',[xy(*p,t) for p in ((a[0]+ox,a[1]+oy),(b[0]+ox,b[1]+oy),(b[0]-ox,b[1]-oy),(a[0]-ox,a[1]-oy))],.018,seal)
  if spec['median'] and t%2==0:
   # Left-turn bay occupies half the median: tapered approach, rounded end.
   m=spec['median']/2;start=core+2.6;bay=stop+32
   pts=[(-m,start+.65),(-m,extent),(m,extent),(m,bay+12),(0,bay),(0,start+.65)]
   for i in range(1,9):
    a=-i*math.pi/8;pts.append((-m/2+m/2*math.cos(a),start+.65+.65*math.sin(a)))
   slab('Median and rounded left-bay nose',[xy(-x,y,t) for x,y in pts])
   # Bay entry taper and left lane boundary.
   strip('Left bay median edge',-.05,.05,start+1,bay,t,.018,yellow)
   strip('Left bay lane divider',-m-.05,-m+.05,stop,bay,t,.018,white)
   for side in (-1,1):strip('Divided median edge',side*m-.05,side*m+.05,bay+12,extent,t,.018,yellow)
  # Left/through symbols are original polygons.
  if (spec['ns'] if t%2==0 else spec['ew'])>=4:
   x=-spec['median']/2+L/2 if spec['median'] else 0;y=stop+8
   pts=[(x-.1,y+1.5),(x+.1,y+1.5),(x+.1,y-.4),(x+.6,y-.4),(x+.6,y-.1),(x+1.4,y-.6),(x+.6,y-1.1),(x+.6,y-.8),(x-.1,y-.8)]
   poly('Left turn arrow',[xy(*p,t) for p in pts],.018,white)
 for sx in (-1,1):
  for sy in (-1,1):
   if 1 not in spec['approaches'] and sx<0:continue
   cx,cy=hx+.4572+R,hy+.4572+R
   # Measured circular return and adjacent walk; tessellated in arc strips.
   for label,ra,rb,z,ma in [('Gutter',R,R+.4572,.009,mats['Concrete']),('Corner curb',R-.1524,R,.1524,mats['Concrete']),('Corner planting verge',R-1.8288,R-.1524,.151,mats['Lawn']),('Corner walk',R-3.3528,R-1.8288,.1524,mats['Concrete'])]:
    vs=[]
    for r in (ra,rb):
     for i in range(25):
      a=i*math.pi/48;vs.append((sx*(cx-r*math.cos(a)),sy*(cy-r*math.sin(a)),z))
    mesh(label,vs,[(i,i+1,26+i,25+i) for i in range(24)],ma)
   pts=[(sx*hx,sy*hy)]+[(sx*(cx-(R+.4572)*math.cos(i*math.pi/48)),sy*(cy-(R+.4572)*math.sin(i*math.pi/48))) for i in range(25)]
   poly('Swept asphalt corner return',pts,.012,mats['Asphalt'])
   rect('Town parcel ground',sx*cx,sx*extent,sy*cy,sy*extent,.149,mats['Lawn'])
   # Fill all quadrants outside the road so the horizon has real ground.
   rect('Roadside parcels',sx*(hx+3.81),sx*extent,sy*(hy+.4572+R),sy*extent,.149,mats['Lawn'])
   rect('Cross-street parcels',sx*(hx+.4572+R),sx*extent,sy*(hy+3.81),sy*extent,.149,mats['Lawn'])
 if spec['radius']>=7:
  # Large outer corner: swept right-turn island and separate slip lane.
  cx,cy=hx+.4572+R,hy+.4572+R
  pts=G.fillet_polygon([(hx+1,hy+1),(hx+.5,hy+3.3),(hx+3.8,hy+.5)],[.25,.25,.25],4)
  slab('Channelizing right-turn island',pts)
 if 1 not in spec['approaches']:
  rect('T junction closed parcel',-extent,-hx-.6096,-extent,extent,.149,mats['Lawn'])
  core=hy+.4572+R
  rect('T closed-side gutter',-hx-.4572,-hx,-core,core,.008,mats['Concrete'])
  slab('T closed-side curb',[(-hx-.6096,-core),(-hx-.4572,-core),(-hx-.4572,core),(-hx-.6096,core)])
  rect('T closed-side verge',-hx-2.286,-hx-.6096,-core,core,.151,mats['Lawn'])
  rect('T junction sidewalk',-hx-3.81,-hx-2.286,-hy-R,hy+R,.1524,mats['Concrete'])
 return rt


def main():
 p=argparse.ArgumentParser();p.add_argument('--spec',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.read_factory_settings(use_empty=True);rootpath=Path(__file__).resolve().parents[2]
 from kit.tiling import export
 rows=json.loads(args.spec.read_text())
 for i,spec in enumerate(rows):
  spec=dict(spec,extent=30);rt=build(spec,rootpath);rt.name='Junction_'+str(spec['seed']);rt.location.x=i*100
  bpy.context.view_layer.update();meshes=[o for o in rt.children_recursive if o.type=='MESH']
  bpy.ops.object.select_all(action='DESELECT')
  for o in meshes:
   o.select_set(True);o.modifiers.new('Game triangles','TRIANGULATE');G.apply(o)
  bpy.context.view_layer.objects.active=meshes[0];bpy.ops.object.join();meshes[0].name=rt.name+'__Surface'
 export(args.out)
 print('ARTERIAL SITES',len(rows),'parametric junction modules',args.out)
if __name__=='__main__':main()
