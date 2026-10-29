"""Original issued finishes and causal handling masks in immutable rest space.

No photo is loaded here. Noise fractures an already located abrasion field;
it never scatters damage over otherwise protected flats. Manufactured wood
layers, pores, enamel grain and phenolic filler are distinct from use wear.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.materials import Nodes

def sub(n,a,b):return n.math('SUBTRACT',a,b)
def ab(n,x):return n.math('ABSOLUTE',x)
def div(n,a,b):return n.math('DIVIDE',a,b)
def mn(n,*xs):
 r=xs[0]
 for x in xs[1:]:r=n.math('MINIMUM',r,x)
 return r
def interval(n,x,a,b,f=.001):return n.mul(n.ramp(x,a-f,a),n.ramp(x,b+f,b))
def inp(n):
 p=n.node('ShaderNodeAttribute',attribute_name='FinishPosition').outputs['Vector']
 normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal').outputs['Vector']
 q=n.node('ShaderNodeAttribute',attribute_name='PartCoord').outputs['Vector']
 return p,*n.split(p),*n.split(normal),*n.split(q)
def box_edge(n,u,v,w,scale=.018):
 # The second-nearest box face is an EDGE. The nearest face is zero over
 # an entire planar side and would turn that whole side into noise wear.
 sizes=n.split(n.node('ShaderNodeAttribute',attribute_name='PartExtent').outputs['Vector'])
 dx=n.mul(mn(n,u,sub(n,1,u)),sizes[0]);dy=n.mul(mn(n,v,sub(n,1,v)),sizes[1]);dz=n.mul(mn(n,w,sub(n,1,w)),sizes[2])
 return n.mul(mn(n,n.maximum(dx,dy),n.maximum(dx,dz),n.maximum(dy,dz)),scale/.018)
def finish(n,base,rough,metal,h=0,wear=0,spec=.56,ao=1):
 n.channel('wear',wear);n.channel('specular_factor',spec);n.channel('micro_ao',ao)
 mat=n.finish(base,rough,metal,h,bump=1)
 n.feed(mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'],n.mul(spec,.5))
 return mat

def text(n,u,v,name):
 tex=n.node('ShaderNodeTexImage',extension='CLIP',interpolation='Linear')
 tex.image=bpy.data.images.load(str(BASE/'build/markings'/(name+'.png')),check_existing=True)
 tex.image.colorspace_settings.name='Non-Color';n.feed(tex.inputs['Vector'],n.combine(u,v,0))
 return tex.outputs['Color']
def outline_distance(n,y,z,points):
 result=1.
 for (a,b),(c,d) in zip(points,points[1:]+points[:1]):
  dy,dz=c-a,d-b;u=sub(n,y,a);v=sub(n,z,b)
  t=n.math('MULTIPLY_ADD',n.add(n.mul(u,dy),n.mul(v,dz)),1/(dy*dy+dz*dz))
  t=n.math('MINIMUM',n.math('MAXIMUM',t,0),1)
  q=sub(n,u,n.mul(t,dy));r=sub(n,v,n.mul(t,dz))
  result=mn(n,result,n.math('SQRT',n.add(n.mul(q,q),n.mul(r,r))))
 return result

def broken(n,p,distance,pressure=1):
 # Millimeter bites along a contact edge, with larger 7-20 mm paint islands.
 warp=n.node('ShaderNodeTexNoise');n.feed(warp.inputs['Vector'],p);warp.inputs['Scale'].default_value=170;warp.inputs['Detail'].default_value=2
 q=n.vec('ADD',p,n.vec('MULTIPLY',n.vec('SUBTRACT',warp.outputs['Color'],(.5,.5,.5)),(.002,.003,.0015)))
 fracture=n.add(n.mul(n.noise(q,135,2),.56),n.mul(n.noise(q,540,2),.32),n.mul(n.noise(q,1650,1),.12))
 threshold=n.add(.46,n.mul(n.maximum(distance,0),105),n.mul(sub(n,1,pressure),.17))
 return n.ramp(sub(n,fracture,threshold),-.018,.018)

def steel(name,part,key,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n);ax=ab(n,x)
 fine=n.noise(p,4200,2);grain=n.noise(p,1150,2)
 paint=key=='paint';bright=key=='steel'
 base=(.0015,.00154,.0015) if paint else ((.25,.26,.27) if bright else (.023,.024,.025))
 metal=0 if paint else 1;spec=.161 if paint else .56
 rough=n.add(.42 if paint else .42 if not bright else .42,n.mul(sub(n,grain,.5),.065))
 if part=='Magazine_Sheet':
  # The used ribbed magazine is gray-black oxide on steel, visibly lighter
  # than the receiver's enamel. Do not force the receiver paint BRDF onto it.
  base=(.029,.030,.029);metal=.75;spec=.56
  rough=n.add(.53,n.mul(sub(n,grain,.5),.055))
 h=n.mul(sub(n,fine,.5),2e-6 if not paint else 8e-6)
 edge=1.;pressure=1;flat=0;carbon=0;mark=0;microao=1
 if part in ('GasBlock_Neck','Bayonet_Lug','Sight_FrontTower'):
  # Fine forging skin is manufacture, not scattered wear. It survives as
  # shallow normal relief and roughness variation beneath the dark bluing.
  forge=n.noise(p,1750,2)
  h=n.add(h,n.mul(sub(n,forge,.5),.000050))
  rough=n.add(rough,n.mul(sub(n,forge,.5),.11))
 if part=='Receiver_Sheet':
  outer=n.ramp(n.mul(x,nx),.013,.016)
  # Exposed folded edges and well corners, with no broad flank damage.
  end=mn(n,ab(n,sub(n,y,-.034)),ab(n,sub(n,y,.219)))
  edge=n.maximum(mn(n,ab(n,sub(n,z,.051)),ab(n,sub(n,z,.0856)),end),sub(n,.016,ax))
  pressure=n.add(.30,n.mul(n.maximum(n.band(y,.192,.012,.018),n.band(y,-.022,.008,.020),n.band(y,.108,.008,.013)),.70))
  mark=n.mul(text(n,sub(n,1,div(n,sub(n,y,.008),.115)),div(n,sub(n,z,.062),.020),'receiver'),n.ramp(n.mul(nx,-1),.8,.98))
 elif part.startswith('Receiver_Rivet'):
  # Crown tops rub; sheltered roots remain enamel. Fractures break the cap.
  edge=n.mul(sub(n,1,n.ramp(ab(n,nx),.65,.97)),.004)
 elif part=='TopCover_Pressed':
  crest=mn(n,*[ab(n,sub(n,y,a)) for a in (-.005,.075,.150)])
  roof=n.maximum(crest,sub(n,.098,z),sub(n,.2,nz))
  bead=n.maximum(ab(n,sub(n,z,.0965)),sub(n,y,.092),sub(n,-.030,y),sub(n,.0178,ax))
  lip=n.maximum(ab(n,sub(n,z,.086)),sub(n,.0178,ax))
  edge=mn(n,roof,bead,lip);pressure=.85
 elif part.startswith(('TopCover_Rear','TopCover_Button','Cover_Return')):
  edge=box_edge(n,u,v,w);pressure=.65
 elif part=='Selector_Lever':
  pts=[(-.004,.062),(-.007,.070),(-.002,.077),(.008,.079),(.034,.081),(.054,.096),(.071,.098),(.152,.099),(.1605,.097),(.1605,.083),(.083,.077),(.032,.066),(.007,.060)]
  edge=outline_distance(n,y,z,pts);pressure=.95
 elif part.startswith('Selector_'):
  edge=box_edge(n,u,v,w,.015);pressure=.65
 elif part=='ChargingHandle':
  edge=box_edge(n,u,v,w,.010)
  flat=n.mul(n.ramp(x,.026,.033),n.ramp(nz,.05,.65),.80)
 elif part.startswith('Carrier_VisualRail'):
  flat=n.ramp(nz,.40,.90)
 elif part=='Carrier_PortCheek':
  edge=n.maximum(ab(n,sub(n,z,.0965)),sub(n,.013,x));flat=n.mul(n.ramp(nz,.4,.8),.65)
 elif part=='Magazine_Sheet':
  s=div(n,sub(n,.070,z),.87);center=n.add(.132,n.mul(s,s,1.65),n.mul(s,s,s,3))
  angle=n.math('ARCTANGENT',n.add(n.mul(s,3.3),n.mul(s,s,9)))
  vv=div(n,sub(n,y,center),n.math('COSINE',angle))
  ribs=mn(n,*[ab(n,sub(n,vv,a)) for a in (-.022,-.011,0,.011,.022)])
  edge=n.maximum(ribs,sub(n,.0125,ax),sub(n,s,.180),sub(n,.018,s))
  pressure=n.add(.35,n.mul(n.band(s,.11,.025,.040),.65))
 elif part.startswith(('Magazine_Floorplate','Magazine_FoldSpine','Magazine_FeedLip')):
  edge=box_edge(n,u,v,w,.012);pressure=.8
 elif part=='TriggerGuard_Stamping':
  edge=n.maximum(sub(n,.0058,ax),sub(n,z,.025));pressure=.55
 elif part=='Muzzle_SlantBrake':
  cutplane=n.add(.588,n.mul(sub(n,z,.085),.70),n.mul(x,.20))
  edge=ab(n,sub(n,y,cutplane))
  carbon=n.mul(n.ramp(sub(n,y,cutplane),-.007,-.001),n.maximum(n.ramp(ny,.1,.65),n.ramp(nz,.2,.9)),.95)
 elif part=='GasBlock_TubeSeat':
  radial=n.math('SQRT',n.add(n.mul(x,x),n.mul(sub(n,z,.107),sub(n,z,.107))))
  edge=n.maximum(mn(n,ab(n,sub(n,y,.345)),ab(n,sub(n,y,.417))),ab(n,sub(n,radial,.0095)))
 elif part.startswith('GasBlock'):
  edge=mn(n,ab(n,sub(n,y,.406)),n.maximum(ab(n,sub(n,z,.1155)),sub(n,ax,.008)))
  carbon=n.mul(n.band(y,.408,.002,.003),n.band(z,.106,.006,.003),n.ramp(ax,.006,.009),.80)
 elif part.startswith(('Sight_','Bayonet_','Handguard_Retainer','Handguard_Sling','Buttplate','Butt_Screw')):
  edge=box_edge(n,u,v,w,.018)
  pressure=.75
  if part=='Sight_TangentLeaf':
   mark=n.mul(text(n,div(n,n.add(x,.0067),.0134),div(n,sub(n,y,.188),.063),'leaf'),n.ramp(nz,.8,.98))
 # Worn conversion coating stays matte gray; rare steel glints are satin.
 chipped=n.mul(broken(n,p,edge,pressure),wear)
 rubbed=n.mul(flat,wear,broken(n,p,0,.95))
 rubbed=n.maximum(rubbed,chipped)
 if paint:
  base=n.mix(chipped,base,(.058,.055,.048),True);rough=n.mix(chipped,rough,.82);metal=n.mix(chipped,metal,.08);spec=n.mix(chipped,spec,.56)
  core=n.mul(chipped,n.ramp(edge,.00028,.00005),n.ramp(n.noise(p,330,2),.58,.72))
 else:core=rubbed
 base=n.mix(core,base,(.27,.28,.29),True);rough=n.mix(core,rough,.56 if paint else .46);metal=n.mix(core,metal,1)
 # Fine sparse carry scratches are pressure-gated, never a brushed field.
 scratches=n.mul(n.ramp(n.noise(n.vec('MULTIPLY',p,(2600,90,2600)),1,1),.76,.83),n.ramp(edge,.004,.0008),wear)
 h=n.add(h,n.mul(scratches,-.000012),n.mul(chipped,-.000016),n.mul(mark,-.00010))
 if part=='Sight_TangentLeaf':base=n.mix(mark,base,(.24,.25,.23),True);metal=n.mix(mark,metal,0);rough=n.mix(mark,rough,.62)
 else:base=n.mix(mark,base,(.010,.011,.010),True)
 carbon=n.mul(carbon,wear);base=n.mix(carbon,base,(.0011,.0010,.0009),True);rough=n.mix(carbon,rough,.86);metal=n.mix(carbon,metal,0);spec=n.mix(carbon,spec,.26)
 if part=='GasBlock_Neck':
  facing=n.ramp(ab(n,nx),.35,.78)
  vents=n.mul(n.maximum(*[n.ellipse(p,(.4085,a),(.00145,.00145),axes=(1,2)) for a in (.104,.1095)]),facing)
  outer=n.mul(n.maximum(*[n.ellipse(p,(.4085,a),(.00175,.00175),axes=(1,2)) for a in (.104,.1095)]),facing)
  lip=n.maximum(sub(n,outer,vents),0)
  base=n.mix(lip,base,(.052,.054,.053),True)
  h=n.add(h,n.mul(vents,-.00090));base=n.mix(vents,base,(.0011,.0010,.0009),True);rough=n.mix(vents,rough,.86)
  metal=n.mix(vents,metal,0);spec=n.mix(vents,spec,.26);microao=sub(n,1,n.mul(vents,.65))
  pins=n.maximum(*[n.ellipse(p,(a,.075),(.00145,.00145),axes=(1,2)) for a in (.433,.448)])
  outer=n.maximum(*[n.ellipse(p,(a,.075),(.00175,.00175),axes=(1,2)) for a in (.433,.448)])
  facing=n.ramp(ab(n,nx),.30,.70);seam=n.mul(n.maximum(sub(n,outer,pins),0),facing);pins=n.mul(pins,facing)
  h=n.add(h,n.mul(pins,.00012),n.mul(seam,-.00018))
  base=n.mix(n.mul(pins,.45),base,(.055,.057,.056),True);base=n.mix(seam,base,(.0035,.0037,.0035),True)
  microao=n.mul(microao,sub(n,1,n.mul(seam,.35)))
 if part=='Handguard_SlingMount':
  # The sling eye's pressed mounting plate has a low rivet crown. Its
  # submillimeter relief belongs in the normal, not extra game geometry.
  rivet=n.mul(n.ellipse(p,(.363,.0735),(.0017,.0017),axes=(1,2)),n.ramp(n.mul(nx,-1),.6,.95))
  h=n.add(h,n.mul(rivet,.00028))
 return finish(n,base,rough,metal,h,n.maximum(chipped,rubbed),spec,microao)

def wood(name,part,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
 stock=part=='Stock_Sculpt'
 # A real blank intersects growth layers; annual latewood and individual
 # vessels follow the fibers. Noise only bends the annual-layer phase.
 zz=sub(n,z,n.add(.040,n.mul(y,.10),n.mul(n.math('SINE',n.mul(y,26)),.0045))) if stock else sub(n,z,.073 if 'Lower' in part else .106)
 rx=n.add(x,.028);rz=n.add(n.mul(zz,.83),.038)
 radius=n.math('SQRT',n.add(n.mul(rx,rx),n.mul(rz,rz)))
 arch=n.mul(sub(n,y,-.16 if stock else .285),sub(n,y,-.16 if stock else .285),1.15 if stock else .90)
 phase=n.add(n.mul(n.add(radius,arch),math.tau/.0039),n.mul(n.math('SINE',n.add(n.mul(zz,145),n.mul(y,20))),.65),n.mul(sub(n,n.noise(n.combine(n.mul(x,95),n.mul(y,7),n.mul(zz,135)),1,2),.5),.65))
 year=n.math('FRACT',n.mul(phase,1/math.tau));late=n.ramp(year,.945,.995)
 tone=n.add(.51,n.mul(n.ramp(year,.08,.75),.085),n.mul(late,-.10),n.mul(n.math('SINE',n.mul(radius,550)),.035))
 base=n.mix(tone,(.020,.008,.0060),(.073,.039,.026),True)
 pores=n.node('ShaderNodeTexVoronoi',feature='F1',distance='EUCLIDEAN')
 n.feed(pores.inputs['Vector'],n.combine(n.mul(x,680),n.mul(y,140),n.mul(zz,780)));pores.inputs['Scale'].default_value=1
 pore=n.ramp(pores.outputs['Distance'],.28,.10)
 base=n.mix(n.mul(pore,.46),base,(.010,.0032,.0016),True)
 h=n.add(n.mul(late,-.000010),n.mul(pore,-.000026));rough=n.add(.32,n.mul(late,.045),n.mul(pore,.1))
 # The hand wraps the compound surface. Its longitudinal contact shifts
 # with height and side; normal orientation protects the sheltered return.
 # A continuous pressure field has neither an oval stencil nor a straight
 # band boundary. Film loss grades through many millimeters of that field.
 center=n.add(-.073 if stock else .286,n.mul(sub(n,z,.065 if stock else .076),.40),n.mul(x,.32),n.mul(n.math('SINE',n.mul(z,130)),.004))
 distance=div(n,sub(n,y,center),.050 if stock else .066)
 pressure=n.maximum(sub(n,1,n.mul(distance,distance)),0)
 orientation=n.maximum(n.ramp(ab(n,nx),.15,.90),n.mul(n.ramp(n.mul(nz,-1 if not stock and 'Lower' in part else 1),.05,.80),.80))
 pressure=n.mul(pressure,pressure,orientation)
 # Pressure fades with the compound surface, then the coating breaks into
 # merged rubbed fields with surviving varnish islands. No axial band.
 fracture=n.add(n.mul(n.noise(p,190,2),.75),n.mul(n.noise(p,800,2),.25))
 # Coating loss follows continuous contact pressure. Fracture perturbs only
 # the transition, leaving a rubbed core and surviving varnish farther away.
 loss=n.mul(n.math('POWER',pressure,1.25),n.add(.88,n.mul(fracture,.24)),wear,.45 if 'Upper' in part else .88)
 base=n.mix(loss,base,n.mix(tone,(.033,.024,.016),(.077,.065,.040),True),True)
 rough=n.mix(loss,rough,.65);h=n.add(h,n.mul(loss,-.000025))
 # Hand oil darkens the raw fibers slightly but does not draw a stripe.
 base=n.mix(n.mul(pressure,wear,.11),base,(.025,.006,.002),True)
 dentmask=0
 sites=([(-.276,-.003,.006,.003),(-.272,.079,.005,.003),(-.259,.002,.0035,.0018),(-.250,.079,.004,.0016),(-.264,.023,.0028,.0013)] if stock else [(.245,.053,.004,.0017),(.341,.055,.003,.0016)])
 for cy,cz,dy,dz in sites:
  a=n.add(div(n,sub(n,y,cy),dy),n.mul(div(n,sub(n,z,cz),dz),.35));b=div(n,sub(n,z,cz),dz)
  radius=n.add(n.math('POWER',ab(n,a),2.6),n.math('POWER',ab(n,b),1.4))
  bowl=n.maximum(sub(n,1,radius),0);dent=n.mul(bowl,bowl,wear,n.ramp(ab(n,nx),.15,.8))
  lip=n.mul(n.band(radius,.90,.08,.15),n.ramp(b,.1,.8),wear)
  h=n.add(h,n.mul(dent,-.00040),n.mul(lip,.000035));rough=n.mix(n.maximum(dent,lip),rough,.71)
  base=n.mix(n.mul(dent,.75),base,(.026,.006,.0022),True);base=n.mix(n.mul(lip,.80),base,(.22,.105,.036),True)
  dentmask=n.maximum(dentmask,dent,lip)
 return finish(n,base,rough,0,h,n.maximum(loss,dentmask),.66)

def grip(name,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
 filler=n.noise(n.vec('MULTIPLY',p,(340,120,220)),1,3)
 base=n.mix(filler,(.020,.0045,.0035),(.072,.017,.0135),True)
 fine=n.noise(p,4000,2);h=n.mul(sub(n,fine,.5),3e-6)
 touch=n.mul(interval(n,z,-.035,.050,.010),n.maximum(n.ramp(ab(n,ny),.4,.9),n.mul(n.ramp(ab(n,nx),.8,.98),.45)),wear)
 rough=n.mix(touch,n.add(.43,n.mul(sub(n,fine,.5),.055)),.29)
 base=n.mix(n.mul(touch,.14),base,(.14,.045,.014),True)
 return finish(n,base,rough,0,h,touch,.64)

def ammo(name,key,fired):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
 q=n.node('ShaderNodeAttribute',attribute_name='AmmoPosition').outputs['Vector'];a,b,c=n.split(q)
 fine=n.noise(q,6000,2);tool=n.noise(n.vec('MULTIPLY',q,(2600,45,2600)),1,2)
 if key=='copper':return finish(n,(.39,.166,.055),n.add(.48,n.mul(tool,.08)),1,n.mul(sub(n,fine,.5),2e-6))
 base=(.043,.024,.0075);rough=n.add(.54,n.mul(sub(n,tool,.5),.08));metal=.12
 r=n.math('SQRT',n.add(n.mul(a,a),n.mul(c,c)))
 head=n.ramp(ny,-.60,-.96);rim=n.mul(head,n.ramp(r,.0046,.00545))
 stamp=n.mul(text(n,n.add(.5,div(n,a,.0098)),n.add(.5,div(n,c,.0098)),'headstamp'),head)
 primer=n.mul(head,n.ramp(r,.0021,.0018));seal=n.mul(head,n.band(r,.00205,.00010,.00006))
 base=n.mix(rim,base,(.22,.23,.22),True);base=n.mix(primer,base,(.18,.17,.12),True);base=n.mix(seal,base,(.10,.005,.002),True)
 metal=n.mix(n.maximum(rim,primer),metal,1)
 soot=n.ramp(b,.034,.0385) if fired else 0
 base=n.mix(soot,base,(.010,.009,.004),True);rough=n.mix(soot,rough,.78)
 h=n.add(n.mul(sub(n,fine,.5),1e-6),n.mul(stamp,-.00006),n.mul(seal,-.00004))
 return finish(n,base,rough,metal,h)

def assign(wear):
 from build import HEADS
 records={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
  part=ob.get('finish_part',ob.name);shift=Vector((.4 if ob.name=='Cartridge_Proof' else .5 if ob.name=='Case_Proof' else 0,0,0))
  # Finalization recenters static proof meshes on their object origins.
  # Attribute coordinates must include that object transform before removing
  # the atlas staging translation, or the primer/stamp evaluates 400 mm away.
  vertices=[ob.matrix_world@v.co-shift for v in ob.data.vertices]
  lo=Vector([min(v[k] for v in vertices) for k in range(3)]);hi=Vector([max(v[k] for v in vertices) for k in range(3)])
  center=Vector(tuple(v*.001 for v in HEADS.get(ob.get('bone'),(0,0,0)))) if ob.get('bone') in ('TopRound','SecondRound','ThirdRound','ChamberRound','EjectedCase') else Vector((0,0,0))
  normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
  fields=[('FinishPosition',vertices,'POINT'),('FinishNormal',[(normal_matrix@row.vector).normalized() for row in ob.data.corner_normals],'CORNER'),('PartCoord',[Vector([(v[k]-lo[k])/max(hi[k]-lo[k],1e-8) for k in range(3)]) for v in vertices],'POINT'),('PartExtent',[hi-lo for v in vertices],'POINT'),('AmmoPosition',[v-center for v in vertices],'POINT')]
  for attr,values,domain in fields:
   old=ob.data.attributes.get(attr)
   if old:ob.data.attributes.remove(old)
   field=ob.data.attributes.new(attr,'FLOAT_VECTOR',domain);field.data.foreach_set('vector',[a for v in values for a in v])
  roles=[]
  for i,old in enumerate(list(ob.data.materials)):
   key=old.name.removeprefix('Inspection_').split('.')[0];name='R39_'+part+'_'+str(i)
   if part.startswith(('TriggerGuard_','Guard_')):key='paint'
   # Boolean cutting tools carried an inspection-paint slot onto a few
   # machined interiors. Their final finish belongs to the manufactured part.
   if part.startswith(('Sight_','GasBlock_','Bayonet_','Barrel','Muzzle_')):key='blue'
   if key=='wood':mat=wood(name,part,wear)
   elif key=='grip':mat=grip(name,wear)
   elif key in ('case','copper'):mat=ammo(name,key,'Case_Proof'==part or part.startswith('EjectedCase'))
   else:mat=steel(name,part,key,wear)
   ob.data.materials[i]=mat;roles.append(key)
  if part in ('Cartridge_Proof','Case_Proof'):
   assert max(abs(v.x) for v in vertices)<.006 and max(abs(v.z) for v in vertices)<.006
   assert abs(min(v.y for v in vertices))<1e-6
   assert abs(max(v.y for v in vertices)-(.0558 if part=='Cartridge_Proof' else .0386))<1e-6
  records[ob.name]=dict(part=part,roles=roles)
 bpy.context.scene['finish_wear']=wear;return records
