"""Measured original 96-gallon municipal cart; meters, +Z up, front -Y.

A second lid is staged at +1.25 m for a single atlas bake. Export selects and
restores it; no second body, material, or texture set is delivered.
"""
import argparse,math,sys,json
from pathlib import Path
import bpy,bmesh
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import model as G
from kit.materials import surface
from finishes import polyethylene


def outline(w,d,r,recess=0,grip=0,n=4):
 pts=[]
 # Start on the front-right tangent and proceed counterclockwise.
 for corner,(cx,cy,start) in enumerate([(w/2-r,-d/2+r,-90),(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180)]):
  for i in range(n+1):
   a=math.radians(start+90*i/n);pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
  if corner in (0,2):
   sign=1 if corner==0 else -1
   ys=[-d/2+r+(d-2*r)*j/8 for j in range(1,8)]
   if sign<0:ys=list(reversed(ys))
   pts.extend([(sign*(w/2-grip*math.exp(-(y/.23)**8)),y) for y in ys])
  elif corner==1:
   for x in [(w/2-r)*f for f in [.9,.8,.7,.6,0,-.6,-.7,-.8,-.9]]:
    dep=grip*.8*math.exp(-((abs(x)-.20)/.022)**4)
    pts.append((x,d/2-dep))
  elif corner==3:
   for x,dep in [(-.19,0),(-.145,0),(-.12,.08),(-.105,1),(0,1),(.105,1),(.12,.08),(.145,0),(.19,0)]:
    pts.append((x,-d/2+dep*recess))
 return pts


def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',default='high',choices=['high','game']);p.add_argument('--wear',type=float,default=.35)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True)
 high=a.quality=='high';ns=7 if high else 3
 root=G.pivot('TrashCart',(0,0,0));root['static_root']=True
 black=polyethylene('Sun-aged charcoal HDPE',a.wear,stamp=ROOT/'trash-cart/build/markings/city.png')
 lidblack=polyethylene('Charcoal lid HDPE',a.wear,(.0035,.005,.006),lid=True)
 blue=polyethylene('Blue lid HDPE',a.wear,(.012,.066,.19),lid=True)
 rubber=polyethylene('Solid black wheel tread',a.wear,(.009,.010,.011),wheel=True)
 steel=surface('Zinc plated axle and lifting bar','stainless',a.wear,grime=.15,dust=.10)
 hub=polyethylene('Molded black wheel web',a.wear,(.012,.014,.015),wheel=True)
 def add(ob,parent=root):return G.attach(ob,parent,'TrashCart')
 # Continuous thick-walled molded shell. Front channel and side gripping
 # recesses are in the wall itself, not plates attached over a box.
 stations=[(0,.558,.642,.070,.092,0),(.020,.566,.650,.074,.094,0),
           (.35,.615,.690,.078,.088,.012),(.64,.650,.725,.085,.077,.016),
           (.682,.660,.735,.087,.068,.015),(.704,.666,.740,.088,.008,.012),
           (.770,.709,.769,.095,0,0),(.797,.716,.778,.097,0,0),
           (1.004,.726,.786,.10,0,0),(1.016,.742,.803,.10,0,0),
           (1.025,.742,.803,.10,0,0)]
 def ring(st,inner=False):
  z,w,d,r,recess,grip=st;t=.006 if inner else 0
  pts=outline(w-2*t,d-2*t,r-t,recess,grip,3) # Match structural high/low rays at thin wheel-well walls.
  result=[]
  for x,y in pts:
   yy=y-.035
   zz=z
   if z<.04 and yy>.100:
    # A closed molded wheel-well floor rises over the rear axle, while the
    # front heel remains on the ground. Both inner and outer floors follow it.
    zz+=max(0,.127+math.sqrt(max(0,.147**2-(yy-.27385)**2))-.014)
   result.append((x,yy,zz+(t if z<.04 else 0)))
  return result
 loops=[ring(st) for st in stations]
 loops += [ring(st,True) for st in reversed(stations)]
 n=len(loops[0]);vs=[v for loop in loops for v in loop]
 fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(loops)-1) for i in range(n)]
 # Close nonplanar bottom skins with explicit fans, never an invalid ngon.
 for j,z in [(0,0),(len(loops)-1,.006)]:
  ci=len(vs);vs.append((0,-.065,z))
  fs.extend([(ci,j*n+(i+1)%n,j*n+i) for i in range(n)])
 body=G.mesh('Rotomolded hollow body and recessed lift channel',vs,fs,black)
 # Nonplanar wheel-well quads must use the same diagonals in source and game.
 bm=bmesh.new();bm.from_mesh(body.data)
 bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
 bm.to_mesh(body.data);bm.free();G.smooth(body,45);add(body)
 # Reinforced upper lifting saddle: hollow behind the molded front flange.
 add(G.box('Upper lifter saddle',(0,-.428,.914),(.262,.032,.043),black,.012,3 if high else 1))
 add(G.cylinder('Rotating steel lift bar',(-.125,-.336,.535),(.125,-.336,.535),.0095,steel,24 if high else 12))
 for s in (-1,1):
  add(G.box('Sealed lift bar journal',(s*.133,-.335,.535),(.035,.059,.056),black,.012,3 if high else 1))
 # Body-integral rear grip with real clearance below its crossbar.
 for s in (-1,1):
  add(G.box('Rear handle support',(s*.263,.380,1.007),(.064,.140,.054),black,.013,3 if high else 1))
 add(G.cylinder('Integral rear carry grip',(-.265,.43085,1.015),(.265,.43085,1.015),.020,black,24 if high else 12))
 add(G.cylinder('Steel axle',(-.331,.27385,.127),(.331,.27385,.127),.0079375,steel,20 if high else 10))
 for s in (-1,1):
  add(G.box('Rear axle journal gusset',(s*.22,.252,.225),(.066,.081,.19),black,.012,3 if high else 1))
  add(G.box('Molded axle journal',(s*.22,.269,.174),(.062,.067,.118),black,.014,3 if high else 1))
 # Two separate wheels, each with a closed tire and recessed web/spokes.
 for s,label in [(-1,'Left'),(1,'Right')]:
  x=s*.305
  pivot=G.pivot('Wheel_'+label,(x,.27385,.127),'X',(-360,360));pivot.parent=root
  prof=[(-.023,.092),(-.023,.116),(-.017,.125),(-.009,.127),(.009,.127),(.017,.125),(.023,.116),(.023,.092)]
  tire=G.lathe('Wheel '+label+' tire',[(x+h,min(r,.1255) if high else r) for h,r in prof],rubber,64 if high else 32,axis='X',center=(.27385,.127),closed=True)
  add(tire,pivot)
  disk=G.lathe('Wheel '+label+' recessed web',[(x-.018,.083),(x-.018,.096),(x+.018,.096),(x+.018,.083)],hub,48 if high else 24,axis='X',center=(.27385,.127),closed=True);add(disk,pivot)
  for k in range(10):
   th=k*math.tau/10
   y=.27385+math.cos(th)*.058;z=.127+math.sin(th)*.058
   spoke=G.box('Wheel '+label+' raised spoke',(x+s*.020,y,z),(.008,.074,.012),hub,.003 if high else 0,2)
   spoke.rotation_euler.x=th;add(spoke,pivot)
  add(G.cylinder('Wheel '+label+' hub', (x-.027,.27385,.127),(x+.027,.27385,.127),.024,hub,24 if high else 12),pivot)
  add(G.cylinder('Wheel '+label+' axle cap',(x+s*.027,.27385,.127),(x+s*.031,.27385,.127),.012,steel,16 if high else 8),pivot)
  if high:
   for k in range(64):
    th=k*math.tau/64
    ob=G.box('Wheel '+label+' tread relief',(x,.27385+.1263*math.cos(th),.127+.1263*math.sin(th)),(.029,.0014,.007),rubber,.0005,1)
    ob.rotation_euler.x=th;add(ob,pivot)
 # Lid is a thin crowned shell with a peripheral skirt and returns.
 for variant,mat,offset,name in [('trash',lidblack,0,'Lid'),('recycling',blue,1.25,'AtlasBlueLid')]:
  pivot=G.pivot(name,(offset,.350,1.032),'X',(-110,0));pivot.parent=root
  pivot['delivery_variant']=variant
  if offset:pivot['atlas_staging_offset']=(offset,0,0);pivot['delivery_name']='Lid'
  def lidadd(ob):
   ob.location.x+=offset
   return add(ob,pivot)
  path=[(1.018,.75165,.812,.080),(1.038,.75565,.820,.082),
        (1.048,.727,.797,.085),(1.075,.605,.666,.105),
        (1.078,.35,.410,.105),(1.079,.10,.16,.04)]
  lidloops=[[(x,y-.04085,z) for x,y in G.rounded_rectangle(w,d,r,ns)] for z,w,d,r in path]
  lidloops += [[(x,y-.04085,z-.005) for x,y in G.rounded_rectangle(w-.008,d-.008,max(.01,r-.004),ns)] for z,w,d,r in reversed(path)]
  ln=len(lidloops[0]);lv=[v for ring in lidloops for v in ring]
  lf=[(j*ln+i,j*ln+(i+1)%ln,((j+1)%len(lidloops))*ln+(i+1)%ln,((j+1)%len(lidloops))*ln+i)
      for j in range(len(lidloops)) if j!=len(path)-1 for i in range(ln)]
  lf.extend([tuple(range((len(path)-1)*ln,len(path)*ln)),tuple(reversed(range(len(path)*ln,(len(path)+1)*ln)))])
  lidadd(G.smooth(G.mesh(variant+' crowned lid skin',lv,lf,mat),45))
  # Raised perimeter bead leaves a visible stepped sealing reveal.
  rimloops=[[(x,y-.04085,z) for x,y in G.rounded_rectangle(w,d,r,ns)]
            for z,w,d,r in [(1.044,.727,.793,.083),(1.053,.727,.793,.083),
                            (1.056,.698,.764,.080),(1.044,.698,.764,.080)]]
  lidadd(G.smooth(G.ring_loft(variant+' raised perimeter sealing bead',rimloops,mat),45))
  # Molded stiffness channels and an accessible front lifting tab.
  for s in (-1,1):
   rib=G.box(variant+' lid reinforcing rail',(s*.257,-.065,1.08355),(.054,.594,.030),mat,.012,4 if high else 2);lidadd(rib)
  for y in (-.20,.0):lidadd(G.box(variant+' lid cross rib',(0,y,1.084),(.454,.026,.019),mat,.009,3 if high else 1))
  lidadd(G.box(variant+' front hand tab',(0,-.426,1.041),(.171,.049,.018),mat,.008,3 if high else 1))
  for s in (-1,1):
   lidadd(G.box(variant+' hinge strap',(s*.263,.309,1.046),(.061,.151,.022),mat,.008,3 if high else 1))
   lidadd(G.cylinder(variant+' hinge barrel',(s*.263-.036,.350,1.032),(s*.263+.036,.350,1.032),.022,mat,24 if high else 12))
   if not offset:add(G.cylinder('Body hinge pin',(s*.263-.042,.350,1.032),(s*.263+.042,.350,1.032),.008,steel,16 if high else 8))
  if variant=='recycling':
   # The large identification mark retains a compact molded silhouette in game.
   curve=bpy.data.curves.new('Molded standard recycling symbol','FONT')
   curve.body='♻';curve.font=bpy.data.fonts.load('/usr/share/fonts/TTF/DejaVuSans.ttf')
   curve.size=.38;curve.align_x='CENTER';curve.align_y='CENTER'
   curve.extrude=.0015;curve.bevel_depth=0;curve.bevel_resolution=0;curve.resolution_u=1
   symbol=bpy.data.objects.new('Recycling symbol source relief',curve);bpy.context.collection.objects.link(symbol)
   symbol.location=(0,.17,1.0792)
   symbolmat=polyethylene('Sun exposed molded recycling relief',a.wear,(.018,.085,.225),lid=True)
   curve.materials.append(symbolmat)
   bpy.ops.object.select_all(action='DESELECT');symbol.select_set(True);bpy.context.view_layer.objects.active=symbol
   bpy.ops.object.convert(target='MESH');symbol=bpy.context.object
   # Conform to our own generated crown, preserving the font extrusion profile.
   from mathutils import Vector
   from mathutils.bvhtree import BVHTree
   crown=bpy.data.objects[variant+' crowned lid skin'];bpy.context.view_layer.update()
   tree=BVHTree.FromPolygons([crown.matrix_world@v.co for v in crown.data.vertices],
                            [list(p.vertices) for p in crown.data.polygons])
   for vertex in symbol.data.vertices:
    hit=tree.ray_cast(Vector((offset+vertex.co.x,.17+vertex.co.y,2)),Vector((0,0,-1)))[0]
    if hit is None:raise RuntimeError('Recycling relief lies outside its authored lid')
    vertex.co.z+=hit.z-symbol.location.z
   bm=bmesh.new();bm.from_mesh(symbol.data)
   bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
   bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8)
   bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(symbol.data);bm.free()
   lidadd(symbol)
 # Place the center of the ground-contact footprint at the asset origin.
 from mathutils import Matrix
 for child in root.children:
  if child.type=='MESH':child.data.transform(Matrix.Translation((0,.041075,0)))
  else:child.location.y+=.041075
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 sc['asset']='TrashCart';sc['quality']=a.quality;sc['wear']=a.wear;sc['seed']=73
 sc['atlas_staging']='Recycling lid only at X +1.25 m; exporter restores hinge and selects one lid'
 bpy.context.view_layer.update();bpy.ops.file.pack_all();Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
 print('BUILT',a.quality,flush=True)

if __name__=='__main__':main()
