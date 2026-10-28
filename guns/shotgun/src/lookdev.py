"""Original bluing, carved walnut, rubber and ammunition, in explicit rest frames.

Only analytic manufacturing/handling fields and our own lettering enter these
nodes. No photographic pixels enter a material or texture. Meter-scale masks
survive rigid-bone isolation and consolidation through mesh attributes.
"""
import math,sys
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.materials import Nodes

def sub(n,a,b):return n.math('SUBTRACT',a,b)
def ab(n,a):return n.math('ABSOLUTE',a)
def mn(n,*values):
 r=values[0]
 for v in values[1:]:r=n.math('MINIMUM',r,v)
 return r
def ramp(n,x,a,b):return n.ramp(n.math('DIVIDE',sub(n,x,a),sub(n,b,a)),0,1)
def interval(n,x,a,b,f=.0005):return n.mul(ramp(n,x,sub(n,a,f),a),ramp(n,x,n.add(b,f),b))
def inp(n):
 p=n.node('ShaderNodeAttribute',attribute_name='FinishPosition').outputs['Vector']
 normal=n.node('ShaderNodeAttribute',attribute_name='FinishNormal').outputs['Vector']
 x,y,z=n.split(p);nx,ny,nz=n.split(normal)
 return p,x,y,z,nx,ny,nz
def finish(n,base,rough,metal,height=0,ao=1):
 n.channel('micro_ao',ao)
 mat=n.finish(base,rough,metal,height,bump=1)
 mat.node_tree.nodes['SURFACE'].inputs['Specular IOR Level'].default_value=.33
 return mat
def text(n,u,v,name):
 tex=n.node('ShaderNodeTexImage',extension='CLIP',interpolation='Cubic')
 tex.image=bpy.data.images.load(str(BASE/'build/markings'/(name+'.png')),check_existing=True)
 tex.image.colorspace_settings.name='Non-Color';n.feed(tex.inputs['Vector'],n.combine(u,v,0))
 return tex.outputs['Color']
def engraved(n,x,y,z,nx):
 marks=[]
 for side,name in [(-1,'receiver-left'),(1,'receiver-right')]:
  u=n.math('DIVIDE',sub(n,y,.067),.105)
  if side<0:u=sub(n,1,u)
  v=n.math('DIVIDE',sub(n,z,.020),.019)
  marks.append(n.mul(text(n,u,v,name),n.ramp(n.mul(nx,side),.8,.98)))
 return n.maximum(*marks)

def steel(name,role,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n);ax=ab(n,x)
 # Resolved axial tool striae: several shipping texels across, never coarse
 # speckles and never a subtexel field that disappears in the 4K -> 2K filter.
 machining=n.noise(n.vec('MULTIPLY',p,(1450,14,1450)),1,2)
 tool=n.math('SINE',n.add(n.mul(z,math.tau/.0014),n.mul(y,31)))
 fine=n.noise(p,6500,2)
 base=(.0397,.0427,.0430)
 rough=n.add(.39,n.mul(sub(n,machining,.5),.10),n.mul(tool,.010))
 metal=1;h=n.mul(sub(n,fine,.5),1.5e-6);rub=0;carbon=0;roof_patina=0
 # High-frequency modulation changes a contact line's continuity slightly;
 # neither coarse noise nor a broad patch determines its shape.
 drag=n.add(.72,n.mul(n.noise(n.vec('MULTIPLY',p,(2200,170,2400)),1,2),.18),
            n.mul(n.math('SINE',n.mul(y,730)),.10))
 if role=='receiver':
  frame=n.node('ShaderNodeAttribute',attribute_name='ReceiverSection').outputs['Vector']
  width,bottom,top=n.split(frame)
  side=ramp(n,ax,sub(n,width,.0025),sub(n,width,.0005))
  roof=n.mul(side,n.band(z,sub(n,top,.0147),.00055,.00115),n.ramp(ab(n,nx),.25,.85))
  # A worn core on the outer chamfer, with only a 0.35 mm feather. The old
  # low-opacity 4 mm band tinted the oxide instead of exposing the substrate.
  lower=n.mul(n.band(z,n.add(bottom,.0020),.00045,.00035),side)
  rear=n.mul(n.ramp(y,.0386,.0377),side)
  # Bare steel stays on the sharp rim. Broad hand contact retains the thin
  # oxide patina below; widening the bare core made a graphic silver patch.
  front=n.mul(n.ramp(y,.2484,.2493),side)
  # Capsule port: distance to the center segment, radius 11.5 mm.
  cy=n.math('MAXIMUM',.1485,n.math('MINIMUM',y,.2255))
  dy=sub(n,y,cy);dz=sub(n,z,.047)
  radius=n.math('SQRT',n.add(n.mul(dy,dy),n.mul(dz,dz)))
  end=n.ramp(ab(n,sub(n,y,.187)),.025,.039)
  port=n.mul(n.band(radius,.0120,.00045,.00035),n.ramp(x,.0158,.0172),n.add(.48,n.mul(end,.52)))
  # Signed distance to the actual 27 x 112 mm, R4.5 loading cutout.
  # A continuous rounded contour avoids square crosses where independent
  # side/end wear bands overlap. The contour is evaluated per bake texel.
  qx=sub(n,ax,.009);qy=sub(n,ab(n,sub(n,y,.159)),.0515)
  ox=n.math('MAXIMUM',qx,0);oy=n.math('MAXIMUM',qy,0)
  load_distance=sub(n,n.add(n.math('SQRT',n.add(n.mul(ox,ox),n.mul(oy,oy))),
                             n.math('MINIMUM',n.maximum(qx,qy),0)),.0045)
  load=n.mul(n.band(load_distance,.00015,.00040,.00030),
             ramp(n,z,n.add(bottom,.0028),n.add(bottom,.0007)))
  carry=n.add(.55,n.mul(interval(n,y,.105,.205,.025),.45))
  rub=n.mul(n.maximum(n.mul(lower,carry),rear,front,port,load),drag,wear,1.18)
  roof_patina=n.mul(roof,.65,drag,wear,1.18)
  # Thin oxide where a carrying hand encloses the flank; broad form-following
  # feathering, without a noisy spot boundary. This remains blue, not bare steel.
  palm=n.mul(interval(n,y,.071,.175,.033),interval(n,z,n.add(bottom,.013),sub(n,top,.022),.012),
             n.ramp(ab(n,nx),.80,.98),wear,.25)
  base=n.mix(palm,base,(.070,.086,.088),True);rough=n.mix(palm,rough,.30)
  carbon=n.mul(n.ramp(radius,.0115,.0105),n.ramp(x,.0178,.0155),n.ramp(y,.222,.233),wear,.6)
  marks=engraved(n,x,y,z,nx);h=n.add(h,n.mul(marks,-.00010))
  base=n.mix(n.mul(marks,.36),base,(.012,.013,.014),True)
 elif role=='barrel':
  crown=n.ramp(y,.7090,.7105)
  underside=n.mul(interval(n,y,.692,.710,.002),n.ramp(y,.692,.704),
                  n.band(x,0,.0010,.0010),n.ramp(nz,-.70,-.95),.90)
  rub=n.mul(n.maximum(crown,underside),drag,wear,1.15)
  radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(sub(n,z,.049),sub(n,z,.049))))
  carbon=n.mul(n.ramp(y,.7068,.7108),n.ramp(radius,.0103,.0095),wear)
 elif role=='tube':
  # Sliding bearings polish a narrow axial rail. Most of the tube stays blue.
  rub=n.mul(n.ramp(nz,.60,.95),interval(n,y,.353,.574,.002),wear,.30)
 elif role=='cap':
  radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(sub(n,z,.013),sub(n,z,.013))))
  rim=n.ramp(radius,.0115,.0130)
  rub=n.mul(n.maximum(n.band(y,.590,.00025,.00025),n.band(y,.599,.00025,.00025)),rim,drag,wear)
 elif role=='guard':
  # The class uses an aluminum housing/guard. Our cast alloy has a dark
  # anodized finish, distinct from the warmer blued receiver, and gray rubs.
  base=(.018,.019,.020)
  rough=n.add(.47,n.mul(fine,.035))
  rub=n.mul(n.maximum(n.ramp(y,.112,.1175),n.mul(n.ramp(z,-.026,-.030),.4)),n.ramp(ax,.002,.004),wear)
 elif role=='control':
  rub=n.mul(n.maximum(n.ramp(ab(n,nx),.55,.95),n.ramp(nz,.80,.98)),wear,.36)
 elif role=='bright':
  base=(.26,.265,.27);rough=n.add(.28,n.mul(machining,.09))
  # Action bars and carrier bearing faces are genuinely polished steel.
  carbon=n.mul(n.ramp(y,.221,.241),n.ramp(ny,.3,.8),wear,.45)
 elif role=='dark':rough=.42
 # Complete oxide loss at a contact core, not a translucent gray wash. Other
 # steel finishes (tube, controls and already-bright bars) retain their values.
 bare_roles=('receiver','barrel','cap','guard')
 if role in bare_roles:rub=n.ramp(rub,.06,.44)
 rub_color=(.48,.51,.53) if role=='guard' else ((.56,.60,.63) if role in bare_roles else (.23,.25,.26))
 n.channel('wear',rub)
 base=n.mix(rub,base,rub_color,True);rough=n.mix(rub,rough,.38 if role in bare_roles else .30)
 if role=='receiver':
  patina=n.mul(roof_patina,sub(n,1,rub))
  base=n.mix(patina,base,(.23,.25,.26),True);rough=n.mix(patina,rough,.30)
 base=n.mix(carbon,base,(.0028,.0024,.0020),True)
 rough=n.mix(carbon,rough,.80);metal=n.mix(carbon,metal,.05)
 return finish(n,base,rough,metal,h)

def panel(n,y,z):
 # Our six-sided utility panel: crisp boundary, independently drawn in meters.
 polygon=[(-.048,-.014),(-.036,-.043),(-.013,-.040),(.010,.013),(-.006,.028),(-.030,.016)]
 distances=[]
 for (a,b),(c,d) in zip(polygon,polygon[1:]+polygon[:1]):
  length=math.hypot(c-a,d-b)
  distances.append(n.math('DIVIDE',sub(n,n.mul(c-a,sub(n,z,b)),n.mul(d-b,sub(n,y,a))),length))
 return mn(n,*distances)

def growth(n,x,y,z,role):
 # A long, slightly tapered blank intersects real concentric growth layers.
 # The wrist follows the blank axis; a curved radial cut reveals cathedrals
 # on the butt and forend. Noise never supplies the visible grain structure.
 if role=='stock':
  axis=n.add(n.mul(y,.10),n.mul(n.math('MAXIMUM',n.add(y,.09),0),.38))
  yy=n.math('MINIMUM',n.add(y,.060),0)
  zz=sub(n,z,axis);arch=n.mul(yy,yy,.12)
  rx=n.add(x,.030);rz=n.add(n.mul(zz,.82),.033)
 else:
  yy=sub(n,y,.460);zz=sub(n,z,.013)
  rx=n.add(x,.031);rz=n.add(n.mul(zz,.85),.024)
  arch=n.mul(yy,yy,.38)
 radius=n.math('SQRT',n.add(n.mul(rx,rx),n.mul(rz,rz)))
 figure=n.add(n.mul(n.math('SINE',n.add(n.mul(zz,115),n.mul(y,9))),.00045),
              n.mul(n.math('SINE',n.add(n.mul(x,165),n.mul(y,18))),.00025))
 phase=n.add(n.mul(n.add(radius,arch,figure),math.tau/.0058),
             n.mul(n.math('SINE',n.mul(radius,220)),.80),
             n.mul(n.math('SINE',n.mul(radius,630)),.50),
             n.mul(n.math('SINE',n.mul(radius,1500)),.25))
 phase=n.add(phase,n.mul(sub(n,n.noise(n.combine(n.mul(x,130),n.mul(y,6),n.mul(zz,180)),1,2),.5),.80))
 year=n.math('FRACT',n.mul(phase,1/math.tau))
 # Dense latewood ends sharply at the next year's open earlywood. A wrapped
 # layer boundary avoids the broad sinusoidal airbrush bands of pass 2.
 late=n.ramp(year,.965,.995);early=n.ramp(year,.14,.65)
 tone=n.add(.49,n.mul(early,.08),n.mul(n.ramp(year,.65,.96),-.12),
            n.mul(n.math('SINE',n.add(n.mul(zz,145),n.mul(y,23))),.045))
 # Sparse individual vessel pores, 0.3-0.6 mm across and 1-4 mm along the
 # fibers. F1 points make separate dark dashes, never motion-blurred noise.
 cells=n.node('ShaderNodeTexVoronoi',feature='F1',distance='EUCLIDEAN')
 n.feed(cells.inputs['Vector'],n.combine(n.mul(x,1400),n.mul(y,165),n.mul(zz,1500)))
 cells.inputs['Scale'].default_value=1
 color=n.node('ShaderNodeSeparateColor',mode='RGB');n.feed(color.inputs[0],cells.outputs['Color'])
 pores=n.mul(n.ramp(cells.outputs['Distance'],.28,.12),n.ramp(color.outputs[0],.48,.65))
 return tone,late,pores,zz

def impacts(n,p,y,z,nx,role,base,rough,h,wear):
 # A crushed bowl with compressed dark fiber, a small broken finish lip and
 # an actual normal-map depression. Positions are isolated knock-prone sites.
 points=([(-.225,-.095,.0030,.0018),(-.233,-.001,.0026,.0015),
          (-.162,.009,.0025,.0013),(-.106,-.041,.0022,.0012)] if role=='stock' else
         [(.371,-.004,.0026,.0017),(.544,-.005,.0022,.0015)])
 facing=n.ramp(ab(n,nx),.32,.78)
 for yy,zz,wy,wz in points:
  u=n.add(n.math('DIVIDE',sub(n,y,yy),wy),n.mul(n.math('DIVIDE',sub(n,z,zz),wz),.22))
  v=n.math('DIVIDE',sub(n,z,zz),wz)
  r2=n.add(n.math('POWER',ab(n,u),2.8),n.math('POWER',ab(n,v),1.6));bowl=n.math('MAXIMUM',sub(n,1,r2),0)
  dent=n.mul(bowl,bowl,facing,wear)
  lip=n.mul(n.band(r2,.84,.10,.16),n.ramp(v,.05,.65),facing,wear)
  h=n.add(h,n.mul(dent,-.00034),n.mul(lip,.000025))
  base=n.mix(n.mul(dent,.55),base,(.011,.006,.0038),True)
  base=n.mix(n.mul(lip,.27),base,(.110,.072,.042),True)
  rough=n.mix(n.maximum(dent,lip),rough,.61)
 # A continuous cut across the fibers. The narrow bottom exposes pale raw
 # wood; no dotted gate or noise interrupts its path.
 yy,zz=(-.214,-.079) if role=='stock' else (.529,-.003)
 cross=n.add(sub(n,y,yy),n.mul(sub(n,z,zz),.27))
 profile=n.math('MAXIMUM',sub(n,1,n.math('DIVIDE',ab(n,cross),.00068)),0)
 scratch=n.mul(profile,profile,interval(n,z,zz-.007,zz+.005,.0012),facing,wear)
 h=n.add(h,n.mul(scratch,-.00024))
 base=n.mix(n.mul(scratch,.86),base,(.150,.091,.050),True)
 rough=n.mix(scratch,rough,.64)
 return base,rough,h

def wood(name,role,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n)
 tone,late,pores,zz=growth(n,x,y,z,role)
 low=(.0302,.019,.0157) if role=='stock' else (.021,.0036,.0017)
 high=(.098,.0585,.0506) if role=='stock' else (.130,.020,.009)
 base=n.mix(tone,low,high,True)
 # Annual layers carry a restrained color change, while dense fiber bundles
 # and separate vessels provide the fine grain. Avoid outlining every ring.
 base=n.mix(n.mul(late,.10),base,(.009,.004,.0022),True)
 bundle=n.voronoi(n.combine(n.mul(x,1050),n.mul(y,55),n.mul(zz,1150)),1,'DISTANCE_TO_EDGE')
 fibergrain=n.ramp(bundle,.16,.05)
 base=n.mix(n.mul(fibergrain,.28),base,(.020,.008,.0035),True)
 base=n.mix(n.mul(pores,.65),base,(.006,.003,.0018),True)
 h=n.add(n.mul(late,-.000008),n.mul(pores,-.000025),n.mul(fibergrain,-.000008))
 rough=n.add(.35 if role=='stock' else .43,n.mul(late,.035),n.mul(pores,.08));ao=n.mix(pores,1,.88)
 fibers=n.noise(n.combine(n.mul(x,950),n.mul(y,60),n.mul(zz,1100)),1,2)
 h=n.add(h,n.mul(sub(n,fibers,.5),12e-6))
 rough=n.add(rough,n.mul(sub(n,fibers,.5),.07))
 if role=='stock':
  distance=panel(n,y,z)
  facing=n.mul(n.ramp(ab(n,x),.010,.013),n.ramp(ab(n,nx),.45,.85))
  inside=n.mul(n.ramp(distance,.00025,.00065),facing)
  a=n.math('PINGPONG',n.add(y,n.mul(z,.80)),.00105)
  b=n.math('PINGPONG',sub(n,y,n.mul(z,.80)),.00105)
  cuts=n.maximum(n.ramp(a,.00034,.00010),n.ramp(b,.00034,.00010))
  border=n.mul(n.band(distance,0,.00030,.00030),facing)
  innerborder=n.mul(n.band(distance,.0014,.00015,.00025),facing)
  check=n.mul(inside,cuts);relief=n.maximum(check,border,innerborder)
  h=n.add(h,n.mul(relief,-.00028))
  base=n.mix(n.mul(relief,.94),base,(.0035,.0020,.0013),True)
  ao=n.mix(relief,ao,.65);rough=n.mix(inside,rough,.52)
  wrist=n.mul(inside,sub(n,1,cuts),wear)
  combheight=n.add(.004,n.mul(n.add(y,.243),.100))
  comb=n.mul(n.band(z,combheight,.003,.004),n.ramp(nz,.45,.90),interval(n,y,-.22,-.065,.012),wear)
  wrap=n.mul(interval(n,y,-.048,.008,.014),n.maximum(n.ramp(ab(n,nx),.25,.70),n.ramp(nz,.3,.8)),wear,.48)
  hand=n.maximum(n.mul(wrist,.7),comb,wrap)
  base=n.mix(n.mul(hand,.23),base,(.011,.007,.004),True)
  base=n.mix(n.mul(wrap,.60),base,(.020,.008,.0035),True)
  rough=n.mix(hand,rough,.52)
 else:
  # Paired-groove period is taken from the actual carved surface construction.
  yy=n.math('PINGPONG',sub(n,y,.367),.004)
  groove=n.maximum(n.band(yy,0,.00035,.00045),n.band(yy,.003,.00035,.00045))
  groove=n.mul(groove,interval(n,y,.366,.557,.0015))
  base=n.mix(n.mul(groove,wear,.78),base,(.005,.0010,.0004),True)
  rough=n.mix(n.mul(groove,wear),rough,.64);ao=n.mix(groove,ao,.77)
  crest=n.mul(sub(n,1,groove),interval(n,y,.364,.562,.005))
  hand=n.mul(crest,interval(n,y,.402,.480,.027),wear)
  base=n.mix(n.mul(hand,.24),base,(.010,.003,.0016),True)
  # Polish only the narrow crown of each physical land, not its entire
  # rounded shoulder. Hand contact leaves the surrounding finish duller.
  period=n.math('MODULO',sub(n,y,.367),.008)
  ridge=n.mul(n.maximum(n.band(period,.0015,.00020,.00028),
                        n.band(period,.0055,.00027,.00030)),crest)
  rough=n.mix(ridge,rough,.27);rough=n.mix(n.mul(hand,sub(n,1,ridge)),rough,.49)
 base,rough,h=impacts(n,p,y,z,nx,role,base,rough,h,wear)
 return finish(n,base,rough,0,h,ao)

def rubber(name,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n)
 fine=n.noise(p,6500,2);base=(.006,.0055,.0050)
 a=n.math('PINGPONG',n.add(x,z),.0014);b=n.math('PINGPONG',sub(n,x,z),.0014)
 pattern=n.maximum(n.ramp(a,.00030,.00010),n.ramp(b,.00030,.00010))
 back=n.ramp(ny,-.4,-.85)
 # Two staggered columns of original molded triangular side recesses.
 # Correct the pad's pitched depth frame so the border follows its casting.
 depth=sub(n,y,n.mul(sub(n,.004,z),.11));holes=[]
 for center,offset,flip in [(-.260,.0,False),(-.252,.004,True)]:
  u=n.add(n.math('DIVIDE',sub(n,depth,center),.0068),.5)
  v=n.math('FRACT',n.math('DIVIDE',n.add(z,.118,offset),.008))
  if flip:v=sub(n,1,v)
  edge=mn(n,v,sub(n,sub(n,.82,v),n.mul(ab(n,sub(n,u,.5)),1.64)))
  holes.append(n.mul(n.ramp(edge,.015,.065),interval(n,u,0,1,.01)))
 side=n.ramp(ab(n,ny),.75,.30)
 recess=n.mul(n.maximum(*holes),side)
 seam=n.maximum(n.band(depth,-.246,.00016,.00022),n.band(depth,-.265,.00016,.00022))
 h=n.add(n.mul(fine,8e-6),n.mul(pattern,back,-.00012),n.mul(recess,-.00085),n.mul(seam,side,-.00018))
 base=n.mix(n.mul(recess,.90),base,(.0006,.0006,.0006),True)
 base=n.mix(n.mul(seam,side,.5),base,(.002,.002,.002),True)
 dusty=n.mul(n.ramp(z,-.079,-.111),wear,.25)
 base=n.mix(dusty,base,(.032,.023,.014),True)
 rough=n.mix(n.mul(back,sub(n,1,pattern),wear),.69,.48)
 return finish(n,base,rough,0,h,n.mix(n.maximum(n.mul(pattern,back,.3),recess),1,.40))

def ammunition(name,kind,fired,wear):
 n=Nodes(name);p,x,y,z,nx,ny,nz=inp(n)
 fine=n.noise(p,6500,2);patch=n.noise(p,600,2)
 h=n.mul(sub(n,fine,.5),1.5e-6);rough=n.add(.30,n.mul(fine,.065));ao=1
 if kind in ('brass','primer'):
  base=(.49,.285,.078) if kind=='brass' else (.37,.34,.25)
  tarnish=n.mul(n.ramp(patch,.48,.76),.21)
  base=n.mix(tarnish,base,(.17,.086,.024),True);metal=1
  radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(z,z)))
  if kind=='brass':
   stamp=text(n,n.add(n.mul(x,46),.5),n.add(n.mul(z,46),.5),'headstamp')
   stamp=n.mul(stamp,n.ramp(ny,-.4,-.9))
   h=n.add(h,n.mul(stamp,-.00008));base=n.mix(n.mul(stamp,.72),base,(.045,.023,.008),True)
  else:
   turn=n.math('SINE',n.mul(radius,math.tau/.00015));h=n.add(h,n.mul(turn,.8e-6))
 else:
  base=(.255,.009,.006) if kind!='follower' else (.20,.045,.006)
  metal=0;rough=n.add(.46,n.mul(fine,.04))
  angle=n.math('ARCTAN2',z,x)
  ribs=n.math('SINE',n.mul(angle,160))
  side=n.ramp(ab(n,ny),.40,.10)
  h=n.add(h,n.mul(ribs,side,.000009))
  rough=n.add(rough,n.mul(ribs,side,.025))
  soot=n.mul(n.ramp(y,.061,.069),n.add(.94,n.mul(patch,.06)),wear,1.18) if fired else 0
  # Interior plastic remains dark red with a soot-loaded fired lip.
  if kind=='mouth':soot=n.maximum(soot,.92)
  base=n.mix(soot,base,(.008,.003,.0018),True);rough=n.mix(soot,rough,.82)
 return finish(n,base,rough,metal,h,ao)

def assign(wear):
 records={}
 for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]:
  base=Vector((0,0,0))
  for prefix,yy,zz in [('TubeShell'+str(i+1),.255+i*.059,.013) for i in range(4)]+[
    ('ChamberShell',.2411,.049),('CarrierShell',.159,.016),('InsertShell',.185,.013)]:
   if ob.name.startswith(prefix):base=Vector((0,yy,zz));break
  position=ob.data.attributes.new('FinishPosition','FLOAT_VECTOR','POINT')
  position.data.foreach_set('vector',[a for v in ob.data.vertices for a in v.co-base])
  normal=ob.data.attributes.new('FinishNormal','FLOAT_VECTOR','CORNER')
  normal.data.foreach_set('vector',[a for row in ob.data.corner_normals for a in row.vector])
  if ob.name=='Receiver':
   from build import receiver_shape,GRIP
   section=ob.data.attributes.new('ReceiverSection','FLOAT_VECTOR','POINT')
   values=[]
   for vertex in ob.data.vertices:
    (width,bottom,top),_=receiver_shape(vertex.co.y*1000+GRIP.y)
    values.extend((width*.001,(bottom-GRIP.z)*.001,(top-GRIP.z)*.001))
   section.data.foreach_set('vector',values)
  roles=[]
  for i,old in enumerate(list(ob.data.materials)):
   key=old.name.removeprefix('CP_').split('.')[0];name='H12_'+ob.name+'_'+str(i)
   role=key
   if key=='wood':
    role='stock' if ob.name=='Stock' else 'forend';mat=wood(name,role,wear)
   elif key=='rubber':mat=rubber(name,wear)
   elif key in ('brass','primer','hull','mouth','follower'):
    mat=ammunition(name,key,ob.name=='Standalone_hull',wear)
   else:
    if ob.name=='Receiver':role='receiver'
    elif ob.name=='Barrel':role='barrel'
    elif ob.name=='Magazine_Tube':role='tube'
    elif ob.name=='Magazine_Cap':role='cap'
    elif ob.name=='Trigger_Plate':role='guard'
    elif ob.name.startswith(('Safety','ActionRelease','Trigger_Shoe','Sling_')):role='control'
    elif key=='steel':role='bright'
    mat=steel(name,role,wear)
   ob.data.materials[i]=mat;roles.append(role)
  records[ob.name]=roles
 bpy.context.scene['finish_wear']=wear
 return records
