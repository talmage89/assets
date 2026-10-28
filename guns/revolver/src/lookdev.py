"""Original brushed/turned finishes and use at named physical sites.

Rest attributes preserve grain, engraving and causal masks during rigid-bone
projection isolation. No downloaded pixels enter any material or texture.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.materials import Nodes
from parameters import chamber

def sub(n,a,b):return n.math('SUBTRACT',a,b)
def absolute(n,a):return n.math('ABSOLUTE',a)
def interval(n,x,a,b,s=.001):return n.mul(n.ramp(x,a-s,a),n.ramp(x,b+s,b))
def inputs(n):
 p=n.node('ShaderNodeAttribute',attribute_name='FinishPosition').outputs['Vector']
 normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal').outputs['Vector']
 return (p,*n.split(p),*n.split(normal))
def finish(n,base,rough,metal,height=0,ao=1,wear=0,carbon=0):
 n.channel('micro_ao',ao);n.channel('wear',wear);n.channel('carbon',carbon)
 return n.finish(base,rough,metal,height,bump=1)
def texture(n,u,v,name):
 tex=n.node('ShaderNodeTexImage',extension='CLIP',interpolation='Linear')
 tex.image=bpy.data.images.load(str(BASE/'build/markings'/(name+'.png')),check_existing=True)
 tex.image.colorspace_settings.name='Non-Color';n.feed(tex.inputs['Vector'],n.combine(u,v,0))
 return tex.outputs['Color']
def mark(n,y,z,nx,name,y0,z0,w,h):
 u=n.math('DIVIDE',sub(n,y,y0),w);v=n.math('DIVIDE',sub(n,z,z0),h)
 left=texture(n,sub(n,1,u),v,name);right=texture(n,u,v,name)
 return n.maximum(n.mul(left,n.ramp(nx,-.75,-.98)),n.mul(right,n.ramp(nx,.75,.98)))
def breakup(n,p):return n.add(.70,n.mul(n.noise(n.vec('MULTIPLY',p,(1500,2400,1700)),1,2),.30))
def radius(n,x,z,zc):return n.math('SQRT',n.add(n.mul(x,x),n.mul(sub(n,z,zc),sub(n,z,zc))))

def stainless(name,part,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n)
 if part=='Cylinder_Fluted':
  angle=n.math('ARCTAN2',sub(n,z,.0482),x)
  tool=n.noise(n.combine(n.mul(angle,8),n.mul(y,14000),n.mul(radius(n,x,z,.0482),2000)),1,2)
 elif part.startswith('Frame_'):
  tool=n.noise(n.vec('MULTIPLY',p,(700,9000,30)),1,2)
 else:tool=n.noise(n.vec('MULTIPLY',p,(10000,24,10000)),1,2)
 if part in ('Cylinder_Fluted','Barrel'):
  zc=.0482 if part=='Cylinder_Fluted' else .061
  turned=n.noise(n.combine(n.mul(radius(n,x,z,zc),16000),n.mul(n.math('ARCTAN2',sub(n,z,zc),x),5),n.mul(y,12)),1,2)
  tool=n.mix(n.ramp(absolute(n,ny),.80,.98),tool,turned)
 fine=n.noise(p,5000,2)
 base=(.51,.52,.53);rough=n.add(.385,n.mul(sub(n,tool,.5),.12))
 height=n.add(n.mul(sub(n,tool,.5),1.7e-6),n.mul(sub(n,fine,.5),.6e-6))
 rub=0;carbon=0;track=0;engrave=0
 if part=='Cylinder_Fluted':
  rr=radius(n,x,z,.0482);outer=n.ramp(rr,.0193,.01965)
  # The stop is at Y=44 mm. A persistent narrow track follows its contact
  # circle, with a darker groove and a fine polished center on the lands.
  track=n.ramp(n.mul(n.band(y,.044,.00030,.00015),outer,wear),.04,.55)
  base=n.mix(track,base,(.085,.09,.095),True)
  center=n.mul(n.band(y,.044,.000075,.000065),outer,wear)
  base=n.mix(center,base,(.62,.63,.64),True)
  height=n.add(height,n.mul(track,-.000012))
  ends=n.maximum(n.band(y,.0386,.00065,.0006),n.band(y,.0816,.00065,.0006))
  rub=n.mul(ends,outer,n.ramp(absolute(n,nx),.30,.85))
  rings=[]
  for i in range(6):
   cx,_,cz=chamber(i);r=radius(n,sub(n,x,cx*.001),z,cz*.001)
   rings.append(n.ramp(r,.0073,.0047))
  carbon=n.mul(n.maximum(*rings),n.ramp(ny,.40,.95),n.ramp(y,.0810,.0821),.92)
 elif part=='Barrel':
  rr=radius(n,x,z,.061)
  nose=n.mul(n.ramp(y,.176,.1835),n.ramp(absolute(n,nx),.45,.97))
  shroud=n.mul(n.ramp(y,.173,.182),n.ramp(z,.054,.048),n.ramp(nz,.10,-.85))
  crown=n.mul(n.ramp(y,.1820,.1839),n.band(rr,.009,.00025,.00035))
  rub=n.maximum(nose,shroud,crown)
  carbon=n.maximum(n.mul(n.ramp(y,.088,.0824),interval(n,rr,.0046,.0090,.001),.90),
   n.mul(n.ramp(y,.1815,.183),n.ramp(rr,.0065,.0045),n.ramp(ny,.3,.9),.60))
  engrave=mark(n,y,z,nx,'barrel',.108,.059,.064,.008)
 elif part.startswith('Frame_'):
  # Hot fouling stays directly above the forcing cone on the underside.
  carbon=n.mul(n.ellipse(p,(0,.081),(.012,.010),axes=(0,1)),
   interval(n,z,.063,.071,.002),n.ramp(nz,-.35,-.92),.93)
  if part=='Frame_Sideplate':engrave=mark(n,y,z,nx,'frame',.003,.033,.026,.011)
 elif part=='Hammer_Body':
  # Curved roof carries fine crossing cuts; cheeks stay smooth. Coordinates
  # live in the rest frame, so the field follows the accepted cocking clip.
  top=n.mul(n.ramp(nz,.40,.85),interval(n,y,-.011,.014,.001),n.ramp(z,.065,.068))
  a=n.math('SINE',n.mul(n.add(x,y),math.tau/.00072))
  b=n.math('SINE',n.mul(sub(n,x,y),math.tau/.00072))
  cut=n.mul(n.maximum(n.ramp(a,.25,.85),n.ramp(b,.25,.85)),top)
  height=n.add(height,n.mul(cut,-.000075))
  rub=n.mul(top,n.ramp(fine,.30,.65),.55)
 elif part.startswith(('Trigger_','Latch_')):rub=n.mul(n.ramp(absolute(n,nx),.65,.95),.30)
 rub=n.mul(rub,wear,breakup(n,p))
 base=n.mix(rub,base,(.61,.62,.63),True);rough=n.mix(rub,rough,.235)
 height=n.mul(height,sub(n,1,n.mul(rub,.65)))
 carbon=n.ramp(n.mul(carbon,wear,breakup(n,p)),.08,.45);metal=n.mix(carbon,1,.05)
 base=n.mix(carbon,base,(.010,.0085,.007),True);rough=n.mix(carbon,rough,.77)
 base=n.mix(engrave,base,(.12,.13,.14),True);height=n.add(height,n.mul(engrave,-.000045))
 return finish(n,base,rough,metal,height,wear=n.maximum(rub,track),carbon=carbon)

def rubber(name,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n)
 grain=n.voronoi(p,1700);micro=n.noise(p,6000,2)
 # Molding texture covers the flank below a clean web and border. Its
 # irregular cells are original, with smaller relief between them.
 panel=n.mul(n.ramp(absolute(n,nx),.35,.80),interval(n,z,-.061,.021,.004))
 pebble=n.ramp(grain,.40,.16)
 web=n.mul(n.ellipse(p,(-.017,.013),(.020,.022),axes=(1,2)),n.ramp(absolute(n,nx),.5,.92))
 front=n.mul(n.ramp(ny,.40,.86),interval(n,z,-.052,.013,.005))
 back=n.mul(n.ramp(ny,-.45,-.9),interval(n,z,-.040,.019,.005),.65)
 palm=n.mul(n.ellipse(p,(-.032,-.020),(.011,.024),axes=(1,2)),n.ramp(absolute(n,nx),.70,.96),.75)
 hand=n.mul(n.maximum(web,front,back,palm),wear)
 height=n.mul(n.add(n.mul(pebble,panel,.000120),n.mul(sub(n,micro,.5),.000009)),sub(n,1,n.mul(hand,.91)))
 base=n.mix(n.mul(pebble,panel),(.019,.0195,.0192),(.036,.037,.036),True)
 base=n.mix(hand,base,(.008,.0084,.0082),True)
 rough=n.mix(hand,n.add(.72,n.mul(sub(n,micro,.5),.07)),.40)
 # A little pale lint remains inside the lower sheltered cell valleys.
 lint=n.mul(panel,n.ramp(z,-.048,-.060),n.ramp(grain,.38,.55),n.ramp(micro,.64,.80),wear,.18)
 base=n.mix(lint,base,(.027,.025,.021),True)
 ao=n.mix(n.mul(panel,sub(n,1,pebble),sub(n,1,hand)),1,.86)
 return finish(n,base,rough,0,height,ao=ao,wear=hand)

def dark(name,part,wear,plastic=False):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n);fine=n.noise(p,3500,2)
 base=(.005,.0055,.006) if not plastic else (.013,.015,.016)
 rough=n.add(.52 if not plastic else .62,n.mul(sub(n,fine,.5),.07));height=n.mul(sub(n,fine,.5),1e-6)
 rub=0
 if 'Sight' in part:
  lines=n.ramp(n.math('SINE',n.mul(z,math.tau/.00055)),.05,.85)
  height=n.add(height,n.mul(lines,n.ramp(ny,-.4,-.9),-.000025))
  rub=n.mul(n.ramp(z,.0821,.083),n.ramp(absolute(n,nx),.30,.95),wear,.45)
 base=n.mix(rub,base,(.24,.25,.26),True)
 metal=0 if plastic else n.mix(rub,0 if 'Sight' in part else .72,1)
 return finish(n,base,n.mix(rub,rough,.34),metal,height,wear=rub)

def ammo(name,role,fired,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n)
 q=n.node('ShaderNodeAttribute',attribute_name='AmmoPosition').outputs['Vector'];a,b,c=n.split(q)
 tool=n.noise(n.vec('MULTIPLY',q,(8000,35,8000)),1,2)
 base={'brass':(.50,.31,.095),'copper':(.46,.16,.060),'primer':(.43,.42,.36),'lead':(.065,.068,.070)}[role]
 rough=n.add(.30 if role!='lead' else .50,n.mul(sub(n,tool,.5),.11));height=n.mul(sub(n,tool,.5),1e-6)
 soot=0
 if role=='brass':
  stamp=n.mul(texture(n,n.add(.5,n.math('DIVIDE',a,.012)),n.add(.5,n.math('DIVIDE',c,.012)),'headstamp'),n.ramp(ny,-.55,-.95))
  height=n.add(height,n.mul(stamp,-.000055));base=n.mix(stamp,base,(.13,.075,.023),True)
  # Seating/handling scuffs are axially stretched and remain near the mouth.
  if fired:
   soot=n.mul(n.ramp(b,.028,.0323),wear)
   base=n.mix(soot,base,(.025,.019,.011),True);rough=n.mix(soot,rough,.71)
 return finish(n,base,rough,.72 if role=='lead' else 1,height,carbon=soot)

def assign(wear):
 records={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
  verts=[v.co.copy() for v in ob.data.vertices]
  pos=ob.data.attributes.new('FinishPosition','FLOAT_VECTOR','POINT');pos.data.foreach_set('vector',[a for v in verts for a in v])
  normal=ob.data.attributes.new('FinishNormal','FLOAT_VECTOR','CORNER');normal.data.foreach_set('vector',[a for r in ob.data.corner_normals for a in r.vector])
  bone=ob.get('bone','Root');ammunition=bone.startswith(('Live','Case','LoaderRound','InsertRound'))
  if ammunition:
   index=0 if bone=='InsertRound' else int(''.join(c for c in bone if c.isdigit()))
   center=Vector(chamber(index))*.001
   attr=ob.data.attributes.new('AmmoPosition','FLOAT_VECTOR','POINT');attr.data.foreach_set('vector',[a for v in verts for a in v-center])
  roles=[]
  for i,old in enumerate(list(ob.data.materials)):
   key=old.name.removeprefix('CP_').split('.')[0];name='Meridian_'+ob.name+'_'+str(i)
   if ammunition:mat=ammo(name,key,bone.startswith('Case'),wear)
   elif key=='rubber':mat=rubber(name,wear)
   elif key in ('dark','loader'):mat=dark(name,ob.name,wear,plastic=key=='loader')
   else:mat=stainless(name,ob.name,wear)
   ob.data.materials[i]=mat;roles.append(key)
  records[ob.name]=roles
 bpy.context.scene['finish_wear']=wear
 return records
