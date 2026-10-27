"""Ranch-specific cladding, period windows and low entry on shared construction.

Uses the accepted Mesh/Builder, analytic wall and roof envelopes, K drainage,
door leaves/hardware, patio slider and socket creation unchanged.
"""
import math
import json
import bpy
from mathutils import Vector
from build import Builder,wall_sections,doors,roofs,fixture
from plan import clip,subtract
from additions import portal
from ranch_masonry import brick_extent,opening_masonry

BRICKS=dict(red=(.265,.080,.044),red_brown=(.18,.068,.038),buff=(.42,.29,.15),tan=(.31,.21,.12))


def shell(b):
 s=b.plan['spec']
 for block in b.plan['blocks']:
  if block.name=='Garage' and s['garage']['kind']=='carport':continue
  for face in ('front','back','left','right'):
   xf,n,length=b.frame(block,face)
   wall=b.mesh(block.name+'_'+face+'_Wall',component='wall',block=block.name,face=face)
   base=b.mesh(block.name+'_'+face+'_Foundation',component='foundation',block=block.name,face=face)
   cap=b.mesh(block.name+'_'+face+'_SoldierSill',component='veneer_cap',block=block.name,face=face)
   for poly,adj in wall_sections(b,block,face):
    parts=[poly]
    for o in [o for o in b.openings if o['block']==block.name and o['face']==face]:
     cuts=[(1,0,-o['u']+o['w']/2),(-1,0,o['u']+o['w']/2),(0,1,-o['z']),(0,-1,o['z']+o['h'])]
     parts=[p for v in parts for p in subtract(v,cuts)]
    brick=s['cladding'][block.name][face]=='veneer'
    transition=(block.floor+1.016-.07) if s['wall_mix']=='wainscot' else block.plate-.03
    for p in parts:
     fields=[('Veneer',clip(p,0,-1,transition)),('Siding',clip(p,0,1,-transition))] if brick else [('Siding',p)]
     if s['battens']:
      fields=[entry for role,piece in fields for entry in ([(role,clip(piece,0,-1,block.plate)),('Trim',clip(piece,0,1,-block.plate))] if role=='Siding' else [(role,piece)])]
     for role,piece in fields:
      if not piece:continue
      # 90 mm brick wythe, cavity and wall lining; never an orange thin decal.
      wall.prism([xf((u,.072 if role=='Veneer' else .012,z)) for u,z in piece],(-n[0],-n[1],0),.165,role)
      if role=='Veneer':
       for a,c in zip(piece,piece[1:]+piece[:1]):
        if abs(a[1]-transition)<1e-7 and abs(c[1]-transition)<1e-7:
         lo,hi=sorted((a[0],c[0]));cap.prism([xf((lo,.025,transition+.025)),xf((hi,.025,transition+.025)),xf((hi,.13,transition+.010)),xf((lo,.13,transition+.010))],(0,0,-1),.025,'Veneer')
    if not adj:
     lo=min(v[0] for v in poly);hi=max(v[0] for v in poly);top=max(.02,block.floor-.205)
     base.prism([xf((lo,-.024,0)),xf((hi,-.024,0)),xf((hi,-.024,top)),xf((lo,-.024,top))],(-n[0],-n[1],0),.18,'Concrete')
   wall.finish();base.finish();cap.finish()
   if s['battens']:
    bats=b.mesh(block.name+'_'+face+'_GableBattens',component='battens')
    for j in range(1,math.ceil(length/.3048)):
     u=j*.3048
     p=xf((u,0,0));height=block.height(p.x,p.y)-.15-block.plate
     if height>.025:bats.box((u,.027,block.plate+height/2),(.038,.028,height),r=.001,xf=xf)
    bats.finish()
   # Narrow painted corner boards only on siding, not glued across brick.
   if not brick:
    trim=b.mesh(block.name+'_'+face+'_CornerTrim',component='corner_posts')
    for u in (.035,length-.035):trim.box((u,.032,(max(.02,block.floor-.2)+block.plate)/2),(.07,.04,block.plate-max(.02,block.floor-.2)),r=.001,xf=xf)
    trim.finish()
   if s['foundation']=='crawlspace' and block.name=='Main':
    vents=b.mesh('Crawlspace_'+face,component='crawl_vent')
    for u in (length*.12,length*.87):
     # Surface-mounted grille over the plinth, shadowed throat and slats.
     vents.box((u,-.002,.22),(.38,.05,.18),color=(.12,.12,.10),r=.002,xf=xf)
     for j in range(4):vents.box((u,.028,.155+j*.043),(.34,.016,.015),color=(.21,.20,.16),r=0,xf=xf)
    vents.finish()


def window(b,o):
 block=next(v for v in b.plan['blocks'] if v.name==o['block']);xf,n,l=b.frame(block,o['face'])
 u,z,w,h=(o[k] for k in ('u','z','w','h'));system=o.get('system','vinyl');picture=o.get('style')=='picture'
 me=b.mesh(o['id'],component='window',opening=json.dumps(o),window_system=system)
 trim=b.colors['Trim'];metal=(.30,.31,.27);paint=(.61,.59,.52) if b.plan['seed']%2==0 else (.52,.47,.36)
 masonry_top=brick_extent(b,o);brick=masonry_top is not None and masonry_top>z
 shift=-.103 if brick else 0
 c=metal if system=='aluminum' else ((.105,.075,.042) if system=='bronze' else (paint if system=='vinyl' else tuple(v*.65 for v in trim)))
 def box(x,v,zz,ww,dd,hh,color=c,r=.0015,role='Trim'):me.box((x,v+shift,zz),(ww,dd,hh),role,color,r,xf)
 # Brick hole side faces are actual brick returns, with no white casing
 # over their outside edge. Siding keeps its receiving/casing assembly.
 for sign in (-1,1):
  box(u+sign*(w/2-.018),-.10,z+h/2,.036,.20,h,(.25,.23,.19))
  if not brick:box(u+sign*(w/2+.027),.09,z+h/2,.054,.050,h+.10)
  elif masonry_top<z+h:
   low=max(z,masonry_top+.025);hh=z+h+.05-low
   if hh>0:me.box((u+sign*(w/2+.027),.047,low+hh/2),(.054,.050,hh),'Trim',c,.0015,xf)
 box(u,-.10,z+h-.018,w-.072,.20,.036,(.25,.23,.19),0)
 if not brick:
  box(u,.09,z+h+.026,w+.108,.052,.052)
  box(u,.10,z-.02,w+.15,.19,.04,trim)
  me.prism([xf((u-w/2-.075,.035,z+.006)),xf((u+w/2+.075,.035,z+.006)),xf((u+w/2+.075,.185,z-.012)),xf((u-w/2-.075,.185,z-.012))],(0,0,-1),.015,'Trim',c)
  box(u,.10,z+h+.062,w+.15,.10,.009,(.35,.35,.31),0)
 elif masonry_top<z+h:me.box((u,.047,z+h+.026),(w+.108,.052,.052),'Trim',c,.0015,xf)
 # One opening, no false casings between the picture unit's three lights.
 panels=[(u-w*.355,w*.27,True),(u,w*.44,False),(u+w*.355,w*.27,True)] if picture else [(u,w,True)]
 for pi,(x,pw,operable) in enumerate(panels):
  inner=pw-.06
  for sign in (-1,1):box(x+sign*(pw/2-.022),.055,z+h/2,.044,.045,h-.02)
  for zz in (z+.025,z+h-.025):box(x,.055,zz,pw-.08,.045,.05)
  if operable:
   for row in (0,1):
    sh=(h-.08)/2;zz=z+.035+row*(h-.07)/2;v=.052-row*.025
    for sign in (-1,1):box(x+sign*(inner/2-.018),v,zz+sh/2,.036,.03,sh)
    for zh in (zz+.020,zz+sh-.020):box(x,v,zh,inner-.06,.03,.04)
    box(x,v-.019,zz+sh/2,inner-.07,.004,sh-.08,(.94,.96,.93),0,'Glass')
   box(x,.07,z+h/2,pw-.05,.04,.027)
  else:box(x,.028,z+h/2,inner-.025,.004,h-.085,(.94,.96,.93),0,'Glass')
  # Curtain folds stay behind glazing and catch real diffuse daylight.
  shade=(.37,.32,.24) if (b.plan['seed']+pi)%2 else (.48,.46,.39)
  box(x,-.30,z+h/2,inner,.014,h-.03,(.006,.006,.005),0)
  if (b.plan['seed']+int(o['id'].split('_')[-1]))%3==0:
   drop=.26+((b.plan['seed']+pi)*13%41)/100
   box(x,-.14,z+h*(1-drop/2),inner-.04,.012,h*drop,shade,0)
   box(x,-.13,z+h*(1-drop),inner-.03,.025,.022,shade)
  else:
   for sign in (-1,1):
    vs=[]
    for j in range(4):
     for k in range(9):vs.append(xf((x+sign*(pw*.29+pw*.16*k/8),-.15+shift-.016*math.cos(k*2)-.005*math.sin(j),z+.035+(h-.07)*j/3-.014*math.sin(k)**2*(1-j/3))))
    me.geom(vs,[(j*9+k,j*9+k+1,(j+1)*9+k+1,(j+1)*9+k) for j in range(3) for k in range(8)],'Trim',shade)
 if system=='wood_storm':
  wood=me;me=b.mesh(o['id']+'_Storm',component='storm_window',window_system='aluminum')
  # A real separate 3 mm storm pane sits 40 mm ahead of the original sash.
  # The picture light stays fixed; only flanking hung units get meeting rails.
  for x,pw,operable in panels:
   for sign in (-1,1):box(x+sign*(pw/2-.008),.12,z+h/2,.019,.022,h,metal)
   rails=(z+.008,z+h/2,z+h-.008) if operable else (z+.008,z+h-.008)
   for zz in rails:box(x,.12,zz,pw-.03,.022,.018,metal)
   count=2 if operable else 1
   for j in range(count):box(x,.113,z+(j+.5)*h/count,pw-.052,.003,h/count-.037,(1,1,1),0,'Glass')
  me.finish();me=wood
 if o['shutters']:
  sw=w/2;sc=b.plan['spec']['colors']['shutter']
  for sign in (-1,1):
   xx=u+sign*(w/2+.09+sw/2);box(xx,.085,z+h/2,sw,.022,h,sc)
   for side in (-1,1):box(xx+side*(sw/2-.025),.104,z+h/2,.05,.020,h,sc)
   for zz in (z+.035,z+h*.5,z+h-.035):box(xx,.104,zz,sw-.1,.02,.07,sc)
   for zz in (z+h*.25,z+h*.75):box(xx,.101,z+zz-z,sw-.11,.008,h*.39,tuple(v*.78 for v in sc),0)
 me.finish()


def entry(b):
 p=b.plan['porch'];m=b.plan['blocks'][0];top=p.floor
 me=b.mesh('Porch_Concrete',component='porch_steps')
 me.box((p.cx,p.cy,top/2),(p.width+.10,p.depth+.07,top),'Concrete',r=.006)
 count=math.ceil(top/.18);riser=top/count
 for i in range(count-1):
  z=(i+1)*riser;y=p.y0-(count-1-i-.5)*.3048
  me.box((p.cx,y,z/2),(1.40,.312,z),'Concrete',r=.004)
 me.finish()
 col=b.mesh('Porch_SlenderPosts',component='porch_structure')
 y=p.y0+.17;beam_top=p.height(p.cx,y)-.225;head=beam_top-.1524
 beam=b.mesh('Porch_Beam',component='porch_beam')
 beam.box((p.cx,y,beam_top-.0762),(p.width-.08,.14,.1524),r=.002);beam.finish()
 for x in (p.x0+.14,p.x1-.14):
  if b.plan['seed']%2:
   iron=(.032,.039,.029)
   for dx in (-.055,.055):col.box((x+dx,y,(top+head)/2),(.025,.025,head-top),color=iron,r=.001)
   # Forged C scrolls are short ornaments inside the paired uprights.
   for j in range(4):
    zz=top+.30+(head-top-.60)*j/3
    pts=[(x+.038*math.cos(a),y,zz+.105*math.sin(a)) for a in [math.pi*.2+k*math.pi*1.65/15 for k in range(16)]]
    col.tube(pts,.006,color=iron,sides=6)
  else:col.box((x,y,(top+head)/2),(.0762,.0762,head-top),r=.002)
  for zz in (top+.012,head-.012):col.box((x,y,zz),(.15,.12,.024),r=.002)
 col.finish()
 foyer=b.mesh('Shallow_Foyer',component='foyer');cream=(.36,.33,.27)
 foyer.box((p.cx,m.y0+1.0,m.floor-.012),(2.0,1.95,.024),color=(.16,.105,.06),r=0)
 for x in (p.cx-1.,p.cx+1.):foyer.box((x,m.y0+1.0,m.floor+1.2),(.06,2.,2.4),color=cream,r=0)
 foyer.box((p.cx,m.y0+2,m.floor+1.2),(2.,.06,2.4),color=cream,r=0)
 foyer.box((p.cx,m.y0+1,m.floor+2.4384),(2.,2.,.04),color=cream,r=0);foyer.finish()


def carport(b):
 if b.plan['spec']['garage']['kind']!='carport':return
 g=b.plan['blocks'][1];me=b.mesh('Carport_Columns',component='carport_structure');outer=g.x1-.04 if b.plan['spec']['garage']['side']=='right' else g.x0+.04
 for y in (g.y0+.025,g.cy,g.y1-.025):
  head=g.height(outer,y)-.20
  me.box((outer,y,(g.floor+head)/2),(.1016,.1016,head-g.floor),r=.002)
  me.box((outer,y,g.floor+.01),(.18,.18,.02),color=(.15,.16,.13),r=.002)
 for y in (g.y0+.12,g.y1-.12):
  me.box((g.cx,y,g.eave-.23),(g.width,.14,.23),r=.002)
 me.box((outer,g.cy,g.eave-.23),(.14,g.depth,.23),r=.002)
 me.box((g.cx,g.cy,.0508),(g.width,g.depth,.1016),'Concrete',r=.004)
 # Exposed ceiling ties bear on the house ledger and outer beam.
 for j in range(math.ceil(g.depth/.6096)+1):
  yy=g.y0+min(g.depth,j*.6096)
  me.box((g.cx,yy,g.eave-.28),(g.width,.045,.14),r=.001)
 me.finish()


def chimney(b):
 s=b.plan['spec'];m=b.plan['blocks'][0];roof=b.plan.get('roof_envelope') or m
 if not s['chimney']:return
 if s['chimney']=='ridge':x=m.cx+m.width*(.17 if s['garage']['side']=='left' else -.17);y=m.cy+.13;bottom=roof.height(x,y)-.35
 else:x=m.x0-.22 if s['garage']['side']=='right' else m.x1+.22;y=m.y0+m.depth*.60;bottom=.02
 w,d=((.6096,1.2192) if s['chimney']=='gable' else (1.2192,.6096));top=roof.height(max(m.x0,min(x,m.x1)),y)+1.02
 me=b.mesh('Brick_Chimney',component='chimney')
 me.box((x,y,(bottom+top)/2),(w,d,top-bottom),'Veneer',r=.003)
 me.box((x,y,top+.045),(w+.13,d+.13,.09),'Concrete',r=.004)
 for dx in (-.22,.22):
  # Open clay liners, dark throat and gauged rain hood.
  me.box((x+dx if w>d else x,y if w>d else y+dx,top+.12),(.22,.27,.12),'Trim',(.24,.095,.045),r=.002)
  me.box((x+dx if w>d else x,y if w>d else y+dx,top+.185),(.16,.21,.005),'Trim',(.025,.024,.019),r=0)
 for dx in (-w*.45,w*.45):
  for dy in (-d*.45,d*.45):me.box((x+dx,y+dy,top+.29),(.016,.016,.25),color=(.10,.11,.095),r=0)
 me.box((x,y,top+.43),(w+.22,d+.22,.035),color=(.10,.11,.095),r=.006)
 # Four gauged aprons follow the roof; clip against every roof plane so a
 # nominal quad cannot bridge two slopes. Overlapping counterflashing
 # beds into the actual masonry face and covers each apron upstand.
 apron=b.mesh('Chimney_Aprons',component='flashing',flashing_kind='apron')
 counter=b.mesh('Chimney_Counterflashing',component='flashing',flashing_kind='counter')
 for axis in (0,1):
  for sign in (-1,1):
   fixed=(x if axis==0 else y)+sign*((w if axis==0 else d)/2+.012)
   center=y if axis==0 else x;half=(d if axis==0 else w)/2
   def xy(u,v):return (v,u) if axis==0 else (u,v)
   outer=fixed+sign*.12;inner=fixed-sign*.12
   ring=[xy(center-half-.132,outer),xy(center+half+.132,outer),xy(center+half-.108,inner),xy(center-half+.108,inner)]
   # Mitered ring pieces share a boundary. Clip each piece against the
   # same plane envelope that built the roof, including hip diagonals.
   for plane in roof.planes():
    points=ring[:]
    for qa,qb,qc in roof.planes():points=clip(points,qa-plane[0],qb-plane[1],qc-plane[2])
    for ca,cb,cc in ((1,0,-roof.x0+roof.overhang),(-1,0,roof.x1+roof.overhang),(0,1,-roof.y0+roof.overhang),(0,-1,roof.y1+roof.overhang)):
     points=clip(points,ca,cb,cc)
    apron.prism([(xx,yy,plane[0]*xx+plane[1]*yy+plane[2]+.012) for xx,yy in points],(0,0,-1),.003,'Trim',(.16,.16,.14))
   length=(d if axis==0 else w);count=math.ceil(length/.15)
   start=(y-d/2) if axis==0 else (x-w/2)
   for j in range(count):
    aa=start+j*length/count-.015;cc=start+(j+1)*length/count+.015
    face=(x if axis==0 else y)+sign*((w if axis==0 else d)/2+.001)
    if axis==0:
     if not m.x0-m.overhang<=face<=m.x1+m.overhang:continue
     aa=max(aa,m.y0-m.overhang);cc=min(cc,m.y1+m.overhang)
    else:
     if not m.y0-m.overhang<=face<=m.y1+m.overhang:continue
     aa=max(aa,m.x0-m.overhang);cc=min(cc,m.x1+m.overhang)
    if cc<=aa:continue
    pa=xy(aa,face);pc=xy(cc,face);za=roof.height(*pa);zc=roof.height(*pc);head=max(za,zc)+.19
    inward=(-sign*.003,0,0) if axis==0 else (0,-sign*.003,0)
    counter.prism([(*pa,za+.010),(*pc,zc+.010),(*pc,head),(*pa,head)],inward,1,'Trim',(.22,.22,.19))
 apron.finish();counter.finish()
 if s['chimney']=='gable':
  # Visible grade collar bears on the ground datum; the brick starts at
  # 20 mm above it rather than floating over an unmodeled footing.
  me.box((x,y,.01),(w+.06,d+.06,.02),'Concrete',r=.002)
 me.finish()


def services(b):
 s=b.plan['spec'];m,g=b.plan['blocks'];me=b.mesh('Services',component='services')
 xf,n,l=b.frame(m,'front');fixture(me,xf,b.plan['door_x']-m.x0+.64,m.floor+1.83)
 xf,n,l=b.frame(m,'back');metal=(.27,.29,.26)
 # Utility pier occupies the interval between kitchen and slider, never a pane.
 u=l*.29;me.box((u,.14,1.25),(.26,.13,.45),color=metal,r=.009,xf=xf)
 p=xf((u,.205,1.36));normal=Vector((*n,0));me.tube([p,p+normal*.07],.094,color=metal,sides=20)
 me.tube([p+normal*.071,p+normal*.076],.077,'Glass',(.50,.55,.48),sides=20)
 for za,zb in ((.10,1.04),(1.48,2.30)):me.tube([xf((u,.13,za)),xf((u,.13,zb))],.018,color=metal,sides=10)
 # Gas regulator on low riser and a flexible shut-off branch along the wall.
 ug=l*.65;me.box((ug,.18,.59),(.25,.22,.20),color=(.30,.31,.27),r=.02,xf=xf)
 me.tube([xf((ug-.20,.13,.06)),xf((ug-.20,.13,.62)),xf((ug,.13,.62))],.021,color=metal,sides=10)
 me.tube([xf((ug+.12,.13,.56)),xf((ug+.24,.13,.56)),xf((ug+.24,.13,.24))],.016,color=metal,sides=10)
 # Dryer hood and two wall-mounted hose bibs.
 uv=l*.65;me.box((uv,.09,1.23),(.16,.06,.16),color=metal,r=.003,xf=xf)
 me.prism([xf((uv-.09,.12,1.32)),xf((uv+.09,.12,1.32)),xf((uv+.09,.23,1.19)),xf((uv-.09,.23,1.19))],(0,0,-1),.004,'Trim',metal)
 for uu in (.055*l,.91*l):
  me.tube([xf((uu,.075,.55)),xf((uu,.20,.55)),xf((uu,.23,.49))],.013,color=(.24,.16,.055),sides=10)
  me.box((uu,.16,.60),(.07,.07,.012),color=(.17,.095,.025),r=.002,xf=xf)
 me.finish()
 # Condenser on a separate pad; real air clearance and slack insulated lines.
 ac=b.mesh('AC_Condenser',component='condenser');x=m.x0+l*.64;y=m.y1+1.03
 ac.box((x,y,.07),(.98,.92,.14),'Concrete',r=.009)
 ac.box((x,y,.50),(.77,.72,.72),color=(.22,.235,.19),r=.018)
 for dx in (-.394,.394):
  for j in range(20):ac.box((x+dx,y,(.21+j*.029)),(.014,.65,.010),color=(.105,.12,.095),r=0)
 for dy in (-.369,.369):
  for j in range(18):ac.box((x,y+dy,.22+j*.032),(.71,.014,.010),color=(.12,.14,.11),r=0)
 ac.tube([(x,y,.86),(x,y,.875)],.29,color=(.065,.075,.060),sides=32)
 for j in range(-5,6):
  off=j*.046;ln=math.sqrt(.27**2-off**2)*2
  ac.box((x+off,y,.895),(.012,ln,.012),color=(.29,.31,.26),r=0)
 ac.tube([(x-.32,y-.29,.35),(x-.46,y-.33,.30),(x-.48,m.y1+.32,.22),(x-.45,m.y1+.14,.29),(x-.45,m.y1+.09,.50)],.027,color=(.035,.038,.03),sides=10)
 ac.tube([(x-.28,y-.30,.31),(x-.40,y-.39,.26),(x-.41,m.y1+.12,.19),(x-.36,m.y1+.085,.45)],.009,color=(.28,.13,.046),sides=8)
 ac.finish()
 if s['aerial']:
  aerial=b.mesh('Legacy_'+s['aerial'],component='aerial');x=m.cx+1.;y=m.cy+1.4;z=m.height(x,y)
  aerial.tube([(x,y,z),(x,y,z+1.40)],.019,color=(.24,.26,.23),sides=10)
  if s['aerial']=='antenna':
   aerial.beam((x,y-.65,z+1.28),(x,y+.65,z+1.28),.022,color=(.28,.29,.25),r=0)
   for j in range(6):
    yy=y-.55+j*.22;half=.65-j*.065
    aerial.tube([(x-half,yy,z+1.29),(x+half,yy,z+1.29)],.008,color=(.32,.33,.29),sides=6)
  else:
   # Shallow parabolic dish, built from our radial profile, with LNB arm.
   vs=[(x,y-.10,z+.90)]
   for ring in range(1,5):
    rr=.29*ring/4
    for j in range(24):
     a=j*math.tau/24;vs.append((x+rr*math.cos(a),y-.10-.14*(rr/.29)**2,z+.9+rr*math.sin(a)))
   fs=[(0,1+j,1+(j+1)%24) for j in range(24)]
   fs += [(1+(k-1)*24+j,1+(k-1)*24+(j+1)%24,1+k*24+(j+1)%24,1+k*24+j) for k in range(1,4) for j in range(24)]
   # A real 3 mm shell: stock real-time backface culling must retain the
   # dish from both sides. The accepted parabolic front stays in place.
   count=len(vs);front=list(fs)
   vs += [(xx,yy+.003,zz) for xx,yy,zz in vs]
   fs += [tuple(count+i for i in reversed(f)) for f in front]
   rim=1+3*24
   fs += [(rim+j,rim+(j+1)%24,count+rim+(j+1)%24,count+rim+j) for j in range(24)]
   aerial.geom(vs,fs,color=(.30,.32,.28));aerial.beam((x,y-.1,z+.7),(x,y-.54,z+.92),.025,r=0)
   aerial.box((x,y-.54,z+.92),(.07,.11,.07),color=(.1,.11,.085),r=.005)
  aerial.finish()


def landing(b):
 m=b.plan['blocks'][0];o=next(o for o in b.openings if o['kind']=='patio');x=m.x0+o['u'];y=m.y1
 me=b.mesh('Rear_Patio',component='rear_landing');me.box((x,y+1.65,.0508),(4.0,3.30,.1016),'Concrete',r=.005)
 top=m.floor-.028;count=math.ceil((top-.1016)/.18)
 for i in range(count):
  z=top-i*(top-.1016)/count
  me.box((x,y+.46+i*.29,(z+.1016)/2),(2.10-i*.20,.92+i*.58,z-.1016),'Concrete',r=.004)
 me.finish()


def build(plan):
 b=Builder(plan);b.colors['Veneer']=BRICKS[plan['spec']['brick_color']]
 shell(b);doors(b);opening_masonry(b);entry(b);roofs(b);carport(b)
 for o in b.openings:
  if o['kind'] in ('patio','service'):portal(b,o)
 if 'ServiceDoor' in b.moving:b.moving['ServiceDoor']['range_degrees']=[-100,0]
 landing(b);chimney(b);services(b);curled_tabs(b)
 bpy.context.view_layer.update();return b


def curled_tabs(b):
 if b.plan['spec']['roof_age']!='tired':return
 import random
 r=random.Random(991+b.plan['seed']);m=b.plan['blocks'][0]
 me=b.mesh('Weather_CurledTabs',component='curled_tab',allow_boundary=True)
 for j in range(12):
  x=m.x0+.45+r.random()*(m.width-.9);y=m.y0-.05+r.random()*m.depth*.32
  # Scattered tabs, each still attached at its uphill edge. Only 8–15 mm curl.
  w=.16+r.random()*.10;depth=.14;rise=.008+r.random()*.007;vs=[]
  for row in range(4):
   t=row/3;yy=y+t*depth
   for sx in (-1,1):
    xx=x+sx*w/2;vs.append((xx,yy,m.height(xx,yy)+.003+rise*(1-t)**3))
  me.geom(vs,[(i*2,i*2+1,(i+1)*2+1,(i+1)*2) for i in range(3)],'Shingles')
 me.finish()
