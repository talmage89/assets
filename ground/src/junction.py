"""Additive parametric arterial pieces, independent of Ground's delivery graph.

Widths, corner returns, raised medians with bay tapers/noses, and channelizing
islands. Only the canonical library's materials are read, never modified.
"""
import math,sys,json,argparse,random
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from ground.src.junction_surfaces import lanes, value, road_grid
from kit import model as G
from kit.tiling import world_uv
_GROUND_MATERIALS={}

def build(spec,rootpath):
 from mathutils import Vector
 global _GROUND_MATERIALS
 # Import the canonical library once per live scene. The four-module export
 # must not retain four copies of its packed images and material graphs.
 try:cached=bool(_GROUND_MATERIALS) and all(bpy.data.materials.get(m.name)==m for m in _GROUND_MATERIALS.values())
 except ReferenceError:cached=False
 if not cached:
  before=set(bpy.context.scene.objects);before_mats=set(bpy.data.materials);before_images=set(bpy.data.images)
  bpy.ops.import_scene.gltf(filepath=str((rootpath/'ground/export/Ground.glb').resolve()))
  old=set(bpy.context.scene.objects)-before;added=set(bpy.data.materials)-before_mats
  _GROUND_MATERIALS={k:next(m for m in added if m.name==k or m.name.startswith(k+'.')) for k in ('Asphalt','Concrete','Lawn')}
  for o in old:bpy.data.objects.remove(o,do_unlink=True)
  for m in added-set(_GROUND_MATERIALS.values()):
   if m.users==0:bpy.data.materials.remove(m)
  for im in set(bpy.data.images)-before_images:
   if im.users==0:bpy.data.images.remove(im)
 mats=dict(_GROUND_MATERIALS)
 mats['Asphalt']=mats['Asphalt'].copy();mats['Asphalt'].name='Arterial dry asphalt'
 p=next(n for n in mats['Asphalt'].node_tree.nodes if n.type=='BSDF_PRINCIPLED')
 for link in list(p.inputs['Roughness'].links):mats['Asphalt'].node_tree.links.remove(link)
 p.inputs['Roughness'].default_value=.96
 polished=mats['Asphalt'].copy();polished.name='Arterial tire-polished aggregate';next(n for n in polished.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Roughness'].default_value=.74
 def material(n,c):
  m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.88
  m['arterial_base_color']=list(c);ns=m.node_tree.nodes;ls=m.node_tree.links;vc=ns.new('ShaderNodeVertexColor');vc.layer_name='Tint';ls.new(vc.outputs['Color'],p.inputs['Base Color']);return m
 white=material('Arterial aged white',(.55,.55,.50));yellow=material('Arterial faded yellow',(.52,.32,.012));seal=material('Arterial loop seal',(.012,.012,.011))
 L=3.3528;hx=spec['ns']*L/2+spec['median']/2;hy=spec['ew']*L/2;R=spec['radius'];extent=spec.get('extent',350)
 rt=G.pivot('ParametricJunction',(0,0,0));rt['presentation_only']=True
 def mesh(n,vs,fs,ma):
  o=G.mesh(n,vs,fs,ma)
  for face in o.data.polygons:
   zz=[o.data.vertices[i].co.z for i in face.vertices]
   if max(zz)-min(zz)<1e-7 and face.normal.z<0:face.flip()
  o.data.update();o.parent=rt
  if ma in (white,yellow):
   # Only paint gets small fracture stations; wheel crossings abrade its edges.
   import bmesh
   bm=bmesh.new();bm.from_mesh(o.data)
   for axis in (0,1):
    lo=min(v.co[axis] for v in bm.verts);hi=max(v.co[axis] for v in bm.verts)
    if hi-lo>.4 and hi-lo<25:
     for index in range(math.floor(lo/.40)+1,math.ceil(hi/.40)):
      co=[0,0,0];co[axis]=index*.40;no=[0,0,0];no[axis]=1
      bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=co,plane_no=no)
   bm.to_mesh(o.data);bm.free()
   ca=o.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
   for vert,datum in zip(o.data.vertices,ca.data):
    wheel=0
    for turn in spec['approaches']:
     aa=turn*math.pi/2;xx=vert.co.x*math.cos(aa)+vert.co.y*math.sin(aa);yy=-vert.co.x*math.sin(aa)+vert.co.y*math.cos(aa)
     if yy<0:continue
     for center in lanes(spec,turn):
      wheel=max(wheel,math.exp(-((abs(xx-center)-.78)/.35)**2))
    broken=.72+.28*math.sin(vert.co.x*31+vert.co.y*19)**2
    factor=1-.72*wheel*broken
    datum.color=(factor,factor,factor,1)
  if ma.get('arterial_base_color'):
   ca=o.data.color_attributes.get('Tint') or o.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
   for datum in ca.data:
    factor=datum.color[0] if ma in (white,yellow) else 1
    datum.color=(*[v*factor for v in ma['arterial_base_color']],1)
  coverage=6.096 if ma==mats['Asphalt'] else 1.524 if ma==mats['Concrete'] else 3.048
  world_uv(o,coverage)
  uv=o.data.uv_layers.active
  for f in o.data.polygons:
   if abs(f.normal.z)>.5:continue
   axes=(1,2) if abs(f.normal.x)>.5 else (0,2)
   for li in f.loop_indices:
    v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]/coverage,v[axes[1]]/coverage)
  if ma in mats.values():
   ca=o.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
   for vert,datum in zip(o.data.vertices,ca.data):
    f=value(vert.co.x,vert.co.y,spec) if ma==mats['Asphalt'] else 1
    datum.color=(f,f,f,1)
  if ma==mats['Asphalt'] and n.startswith('Continuing worn'):
   o.data.materials.append(polished)
   for face in o.data.polygons:
    p=face.center
    for turn in spec['approaches']:
     aa=turn*math.pi/2;xx=p.x*math.cos(aa)+p.y*math.sin(aa);yy=-p.x*math.sin(aa)+p.y*math.cos(aa)
     if yy<0:continue
     if any(abs(abs(xx-c)-.78)<.30 for c in lanes(spec,turn)):face.material_index=1
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
  approach_before=set(bpy.context.scene.objects)
  h=hx if t%2==0 else hy;fh=hy if t%2==0 else hx;core=fh+.4572+R;stop=core+3.9624
  xx,yy=road_grid(h,fh,stop,extent,lanes(spec,t));vs=[(*xy(x,y,t),.012) for y in yy for x in xx];N=len(xx)
  mesh('Continuing worn road',vs,[(j*N+i,j*N+i+1,(j+1)*N+i+1,(j+1)*N+i) for j in range(len(yy)-1) for i in range(N-1)],mats['Asphalt'])
  for side in (-1,1):
   # Gutter / full-width unscaled sidewalk / planting strip.
   strip('Concrete gutter',side*h,side*(h+.4572),core,extent,t,.008,mats['Concrete'])
   pts=[xy(side*x,y,t) for x,y in [(h+.4572,core),(h+.6096,core),(h+.6096,extent),(h+.4572,extent)]];slab('Straight curb',pts)
   strip('Planted verge',side*(h+.6096),side*(h+2.286),core,extent,t,.151,mats['Lawn'])
   strip('Continuing sidewalk',side*(h+2.286),side*(h+3.81),core,extent,t,.1524,mats['Concrete'])
   # Walking paving has joints, generated in geometry.
   for y in range(math.ceil(core/1.524),math.ceil(extent/1.524)):
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
    for y in range(round(stop+3),math.floor(extent-3.048),9):strip('White lane dash',x-.05,x+.05,y,y+3.048,t,.016,white)
  strip('Stop bar',-h,(L/2 if spec['ns']==5 and t%2==0 else -.1),stop-.3048,stop+.3048,t,.017,white)
  for i in range(math.floor(2*h/.76)):
   x=-h+.3+i*.76;strip('Crosswalk bar',x,x+.4572,core+.6,core+2.4288,t,.017,white)
  for x in lanes(spec,t):
   if abs(x)>h-.5:continue
   y=stop+3
   pts=[(x-.9144,y-.70),(x-.70,y-.9144),(x+.70,y-.9144),(x+.9144,y-.70),(x+.9144,y+.70),(x+.70,y+.9144),(x-.70,y+.9144),(x-.9144,y+.70)]
   for a,b in zip(pts,pts[1:]+pts[:1]):
    dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);ox,oy=-dy/l*.005,dx/l*.005
    poly('Sealed detector sawcut',[xy(*p,t) for p in ((a[0]+ox,a[1]+oy),(b[0]+ox,b[1]+oy),(b[0]-ox,b[1]-oy),(a[0]-ox,a[1]-oy))],.018,seal)
   lead=y+.24+x*.045
   strip('Detector lead-in sealed slot',-h-.4572,x-.9144,lead-.005,lead+.005,t,.019,seal)
  strip('Curbside detector lead collection slot',-h-.28,-h-.27,stop+2.55,stop+3.4,t,.020,seal)
  # One flush pull box takes each approach's twisted lead-ins.
  strip('Detector pull-box concrete surround',-h-.44,-h+.02,stop+2.2,stop+2.82,t,.021,mats['Concrete'])
  strip('Detector pull-box cast lid',-h-.39,-h-.03,stop+2.25,stop+2.77,t,.023,seal)
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
  # Routed cracks follow lane loading, with short branching seams.
  rng=random.Random(spec['seed']*71+t*13)
  for index in range(2):
   start=stop+rng.uniform(9,39);startx=rng.uniform(-h+.4,-.5);reach=min(h-.4-startx,rng.uniform(2.2,5.5))
   pts=[(startx+k*reach/6,start+k*.17+rng.uniform(-.27,.27)) for k in range(7)]
   if index:pts=pts[:4]+[(pts[3][0]-.25,pts[3][1]+1.3)]
   for a,b in zip(pts,pts[1:]):
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);ox,oy=-dy/length*.022,dx/length*.022
    poly('Routed crack seal',[xy(*p,t) for p in ((a[0]+ox,a[1]+oy),(b[0]+ox,b[1]+oy),(b[0]-ox,b[1]-oy),(a[0]-ox,a[1]-oy))],.014,seal)
  # Utility repair retains the same aggregate and darkens only its patch.
  if t==spec['approaches'][spec['seed']%len(spec['approaches'])]:
   patch=strip('Utility trench wearing patch',-h+.2,-h+2.4,stop+17.4,stop+18.65,t,.014,mats['Asphalt'])
   for datum in patch.data.color_attributes['Tint'].data:datum.color=(.26,.26,.26,1)
   for edge in (stop+17.4,stop+18.65):strip('Utility patch sealed edge',-h+.18,-h+2.42,edge-.018,edge+.018,t,.015,seal)
  approach_meshes=[ob for ob in set(bpy.context.scene.objects)-approach_before if ob.type=='MESH']
  for ob in approach_meshes:ob['arterial_approach']=t
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
 if spec['radius']>=10.668:
  # Large outer corner: swept right-turn island and separate slip lane.
  cx,cy=hx+.4572+R,hy+.4572+R
  pts=G.fillet_polygon([(hx+.55,hy+.55),(hx+.1,hy+1.5),(hx+1.5,hy+.1)],[.12,.12,.12],4)
  slab('Channelizing right-turn island',pts)
  clear=min(math.hypot(cx-x,cy-y)-(R+.4572) for x,y in pts)
  assert clear>=L,('Channelized carriageway narrower than one lane',clear)
  rt['island_min_carriageway_width_m']=clear
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
  spec=dict(spec,extent=100);rt=build(spec,rootpath);rt.name='Junction_'+str(spec['seed']);rt.location.x=i*250
  bpy.context.view_layer.update();meshes=[o for o in rt.children_recursive if o.type=='MESH']
  pieces={}
  for ob in meshes:
   ob.data.calc_loop_triangles();key=str(ob.get('arterial_approach','corners'))
   pieces[key]=pieces.get(key,0)+len(ob.data.loop_triangles)
  assert all(n<=2000 for key,n in pieces.items() if key!='corners'),('Approach piece budget',spec['seed'],pieces)
  rt['measured_piece_triangles']=pieces;print('APPROACH PIECES',spec['seed'],pieces,flush=True)
  bpy.ops.object.select_all(action='DESELECT')
  for o in meshes:o.select_set(True)
  bpy.context.view_layer.objects.active=meshes[0];bpy.ops.object.join();ob=meshes[0];ob.name=rt.name+'__Surface'
  ob.modifiers.new('Game triangles','TRIANGULATE');G.apply(ob)
  local=[rt.matrix_world.inverted()@ob.matrix_world@v.co for v in ob.data.vertices]
  assert max(abs(p[k]) for p in local for k in (0,1))<=spec['extent']+.001,('Ground outside module',spec['seed'])
  print('JUNCTION',spec['seed'],len(ob.data.polygons),'triangles; bounded to',spec['extent'],'m radius',flush=True)
 export(args.out)
 print('ARTERIAL SITES',len(rows),'parametric junction modules',args.out)
if __name__=='__main__':main()
