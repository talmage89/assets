"""Original meter-scale coatings and causal field wear; no photo shader inputs.

FinishPosition/Normal survive kit rigid-bone isolation. Fine spatter describes
paint manufacture; use wear follows contact paths and exposes opaque substrate.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.materials import Nodes

def sub(n,a,b):return n.math('SUBTRACT',a,b)
def ab(n,a):return n.math('ABSOLUTE',a)
def ramp(n,x,a,b):return n.ramp(n.math('DIVIDE',sub(n,x,a),sub(n,b,a)),0,1)
def interval(n,x,a,b,f=.001):return n.mul(ramp(n,x,sub(n,a,f),a),ramp(n,x,n.add(b,f),b))
def inp(n):
 p=n.node('ShaderNodeAttribute',attribute_name='FinishPosition').outputs['Vector']
 normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal').outputs['Vector']
 return (p,*n.split(p),*n.split(normal))
def finish(n,base,rough,metal,height=0,ao=1,wear=0):
 n.channel('micro_ao',ao);n.channel('wear',wear)
 return n.finish(base,rough,metal,height,bump=1)
def texture(n,u,v,name):
 tex=n.node('ShaderNodeTexImage',extension='CLIP',interpolation='Linear')
 tex.image=bpy.data.images.load(str(BASE/'build/markings'/(name+'.png')),check_existing=True)
 tex.image.colorspace_settings.name='Non-Color';n.feed(tex.inputs['Vector'],n.combine(u,v,0))
 return tex.outputs['Color']
def letter(n,y,z,nx):
 rows=[]
 for sign,name in [(-1,'receiver-left'),(1,'receiver-right')]:
  u=n.math('DIVIDE',sub(n,y,.050 if sign>0 else .057),.043 if sign>0 else .112)
  if sign<0:u=sub(n,1,u)
  v=n.math('DIVIDE',sub(n,z,.055),.019)
  rows.append(n.mul(texture(n,u,v,name),n.ramp(n.mul(nx,sign),.75,.98)))
 return n.maximum(*rows)
def fractured(n,p):
 # Resolved submillimeter boundary perturbation, not large noisy patches.
 return n.add(.78,n.mul(n.noise(n.vec('MULTIPLY',p,(2100,900,1800)),1,2),.22))

def steel(name,role,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n)
 tool=n.noise(n.vec('MULTIPLY',p,(1600,18,1600)),1,2)
 fine=n.noise(p,4200,2)
 base=(.0035,.0035,.0035);rough=n.add(.60,n.mul(sub(n,tool,.5),.09));metal=0
 h=n.mul(sub(n,fine,.5),2.5e-6);rub=0;carbon=0
 if role=='receiver':
  marks=letter(n,y,z,nx);h=n.add(h,n.mul(marks,-.00010))
  base=n.mix(marks,base,(.005,.006,.006),True)
  # Port lip only, in the physically exposed outer shell.
  cy=n.math('MAXIMUM',.104,n.math('MINIMUM',y,.168));dy=sub(n,y,cy)
  dz=n.math('MAXIMUM',.053,n.math('MINIMUM',z,.087));dz=sub(n,z,dz)
  dist=n.math('SQRT',n.add(n.mul(dy,dy),n.mul(dz,dz)))
  rub=n.mul(n.band(dist,.0041,.00035,.00025),n.ramp(x,.011,.016),.8)
 elif role=='bolt':
  base=(.010,.013,.015);metal=1;rough=.39
  # Raceways polish two long bearing strips, with circumferential entry bands.
  bands=n.maximum(interval(n,y,.051,.068,.001),interval(n,y,.157,.179,.001))
  tracks=n.mul(interval(n,y,.041,.194,.002),n.ramp(ab(n,nx),.85,.98),.65)
  rub=n.maximum(bands,tracks);h=n.mul(sub(n,tool,.5),1e-6)
  carbon=n.mul(n.ramp(y,.208,.2094),n.ramp(ny,.5,.9),.8)
 elif role=='lug':rub=n.ramp(ny,-.6,-.98)
 elif role=='barrel':
  r=n.math('SQRT',n.add(n.mul(x,x),n.mul(sub(n,z,.065),sub(n,z,.065))))
  carbon=n.mul(n.ramp(y,.8165,.819),n.ramp(r,.010,.0075))
  rub=n.mul(n.band(y,.8191,.00025,.0003),n.ramp(r,.0105,.0113),.6)
 elif role=='ring_screw':
  # Ring heads are coated steel: silver substrate agrees with the underlying
  # metal, while the adjacent scope is anodized aluminum.
  q=n.node('ShaderNodeAttribute',attribute_name='PartCoord').outputs['Vector']
  a,b,c=n.split(q);rub=n.mul(n.ramp(c,.55,.95),n.ramp(nz,.1,.7))
 elif role=='bipod':
  line=n.band(sub(n,x,n.mul(n.math('SINE',n.mul(y,55)),.0004)),0,.00065,.00035)
  # Part-centered transverse coordinate follows each leg's front wear track.
  q=n.node('ShaderNodeAttribute',attribute_name='PartOffset').outputs['Vector'];qx,qy,qz=n.split(q)
  radial=n.math('SQRT',n.add(n.mul(qx,qx),n.mul(qz,qz)))
  exterior=n.ramp(radial,.0067,.0071) if 'Sleeve' in name else n.ramp(radial,.0042,.0046)
  rub=n.mul(n.band(qx,0,.0010,.00035),n.ramp(nz,.72,.97),interval(n,y,.43,.552,.004),exterior)
 elif role=='spring':base=(.11,.125,.13);metal=1;rough=.33
 elif role=='control':
  q=n.node('ShaderNodeAttribute',attribute_name='PartCoord').outputs['Vector'];a,b,c=n.split(q)
  rub=n.mul(n.ramp(c,.86,.99),.38)
 rub=n.ramp(n.mul(rub,wear,fractured(n,p)),.10,.58)
 base=n.mix(rub,base,(.55,.59,.62),True);rough=n.mix(rub,rough,.29);metal=n.mix(rub,metal,1)
 carbon=n.mul(carbon,wear);base=n.mix(carbon,base,(.0018,.0019,.0018),True)
 rough=n.mix(carbon,rough,.84);metal=n.mix(carbon,metal,0)
 return finish(n,base,rough,metal,h,wear=rub)

def alloy(name,role,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n)
 fine=n.noise(p,3800,2);satin=n.noise(n.vec('MULTIPLY',p,(1800,22,1800)),1,2)
 base=(.0018,.0018,.0018);rough=n.add(.33,n.mul(sub(n,satin,.5),.055));rub=0;mark=0
 if role=='body':
  rub=n.mul(n.maximum(n.band(y,-.1244,.00018,.00015),n.band(y,.2314,.00016,.00014)),n.ramp(nz,-.2,.45))
  u=n.math('DIVIDE',sub(n,y,-.038),.090);v=n.math('DIVIDE',sub(n,z,.107),.012)
  mark=n.mul(texture(n,u,v,'scope'),n.ramp(ab(n,nx),.75,.98))
 elif role in ('Elevation','Windage','Parallax'):
  axis={'Elevation':z,'Windage':x,'Parallax':x}[role]
  start={'Elevation':.129,'Windage':.0165,'Parallax':-.039}[role]
  # Fine bright lip remains 0.6–0.8 mm, about two shipping texels.
  rub=n.band(axis,start+.0205,.00020,.00015)
  if role=='Elevation':a=x;b=sub(n,y,.062)
  else:a=sub(n,y,.062);b=sub(n,z,.113)
  angle=n.math('ARCTAN2',b,a)
  phase=n.math('SINE',n.mul(angle,32))
  crest=n.mul(n.ramp(phase,.96,1),interval(n,axis,start+.011,start+.019,.0005))
  rub=n.maximum(rub,n.mul(crest,.65))
  u=n.math('DIVIDE',n.add(angle,math.pi),math.tau)
  v=n.math('DIVIDE',sub(n,axis,start+.0045),.006)
  mark=0 if role=='Elevation' else texture(n,u,v,'turret')
 elif role in ('PowerRing','Diopter'):
  center=-.078 if role=='PowerRing' else -.119
  rub=n.mul(n.band(y,center+.0004,.00016,.00014),n.ramp(nz,-.2,.6))
 rub=n.ramp(n.mul(rub,wear,fractured(n,p)),.08,.55)
 base=n.mix(rub,base,(.62,.65,.68),True);rough=n.mix(rub,rough,.34)
 base=n.mix(mark,base,(.56,.57,.52),True)
 h=n.add(n.mul(sub(n,fine,.5),1.1e-6),n.mul(mark,-.000025))
 return finish(n,base,rough,n.mix(rub,0,1),h,wear=rub)

def stock(name,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n)
 # Three spatter sizes/colors with a dense background coat, generated in 3D.
 base=(.043,.052,.037)
 dark=n.ramp(n.voronoi(p,630),.32,.23)
 light=n.ramp(n.voronoi(n.vec('ADD',p,(.041,.033,.017)),920),.26,.17)
 mid=n.ramp(n.voronoi(n.vec('ADD',p,(.018,.071,.032)),420),.20,.14)
 base=n.mix(dark,base,(.009,.014,.006),True)
 base=n.mix(light,base,(.14,.135,.078),True)
 base=n.mix(mid,base,(.023,.031,.013),True)
 micro=n.noise(p,2000,2);h=n.mul(sub(n,micro,.5),.000025)
 # Narrow patches follow the high-contact longitudinal forms. Fine boundary
 # noise moves their edges <1 mm; it cannot create broad detached blotches.
 broken=n.add(n.mul(sub(n,n.noise(p,1450,2),.5),.18),
              n.mul(sub(n,n.noise(p,420,2),.5),.50))
 # Submillimeter lateral fray at 5–12 mm intervals. These perturb only the
 # cause-defined contact boundaries; no broad noise field supplies the wear.
 axial=n.add(n.mul(n.math('SINE',n.mul(y,720)),.00065),n.mul(n.math('SINE',n.mul(y,1310)),.00035))
 hand=n.add(n.mul(n.math('SINE',n.mul(z,620)),.0007),n.mul(n.math('SINE',n.mul(z,1140)),.00035))
 def patch(a,b,ca,cb,ra,rb):
  u=n.math('DIVIDE',sub(n,a,ca),ra);v=n.math('DIVIDE',sub(n,b,cb),rb)
  d=n.math('SQRT',n.add(n.mul(u,u),n.mul(v,v)))
  return n.ramp(n.add(d,broken),1.0,.75)
 comb=n.mul(patch(y,n.add(x,n.mul(axial,.65)),-.223,-.003,.047,.0055),n.ramp(nz,.76,.98))
 palm=n.mul(patch(z,n.add(sub(n,y,n.mul(z,.25)),hand),-.010,-.016,.030,.0048),n.ramp(ab(n,nx),.65,.97))
 front=n.mul(patch(z,n.add(y,n.mul(z,-.17),n.mul(hand,.6)),-.007,.008,.024,.0030),n.ramp(ny,.50,.9))
 lower=n.mul(patch(y,n.add(ab(n,x),axial),.332,.024,.091,.0028),n.ramp(nz,-.40,-.85))
 bag=n.mul(patch(y,n.add(x,n.mul(axial,1.2)),.330,-.004,.052,.006),n.ramp(nz,-.85,-.99))
 touch=n.maximum(comb,palm,front,lower,bag)
 rub=n.ramp(n.mul(touch,wear),.10,.65)
 base=n.mix(rub,base,(.015,.021,.014),True)
 core=n.mul(n.ramp(touch,.78,.99),n.ramp(n.noise(p,800,2),.57,.68),wear)
 base=n.mix(core,base,(.105,.115,.105),True)
 rough=n.mix(n.mul(n.ramp(touch,.03,.20),wear),n.add(.61,n.mul(sub(n,micro,.5),.05)),.37)
 h=n.add(n.mul(h,sub(n,1,n.mul(rub,.78))),n.mul(rub,-.000035))
 return finish(n,base,rough,0,h,wear=rub)

def rubber(name,foot,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n);noise=n.noise(p,1600,2)
 if foot:
  abrasion=n.mul(n.ramp(y,.560,.566),wear)
  dust=n.mul(abrasion,n.add(.35,n.mul(noise,.65)))
  base=n.mix(dust,(.006,.007,.007),(.082,.071,.048),True)
  h=n.mul(sub(n,noise,.5),.00008)
 else:
  grooves=n.ramp(n.math('SINE',n.mul(z,math.tau/.0036)),.6,.95)
  base=(.005,.006,.006);h=n.mul(grooves,-.00010)
 return finish(n,base,.83,0,h)

def ammo(name,role,fired,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n)
 # PartOffset is centered on the cartridge axis, with Y measured from its head.
 q=n.node('ShaderNodeAttribute',attribute_name='AmmoPosition').outputs['Vector'];a,b,c=n.split(q)
 tool=n.noise(n.vec('MULTIPLY',q,(2200,25,2200)),1,2)
 base=(.48,.29,.075) if role=='brass' else ((.47,.135,.049) if role=='copper' else (.40,.42,.42))
 rough=n.add(.29,n.mul(tool,.12));h=n.mul(sub(n,tool,.5),1e-6);metal=1
 if role=='brass':
  anneal=n.mul(interval(n,b,.038,.049,.003),.6)
  base=n.mix(anneal,base,(.30,.205,.10),True)
  stamp=n.mul(texture(n,n.add(.5,n.math('DIVIDE',a,.012)),n.add(.5,n.math('DIVIDE',c,.012)),'headstamp'),n.ramp(ny,-.7,-.98))
  h=n.add(h,n.mul(stamp,-.00006));base=n.mix(stamp,base,(.12,.072,.022),True)
  if fired:
   soot=n.mul(n.ramp(b,.046,.051),wear)
   base=n.mix(soot,base,(.023,.020,.014),True);rough=n.mix(soot,rough,.73)
 return finish(n,base,rough,metal,h)

def assign(wear):
 records={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
  offset=Vector((.3,0,0)) if ob.name=='Case_Proof' else Vector((0,0,0))
  verts=[v.co-offset for v in ob.data.vertices]
  lo=Vector(tuple(min(v[k] for v in verts) for k in range(3)));hi=Vector(tuple(max(v[k] for v in verts) for k in range(3)))
  center=(lo+hi)/2
  ammo_center=Vector((center.x,lo.y,center.z))
  pos=ob.data.attributes.new('FinishPosition','FLOAT_VECTOR','POINT');pos.data.foreach_set('vector',[a for v in verts for a in v])
  normal=ob.data.attributes.new('FinishNormal','FLOAT_VECTOR','CORNER');normal.data.foreach_set('vector',[a for r in ob.data.corner_normals for a in r.vector])
  for name,fn in [('PartOffset',lambda v:v-center),('PartCoord',lambda v:Vector(tuple((v[k]-lo[k])/max(hi[k]-lo[k],1e-8) for k in range(3)))),('AmmoPosition',lambda v:v-ammo_center)]:
   attr=ob.data.attributes.new(name,'FLOAT_VECTOR','POINT');attr.data.foreach_set('vector',[a for v in verts for a in fn(v)])
  roles=[]
  for i,old in enumerate(list(ob.data.materials)):
   key=old.name.removeprefix('CP_').split('.')[0];role=key;name='B24_'+ob.name+'_'+str(i)
   if key=='stock':mat=stock(name,wear)
   elif key=='rubber':mat=rubber(name,ob.name.startswith('Bipod'),wear)
   elif key in ('brass','copper') or 'Primer' in ob.name:
    role='primer' if 'Primer' in ob.name else key;mat=ammo(name,role,ob.name=='Case_Proof',wear)
   elif key=='alloy':
    role='body' if ob.name=='Scope_Body' else ob['bone'] if 'bone' in ob else 'other'
    mat=alloy(name,role,wear)
   elif key in ('reticle','marks','glass'):
    n=Nodes(name)
    color={'reticle':(.0001,.0001,.0001),'marks':(.56,.57,.52),'glass':(.87,.93,.95)}[key]
    mat=finish(n,color,.035 if key=='glass' else .6,.06 if key=='glass' else 0)
    if key=='glass':
     bs=mat.node_tree.nodes['SURFACE'];bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.46
     bs.inputs['Thin Film Thickness'].default_value=380
   else:
    role='receiver' if ob.name=='Receiver' else ('bolt' if ob.name=='Bolt_Body' else ('lug' if ob.name.startswith('Bolt_Lug') else ('barrel' if ob.name=='Barrel' else ('ring_screw' if ob.name.startswith('Ring_Screw') else ('bipod' if ob.name.startswith(('Bipod_Sleeve','Bipod_Extension')) else ('spring' if ob.name.startswith('Bipod_Return') else 'control' if ob.name.startswith(('Safety','Trigger','Bolt_Handle','Bolt_Knob')) else 'dark'))))))
    mat=steel(name,role,wear)
   ob.data.materials[i]=mat;roles.append(role)
  records[ob.name]=roles
 bpy.context.scene['finish_wear']=wear
 return records
