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
def section_value(n,coordinate,stations):
 """Piecewise linear construction datum used only to locate edge abrasion."""
 value=stations[0][1]
 for (a,va),(b,vb) in zip(stations,stations[1:]):
  t=n.math('MINIMUM',n.math('MAXIMUM',div(n,sub(n,coordinate,a),b-a),0),1)
  value=n.add(value,n.mul(t,vb-va))
 return value
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

def rub(n,p,distance,along,start,end,width,fade=.006):
 """Continuous contact stroke with ragged margins and tapered ends.

 Millimeter variation changes its width; it cannot punch periodic holes
 through the core. Sheltered edges have no stroke and receive no abrasion.
 """
 contour=n.mul(sub(n,n.noise(p,680,2),.5),width*.40)
 widthfield=n.mul(width,n.add(.30,n.mul(n.noise(p,105,2),1.35)))
 cross=n.ramp(div(n,n.add(distance,contour),widthfield),1,.84)
 return n.mul(cross,interval(n,along,start,end,fade))

def metal_rubs(n,p,x,y,z,nx,ny,nz,u,v,w,part):
 """Named exposed sites, rather than a generic every-edge chip field."""
 ax=ab(n,x);mask=0;sharp=1.
 outer=n.ramp(ax,.0145,.0167)
 if part=='Receiver_Sheet':
  # Magazine entry and lower front corners: connected rubs, black elsewhere.
  lower=ab(n,sub(n,z,.0525))
  front=rub(n,p,lower,y,.176,.216,.0038,.009)
  well=rub(n,p,lower,y,.098,.127,.0019,.006)
  corner=rub(n,p,ab(n,sub(n,y,.2194)),z,.051,.061,.0022,.004)
  mask=n.mul(n.maximum(front,well,corner),outer)
  sharp=mn(n,lower,ab(n,sub(n,y,.2194)))
 elif part.startswith('Receiver_Rivet') and part.endswith('_2'):
  # Only the exposed lower front crown, not all twelve rivets.
  mask=n.mul(n.ramp(ab(n,nx),.76,.98),n.ramp(nz,.10,.7),.65)
  sharp=.0004
 elif part=='TopCover_Pressed':
  bead=rub(n,p,ab(n,sub(n,z,.0965)),y,-.023,.047,.0027,.013)
  bead=n.mul(bead,n.ramp(ax,.0175,.0183))
  rear=rub(n,p,ab(n,sub(n,y,-.0325)),x,-.016,.009,.0023,.004)
  rear=n.mul(rear,n.ramp(z,.091,.099))
  # One rear roof crest takes the hand; one shorter mid crest takes the sling.
  rib1=rub(n,p,ab(n,sub(n,y,-.005)),x,-.016,-.007,.0017,.003)
  rib2=rub(n,p,ab(n,sub(n,y,.075)),x,-.012,-.002,.0011,.004)
  roof=n.mul(n.maximum(rib1,rib2),n.ramp(nz,.25,.8))
  mask=n.maximum(bead,rear,roof)
  sharp=mn(n,ab(n,sub(n,z,.0965)),ab(n,sub(n,y,-.005)),ab(n,sub(n,y,.075)))
 elif part=='TopCover_RearCap':
  mask=rub(n,p,box_edge(n,u,v,w),z,.092,.108,.0012,.003)
  sharp=box_edge(n,u,v,w)
 elif part=='TriggerGuard_Stamping':
  sharp=ab(n,sub(n,z,.016))
  mask=n.mul(rub(n,p,sharp,y,.023,.055,.0014,.008),n.ramp(ax,.0057,.0064))
 elif part=='Selector_Lever':
  points=[(-.004,.062),(-.007,.070),(-.002,.077),(.008,.079),(.034,.081),(.054,.096),(.071,.098),(.152,.099),(.1605,.097),(.1605,.083),(.083,.077),(.032,.066),(.007,.060)]
  sharp=outline_distance(n,y,z,points)
  mask=rub(n,p,sharp,y,.105,.160,.00065,.011)
 elif part=='Selector_ThumbFold':
  sharp=box_edge(n,u,v,w)
  mask=n.mul(rub(n,p,sharp,y,.150,.157,.0010,.004),n.ramp(x,.023,.026))
 elif part=='ChargingHandle':
  sharp=box_edge(n,u,v,w)
  mask=n.mul(n.ramp(x,.025,.032),n.ramp(nz,.05,.6),.8)
 elif part.startswith('Carrier_VisualRail'):
  mask=n.ramp(nz,.4,.9);sharp=.001
 elif part=='Carrier_PortCheek':
  sharp=ab(n,sub(n,z,.0965));mask=n.mul(rub(n,p,sharp,y,.090,.156,.00065,.006),n.ramp(x,.013,.016))
 elif part=='Magazine_Sheet':
  # Inverse of the authored sweep: axial S and transverse V are stable
  # attributes. Using world Z alone makes diagonal scratches on curved ribs.
  mx,mv,ms=n.split(n.node('ShaderNodeAttribute',attribute_name='MagazineCoord').outputs['Vector'])
  width=.00090
  a=rub(n,p,ab(n,sub(n,mv,-.022)),ms,.047,.145,width,.018)
  b=rub(n,p,ab(n,mv),ms,.070,.168,.00068,.022)
  c=rub(n,p,ab(n,sub(n,mv,.022)),ms,.119,.179,.00075,.016)
  mask=n.mul(n.maximum(a,b,c),n.ramp(ax,.01325,.01385))
  sharp=mn(n,ab(n,sub(n,mv,-.022)),ab(n,mv),ab(n,sub(n,mv,.022)))
 elif part.startswith('Magazine_FoldSpine'):
  mx,mv,ms=n.split(n.node('ShaderNodeAttribute',attribute_name='MagazineCoord').outputs['Vector'])
  mask=n.mul(interval(n,ms,.036,.172,.021),n.ramp(ab(n,ny),.15,.65))
  sharp=.0006
 elif part=='Magazine_Floorplate':
  sharp=box_edge(n,u,v,w)
  mask=n.mul(rub(n,p,sharp,v,.15,.64,.00095,.12),n.ramp(ax,.010,.013))
 elif part.startswith('Magazine_FeedLip'):
  sharp=box_edge(n,u,v,w);mask=n.mul(n.ramp(nz,.6,.97),.55)
 elif part=='GasBlock_Neck':
  # Smooth gray friction on the collar rims. The diagonal web stays blued.
  a=rub(n,p,ab(n,sub(n,y,.4062)),x,-.009,.006,.00065,.004)
  b=rub(n,p,ab(n,sub(n,y,.4507)),z,.078,.093,.00055,.003)
  mask=n.maximum(n.mul(a,n.ramp(z,.110,.116)),n.mul(b,n.ramp(ax,.009,.011)))
  sharp=1.
 elif part=='GasBlock_TubeSeat':
  sharp=ab(n,sub(n,y,.3455))
  mask=n.mul(rub(n,p,sharp,x,-.008,.004,.00055,.004),n.ramp(nz,.25,.80))
 elif part=='Muzzle_SlantBrake':
  cut=n.add(.588,n.mul(sub(n,z,.085),.70),n.mul(x,.20));sharp=ab(n,sub(n,y,cut))
  mask=n.mul(rub(n,p,sharp,x,-.007,.005,.00050,.003),n.ramp(nz,.15,.8))
 elif part in ('Sight_FrontHood','Sight_RearNotch','Sight_SliderButton-1','Sight_SliderButton1'):
  sharp=box_edge(n,u,v,w)
  mask=n.mul(rub(n,p,sharp,v,.13,.5,.00028,.10),n.ramp(nz,.1,.8))
 elif part in ('Buttplate','Handguard_Retainer363'):
  sharp=box_edge(n,u,v,w)
  mask=n.mul(rub(n,p,sharp,w,.14,.34,.00055,.12),n.ramp(ab(n,nx),.25,.80))
 # Bright steel is a tiny high-point subset, never the whole rubbed band.
 core=n.mul(mask,n.ramp(sharp,.00022,.000045),n.ramp(n.noise(p,180,2),.58,.75))
 return mask,core

def steel(name,part,key,wear,metal_wear=1):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n);ax=ab(n,x)
 fine=n.noise(p,4200,2);grain=n.noise(p,1150,2)
 paint=key=='paint' and part!='Magazine_Sheet';bright=key=='steel'
 base=(.022,.023,.024) if paint else ((.25,.26,.27) if bright else (.023,.024,.025))
 metal=0 if paint else 1;spec=.8 if paint else .56
 rough=n.add(.42 if paint else .42 if not bright else .42,n.mul(sub(n,grain,.5),.065))
 if part=='Magazine_Sheet':
  # The used ribbed magazine is gray-black oxide on steel, visibly lighter
  # than the receiver's enamel. Do not force the receiver paint BRDF onto it.
  base=(.029,.030,.029);metal=.75;spec=.56
  rough=n.add(.53,n.mul(sub(n,grain,.5),.055))
 h=n.mul(sub(n,fine,.5),2e-6 if not paint else 8e-6)
 carbon=0;mark=0;microao=1
 if part in ('GasBlock_Neck','Bayonet_Lug','Sight_FrontTower'):
  # Fine forging skin is manufacture, not scattered wear. It survives as
  # shallow normal relief and roughness variation beneath the dark bluing.
  forge=n.noise(p,1750,2)
  h=n.add(h,n.mul(sub(n,forge,.5),.000050))
  rough=n.add(rough,n.mul(sub(n,forge,.5),.11))
 if part=='Receiver_Sheet':
  mark=n.mul(text(n,sub(n,1,div(n,sub(n,y,.008),.115)),div(n,sub(n,z,.062),.020),'receiver'),n.ramp(n.mul(nx,-1),.8,.98))
 elif part=='Sight_TangentLeaf':
  mark=n.mul(text(n,div(n,n.add(x,.0067),.0134),div(n,sub(n,y,.188),.063),'leaf'),n.ramp(nz,.8,.98))
 elif part=='Muzzle_SlantBrake':
  cutplane=n.add(.588,n.mul(sub(n,z,.085),.70),n.mul(x,.20))
  carbon=n.mul(n.ramp(sub(n,y,cutplane),-.007,-.001),n.maximum(n.ramp(ny,.1,.65),n.ramp(nz,.2,.9)),.95)
 elif part.startswith('GasBlock'):
  carbon=n.mul(n.band(y,.408,.002,.003),n.band(z,.106,.006,.003),n.ramp(ax,.006,.009),.80)
 # Continuous, cause-located abrasion supersedes all generic edge chips.
 chipped,core=metal_rubs(n,p,x,y,z,nx,ny,nz,u,v,w,part)
 chipped=n.mul(chipped,wear*metal_wear);core=n.mul(core,wear*metal_wear);rubbed=chipped
 if paint:
  base=n.mix(chipped,base,(.110,.108,.101),True);rough=n.mix(chipped,rough,.88)
  metal=n.mix(chipped,metal,.08);spec=n.mix(chipped,spec,.56)
 elif part.startswith(('Magazine_Sheet','Magazine_FoldSpine','Magazine_Floorplate','Magazine_FeedLip')):
  # Pouch contact exposes matte conversion-coated gray before the small
  # metallic crest. Diffuse value AND gloss identify it at whole-gun scale.
  base=n.mix(chipped,base,(.180,.176,.165),True);rough=n.mix(chipped,rough,.86)
  metal=n.mix(chipped,metal,.08);spec=n.mix(chipped,spec,.56)
 else:
  # Friction thins the dark oxide smoothly, leaving a warm gray steel land.
  base=n.mix(chipped,base,(.118,.115,.108),True);rough=n.mix(chipped,rough,.54)
  metal=n.mix(chipped,metal,1)
 base=n.mix(core,base,(.235,.232,.220),True);rough=n.mix(core,rough,.56);metal=n.mix(core,metal,1)
 # Fine sparse carry scratches are pressure-gated, never a brushed field.
 scratches=n.mul(n.ramp(n.noise(n.vec('MULTIPLY',p,(2600,90,2600)),1,1),.76,.83),chipped,wear)
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
 if part=='Handguard_Retainer363':
  radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(sub(n,z,.085),sub(n,z,.085))))
  rim=n.mul(n.band(radius,.00953,.00030,.00055),n.ramp(ny,.85,.99),n.ramp(y,.367,.368))
  h=n.add(h,n.mul(rim,.000045))
 if part=='Handguard_SlingMount':
  # The sling eye's pressed mounting plate has a low rivet crown. Its
  # submillimeter relief belongs in the normal, not extra game geometry.
  rivet=n.mul(n.ellipse(p,(.363,.0735),(.0017,.0017),axes=(1,2)),n.ramp(n.mul(nx,-1),.6,.95))
  h=n.add(h,n.mul(rivet,.00028))
 return finish(n,base,rough,metal,h,n.maximum(chipped,rubbed),spec,microao)

def wood(name,part,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz,u,v,w=inp(n)
 stock=part=='Stock_Sculpt';upper='Upper' in part
 # Growth layers intersect the carved blank, with slow longitudinal drift.
 # Broad earlywood/latewood figure is 2-6 mm across, safely above a 2K texel.
 # Fine individual vessels are separate; they do not stand in for figure.
 zz=sub(n,z,n.add(.040,n.mul(y,.085))) if stock else sub(n,z,.073 if not upper else .106)
 rx=n.add(x,.028 if stock else .024);rz=n.add(n.mul(zz,.83),.038)
 radius=n.math('SQRT',n.add(n.mul(rx,rx),n.mul(rz,rz)))
 yy=sub(n,y,-.16 if stock else .285)
 arch=n.mul(yy,yy,.35 if stock else 2.5)
 wander=n.add(n.mul(n.math('SINE',n.add(n.mul(zz,125),n.mul(y,13))),.00048),n.mul(sub(n,n.noise(n.combine(n.mul(x,90),n.mul(y,11),n.mul(zz,110)),1,2),.5),.0026))
 layer=n.add(radius,arch,wander)
 phase=n.add(n.mul(layer,1/.0047),n.mul(n.math('SINE',n.mul(radius,720)),.38),n.mul(n.math('SINE',n.mul(radius,1730)),.20))
 year=n.math('FRACT',phase)
 late=n.ramp(year,.79,.96)
 contrast=n.add(.42,n.mul(n.noise(n.combine(n.mul(x,65),n.mul(y,19),n.mul(zz,190)),1,2),.58))
 tone=n.add(.49,n.mul(n.add(-.20,n.mul(n.ramp(year,.06,.65),.40),n.mul(late,-.42)),n.mul(contrast,.75)))
 figure=n.noise(n.combine(n.mul(x,85),n.mul(y,8),n.mul(zz,130)),1,2)
 tone=n.add(tone,n.mul(sub(n,figure,.5),.30))
 # Slow stain absorption follows curved growth structure in the blank.
 # 20-80 mm zones carry the larger figure; the accepted 2-6 mm layers
 # and vessels remain subordinate detail, rather than the entire variation.
 broad=n.noise(n.combine(n.mul(x,34),n.add(n.mul(y,8),2.7 if stock else 6.2 if upper else 11.4),n.mul(zz,42)),1,1)
 tone=n.add(tone,n.mul(sub(n,broad,.5),.45 if stock else 1.10 if upper else 1.05))
 # Wide heartwood/earlywood bands accept different amounts of stain. Their
 # section follows the same curved blank as the accepted fine layers.
 heart_phase=n.channel('growth_phase',0.0 if stock else 5.15 if upper else 4.712389)
 heart_strength=n.channel('growth_strength',.30 if stock else .50 if upper else .55)
 heart=n.math('SINE',n.add(n.mul(layer,math.tau/(.14 if stock else .060 if upper else .100)),n.mul(sub(n,broad,.5),2.5),heart_phase))
 tone=n.add(tone,n.mul(heart,heart_strength))
 if stock:low,high=(.0138,.0078,.0058),(.0805,.0495,.0368)
 elif upper:low,high=(.008,.0034,.0025),(.054,.024,.015)
 else:low,high=(.028,.013,.0095),(.180,.081,.057)
 base=n.mix(tone,low,high,True)
 # Retain the handed-off per-blank hero palette after changing the broad
 # absorption distribution. These are uniform stain corrections, not wear.
 if upper:base=n.vec('MULTIPLY',base,(1.16,1.16,1.18))
 elif not stock:base=n.vec('MULTIPLY',base,(.96,.970,.997))
 pores=n.node('ShaderNodeTexVoronoi',feature='F1',distance='EUCLIDEAN')
 n.feed(pores.inputs['Vector'],n.combine(n.mul(x,1000),n.mul(y,125),n.mul(zz,1250)));pores.inputs['Scale'].default_value=1
 pore=n.ramp(pores.outputs['Distance'],.23,.09)
 base=n.mix(n.mul(pore,.43),base,(.008,.003,.0018),True)
 h=n.add(n.mul(late,-.000012),n.mul(pore,-.000030))
 rough=n.add(.52 if upper else .40,n.mul(late,.035),n.mul(pore,.06))
 # Oil-darkened dust accumulates at the receiver/wood junction and wrist,
 # under the comb and at the sheltered rear handguard roots. Contact and
 # recess distance locate it; slow porosity variation only breaks its edge.
 if stock:
  root=n.ramp(y,-.130,-.043)
  wrist=n.mul(root,n.maximum(n.band(z,.052,.013,.014),n.mul(n.band(z,.079,.003,.006),.55)))
  cheek=n.mul(n.ramp(z,.052,.076),interval(n,y,-.253,-.105,.023),.55)
  grime=n.mul(n.maximum(wrist,cheek),n.add(.65,n.mul(broad,.35)),wear)
 else:
  root=n.ramp(y,.278 if upper else .260,.245 if upper else .221)
  recess=n.ramp(z,.101 if upper else .044,.093 if upper else .068)
  grime=n.mul(n.maximum(n.mul(root,.65),n.mul(recess,.85)),n.add(.50,n.mul(broad,.50)),wear)
 base=n.mix(grime,base,n.vec('MULTIPLY',base,(.32,.30,.27)),True)
 rough=n.mix(grime,rough,.56)
 # Only flaked streaks inside actual hand-contact margins lose their film.
 # No graded pale field covers the wrist or handguard's broad flat side.
 if stock:
  bottom=n.add(.039,n.mul(sub(n,y,-.062),.12))
  contact=n.maximum(n.mul(n.band(z,bottom,.0020,.0030),interval(n,y,-.112,-.043,.011)),n.mul(n.band(z,.0845,.0012,.0023),interval(n,y,-.104,-.058,.009),.70))
  edgeknocks=n.maximum(n.mul(n.band(z,.080,.0015,.0020),interval(n,y,-.279,-.249,.005)),n.mul(n.band(z,n.add(-.010,n.mul(sub(n,y,-.250),.40)),.002,.002),interval(n,y,-.276,-.211,.010)))
  # Toe/heel and comb are exposed, with handling strongest at the wrist.
  comb=n.mul(n.band(z,.084,.0022,.0030),interval(n,y,-.274,-.051,.010))
  heeltoe=n.mul(n.ramp(y,-.245,-.280),n.maximum(n.ramp(z,.065,.080),n.ramp(z,.014,-.003)))
  contact=n.maximum(contact,n.mul(edgeknocks,.8))
  toe_line=section_value(n,y,[(-.282,-.013),(-.250,-.010),(-.210,.001),(-.170,.014),(-.135,.025),(-.108,.032),(-.088,.035),(-.062,.039),(-.035,.041)])
  toe_rub=n.mul(n.band(z,toe_line,.006,.005),interval(n,y,-.278,-.205,.018))
  exposed=n.maximum(n.mul(comb,.92),heeltoe,edgeknocks,toe_rub)
 else:
  contact=n.mul(interval(n,y,.251 if upper else .244,.330 if upper else .346,.012),n.maximum(n.band(z,.093 if upper else .058,.0022,.0035),n.mul(n.band(z,.111 if upper else .077,.0014,.0025),.66)))
  # Lower outside belly and the front lip take knocks and supporting hands.
  front=n.mul(n.ramp(y,.331 if upper else .347,.344 if upper else .362),n.ramp(ab(n,nx),.28,.75))
  belly=n.mul(n.ramp(z,.099 if upper else .065,.092 if upper else .050),interval(n,y,.253,.336,.015),n.ramp(ab(n,nx),.25,.65))
  exposed=n.maximum(front,belly)
 # Long fragments follow fibers; small noise roughens flaked boundaries only.
 flakes=n.add(n.mul(n.noise(n.combine(n.mul(x,650),n.mul(y,85),n.mul(z,730)),1,2),.72),n.mul(n.noise(p,1400,1),.28))
 outside=n.maximum(n.ramp(n.mul(x,nx),.004,.009),n.ramp(n.mul(sub(n,z,.065 if stock else .091 if upper else .084),nz),.010,.020))
 original_loss=n.mul(n.ramp(contact,.35,.85),n.ramp(flakes,.50,.59),outside,wear)
 # Edge impacts break film into irregular flakes, not parallel fiber strokes.
 # The existing exposure field keeps the sites and their fading end margins;
 # near-isotropic 5-8 mm fragments and smaller chips break only its boundary.
 # Keep the accepted smaller hand-contact flakes unchanged.
 edgefield=n.noise(n.combine(n.mul(x,170),n.mul(y,130),n.mul(z,180)),1,2)
 chips=n.noise(p,620,2)
 edgeflakes=n.ramp(n.add(n.mul(edgefield,.78),n.mul(chips,.22)),.43,.55)
 edge_loss=n.mul(n.ramp(exposed,.35,.85),edgeflakes,outside,wear)
 loss=n.maximum(original_loss,edge_loss)
 # Exposed fibers are the SAME stained wood, slightly lighter/less red.
 raw=n.vec('MULTIPLY',base,(1.08,1.20,1.25))
 raw_edge=n.vec('MULTIPLY',base,(1.45,1.60,1.65))
 base=n.mix(original_loss,base,raw,True)
 base=n.mix(edge_loss,base,raw_edge,True);rough=n.mix(loss,rough,.70);h=n.add(h,n.mul(loss,-.000026))
 # Dents are crushed depressions with dark bottoms. No orange crescent lips.
 dentmask=0
 sites=([(-.276,-.003,.006,.003),(-.272,.079,.005,.003),(-.259,.002,.0035,.0018),(-.250,.079,.004,.0016),(-.264,.023,.0028,.0013)] if stock else [(.245,.053,.004,.0017),(.341,.055,.003,.0016)])
 for cy,cz,dy,dz in sites:
  a=n.add(div(n,sub(n,y,cy),dy),n.mul(div(n,sub(n,z,cz),dz),.35));b=div(n,sub(n,z,cz),dz)
  radius=n.add(n.math('POWER',ab(n,a),2.6),n.math('POWER',ab(n,b),1.4))
  bowl=n.maximum(sub(n,1,radius),0);dent=n.mul(bowl,bowl,wear,n.ramp(ab(n,nx),.15,.8))
  lip=n.mul(n.band(radius,.90,.08,.15),n.ramp(b,.1,.8),wear,n.ramp(ab(n,nx),.15,.8))
  h=n.add(h,n.mul(dent,-.00055),n.mul(lip,.000020));rough=n.mix(n.maximum(dent,lip),rough,.71)
  base=n.mix(n.mul(dent,.70),base,n.vec('MULTIPLY',base,(.38,.38,.38)),True)
  dentmask=n.maximum(dentmask,dent,lip)
 n.channel('varnish_loss',loss);n.channel('grain',tone)
 return finish(n,base,rough,0,h,n.maximum(loss,dentmask),.10 if upper else .28)

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

def assign(wear,metal_wear=1):
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
  if part.startswith('Magazine_') and ob.get('bone') in ('Magazine','Follower'):
   coords=[]
   for point in vertices:
    a,b=-.04,.24
    for _ in range(24):
     t=(a+b)/2;center=.132+1.65*t*t+3*t*t*t;slope=3.3*t+9*t*t
     error=point.z-.070+.87*t-(point.y-center)*slope
     if error>0:b=t
     else:a=t
    t=(a+b)/2;center=.132+1.65*t*t+3*t*t*t
    cross=(point.y-center)/math.cos(math.atan(3.3*t+9*t*t))
    coords.append((point.x,cross,t))
   field=ob.data.attributes.new('MagazineCoord','FLOAT_VECTOR','POINT')
   field.data.foreach_set('vector',[a for row in coords for a in row])
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
   else:mat=steel(name,part,key,wear,metal_wear)
   ob.data.materials[i]=mat;roles.append(key)
  if part in ('Cartridge_Proof','Case_Proof'):
   assert max(abs(v.x) for v in vertices)<.006 and max(abs(v.z) for v in vertices)<.006
   assert abs(min(v.y for v in vertices))<1e-6
   assert abs(max(v.y for v in vertices)-(.0558 if part=='Cartridge_Proof' else .0386))<1e-6
  records[ob.name]=dict(part=part,roles=roles)
 bpy.context.scene['finish_wear']=wear;return records
