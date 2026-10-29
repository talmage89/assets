"""Blued steel, longitudinal walnut and .30-30 metals, entirely procedural.

Finish fields use explicit rest-position/corner-normal attributes, so bone
isolation cannot move their masks. Reference images are never read here.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.materials import Nodes

def sub(n,a,b):return n.math('SUBTRACT',a,b)
def absolute(n,a):return n.math('ABSOLUTE',a)
def ramp(n,x,a,b):return n.ramp(n.math('DIVIDE',sub(n,x,a),sub(n,b,a)),0,1)
def interval(n,x,a,b,f=.001):return n.mul(ramp(n,x,sub(n,a,f),a),ramp(n,x,n.add(b,f),b))
def oval(n,y,z,cy,cz,ry,rz):
 # Smooth contact pressure, with no straight boundary across a curved part.
 d=n.add(n.math('POWER',n.math('DIVIDE',sub(n,y,cy),ry),2),
         n.math('POWER',n.math('DIVIDE',sub(n,z,cz),rz),2))
 return n.math('EXPONENT',n.mul(d,-1.8))
def inputs(n):
 p=n.node('ShaderNodeAttribute',attribute_name='FinishPosition').outputs['Vector']
 normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal').outputs['Vector']
 return (p,*n.split(p),*n.split(normal))
def finish(n,base,rough,metal,height,wear=0,ao=1):
 n.channel('wear',wear);n.channel('micro_ao',ao)
 mat=n.finish(base,rough,metal,height,bump=1)
 mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'].default_value=.16
 return mat

def lettering(n,u,v,name):
 tex=n.node('ShaderNodeTexImage',extension='CLIP',interpolation='Cubic')
 tex.image=bpy.data.images.load(str(BASE/'build/markings'/(name+'.png')),check_existing=True)
 tex.image.colorspace_settings.name='Non-Color';n.feed(tex.inputs['Vector'],n.combine(u,v,0))
 return tex.outputs['Color']

def steel(name,role,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n);ax=absolute(n,x)
 fine=n.noise(p,6000,2)
 striae=n.noise(n.combine(n.mul(x,1800),n.mul(y,12),n.mul(z,1800)),1,2)
 base=(.021,.022,.023);rough=n.add(.36,n.mul(sub(n,striae,.5),.075));metal=1
 height=n.mul(sub(n,fine,.5),1.2e-6);rub=0;soot=0
 # Longitudinal contact pressure breaks the edge's width at several scales;
 # noise never supplies the location or turns the finish into random blobs.
 drag=n.add(.78,n.mul(n.math('SINE',n.mul(y,257)),.12),n.mul(striae,.16))
 if role=='receiver':
  section=n.node('ShaderNodeAttribute',attribute_name='ReceiverSection').outputs['Vector']
  width,bottom,top=n.split(section)
  side=ramp(n,ax,sub(n,width,.0024),sub(n,width,.0007))
  # Years of palm contact thin the oxide across the flat, leaving a plum /
  # brown cast. This is translucent oxide, separate from exposed edge steel.
  hand=n.mul(interval(n,y,.081,.183,.027),interval(n,z,n.add(bottom,.006),sub(n,top,.006),.008),
    n.ramp(absolute(n,nx),.7,.95),wear)
  # Palm/holster pressure reaches the flats, but not the shadow of screw
  # heads, the gate's recess or either tang junction. These are distance
  # fields in the original forging frame, never photographic masks.
  protected=0
  for cy,cz,r in ((.074,.015,.00315),(.092,.038,.00255),(.148,.040,.00265),(.185,.016,.0025)):
   d=n.math('SQRT',n.add(n.math('POWER',sub(n,y,cy),2),n.math('POWER',sub(n,z,cz),2)))
   protected=n.maximum(protected,n.mul(n.ramp(d,r+.0030,r+.0003),.52))
  cy=n.math('MAXIMUM',.1286,n.math('MINIMUM',y,.1668))
  gate_distance=n.math('SQRT',n.add(n.math('POWER',sub(n,y,cy),2),n.math('POWER',sub(n,z,.020),2)))
  protected=n.maximum(protected,n.mul(n.ramp(gate_distance,.011,.0068),n.ramp(nx,.65,.95)),
    n.ramp(y,.087,.068),n.ramp(y,.181,.202))
  pressure=n.maximum(oval(n,y,z,.123,.032,.066,.040),n.mul(oval(n,y,z,.170,.025,.038,.027),.65))
  patina=n.mul(hand,sub(n,1,protected),pressure,
    n.add(.68,n.mul(n.noise(n.combine(n.mul(x,19),n.mul(y,44),n.mul(z,78)),1,2),.32)))
  # A metal/oxide effective layer: the brown oxide contributes mostly diffuse
  # color, while steel and the dielectric surface supply a near-neutral
  # reflection. A fully metallic orange base is copper, not thinned bluing.
  base=n.mix(patina,base,(.072,.031,.011),True)
  metal=n.mix(n.ramp(patina,.05,.35),metal,.05)
  rough=n.mix(patina,rough,n.add(.46,n.mul(sub(n,striae,.5),.10)))
  # Resolved 0.2-0.4 mm carry striae, elongated along the barrel. Pressure
  # locates them; they modulate thinning/roughness rather than become wires.
  scratch=n.mul(patina,n.ramp(striae,.64,.78),.12)
  base=n.mix(scratch,base,(.10,.093,.084),True)
  rough=n.add(rough,n.mul(scratch,.13));height=n.add(height,n.mul(scratch,-3e-6))
  lower_width=n.add(.00093,n.mul(interval(n,y,.085,.140,.025),.00028),
    n.mul(n.math('SINE',n.mul(y,97)),.00010),n.mul(sub(n,striae,.5),.00006))
  # A cupped carrying hand reaches around the rear action belly: contact
  # descends toward the corner around the pivot, then returns onto the side.
  # Both center and width vary; following only the geometric edge is too even.
  lower_center=n.add(.00275,n.mul(interval(n,y,.097,.120,.012),-.00150),
    n.mul(n.math('SINE',n.mul(y,55)),.00022))
  lower=n.mul(n.ramp(n.math('DIVIDE',absolute(n,sub(n,sub(n,z,bottom),lower_center)),lower_width),1.3,.45),side)
  # Preserve the accepted cupped lower-fillet field exactly. Other corners
  # have isolated impacts/carry rubs, rather than a continuous silver outline.
  upper=n.mul(n.band(sub(n,top,z),.00105,.00015,.00028),side,
    n.maximum(interval(n,y,.078,.087,.0015),n.mul(interval(n,y,.178,.185,.0012),.65)))
  ends=n.maximum(n.mul(n.ramp(y,.067,.0654),interval(n,z,.010,.020,.003),.48),
    n.mul(n.ramp(y,.2029,.2046),interval(n,z,.012,.029,.004),.85))
  rub=n.mul(n.maximum(lower,upper,n.mul(ends,side)),drag,wear)
  marks=n.mul(lettering(n,n.math('DIVIDE',sub(n,.177,y),.072),n.math('DIVIDE',sub(n,z,.040),.013),'receiver'),n.ramp(nx,-.8,-.98))
  marks=n.maximum(marks,n.mul(lettering(n,n.math('DIVIDE',sub(n,y,.076),.046),n.math('DIVIDE',sub(n,z,.043),.009),'serial'),n.ramp(nx,.8,.98)))
  height=n.add(height,n.mul(marks,-.000075));base=n.mix(n.mul(marks,.65),base,(.006,.005,.004),True)
 elif role=='lever':
  rough=n.add(.44,n.mul(sub(n,striae,.5),.10))
  # Hand-ridden inner lower finger-loop rail; the S web remains blued.
  u=n.add(n.mul(n.add(y,.006),math.cos(math.radians(12))),n.mul(n.add(z,.0305),math.sin(math.radians(12))))
  v=n.add(n.mul(n.add(y,.006),-math.sin(math.radians(12))),n.mul(n.add(z,.0305),math.cos(math.radians(12))))
  rail=n.mul(interval(n,u,-.047,.046,.007),n.band(v,-.0161,.0012,.0013))
  # Fingers rub the inside wall; the exterior lower rail and forward bow
  # retain blue. Pressure dies away around both ends of the aperture.
  inner=n.mul(rail,n.ramp(n.add(n.mul(nz,math.cos(math.radians(12))),n.mul(ny,-math.sin(math.radians(12)))),.05,.75))
  rear=n.mul(oval(n,y,z,-.052,-.035,.015,.015),n.ramp(ny,-.1,-.8),.80)
  rub=n.mul(n.maximum(inner,rear),drag,wear)
 elif role=='gate':
  cy=n.math('MAXIMUM',.1286,n.math('MINIMUM',y,.1668))
  radius=n.math('SQRT',n.add(n.math('POWER',sub(n,y,cy),2),n.math('POWER',sub(n,z,.020),2)))
  rub=n.mul(n.ramp(radius,.0059,.00635),drag,wear,n.add(.7,n.mul(n.math('SINE',n.mul(y,150)),.3)))
 elif role=='band':
  rough=n.add(.45,n.mul(sub(n,striae,.5),.10))
  rim=n.maximum(n.band(y,.428,.00025,.00045),n.band(y,.436,.00025,.00045),
    n.band(y,.663,.00025,.00045),n.band(y,.671,.00025,.00045))
  rub=n.mul(rim,n.add(.6,n.mul(n.ramp(absolute(n,nx),.35,.8),.4)),drag,wear)
 elif role=='barrel':
  radius=n.math('SQRT',n.add(n.mul(x,x),n.math('POWER',sub(n,z,.048),2)))
  crown=n.mul(n.ramp(y,.7069,.7078),n.ramp(radius,.0079,.0087))
  rub=n.mul(crown,wear,drag)
  soot=n.mul(n.ramp(y,.706,.708),n.ramp(radius,.0048,.0040),wear)
  marks=n.mul(lettering(n,n.math('DIVIDE',sub(n,y,.224),.067),n.math('DIVIDE',sub(n,z,.043),.010),'barrel'),n.ramp(nx,.6,.95))
  height=n.add(height,n.mul(marks,-.000065));base=n.mix(n.mul(marks,.75),base,(.006,.005,.004),True)
 elif role=='plate':
  rub=n.mul(n.maximum(n.ramp(z,-.097,-.106),n.ramp(z,.001,.007)),n.ramp(absolute(n,ny),.15,.9),wear,.85)
 elif role=='trigger':
  rough=n.add(.45,n.mul(sub(n,striae,.5),.10))
  rub=n.mul(n.ramp(ny,.35,.9),interval(n,z,-.026,-.007,.004),wear,.72)
 elif role=='control':
  # A thumb smooths the crowned pad only. Sidewalls are still blue.
  rub=n.mul(n.ramp(nz,.55,.95),interval(n,y,.046,.067,.003),wear,.20)
 elif role=='tang':
  rough=n.add(.55,n.mul(sub(n,striae,.5),.10))
  rub=n.mul(oval(n,y,z,-.016,.026,.027,.009),n.ramp(nz,.65,.95),wear,.23)
 elif role=='bright':
  base=(.32,.34,.36);rough=n.add(.28,n.mul(striae,.07))
 elif role=='dark':base=(.012,.013,.014);rough=.42
 if role in ('receiver','lever','gate','band','barrel','plate'):
  rub=n.ramp(rub,.13,.65)
 bare=(.24,.26,.28) if role=='receiver' else (.12,.135,.145)
 base=n.mix(rub,base,bare,True);rough=n.mix(rub,rough,n.add(.62,n.mul(sub(n,striae,.5),.16)))
 metal=n.mix(rub,metal,1)
 base=n.mix(soot,base,(.0025,.0021,.0018),True);rough=n.mix(soot,rough,.78);metal=n.mix(soot,metal,.05)
 return finish(n,base,rough,metal,height,rub)

def wood(name,role,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n)
 # Curved growth layers cut by a longitudinal blank. Broad annual growth
 # and individual vessel pores are separate physical structures.
 if role=='stock':
  axis=n.add(n.mul(y,.12),n.mul(n.math('MAXIMUM',n.add(y,.065),0),.35))
  yy=n.math('MINIMUM',n.add(y,.08),0);zz=sub(n,z,axis)
  rx=n.add(x,.035);rz=n.add(n.mul(zz,.78),.041);arch=n.mul(yy,yy,.18)
 else:
  yy=sub(n,y,.325);zz=sub(n,z,.02)
  rx=n.add(x,.030);rz=n.add(n.mul(zz,.88),.025);arch=n.mul(yy,yy,.42)
 radius=n.math('SQRT',n.add(n.mul(rx,rx),n.mul(rz,rz)))
 figure=n.add(n.mul(n.math('SINE',n.add(n.mul(zz,125),n.mul(y,13))),.00032),
              n.mul(n.math('SINE',n.add(n.mul(x,160),n.mul(y,17))),.00022))
 phase=n.add(n.mul(n.add(radius,arch,figure),math.tau/.0028),
   n.mul(n.math('SINE',n.mul(radius,310)),.6),n.mul(n.math('SINE',n.mul(radius,850)),.25))
 year=n.math('FRACT',n.mul(phase,1/math.tau))
 late=n.ramp(year,.86,.99)
 tone=n.add(.50,n.mul(n.ramp(year,.13,.62),.12),n.mul(n.ramp(year,.64,.96),-.14),
   n.mul(n.math('SINE',n.add(n.mul(zz,142),n.mul(y,19))),.045))
 low,high=((.022,.008,.0035),(.155,.063,.034)) if role=='stock' else ((.026,.010,.005),(.180,.082,.050))
 base=n.mix(tone,low,high,True)
 base=n.mix(n.mul(late,.25),base,(.008,.0028,.0014),True)
 cells=n.node('ShaderNodeTexVoronoi',feature='F1',distance='EUCLIDEAN')
 n.feed(cells.inputs['Vector'],n.combine(n.mul(x,1450),n.mul(y,170),n.mul(zz,1500)));cells.inputs['Scale'].default_value=1
 color=n.node('ShaderNodeSeparateColor',mode='RGB');n.feed(color.inputs[0],cells.outputs['Color'])
 pores=n.mul(n.ramp(cells.outputs['Distance'],.29,.13),n.ramp(color.outputs[0],.45,.7))
 bundle=n.voronoi(n.combine(n.mul(x,1000),n.mul(y,60),n.mul(zz,1100)),1,'DISTANCE_TO_EDGE')
 fibers=n.ramp(bundle,.13,.045)
 base=n.mix(n.mul(fibers,.19),base,(.017,.0050,.0022),True)
 base=n.mix(n.mul(pores,.68),base,(.005,.0022,.0012),True)
 height=n.add(n.mul(late,-9e-6),n.mul(fibers,-7e-6),n.mul(pores,-23e-6))
 rough=n.add(.48,n.mul(pores,.09),n.mul(late,.025))
 if role=='stock':
  # Palm wraps the wrist, tapering diagonally with its carved crown. Vary
  # pressure around its section so no axial plane becomes a dark cuff.
  center=n.add(-.014,n.mul(nz,.018),n.mul(absolute(n,x),.50))
  distance=n.math('DIVIDE',sub(n,y,center),.067)
  hand=n.mul(n.math('EXPONENT',n.mul(distance,distance,-1.7)),
    n.add(.70,n.mul(n.ramp(absolute(n,nx),.15,.9),.30)),wear)
 else:hand=n.mul(interval(n,y,.268,.367,.028),wear,.45)
 base=n.mix(n.mul(hand,.88),base,(.0067,.0034,.0022),True);rough=n.mix(hand,rough,.40)
 # Local blows at toe, heel and exposed forend margins crush dark fibers,
 # with small pale broken-finish lips. No uniform dirt band/no noise wash.
 sites=([(-.242,-.096,.0045,.0024),(-.238,.001,.0034,.0018),(-.214,-.082,.0025,.0013),(-.190,-.061,.002,.001)]
        if role=='stock' else [(.218,.011,.0035,.002),(.420,.007,.0037,.0017),(.439,.025,.0023,.0014)])
 facing=n.ramp(absolute(n,nx),.18,.65);dings=0
 for yy,zz,wy,wz in sites:
  u=n.add(n.math('DIVIDE',sub(n,y,yy),wy),n.mul(n.math('DIVIDE',sub(n,z,zz),wz),.3))
  v=n.math('DIVIDE',sub(n,z,zz),wz)
  r2=n.add(n.math('POWER',absolute(n,u),2.6),n.math('POWER',absolute(n,v),1.7))
  bowl=n.math('MAXIMUM',sub(n,1,r2),0);dent=n.mul(bowl,bowl,facing,wear)
  lip=n.mul(n.band(r2,.86,.09,.12),n.ramp(v,-.1,.6),facing,wear)
  dings=n.maximum(dings,dent,lip)
  height=n.add(height,n.mul(dent,-.00036),n.mul(lip,.000025))
  base=n.mix(n.mul(dent,.75),base,(.009,.004,.0021),True)
  base=n.mix(n.mul(lip,.9),base,(.13,.065,.027),True);rough=n.mix(n.maximum(dent,lip),rough,.62)
 mat=finish(n,base,rough,0,height,dings,n.mix(pores,1,.87))
 mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'].default_value=.16
 return mat

def ammo(name,kind,fired):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inputs(n)
 fine=n.noise(p,6000,2);patch=n.noise(p,550,2)
 height=n.mul(sub(n,fine,.5),1.2e-6);rough=n.add(.29,n.mul(fine,.06))
 base={'brass':(.49,.29,.085),'copper':(.43,.16,.062),'lead':(.14,.145,.15),'steel':(.36,.37,.38),'stamp':(.028,.021,.012)}[kind]
 base=n.mix(n.mul(n.ramp(patch,.52,.78),.18),base,(.14,.070,.022) if kind=='brass' else base,True)
 if kind=='lead':rough=.55
 if fired and kind=='brass':
  soot=n.mul(n.ramp(y,.048,.0518),n.add(.82,n.mul(patch,.18)))
  base=n.mix(soot,base,(.025,.014,.006),True);rough=n.mix(soot,rough,.72)
 return finish(n,base,rough,1,height)

def assign(wear=1):
 from forms import RECEIVER_ROWS
 from dimensions import HEADS
 records={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
  position=ob.data.attributes.new('FinishPosition','FLOAT_VECTOR','POINT')
  normal=ob.data.attributes.new('FinishNormal','FLOAT_VECTOR','CORNER')
  base=Vector((0,0,0));transform=Matrix.Identity(4)
  name=ob.name
  if name.startswith('Tube_Round'):
   i=int(name[len('Tube_Round')]);base=Vector(HEADS['Tube'+str(i)])*.001
  for prefix,point in [('Chamber_Live',(0,200,48)),('Extracted_Case',(0,200,48)),('Insert_Live',(25,113,20))]:
   if name.startswith(prefix):base=Vector(point)*.001
  if name.startswith('Carrier_Live'):
   pivot=Vector(HEADS['Carrier'])*.001
   transform=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(20),4,'X')@Matrix.Translation(-pivot)
   base=Vector((0,.125,.048))
  position.data.foreach_set('vector',[a for v in ob.data.vertices for a in (transform@v.co-base)])
  normal.data.foreach_set('vector',[a for row in ob.data.corner_normals for a in (transform.to_3x3()@row.vector)])
  if name=='Receiver':
   section=ob.data.attributes.new('ReceiverSection','FLOAT_VECTOR','POINT');values=[]
   for v in ob.data.vertices:
    yy=max(65,min(205,v.co.y*1000));a,b=next((a,b) for a,b in zip(RECEIVER_ROWS,RECEIVER_ROWS[1:]) if a[0]<=yy<=b[0]);t=(yy-a[0])/(b[0]-a[0])
    values.extend((a[k]+t*(b[k]-a[k]))*.001 for k in (1,2,3))
   section.data.foreach_set('vector',values)
  roles=[]
  for index,old in enumerate(list(ob.data.materials)):
   key=old.name.removeprefix('CP_').split('.')[0];role=key;label='L20_'+name+'_'+str(index)
   isammo=name.startswith(('Standalone_','Tube_Round','Chamber_Live','Carrier_Live','Insert_Live','Extracted_Case'))
   if key=='wood':role='stock' if name=='Stock' else 'forend';mat=wood(label,role,wear)
   elif isammo:mat=ammo(label,key,name.startswith(('Standalone_case','Extracted_Case')))
   elif key=='brass':mat=ammo(label,'brass',False)
   else:
    if name=='Receiver':role='receiver'
    elif name=='Lever_FingerLoop':role='lever'
    elif name=='Loading_Gate':role='gate'
    elif name in ('Forend_Band','Muzzle_Band'):role='band'
    elif name=='Barrel':role='barrel'
    elif name=='Butt_Plate':role='plate'
    elif name=='Trigger_Blade':role='trigger'
    elif name.startswith('Hammer'):role='control'
    elif name=='Upper_Tang':role='tang'
    elif key=='steel':role='bright'
    mat=steel(label,role,wear)
   ob.data.materials[index]=mat;roles.append(role)
  records[name]=roles
 bpy.context.scene['finish_wear']=wear
 return records
