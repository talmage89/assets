"""Black paint over phosphate, molded polymer and causal years-of-carry wear.

All masks use immutable rest-coordinate attributes before rigid bake isolation.
Contact pressure gates broken chips; submillimeter noise frays their boundaries.
No photographs, external textures or generic all-over damage enter the shaders.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.materials import Nodes
from paint_masks import Y0,Y1,Z0,Z1

def sub(n,a,b):return n.math('SUBTRACT',a,b)
def ab(n,x):return n.math('ABSOLUTE',x)
def div(n,a,b):return n.math('DIVIDE',a,b)
def interval(n,x,a,b,f=.001):return n.mul(n.ramp(x,a-f,a),n.ramp(x,b+f,b))
def minimum(n,*values):
 result=values[0]
 for v in values[1:]:result=n.math('MINIMUM',result,v)
 return result
def inp(n):
 p=n.node('ShaderNodeAttribute',attribute_name='FinishPosition').outputs['Vector']
 normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal').outputs['Vector']
 q=n.node('ShaderNodeAttribute',attribute_name='PartCoord').outputs['Vector']
 return (p,*n.split(p),*n.split(normal),*n.split(q))
def finish(n,base,rough,metal,height=0,ao=1,wear=0,specular_factor=.56):
 n.channel('micro_ao',ao);n.channel('wear',wear)
 # glTF specular factor is twice Blender's Principled specular level. It is
 # data in the opaque BaseColor alpha, never transparency or a fourth map.
 n.channel('specular_factor',specular_factor)
 return n.finish(base,rough,metal,height,bump=1)
def tex(n,u,v,name):
 t=n.node('ShaderNodeTexImage',extension='CLIP',interpolation='Linear')
 t.image=bpy.data.images.load(str(BASE/'build/markings'/(name+'.png')),check_existing=True);t.image.colorspace_settings.name='Non-Color'
 n.feed(t.inputs['Vector'],n.combine(u,v,0));return t.outputs['Color']
def textfield(n,y,z,nx,name,cy,cz,w,h):
 u=n.add(.5,div(n,sub(n,y,cy),w));u=sub(n,1,u)
 v=n.add(.5,div(n,sub(n,z,cz),h))
 return n.mul(tex(n,u,v,name),n.ramp(n.mul(nx,-1),.75,.98))
def steel(name,part,wear,bright=False):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
 micro=n.noise(p,1700,2);tool=n.noise(n.vec('MULTIPLY',p,(2100,27,2100)),1,2)
 base=(.0015,.00154,.0015);rough=n.add(.42,n.mul(sub(n,micro,.5),.06));metal=0;specular=.08
 height=n.add(n.mul(sub(n,micro,.5),30e-6),n.mul(sub(n,n.noise(p,5800,2),.5),1.5e-6))
 # Distance in meters to exposed contact edges. Each part has its own causes.
 edge=1.;flat=0;dust=0;carbon=0;mark=0;rib_phosphate=0;rib_core_edge=0
 if part=='Receiver_Shell':
  ends=minimum(n,ab(n,sub(n,y,-.0396)),ab(n,sub(n,y,.1896)))
  edge=n.math('MAXIMUM',ends,sub(n,.0145,ab(n,x)))
  # End-cap abrasion follows the rolled outer contour as well as the flanks;
  # distance from the end plane alone would strip the entire cap face.
  roof_radius=n.math('SQRT',n.add(n.mul(div(n,x,.0167),div(n,x,.0167)),n.mul(div(n,sub(n,z,.1105),.0205),div(n,sub(n,z,.1105),.0205))))
  roof_rim=n.maximum(n.mul(ab(n,sub(n,roof_radius,1)),.0167),sub(n,.1105,z))
  edge=minimum(n,edge,n.maximum(ends,roof_rim))
  # Original 2-D fracture fields are generated in our rest frame. Their
  # physical bands and forward contact pressure precede the random fracture.
  # They contain no reference pixels or traced outlines.
  tu=div(n,sub(n,y,Y0),Y1-Y0);tv=div(n,sub(n,z,Z0),Z1-Z0)
  left=n.split(tex(n,tu,tv,'receiver_wear_left'))
  right=n.split(tex(n,tu,tv,'receiver_wear_right'))
  outer=n.ramp(n.mul(x,nx),.006,.012)
  rib_phosphate=n.mul(n.mix(n.ramp(x,-.001,.001),left[0],right[0]),outer)
  rib_core_edge=n.mul(n.mix(n.ramp(x,-.001,.001),left[1],right[1]),outer)
  pressure=n.maximum(n.ramp(ends,.045,.008),n.ramp(ab(n,sub(n,y,.116)),.045,.012))
  top=n.add(n.math('SQRT',n.add(n.mul(sub(n,ab(n,x),.0118),sub(n,ab(n,x),.0118)),n.mul(sub(n,z,.125),sub(n,z,.125)))),n.mul(sub(n,1,pressure),.0020))
  edge=minimum(n,edge,top)
  # Rounded rectangular ejection-port boundary, evaluated on the actual outer cheek.
  dy=n.math('MAXIMUM',sub(n,ab(n,sub(n,y,.112)),.017),0)
  dz=n.math('MAXIMUM',sub(n,ab(n,sub(n,z,.111)),.004),0)
  radius=n.math('SQRT',n.add(n.mul(dy,dy),n.mul(dz,dz)))
  port=ab(n,sub(n,radius,.005))
  edge=minimum(n,edge,n.math('MAXIMUM',port,sub(n,.0158,x)))
  dust=n.mul(n.maximum(n.band(z,.0915,.0002,.00055),n.band(z,.1088,.00015,.0005)),n.ramp(ab(n,nx),.65,.97),.27)
  carbon=n.mul(n.band(radius,.005,.0013,.0025),n.ramp(x,.015,.017),.42)
  mark=textfield(n,y,z,nx,'receiver',.058,.096,.094,.014)
  mark=n.maximum(mark,textfield(n,y,z,nx,'serial',.060,.080,.072,.0055))
 elif part=='Cocking_Tube':
  # Front rim is at 332 mm after the accepted silhouette calibration.
  # Slot edges follow the actual through-cut and its raised locking branch.
  front=ab(n,sub(n,y,.332))
  slot=minimum(n,n.maximum(minimum(n,ab(n,sub(n,z,.1201)),ab(n,sub(n,z,.1239))),sub(n,.2145,y),sub(n,y,.310)),
    n.maximum(minimum(n,ab(n,sub(n,y,.2145)),ab(n,sub(n,y,.310))),sub(n,.1201,z),sub(n,z,.1239)))
  branch=n.maximum(minimum(n,ab(n,sub(n,y,.2145)),ab(n,sub(n,y,.2245))),sub(n,.1239,z),sub(n,z,.130))
  slot=minimum(n,slot,branch)
  slot=n.math('MAXIMUM',slot,sub(n,x,-.006))
  edge=minimum(n,front,slot)
  flat=n.mul(interval(n,y,.205,.325,.006),n.ramp(nz,.85,.99))
 elif part=='Cocking_FrontCap':
  r=n.math('SQRT',n.add(n.mul(x,x),n.mul(sub(n,z,.122),sub(n,z,.122))))
  edge=n.math('MAXIMUM',ab(n,sub(n,y,.3337)),ab(n,sub(n,r,.0084)))
 elif part.startswith('MagazineWell'):
  edge=n.math('MAXIMUM',ab(n,sub(n,z,.0386)),sub(n,.014,ab(n,x)))
 elif part.startswith('Magazine_Body'):
  s=sub(n,.080,z)
  # The lower magazine's quadratic center follows its accepted curved shell.
  t=n.math('MAXIMUM',sub(n,s,.020),0);center=n.add(.143,n.mul(s,.12),n.mul(t,t,1.6))
  spine=ab(n,sub(n,sub(n,y,center),-.0171))
  edge=spine
  edge=minimum(n,edge,n.math('MAXIMUM',ab(n,sub(n,z,.0749)),sub(n,.009,ab(n,x))))
 elif part.startswith('Magazine_FeedLip'):edge=minimum(n,n.mul(minimum(n,u,sub(n,1,u)),.008),n.mul(sub(n,1,w),.013))
 elif part.startswith('Magazine_Floorplate'):
  theta=math.atan(.12+.0032*144)
  ly=n.add(n.mul(sub(n,y,.19644),math.cos(theta)),n.mul(sub(n,z,-.0864),math.sin(theta)))
  lz=n.add(-.0864,n.mul(sub(n,y,.19644),-math.sin(theta)),n.mul(sub(n,z,-.0864),math.cos(theta)))
  dx=ab(n,sub(n,ab(n,x),.0126));dy=ab(n,sub(n,ab(n,ly),.0183));dz=minimum(n,ab(n,sub(n,lz,-.0846)),ab(n,sub(n,lz,-.0882)))
  edge=minimum(n,n.math('MAXIMUM',dx,dy),n.math('MAXIMUM',minimum(n,dx,dy),dz))
 elif part=='Sight_FrontHood':
  r=n.math('SQRT',n.add(n.mul(x,x),n.mul(sub(n,z,.148),sub(n,z,.148))))
  axial=minimum(n,ab(n,sub(n,y,.337)),ab(n,sub(n,y,.344)))
  radial=minimum(n,ab(n,sub(n,r,.0125)),ab(n,sub(n,r,.0149)))
  edge=n.math('MAXIMUM',axial,radial)
 elif part=='Sight_RearDrum':
  ly=n.add(n.mul(sub(n,y,.0005),math.cos(math.radians(16))),n.mul(sub(n,z,.133),math.sin(math.radians(16))))
  lz=n.add(.133,n.mul(sub(n,y,.0005),-math.sin(math.radians(16))),n.mul(sub(n,z,.133),math.cos(math.radians(16))))
  r=n.math('SQRT',n.add(n.mul(x,x),n.mul(ly,ly)))
  edge=minimum(n,n.math('MAXIMUM',ab(n,sub(n,lz,.1555)),ab(n,sub(n,r,.0112))),n.math('MAXIMUM',ab(n,sub(n,lz,.137)),ab(n,sub(n,r,.013))))
  dust=n.mul(n.band(lz,.137,.00012,.00045),.27)
 elif part.startswith(('Sight_Adjustment','Sight_Clamp')):
  du=n.mul(minimum(n,u,sub(n,1,u)),.014);dv=n.mul(minimum(n,v,sub(n,1,v)),.020);dw=n.mul(minimum(n,w,sub(n,1,w)),.004)
  edge=minimum(n,n.math('MAXIMUM',du,dv),n.math('MAXIMUM',du,dw),n.math('MAXIMUM',dv,dw))
 elif part.startswith('Handle_Grip'):
  du=n.mul(minimum(n,u,sub(n,1,u)),.009);dv=n.mul(minimum(n,v,sub(n,1,v)),.014);dw=n.mul(minimum(n,w,sub(n,1,w)),.011)
  edge=minimum(n,n.math('MAXIMUM',du,dv),n.math('MAXIMUM',du,dw),n.math('MAXIMUM',dv,dw))
 elif part.startswith(('Trigger_Shoe','MagazineRelease_Paddle')):edge=n.mul(minimum(n,v,sub(n,1,v),w,sub(n,1,w)),.015)
 elif part in ('Barrel','Muzzle_Collar'):
  edge=ab(n,sub(n,y,.3996));carbon=n.mul(n.ramp(y,.389,.400),.75)
 elif part.startswith(('Rear_LockingPin','Lower_FrontPin','Handguard_Pin')):edge=n.mul(minimum(n,v,sub(n,1,v),w,sub(n,1,w)),.006)
 if 'Weld' in part:
  phase=n.mul(y,math.tau/.0007) if part.startswith('Sight_Front') else n.mul(n.math('ARCTAN2',sub(n,z,.122),x),40)
  height=n.add(height,n.mul(n.math('SINE',phase),22e-6))
  rough=n.add(rough,n.mul(sub(n,tool,.5),.10))
 if bright:
  base=(.30,.32,.33);rough=n.add(.30,n.mul(sub(n,tool,.5),.08));metal=1
  specular=.28
  height=n.mul(sub(n,tool,.5),.8e-6)
 # Chipped paint, not polished trim. Gray conversion coating is mostly
 # dielectric and very rough. Rare steel flecks survive only at sharp points.
 warp=n.node('ShaderNodeTexNoise');n.feed(warp.inputs['Vector'],p)
 warp.inputs['Scale'].default_value=230;warp.inputs['Detail'].default_value=1
 offset=n.vec('MULTIPLY',n.vec('SUBTRACT',warp.outputs['Color'],(.5,.5,.5)),(.002,.002,.002))
 warped=n.vec('ADD',p,offset)
 chips=n.add(n.mul(n.noise(warped,650,1),.74),n.mul(n.noise(warped,210,1),.26))
 # A bias in threshold reduces density outward. There is no second straight
 # ribbon mask and no uniform wash of low-opacity gray at the margins.
 distance=n.maximum(edge,0)
 chipped=n.ramp(sub(n,chips,n.add(.49,n.mul(distance,90))),-.012,.012)
 phosphate=n.maximum(rib_phosphate,chipped)
 flat=n.mul(flat,n.ramp(sub(n,chips,.51),-.010,.010))
 phosphate=n.mul(n.maximum(phosphate,flat),wear)
 sharp=n.maximum(n.ramp(distance,.00016,.00003),rib_core_edge)
 core=n.mul(phosphate,sharp,n.ramp(n.noise(n.vec('MULTIPLY',p,(640,450,770)),1,2),.72,.77))
 core=n.maximum(core,n.mul(rib_core_edge,wear))
 phosphate_color=(.060,.064,.061)
 if part=='Receiver_Shell':
  land_color=n.mul(rib_phosphate,interval(n,z,.109,.1255,.0006),interval(n,y,-.022,.154,.002))
  # Porous conversion-coating grain is intrinsic to the exposed substrate.
  # Multiplier is centered on one; it adds no wear or change of hue/BRDF.
  grain=n.add(.12,n.mul(n.noise(p,900,2),1.76))
  gray=n.vec('MULTIPLY',(.058,.049,.0375),n.combine(grain,grain,grain))
  phosphate_color=n.mix(land_color,phosphate_color,gray,True)
 base=n.mix(phosphate,base,phosphate_color,True);metal=n.mix(phosphate,metal,.08);rough=n.mix(phosphate,rough,.88)
 specular=n.mix(phosphate,specular,.28)
 base=n.mix(core,base,(.30,.32,.33),True);metal=n.mix(core,metal,1);rough=n.mix(core,rough,.58)
 specular=n.mix(core,specular,.28)
 height=n.add(height,n.mul(phosphate,-.000014),n.mul(mark,-.000075))
 base=n.mix(mark,base,(.012,.013,.012),True)
 specular=n.mix(mark,specular,.28)
 dust=n.mul(dust,wear);base=n.mix(dust,base,(.055,.049,.037),True);rough=n.mix(dust,rough,.83)
 specular=n.mix(dust,specular,.28)
 carbon=n.mul(carbon,wear);base=n.mix(carbon,base,(.0012,.0011,.0010),True);rough=n.mix(carbon,rough,.85);metal=n.mix(carbon,metal,0)
 specular=n.mix(carbon,specular,.28)
 mat=finish(n,base,rough,metal,height,wear=n.maximum(phosphate,core),specular_factor=n.mul(specular,2))
 n.feed(mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'],specular)
 return mat
def polymer(name,part,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
 grain=n.noise(p,5200,2);base=(.012,.013,.012);rough=.78;touch=0;dust=0;mark=0
 if part.startswith(('Lower_Mold','Grip_TexturePanel')):
  # Front/back straps and the panel's contact peaks polish from hands.
  touch=n.mul(interval(n,z,-.050,.020,.007),n.maximum(n.ramp(ab(n,ny),.55,.94),n.mul(n.ramp(ab(n,nx),.8,.98),.5)))
  dust=n.mul(n.band(n.math('SQRT',n.add(n.mul(sub(n,y,.003),sub(n,y,.003)),n.mul(sub(n,z,.057),sub(n,z,.057)))),.0117,.00012,.00025),interval(n,z,.060,.070,.0005),n.ramp(ab(n,nx),.7,.95),.22)
  if part=='Lower_Mold':mark=textfield(n,y,z,nx,'lower',-.027,.062,.034,.007)
 elif part=='Handguard_Mold':touch=n.mul(interval(n,y,.205,.305,.010),n.ramp(ab(n,nx),.55,.92))
 elif part=='Stock_Mold':touch=n.mul(interval(n,y,-.220,-.070,.014),n.ramp(nz,.74,.97))
 elif part.startswith('Selector_Mark'):mark=1
 touch=n.mul(touch,wear)
 rough=n.mix(touch,n.add(rough,n.mul(sub(n,grain,.5),.06)),.48)
 base=n.mix(touch,base,(.0095,.0105,.0095),True)
 base=n.mix(n.mul(dust,wear),base,(.037,.034,.027),True)
 height=n.add(n.mul(sub(n,grain,.5),n.mix(touch,6e-6,1.5e-6)),n.mul(mark,.00007))
 # Dense geometry supplies the pebbled shape. Worn areas also reduce its bump
 # response through the finer material field; the game mesh stays unchanged.
 return finish(n,base,rough,0,height,n.mix(n.mul(dust,wear),1,.88),touch)
def ammo(name,role,fired):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
 q=n.node('ShaderNodeAttribute',attribute_name='AmmoPosition').outputs['Vector'];a,b,c=n.split(q)
 tool=n.noise(n.vec('MULTIPLY',q,(2600,30,2600)),1,2)
 base={'brass':(.48,.285,.075),'copper':(.48,.14,.052),'primer':(.40,.42,.40)}[role]
 rough=n.add(.29,n.mul(tool,.09));height=n.mul(sub(n,tool,.5),.7e-6)
 if role=='brass':
  stamp=n.mul(tex(n,n.add(.5,div(n,a,.010)),n.add(.5,div(n,c,.010)),'headstamp'),n.ramp(ny,-.8,-.98))
  height=n.add(height,n.mul(stamp,-.000055));base=n.mix(stamp,base,(.10,.058,.017),True)
  if fired:
   soot=n.ramp(b,.017,.0192);base=n.mix(soot,base,(.024,.019,.010),True);rough=n.mix(soot,rough,.74)
 return finish(n,base,rough,1,height)
def assign(wear):
 records={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
  shift=Vector((.4 if ob.name=='Cartridge_Proof' else .5 if ob.name=='Case_Proof' else 0,0,0))
  vertices=[v.co-shift for v in ob.data.vertices]
  lo=Vector(tuple(min(v[k] for v in vertices) for k in range(3)));hi=Vector(tuple(max(v[k] for v in vertices) for k in range(3)));center=(lo+hi)/2
  ammo_center=Vector((center.x,lo.y,center.z))
  for attr,values,domain in [('FinishPosition',vertices,'POINT'),('FinishNormal',[n.vector for n in ob.data.corner_normals],'CORNER'),('PartCoord',[Vector(tuple((v[k]-lo[k])/max(hi[k]-lo[k],1e-8) for k in range(3))) for v in vertices],'POINT'),('AmmoPosition',[v-ammo_center for v in vertices],'POINT')]:
   field=ob.data.attributes.new(attr,'FLOAT_VECTOR',domain);field.data.foreach_set('vector',[a for v in values for a in v])
  roles=[]
  for i,old in enumerate(list(ob.data.materials)):
   key=old.name.removeprefix('CP_').split('.')[0];name='R9_'+ob.name+'_'+str(i)
   if ob.name=='Handle_Grip':mat=steel(name,ob.name,wear)
   elif key in ('brass','copper','primer'):mat=ammo(name,key,ob.name=='Case_Proof')
   elif key in ('polymer','follower') or ob.name.startswith('Selector_Mark'):mat=polymer(name,ob.name,wear)
   elif key=='rubber':
    n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n);groove=n.ramp(n.math('SINE',n.mul(z,math.tau/.003)),.6,.95)
    mat=finish(n,(.0025,.0027,.0025),.78,0,n.mul(groove,-.00011))
   else:mat=steel(name,ob.name,wear,bright=key=='steel' or ob.name=='Handle_Stem')
   ob.data.materials[i]=mat;roles.append(key)
  records[ob.name]=roles
 bpy.context.scene['finish_wear']=wear;return records
