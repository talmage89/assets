"""Original Waycroft signal, Morrow Controls cabinet and Cress APS construction."""
import math
from pathlib import Path
import bpy
from mathutils import Vector
from geometry import *
from graphics import TILES
from plan import *
from layout import SITES

def shaft_radius(z):
 return SHAFT_R0+(SHAFT_R1-SHAFT_R0)*(z-SHAFT_BASE)/(POLE_TOP-SHAFT_BASE)
def arm_radius(distance):
 return (.1778-(distance-.2735)*.011666667/2)/math.cos(math.pi/12)

def lens(rt,name,center,radius,kind,lit=False):
 x,y,z=center
 # The shared sheet carries an opaque circular optical cover and LED packages.
 j=TILES.index(kind);rect=((j%4)/4,1-(j//4+1)/2,(j%4+1)/4,1-(j//4)/2)
 o=quad(name,(x,y-.0003,z),radius*2,radius*2,'lit' if lit else 'off',rt,rect)
 o['signal_lens']=True;o['signal_kind']=kind;o['powered']=lit
 o['off_material']='SharedLens_Off';o['lit_material']='SharedLens_Lit'
 return o

def visor(rt,x,z,style,coating):
 # Formed sheet with two shells and actual 1.6 mm gauge, open drainage below.
 start,end=(-.35,math.pi+.35) if style=='tunnel' else (-.03,math.pi+.03)
 n=20 if style=='tunnel' else 18
 vs=[];fs=[];shell=[]
 for r in (.1585,.1601):
  for y in (-.147,-.147-(.245 if style=='tunnel' else .205)):
   for i in range(n+1):
    a=start+(end-start)*i/n
    vs.append((x+r*math.cos(a),y,z+r*math.sin(a)))
 stride=n+1
 for k in range(n):
  fs += [(k,k+1,stride+k+1,stride+k),(2*stride+k,3*stride+k,3*stride+k+1,2*stride+k+1),
         (stride+k,stride+k+1,3*stride+k+1,3*stride+k)]
 for k in (0,n):fs.append((k,stride+k,3*stride+k,2*stride+k))
 o=G.smooth(G.mesh('Sheet visor',vs,fs,M[coating]),40);o.data.materials.append(M['black'])
 for i,p in enumerate(o.data.polygons):
  if i%3==0:p.material_index=1
 return own(o,rt)

def aperture(rt,x,z):
 n=20;vs=[];fs=[]
 for y,r in [(-.145,.169),(-.151,.1524),(-.140,.1524)]:
  vs.extend((x+r*math.cos(i*math.tau/n),y,z+r*math.sin(i*math.tau/n)) for i in range(n))
 for j in range(1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 return G.smooth(mesh('Door lens retaining rim',vs,fs,'black',rt),40)

def head(name,parent,p=(0,0,0),yaw=0,kind='three',color='yellow',style='tunnel',border=True,active='red'):
 rt=root(name,p,parent,kind='Head_'+kind,yaw=yaw)
 rt['pivot_axis']='Z';rt['range_degrees']=[-15,15];rt['swing_axis']='X';rt['swing_range_degrees']=[-4,4]
 if kind=='fya':sections=[(0,0,'red_arrow'),(0,1,'yellow_arrow'),(0,2,'yellow_arrow'),(0,3,'green_arrow')]
 elif kind=='five':sections=[(0,0,'red'),(-.187,1,'yellow'),(.187,1,'yellow_arrow'),(-.187,2,'green'),(.187,2,'green_arrow')]
 elif kind=='protected':sections=[(0,0,'red_arrow'),(0,1,'yellow_arrow'),(0,2,'green_arrow')]
 else:sections=[(0,0,'red'),(0,1,'yellow'),(0,2,'green')]
 rows=max(j for x,j,k in sections)+1;height=.370*rows+.02;width=.754 if kind=='five' else .376
 # Rounded thin backplate with a two-inch retroreflective border when selected.
 bpw=width+.254;bph=height+.254;mid=-.12-height/2
 if border:
  profile('Two-inch backplate border',[(x,z+mid) for x,z in G.rounded_rectangle(bpw,bph,.045,3)],.116,.119,'border',rt)
  bpw-=.1016;bph-=.1016
 profile('Dull black backplate',[(x,z+mid) for x,z in G.rounded_rectangle(bpw,bph,.031,3)],.110,.114,'black',rt)
 for section,(x,j,kindmark) in enumerate(sections):
  z=-.305-j*.370
  # Compound die-cast housing: stepped rear bulge, rounded shoulder and door.
  loops=[]
  for y,w,h,r in [(.112,.272,.291,.065),(.060,.335,.345,.072),(-.130,.354,.355,.027)]:
   loops.append([(x+u,y,z+v) for u,v in G.rounded_rectangle(w,h,r,2)])
  body=G.loft('Compound cast section',loops,M[color]);body.data.polygons[len(body.data.polygons)-2].material_index=0
  # Back caps are hidden against the backplate; delete them before triangulation.
  import bmesh
  bm=bmesh.new();bm.from_mesh(body.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[-2]],context='FACES');bm.to_mesh(body.data);bm.free()
  own(G.smooth(body,40),rt)
  aperture(rt,x,z);visor(rt,x,z,style,color)
  for side in (-1,1):
   box('Door hinge' if side<0 else 'Captive latch',(x+side*.176,-.110,z+.105),(.024,.034,.064),color,rt,0)
   if side<0:cyl('Hinge pin',(x+side*.178,-.132,z+.088),(x+side*.178,-.132,z+.125),.005,'steel',rt,6)
   else:quad('Captive latch screw cap',(x+side*.178,-.138,z+.105),.010,.010,'steel',rt)
  # Lens remains a named part even in the dark state.
  on=(kindmark==active and (kind!='fya' or j!=1)) if active else False
  ob=lens(rt,f'{name}__S{section:02d}_{kindmark}',(x,-.144,z),.1524,kindmark,on)
  ob['section_index']=section
  if kind=='fya' and j==2:ob['flashing_yellow_arrow']=True
 # Keep the backplate below the indexed hanger, with real swing clearance.
 for ob in rt.children:
  if ob.type=='MESH':ob.location.z-=.085
 cyl('Indexed top boss',(0,0,-.215),(0,0,-.04),.028,color,rt,12)
 cyl('Top mounting stem',(0,0,-.05),(0,0,.04),.021,'steel',rt,10)
 box('Original maker blank',(0,.114,-.485),(.086,.002,.023),'steel',rt,0)
 join_fixed(rt);return rt

def footing(rt,finish='zinc',pedestal=False):
 radius=.24 if pedestal else .6096
 cyl('Round concrete pier',(0,0,0),(0,0,.1524),radius,'concrete',rt,24 if pedestal else 40)
 if pedestal:
  # 4 inch pedestal with cast aluminum frangible transformer base.
  own(G.lathe('Cast pedestal base',[(.1524,.135),(.20,.135),(.32,.092),(.43,.060)],M[finish],16),rt)
  for a in (45,135,225,315):
   x,y=.105*math.cos(math.radians(a)),.105*math.sin(math.radians(a));bolt('Pedestal anchor',(x,y,.20),(0,0,1),.008,'steel',rt)
  return
 # FDOT S1: 30 inch plate, six 1.75 inch rods on derived 23 inch circle.
 plate=ring('Base plate',PLATE_BOTTOM,.118,.381,PLATE_THICK,finish,rt,40)
 for j in range(6):
  a=j*math.tau/6;x,y=.2921*math.cos(a),.2921*math.sin(a)
  G.boolean(plate,G.cylinder('Anchor clearance bore',(x,y,PLATE_BOTTOM-.010),(x,y,SHAFT_BASE+.010),.0238,M[finish],12))
 plate.data.materials.clear();plate.data.materials.append(M[finish])
 import surfaces;surfaces.assign(plate)
 for j in range(6):
  a=j*math.tau/6;x,y=.2921*math.cos(a),.2921*math.sin(a)
  cyl('Anchor rod',(x,y,.145),(x,y,.36885),.022225,'steel',rt,8)
  cyl('Leveling nut',(x,y,PLATE_BOTTOM-.042),(x,y,PLATE_BOTTOM),.038,'steel',rt,6)
  cyl('Plate washer',(x,y,SHAFT_BASE),(x,y,SHAFT_BASE+.0095),.047,finish,rt,12)
  cyl('Anchor nut',(x,y,SHAFT_BASE+.0095),(x,y,SHAFT_BASE+.0475),.039,'steel',rt,6)
  cyl('Jam nut',(x,y,SHAFT_BASE+.0475),(x,y,SHAFT_BASE+.0705),.039,'steel',rt,6)
  # Individual cast nut covers rather than a skirt concealing the real joint.
  own(G.lathe('Nut weather cover',[(z-.01315,r) for z,r in [(.343,.049),(.375,.049),(.395,.034),(.400,0),(.397,0),(.392,.032),(.373,.046),(.343,.0375)]],M[finish],12,center=(x,y),closed=True),rt)

def mast(name,p,angle,plan,parent=None,shared_pole=False):
 rt=root(name,p,parent,kind='MastArm',yaw=angle);rt['arm_reach_m']=plan.arm;rt['finish']=plan.finish
 rt['pole_shared_with']='Mast_'+str(int(angle/90)-1) if SITES[plan.seed].diagonal and int(angle/90)%2 else ''
 footing(rt,plan.finish)
 # 12-sided brake-formed hollow steel; sealed installed parts have no hidden bore.
 own(G.lathe('Tapered shaft',[(SHAFT_BASE,SHAFT_R0),(POLE_TOP,SHAFT_R1)],M[plan.finish],12),rt)
 cyl('Pole cap',(0,0,POLE_TOP),(0,0,POLE_TOP+.021),SHAFT_R1+.0026,plan.finish,rt,12)
 # Handhole lies on the opposite face from arm, with its rounded end frame.
 # 11-gauge cover follows the two real polygonal shaft facets.
 radius=.058;straight=.273/2-radius;bends=3
 lower=[-straight-radius*math.cos(i*math.pi/(2*bends)) for i in range(bends+1)]
 levels=lower+[0]+[-z for z in reversed(lower)];vs=[];fs=[];stride=3;layer=len(levels)*stride
 for offset in (-.001,.00204):
  for zz in levels:
   distance=max(abs(zz)-straight,0);half=.146/2-radius+math.sqrt(max(0,radius*radius-distance*distance));z=.74+zz
   for y in (-half,0,half):vs.append((shaft_radius(z)-math.tan(math.pi/12)*abs(y)+offset,y,z))
 for j in range(len(levels)-1):
  for i in range(2):
   k=j*stride+i;q=(k,k+1,k+stride+1,k+stride)
   fs.extend([q,tuple(v+layer for v in reversed(q))])
 perimeter=list(range(stride))+[j*stride+2 for j in range(1,len(levels))]+[(len(levels)-1)*stride+i for i in (1,0)]+[j*stride for j in range(len(levels)-2,0,-1)]
 for i,k in enumerate(perimeter):
  q=perimeter[(i+1)%len(perimeter)];fs.append((k,k+layer,q+layer,q))
 mesh('Curved handhole cover',vs,fs,plan.finish,rt)
 for z in (.64,.84):bolt('Handhole screw',(shaft_radius(z)+.00204,0,z),(1,0,0),.004,'steel',rt)
 normal=Vector((math.cos(math.pi/12),math.sin(math.pi/12),0));point=normal*(shaft_radius(.96)*math.cos(math.pi/12)+.001)
 tag=box('Pole identification tag',(point.x,point.y,.96),(.002,.084,.042),'steel',rt,0);tag.rotation_euler.z=math.pi/12
 arm_len=plan.arm;z=ARM_Z
 # Paired vertical flange, top/bottom box gussets and six through-bolts.
 for x in (-.225,-.263):
  box('Arm connection flange',(x,0,z),(.01905,.508,.635),plan.finish,rt,.006)
 for y in (-.18,.18):
  for zz in (-.22,0,.22):bolt('Arm connection bolt',(-.282,y,z+zz),(-1,0,0),.016, 'steel',rt)
 # Four 3/4-inch walls form the welded transition box; it is hollow,
 # rather than two solid wedges. Rear edges follow the real pole facets.
 def pole_face(y,zz):
  rr=shaft_radius(zz)*math.cos(math.pi/12)
  return max((rr-math.sin((k+.5)*math.tau/12)*y)/math.cos((k+.5)*math.tau/12)
             for k in range(12) if math.cos((k+.5)*math.tau/12)<-1e-5)
 loops=[]
 for back,inside in ((False,False),(True,False),(False,True),(True,True)):
  gauge=.01905 if inside else 0;ww=(.115 if back else .178)-gauge;hh=.25-gauge
  loops.append([((pole_face(y,z+zz)+.002) if back else -.225,y,z+zz) for y,zz in ((-ww,-hh),(ww,-hh),(ww,hh),(-ww,hh))])
 vs=[v for loop in loops for v in loop];faces=[]
 for i in range(4):
  j=(i+1)%4
  faces.extend([(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)])
 mesh('Folded pole connection box',vs,faces,plan.finish,rt)
 # 2 degree camber and 0.14 in/ft diameter taper. Original shorter arm options.
 loops=[]
 for t in (0,.16,.48,.78,1):
  x=-.2735-(arm_len-.2735)*t;zz=z+math.tan(math.radians(2))*abs(x+.2735)
  rad=arm_radius(abs(x))
  loops.append([(x,rad*math.cos(i*math.tau/12),zz+rad*math.sin(i*math.tau/12)) for i in range(12)])
 own(G.loft('Cambered tapered mast arm',loops,M[plan.finish]),rt)
 cyl('Vented end cap',(-arm_len,0,z+(arm_len-.2735)*.03492),(-arm_len-.012,0,z+(arm_len-.2735)*.03492),arm_radius(arm_len),plan.finish,rt,12)
 # Two through faces eight feet apart; turn face over central left-turn lane.
 site=SITES[plan.seed];turn=int(angle/90);stations=[site.face(turn)+1.02-x for x in site.positions(turn)]
 if site.diagonal and turn%2:stations=[site.core(0)-1+x for x in site.positions(turn)]
 for j,dist in enumerate(stations):
  zz=z+(dist-.2735)*.03492
  # Balanced rigid clamp: steel collars, rear support spine and aiming clevis.
  cyl('Arm clamp collar',(-dist-.045,0,zz),(-dist+.045,0,zz),arm_radius(dist)+.010,'steel',rt,12)
  flipped=site.diagonal and turn%2
  side=1 if flipped else -1;head_y=side*.42
  box('Clamp saddle',(-dist,side*.195,zz),(.12,.095,.17),'steel',rt,.004)
  tube('Rigid hanger pipe',[(-dist,side*.22,zz),(-dist,side*.20,zz),(-dist,side*.20,zz+.45),(-dist,head_y,zz+.45)],.021,'steel',rt,10)
  bolt('Hanger aiming clamp',(-dist,side*.35,zz+.48),(0,side,0),.009,'steel',rt)
  k=plan.left if j==len(stations)-1 and plan.left!='permissive' else 'three'
  h=head(f'{name}__Head{j}',rt,(-dist,head_y,zz+.45),yaw=180 if site.diagonal and int(angle/90)%2 else 0,kind=k,color=plan.head,style=plan.visor,border=plan.border,active='red_arrow' if k in ('fya','protected') else 'red')
  # Wiring enters the top boss and runs through the hollow hanger to the
  # arm. No decorative cable projects into air (FDOT 17745 conduit detail).
  cyl('Head cable gland',(-dist,head_y,zz+.40),(-dist,head_y,zz+.45),.016,'rubber',rt,8)
 # Sign, mounted with two clamps/standoffs; name rows swap without geometry.
 sx=-1.40;sy=-.30;sz=z-(1.25 if site.half(int(angle/90))<4 else .28)
 box('Street sign extruded frame',(sx,sy,sz),(2.134,.085,.4572),plan.finish,rt,.009)
 row=plan.seed-201;col=(angle//90)%2
 nameface=quad('Swappable street name',(sx,sy-.044,sz),2.10,.427,'names',rt,(col*.5,1-(row+1)*.25,(col+1)*.5,1-row*.25))
 if plan.illuminated:
  # Quick emissive sign prototype shares original name image; final uses graphics palette.
  nameface.data.materials.clear();nm=bpy.data.materials.get('SharedNames_Lit')
  if nm is None:nm=M['names'].copy();nm.name='SharedNames_Lit'
  pnode=nm.node_tree.nodes.get('Principled BSDF');im=next(n for n in nm.node_tree.nodes if n.type=='TEX_IMAGE')
  nm.node_tree.links.new(im.outputs['Color'],pnode.inputs['Emission Color']);pnode.inputs['Emission Strength'].default_value=.6;nameface.data.materials.append(nm)
 for x in (sx-.78,sx+.78):
  tube('Street sign hanger',[(x,0,z+abs(x+.2735)*.03492),(x,-.15,sz+.20)],.013,'steel',rt,8)
  box('Street name saddle',(x,-.15,sz+.19),(.085,.32,.12),'steel',rt)
  bolt('Name sign bolt',(x,sy-.048,sz+.15),(0,-1,0),.005,'steel',rt)
 # Camera with shade hood and explicitly routed cable to arm entrance.
 cx=-arm_len*.65;cz=z+(-cx-.2735)*.03492
 cyl('Detection riser',(cx,0,cz),(cx,0,cz+.52),.025,plan.finish,rt)
 box('Detection camera',(cx,-.045,cz+.56),(.13,.245,.11),'white',rt,.025)
 cyl('Camera optical port',(cx,-.1665,cz+.56),(cx,-.183,cz+.56),.035,'black',rt,12)
 box('Camera rain hood',(cx,-.08,cz+.620),(.17,.30,.012),'white',rt,.002)
 # Detector lead is clipped down the riser and enters the arm at its foot.
 tube('Detection cable down riser',[(cx,.026,cz+.54),(cx,.026,cz+.30),(cx,.026,cz+.03)],.005,'rubber',rt,6)
 for dz in (.12,.35):box('Detection cable clip',(cx,.028,cz+dz),(.018,.015,.018),'steel',rt,0)
 root(name+'__LuminaireSocket',(0,0,POLE_TOP),rt,kind='socket')
 if plan.luminaire:luminaire(rt,plan)
 if plan.ped_mount=='mast':
  ped_head(name+'__Ped',rt,(-.32,0,2.65),yaw=-90,walk=angle%180==0)
  tube('Pole pedestrian bracket',[(-.17,0,2.28),(-.275,0,2.28),(-.275,0,2.40)],.023,'steel',rt,10)
 if plan.near:
  head(name+'__Near',rt,(.05,.52,4.6),yaw=180,kind='three',color=plan.head,style=plan.visor,border=False,active='green')
  ring('Near-side mounting band',4.48,shaft_radius(4.48),shaft_radius(4.48)+.012,.05,'steel',rt,12)
  tube('Near-side mounting elbow',[(.05,.10,4.50),(.05,.10,4.68),(.05,.52,4.68),(.05,.52,4.60)],.021,'steel',rt,10)
 join_fixed(rt);return rt

def luminaire(rt,plan):
 # Select only the owner's existing library fixture; preserve canonical delivery.
 path=Path(__file__).resolve().parents[2]/'street-light/export/StreetLight.glb'
 before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path));imported=set(bpy.context.scene.objects)-before
 # The static shipped mesh is spatially partitioned at fixture's manufacturing envelope.
 import bmesh
 for o in list(imported):
  if o.type!='MESH':continue
  bm=bmesh.new();bm.from_mesh(o.data);delete=[v for v in bm.verts if not (-2.40<v.co.y<-1.759 and v.co.z>7.72)]
  bmesh.ops.delete(bm,geom=delete,context='VERTS');bm.to_mesh(o.data);bm.free()
  if not len(o.data.polygons):continue
  o.parent=rt;o.name='Rill_LibraryHead';o.location=(0,.1288,2.8728)
  import surfaces;surfaces.assign(o)
  # Retains the exact library vertices/materials: only instance translation changes.
 for o in imported:
  if o.type!='MESH' or not len(o.data.polygons):bpy.data.objects.remove(o,do_unlink=True)
 own(G.lathe('Luminaire extension',[(POLE_TOP,SHAFT_R1),(10.70,.146)],M[plan.finish],12),rt)
 tube('Luminaire curved arm',G.bezier((0,0,10.30),(0,-.25,10.78),(0,-1.15,10.71),(0,-1.70,10.71),12),.03015,plan.finish,rt,12)
 root('Socket_RillHead',(0,-1.70,10.71),rt,kind='luminaire_mount')

def push(rt,p=(0,0,0),yaw=0,name='PushButton'):
 station=root(name,p,rt,kind='PushButton',yaw=yaw)
 # Original APS: asymmetrical lower speaker, chamfered cast surround and raised arrow.
 box('APS cast body',(0,-.080,1.0668),(.140,.12,.258),'black',station,.030)
 box('APS front plate',(0,-.145,1.0668),(.116,.012,.230),'yellow',station,.014)
 cyl('Accessible button',(0,-.152,BUTTON_AXIS),(0,-.170,BUTTON_AXIS),.037,'steel',station,16)
 arrow=[(-.025,1.108),(.001,1.130),(.001,1.117),(.026,1.117),(.026,1.099),(.001,1.099),(.001,1.087)]
 arrow=[(x,z+(BUTTON_AXIS-1.108)) for x,z in arrow]
 profile('Raised tactile crossing arrow',arrow,-.174,-.171,'black',station)
 quad('APS service sticker',(-.036,-.153,1.166),.034,.028,'record',station)
 for i in range(4):box('APS speaker slot',(0,-.153,.987+i*.009),(.060,.006,.003),'inside',station,0)
 box('R10 sign blank',(0,-.09,1.63),(.2286,.003,.3048),'steel',station,0)
 quad('R10-3 instructions',(0,-.093,1.63),.223,.300,'r10',station)
 for z in (1.49,1.77):
  box('R10 back mounting spacer',(0,-.065,z),(.035,.050,.035),'steel',station,0)
  bolt('R10 mounting bolt',(0,-.098,z),(0,-1,0),.003,'steel',station)
 join_fixed(station);return station

def ped_head(name,rt,p,yaw=0,walk=False):
 h=root(name,p,rt,kind='PedHead',yaw=yaw);h['pivot_axis']='Z';h['range_degrees']=[-15,15]
 box('Pedestrian cast housing',(0,0,0),(.4445,.18,.4191),'yellow',h,.032)
 box('Pedestrian gasket',(0,-.096,0),(.410,.012,.386),'black',h,.015)
 box('Recessed dark face',(0,-.106,0),(.388,.014,.364),'inside',h,.008)
 # Folded top and side hood, .15 m deep.
 box('Pedestrian hood roof',(0,-.185,.215),(.463,.32,.008),'black',h,.002)
 for s in (-1,1):box('Pedestrian hood cheek',(s*.226,-.185,.01),(.008,.32,.409),'black',h,.002)
 for kind,on in [('hand',not walk),('walk',walk)]:
  j=TILES.index(kind);o=quad(f'{name}__{kind}',(-.09,-.115-(.0001 if kind=='walk' else 0),0),.190,.290,'lit' if on else 'off',h,((j%4)/4,0,(j%4+1)/4,.5))
  o['signal_lens']=True;o['signal_kind']=kind;o['powered']=on
 # Two independently named seven-segment digits. Each segment is its own lens.
 segs={'A':(0,.080,.054,.012),'B':(.030,.043,.012,.060),'C':(.030,-.043,.012,.060),'D':(0,-.080,.054,.012),'E':(-.030,-.043,.012,.060),'F':(-.030,.043,.012,.060),'G':(0,0,.054,.012)}
 litsegments=('ABGED','ABGCD') # "23", shown only with hand clearance state.
 for digit in range(2):
  for seg,(dx,dz,w,hh) in segs.items():
   on=not walk and seg in litsegments[digit]
   o=quad(f'{name}__Countdown_{"Tens" if digit==0 else "Ones"}_{seg}',(.065+digit*.086+dx,-.116,dz),w,hh,'lit' if on else 'off',h,(.25,.5,.5,1))
   # Cropping a solid dot gives a soft LED segment rather than a full tile.
   uv=o.data.uv_layers.active
   for entry in uv.data:entry.uv=(.37451171875,.7509765625)
   o['signal_lens']=True;o['signal_kind']='countdown';o['segment']=seg;o['digit']=digit;o['powered']=on
 cyl('Ped head mounting boss',(0,.045,-.285),(0,.045,-.20),.023,'steel',h,10)
 tube('Ped head service slack',G.bezier((.12,.10,.02),(.23,.16,-.24),(.01,.18,-.27),(0,.045,-.26),10),.006,'rubber',h,6)
 join_fixed(h);return h

def pedestal(name,p,angle,parent=None,walk=False,with_head=True):
 rt=root(name,p,parent,kind='Pedestal' if with_head else 'PushButtonPost',yaw=angle);footing(rt,'zinc',True)
 top=3.15 if with_head else 1.95
 cyl('Four inch pedestal',(0,0,.35),(0,0,top),.0508,'zinc',rt,16)
 cyl('Pedestal cap',(0,0,top),(0,0,top+.02),.055,'zinc',rt,16)
 if with_head:
  ped_head(name+'__Ped',rt,(0,-.16,2.65),walk=walk)
  tube('Pedestrian elbow',[(0,0,2.28),(0,-.115,2.28),(0,-.115,2.40)],.023,'steel',rt,10)
 push(rt,yaw=90,name=name+'__APS')
 join_fixed(rt);return rt

def cabinet(name,p,yaw,parent=None):
 rt=root(name,p,parent,kind='Cabinet',yaw=yaw)
 box('Concrete housekeeping plinth',(0,.1,.10),(1.35,1.10,.20),'concrete',rt,.025)
 # Bent 3 mm aluminum shell with open front, floor, roof, gasket and folded returns.
 box('Cabinet rear',(0,.390,1.03),(.910,.003,1.66),'cabinet',rt,.001)
 for s in (-1,1):
  box('Cabinet side',(s*.455,.03,1.03),(.003,.72,1.66),'cabinet',rt,.001)
  box('Front return',(s*.43,-.328,1.03),(.050,.018,1.66),'cabinet',rt,.001)
 box('Cabinet bottom',(0,.03,.20),(.910,.72,.006),'cabinet',rt,.001)
 box('Folded rain roof',(0,.03,1.875),(.967,.78,.025),'cabinet',rt,.006)
 box('Drip lip',(0,-.358,1.854),(.963,.035,.03),'cabinet',rt,.002)
 # Black cavity remains visible inside the openable leaf.
 # Open 19-inch-style rack: controller, monitor and removable load modules.
 box('Cabinet rack shadow',(0,.29,1.10),(.72,.025,1.40),'inside',rt,0)
 for x in (-.285,.285):box('Rack upright',(x,.04,1.06),(.026,.035,1.44),'steel',rt,0)
 for label,z,h,w in [('Controller',1.56,.22,.51),('Conflict monitor',1.30,.17,.27),('Detector cards',1.08,.18,.51),('Load switch bay',.75,.22,.51),('Power panel',.43,.22,.51)]:
  box(label+' chassis',(0,.10,z),(w,.30,h),'black' if label=='Controller' else 'cabinet',rt,0)
  quad(label+' generated panel',(0,-.052,z),w-.02,h-.018,'panel',rt)
 for i in range(8):box('Load switch module',(-.224+i*.064,-.075,.75),(.051,.08,.18),'panel',rt,0)
 for i in range(4):box('Circuit breaker',(-.18+i*.09,-.073,.43),(.049,.045,.068),'black',rt,0)
 for x in (-.32,.32):
  tube('Rack harness',G.bezier((x,.12,.28),(x*.92,-.02,.58),(x*.92,.0,1.15),(x,.12,1.72),14),.014,'rubber',rt,6)
 for z in (.50,.93,1.45):box('Harness restraint',(.32,.09,z),(.044,.03,.015),'white',rt,0)
 door=root(name+'__Door',(-.435,-.380,.23),rt,kind='CabinetDoor')
 door['pivot_axis']='Z';door['range_degrees']=[-110,0]
 box('Folded aluminum door',(.44375,-.012,.80075),(.8475,.040,1.5965),'cabinet',door,.007)
 box('Weather gasket',(.435,.012,.81),(.824,.009,1.574),'rubber',door,.008)
 for z in (.20,.80,1.40):cyl('Continuous hinge segment',(-.003,-.005,z-.07),(-.003,-.005,z+.07),.011,'steel',door,8)
 box('Vent dark aperture',(.23,-.034,.30),(.31,.004,.28),'inside',door,0)
 for i in range(9):box('Pressed louver',(.23,-.048,.18+i*.03),(.33,.030,.020),'cabinet',door,.001)
 box('Padlock hasp',(.81,-.046,.86),(.025,.032,.12),'steel',door,.002)
 tube('Padlock shackle',G.bezier((.80,-.072,.85),(.79,-.072,.91),(.85,-.072,.91),(.84,-.072,.85),8),.004,'steel',door,6)
 box('Padlock body',(.82,-.072,.83),(.040,.024,.040),'bronze',door,.003)
 box('Original Morrow Controls plate',(.48,-.034,1.42),(.125,.002,.032),'black',door,0)
 # Small service lock and maintenance sticker form, markings wait for look-dev.
 cyl('Door service lock',(.80,-.035,1.04),(.80,-.047,1.04),.012,'steel',door,12)
 box('Inspection sticker',(.55,-.034,1.08),(.071,.001,.10),'white',door,0)
 box('Door document pocket',(.43,.085,.48),(.56,.045,.29),'cabinet',door,0)
 quad('Maintenance record',(.43,.111,.51),.39,.22,'record',door)
 # Service pedestal / meter next to cabinet, conduits terminate at grade.
 cyl('Service riser',(1.02,.18,.0),(1.02,.18,1.72),.030,'zinc',rt,12)
 box('Electric disconnect',(1.02,.12,1.13),(.27,.18,.40),'cabinet',rt,.006)
 cyl('Meter socket',(1.02,.05,1.58),(1.02,-.10,1.58),.109,'cabinet',rt,20)
 cyl('Meter glass face',(1.02,-.10,1.58),(1.02,-.15,1.58),.089,'black',rt,20)
 cyl('Meter dial',(1.02,-.152,1.58),(1.02,-.154,1.58),.071,'white',rt,16)
 for x in (-.20,.18):tube('Conduit sweep',G.bezier((x,.1,.25),(x,.1,.05),(x,.40,-.08),(x,.60,-.10),8),.025,'zinc',rt,8)
 # Hinge pin axes sit in front of the returned jamb, so the leaf clears it.
 for ob in door.children:
  if ob.type!='MESH':continue
  if ob.name.startswith('Continuous hinge segment'):ob.location.y=0
  else:ob.location.y+=.036
 for station in (.20,.80,1.40):
  box('Operating hinge leaf',(.014,.010,station),(.030,.050,.025),'cabinet',door,0)
  for dz in (-.10,.10):
   zz=.23+station+dz
   box('Welded hinge leaf',(-.438,-.348,zz),(.035,.065,.025),'cabinet',rt,0)
   cyl('Fixed hinge knuckle',(-.438,-.380,zz-.0125),(-.438,-.380,zz+.0125),.012,'steel',rt,8)
 join_fixed(door);join_fixed(rt);return rt

def pullbox(name,p,rt):
 r=root(name,p,rt,kind='PullBox')
 box('Concrete pull box frame',(0,0,-.005),(.47,.69,.064),'concrete',r,.015)
 box('Flush composite lid',(0,0,.021),(.388,.610,.012),'black',r,.006)
 for x in (-.12,.12):bolt('Lid screw',(x,0,.028),(0,0,1),.003,'steel',r)
 join_fixed(r);return r

def span(name,parent,plan):
 rt=root(name,parent=parent,kind='SpanSet')
 a=Vector((-(FACE+4.2),-(CORE+4),0));b=-a
 # One diagonally spanning two-pole installation; all four approaches see two faces.
 for i,p in enumerate((a,b)):
  pole=root(name+f'__Strain{i}',p,rt,kind='StrainPole');footing(pole,plan.finish)
  own(G.lathe('Steel strain pole',[(SHAFT_BASE,.215),(9.0,.162)],M[plan.finish],16),pole)
  for z in (7.72,8.65):
   cyl('Split steel band',(-.225,0,z),(.225,0,z),.045,'steel',pole,10)
  join_fixed(pole)
 def wire(t,zbase,sag):
  v=a.lerp(b,t);return (v.x,v.y,zbase-4*sag*t*(1-t))
 for label,zbase,sag,r,ma in [('Catenary',8.65,.66,.0065,'steel'),('Messenger',7.72,.26,.0048,'steel'),('Tether',5.62,.14,.0040,'steel'),('Lashed signal cable',7.74,.26,.010,'rubber')]:
  tube(label,[wire(i/48,zbase,sag) for i in range(49)],r,ma,rt,6)
 # Stagger the four pairs on the same cable; avoid co-located perpendicular heads.
 for j,(t,angle) in enumerate(((.53,0),(.66,0),(.27,180),(.40,180),(.345,90),(.433,90))):
  x,y,z=wire(t,7.72,.26);h=head(f'{name}__Head{j}',rt,(x,y,z-.20),yaw=angle,color=plan.head,style='tunnel',border=False,active='red' if angle in (0,180) else 'green')
  # Messenger clamp, balancer, conduit drop, plus the lower tether restraint.
  along=(b-a).normalized();point=Vector((x,y,z));cyl('Span wire clamp',point-along*.065,point+along*.065,.025,'steel',rt,8)
  cz=wire(t,8.65,.66)[2];cyl('Catenary drop tie',(x,y,z),(x,y,cz),.006,'steel',rt,6)
  tube('Balanced hanger',[(x-.08,y,z),(x-.08,y,z-.11),(x,y,z-.11),(x,y,z-.20)],.017,'steel',rt,8)
  tz=wire(t,5.62,.14)[2]
  bpy.context.view_layer.update();inverse=h.matrix_world.inverted()
  tetherpts=[inverse@Vector(p) for p in ((x,y,tz),(x,y,z-1.30))]
  tube('Tether restraint',tetherpts,.005,'steel',h,6)
  sock=root(h.name+'__TetherSocket',tetherpts[0],h,kind='socket');sock['socket_kind']='flexible_tether_end'
  join_fixed(h)
  # FDOT 17727 sheet 2: adjustable extension bar, two overlapping
  # fasteners, balance adjuster and 8–12 inch drip loop at the entry.
  box('Hanger extension bar',(x,y,z-.115),(.046,.024,.19),'steel',rt,0)
  for dz in (.05,.11):bolt('Hanger extension bolt',(x,y-.016,z-dz),(0,-1,0),.007,'steel',rt)
  cyl('Balance adjuster',(x,y,z-.20),(x,y,z-.155),.031,'steel',rt,10)
  pts=G.bezier((x-.13,y-.02,z+.02),(x-.16,y-.035,z-.30),(x+.08,y-.035,z-.31),(x,y,z-.18),16)
  tube('Short head entry slack',pts,.0075,'rubber',rt,6)
 # Lashed wiring follows messenger. One gravity-draining loop at each pole.
 for t in [i/36 for i in range(37)]:
  x,y,z=wire(t,7.72,.26);cyl('Cable lashing',(x,y-.014,z-.01),(x,y+.014,z+.023),.003,'steel',rt,4)
 for t in (0,1):
  x,y,z=wire(t,7.72,.26);sign=1 if t==0 else -1
  tube('Pole drip loop',G.bezier((x+sign*.15,y,z+.02),(x+sign*.37,y-.04,z-.51),(x-sign*.14,y-.04,z-.49),(x,y,7.60),22),.009,'rubber',rt,6)
 join_fixed(rt);return rt
