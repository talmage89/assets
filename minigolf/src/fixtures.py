"""Original constructed roadside themes; all ball passages are actual voids."""
import math
from geometry import *

def cone(name,z0,z1,r0,r1,mat,rt,n=24):
 return own(G.lathe(name,[(z0,r0),(z1,r1)],M[mat],n),rt)

def arch(rt,name,y,base,clear=.60,height=.65,depth=.18,mat='ivory'):
 # Arch is an original extruded ring section, opening through both faces.
 r=clear/2;spring=height-r;n=16;vs=[]
 for yy in (y-depth/2,y+depth/2):
  for rad in (r,r+.16):
   vs.extend((rad*math.cos(i*math.pi/n),yy,base+spring+rad*math.sin(i*math.pi/n)) for i in range(n+1))
 stride=n+1;fs=[]
 for i in range(n):
  fs.extend(((i,i+1,2*stride+i+1,2*stride+i),(stride+i,3*stride+i,3*stride+i+1,stride+i+1),(i,stride+i,stride+i+1,i+1),(2*stride+i,2*stride+i+1,3*stride+i+1,3*stride+i)))
 mesh(name,vs,fs,mat,rt)
 for s in (-1,1):box(name+' pier',(s*(r+.08),y,base+spring/2),(.16,depth,spring),mat,rt)

def roof(rt,name,w,d,z,rise,mat='navy'):
 vs=[(-w/2,-d/2,z),(w/2,-d/2,z),(w/2,d/2,z),(-w/2,d/2,z),(0,-d/2,z+rise),(0,d/2,z+rise)]
 ob=mesh(name,vs,[(0,1,4),(3,5,2),(0,4,5,3),(1,2,5,4)],mat,rt,False)
 solid=ob.modifiers.new('Folded roof gauge','SOLIDIFY');solid.thickness=.025
 for y in (-d/2,d/2):
  beam('Bargeboard',(-w/2,y,z),(0,y,z+rise),.055,.065,'ivory',rt);beam('Bargeboard',(0,y,z+rise),(w/2,y,z),.055,.065,'ivory',rt)
 return ob

def windmill(rt):
 # Tapered timber-clad tower with a .60 m clear ball tunnel.
 for s in (-1,1):box('Windmill lower side wall',(s*.49,0,.36),(.30,.98,.72),'ivory',rt,.008,2)
 arch(rt,'Windmill portal',-.53,0,.60,.65,.10)
 cone('Octagonal tower',.72,2.55,.72,.46,'ivory',rt,8)
 ring('Tower foot flashing',(0,0),.75,.66,.68,.76,'red',rt,8)
 cone('Windmill hipped cap',2.53,3.2,.65,.015,'navy',rt,8)
 for a in range(8):
  th=a*math.tau/8
  beam('Corner trim',(.70*math.cos(th),.70*math.sin(th),.74),(.45*math.cos(th),.45*math.sin(th),2.55),.045,.045,'red',rt)
 box('Motor service door',(0,.60,1.16),(.34,.035,.50),'navy',rt)
 # Overlapping horizontal weatherboards follow the octagonal taper.
 for j in range(19):
  z=.76+j*.092;r=.72-(z-.72)*(.26/1.83)
  cone('Painted tower lap siding',z,z+.097,r+.012,r-.014,'ivory',rt,8)
 for side in (-1,1):
  box('Tower recessed sash',(side*.38,-.54,2.13),(.22,.04,.30),'navy',rt)
  for zz in (1.96,2.30):box('Tower window sill',(side*.38,-.57,zz),(.29,.07,.045),'red',rt)
  box('Tower window mullion',(side*.38,-.57,2.13),(.024,.04,.30),'ivory',rt)
 cyl('Rotor shaft',(0,-.76,1.63),(0,.55,1.63),.035,'metal',rt,16)
 rotor=root(rt.name+'__Rotor',(0,-.79,1.63),parent=rt,kind='moving rotor');rotor['pivot_axis']='Y';rotor['range_degrees']=[0,360];rotor['module']=False
 hub=ring('Bored rotor hub',(0,0),.13,.0375,-.07,.07,'red',rotor,32);hub.rotation_euler.x=math.pi/2
 for k in range(4):
  blade=root('Blade_%d'%k,parent=rotor);blade.rotation_euler.y=k*math.pi/2;blade['module']=False
  # Child blade nodes are retained, then flattened to owning moving root below.
  for s in (-1,1):
   beam('Sail longitudinal batten',(s*.07,0,.16),(s*.24,0,1.60),.035,.032,'red',blade)
  for j in range(9):
   z=.43+j*.142;w=.14+z*.20;box('Sail cross lath',(0,-.012,z),(w,.030,.052),'ivory',blade,.001,1)
  beam('Heavy sail stock',(-.035,-.03,.12),(-.035,-.03,1.61),.065,.055,'red',blade)
  # The leading third is closed with long pitched sail boards. The trailing
  # lattice is left open; diagonal braces stop it reading as a ladder.
  for j in range(3):
   ob=box('Sail leading board',(-.065-j*.046,-.039,1.015),(.043,.024,1.17),'ivory',blade,.001)
   ob.rotation_euler.z=.024
  for off in (.065,.145):beam('Sail trailing lattice batten',(off,-.035,.42),(off*1.6,-.035,1.59),.018,.022,'ivory',blade)
  beam('Sail diagonal brace',(-.15,-.048,.46),(.22,-.048,1.52),.022,.025,'red',blade)
 # Original door handle and base anchors read in fixture close-up.
 for x in (-.58,.58):
  box('Tower anchor shoe',(x,0,.025),(.22,.64,.05),'metal',rt)
  for y in (-.24,.24):cyl('Anchor bolt',(x,y,.045),(x,y,.07),.012,'metal',rt,8)
 return dict(height=3.2,blade_radius=1.60,hub_height=1.63,rotor_plane=-.79)

def lighthouse(rt):
 # Masonry tunnel and coping support a tapered shell. The small gallery is
 # ornamental course construction, not a visitor-accessible platform.
 for s in (-1,1):box('Lighthouse masonry abutment',(s*.60,0,.30),(.62,1.60,.60),'rocklight',rt,.025,2)
 arch(rt,'Lighthouse masonry tunnel',0,0,.55,.57,1.60,'rocklight')
 ring('Lighthouse masonry base coping',(0,0),.94,.30,.57,.64,'concrete',rt,16)
 def radius(z):return .85-.35*(z-.64)/(3.23-.64)
 cone('Tapered lighthouse shaft',.64,3.23,.85,.50,'ivory',rt,32)
 for z in (1.15,2.15):cone('Painted tower band',z,z+.24,radius(z)+.001,radius(z+.24)+.001,'red',rt,32)
 ring('Gallery deck',(0,0),.52,.35,3.22,3.29,'navy',rt,32)
 for i in range(16):
  a=i*math.tau/16;cyl('Gallery stanchion',(.49*math.cos(a),.49*math.sin(a),3.29),(.49*math.cos(a),.49*math.sin(a),3.64),.012,'metal',rt,8)
 for z in (3.47,3.64):ring('Gallery handrail',(0,0),.504,.48,z-.008,z+.008,'metal',rt,32)
 ring('Lantern glazing',(0,0),.35,.347,3.30,4.20,'glass',rt,8)
 cyl('Lantern support',(0,0,3.29),(0,0,3.48),.022,'metal',rt,10)
 cyl('Lantern reflector',(0,0,3.47),(0,0,3.77),.14,'metal',rt,12)
 for i in range(8):
  a=i*math.tau/8;cyl('Lantern mullion',(.36*math.cos(a),.36*math.sin(a),3.30),(.36*math.cos(a),.36*math.sin(a),4.22),.018,'navy',rt,8)
 cone('Lantern roof',4.20,4.61,.48,.025,'navy',rt,24)
 cyl('Finial',(0,0,4.56),(0,0,4.73),.025,'metal',rt)
 for z in (.97,1.78,2.70):box('Small recessed tower window',(0,-(radius(z)+.006),z),(.14,.025,.25),'navy',rt,.015,2)
 return dict(height=4.73,ball_portal=.55)

def covered_bridge(rt):
 # Covered ball bridge, separate from the human footbridge over the stream.
 for x in (-.58,.58):
  for y in (-.80,0,.80):
   box('Bridge post',(x,y,.83),(.09,.09,1.66),'wood',rt)
  for z in (.22,.56,1.47):box('Bridge side rail',(x,0,z),(.09,1.85,.10),'red',rt)
  for y in (-.4,.4):beam('Bridge diagonal',(x,y-.38,.25),(x,y+.38,1.43),.07,.055,'red',rt)
 # Playing carpet is the deck. Sills sit out of the putt line.
 roof(rt,'Covered bridge shingle roof',1.6,2.3,1.65,.65)
 for y in (-.84,.84):beam('Tie beam',(-.58,y,1.52),(.58,y,1.52),.09,.10,'wood',rt)
 return dict(height=2.30,clear_width=1.07)

def castle(rt):
 arch(rt,'Castle gateway',-.36,0,.72,.92,.48,'stonepaint')
 for x in (-.80,.80):
  sub=root('Castle turret',(x,0,0),parent=rt);sub['module']=False
  cone('Turret barrel',0,1.89,.30,.30,'stonepaint',sub,16)
  for z in (.18,.85,1.72):ring('Turret projecting stone course',(0,0),.327,.29,z,z+.06,'stonepaint',sub,16)
  ring('Turret parapet',(0,0),.36,.26,1.85,2.04,'ivory',sub,16)
  for j in range(8):
   a=j*math.tau/8;box('Crenel',(.30*math.cos(a),.30*math.sin(a),2.13),(.16,.16,.22),'stonepaint',sub)
  box('Arrow slit',(0,-.304,1.30),(.055,.014,.28),'black',sub)
  cone('Painted conical turret cap',2.02,2.80,.30,.015,'navy',sub,24)
 box('Gatehouse upper wall',(0,0,1.41),(1.1,.60,.70),'stonepaint',rt)
 for x in (-.40,0,.40):box('Gatehouse merlon',(x,0,1.88),(.20,.63,.25),'ivory',rt)
 # Raised portcullis above the ball envelope, separate translation pivot.
 gate=root(rt.name+'__Portcullis',(0,-.66,.55),parent=rt);gate['module']=False;gate['slide_axis']='Z';gate['range_m']=[0,.40]
 for x in (-.24,-.12,0,.12,.24):box('Portcullis vertical',(x,0,.30),(.018,.028,.6),'navy',gate)
 for z in (.03,.25,.48):box('Portcullis crossbar',(0,0,z),(.55,.03,.025),'navy',gate)
 for x in (-.33,.33):
  box('Gate guide channel',(x,-.67,1.02),(.045,.045,1.16),'navy',rt)
 # A course-built gatehouse has depth, buttresses and a central keep.
 for x in (-1.09,1.09):box('Battered castle buttress',(x,.13,.56),(.25,.88,1.12),'stonepaint',rt,.015)
 keep=root('Castle rear keep',(0,.65,0),parent=rt);keep['module']=False
 arch(keep,'Rear keep through portal',0,0,.72,.80,.80,'stonepaint')
 cone('Rear keep barrel',.90,2.85,.40,.40,'stonepaint',keep,16)
 cone('Rear keep spire',2.85,4.0,.48,.012,'navy',keep,20)
 for z in (1.10,1.75,2.30):box('Keep slit window',(0,-.405,z),(.08,.025,.28),'black',keep,.012)
 # 1.5x construction scale, baked into meshes and pivot offsets, never an
 # unapplied root transform. Overall 3.6m wide, 6m high; putt arch 1.08m.
 for ob in list(rt.children_recursive):
  ob.location*=1.5
  if ob.type=='MESH':ob.data.transform(Matrix.Scale(1.5,4))
 return dict(height=6.0,ball_portal=1.08,gate_lowest=.825)

def shipwreck(rt):
 # Open wreck is a ribbed plank shell with a .56 m putt passage down its keel.
 for s in (-1,1):
  for j in range(7):
   y=-1.2+j*.4;w=.45+.30*math.sin((j/6)*math.pi)
   pts=[(s*.30,y,.06),(s*w,y,.27),(s*(w+.14),y,.68)]
   for a,b in zip(pts,pts[1:]):beam('Exposed hull rib',a,b,.07,.07,'wood',rt)
  for k in range(5):
   z=.15+k*.115;pts=[]
   for j in range(13):
    y=-1.2+j*.2;w=.45+.30*math.sin(j/12*math.pi);pts.append((s*(.30+(w-.30)*min(1,z/.60)),y,z))
   for j,(a,b) in enumerate(zip(pts,pts[1:])):
    if not (s==1 and k>2 and j in (7,8)):beam('Weatherboard hull plank',a,b,.095,.032,'wood',rt)
 cyl('Broken mast',(1.10,0,0),(1.02,.1,2.4),.055,'wood',rt)
 tube('Slack rigging',[(1.02,.1,2.28),(.95,-.45,1.60),(.83,-1,.72)],.009,'navy',rt,8)
 return dict(height=2.4,length=2.4,ball_passage=.56)

BUILDERS=dict(windmill=windmill,lighthouse=lighthouse,covered_bridge=covered_bridge,castle=castle,shipwreck=shipwreck)

def build(kind,p,yaw,parent,name=None):
 rt=root(name or kind.title(),p,yaw,parent,kind='fixture');rt['fixture_kind']=kind
 info=BUILDERS[kind](rt)
 # Flatten structural subframes into their immediate module or moving owner.
 bpy.context.view_layer.update()
 for ob in [o for o in rt.children_recursive if o.type=='MESH']:
  owner=ob.parent
  while owner!=rt and not owner.get('pivot_axis') and not owner.get('slide_axis'):owner=owner.parent
  if owner!=ob.parent:
   xf=owner.matrix_world.inverted()@ob.matrix_world;ob.data.transform(xf);ob.parent=owner;ob.matrix_parent_inverse=Matrix.Identity(4);ob.matrix_basis=Matrix.Identity(4)
 return rt,info
