"""Low-angle unibody AWD construction, inside the 205 mm clearance target."""
import bpy,math
from kit import model as G
from detail_helpers import box,tube
import suv_spec as S


def build(b):
 # Pressed unibody longitudinals and two bolted cradle/subframe assemblies.
 for s in [-1,1]:
  rows=[]
  for y,z in [(-1.90,.40),(-1.45,.40),(-.95,.35),(.65,.35),(1.12,.46),(1.75,.47),(2.06,.43)]:
   rows.append([(s*.46+dx,y,z+dz) for dx,dz in [(-.035,-.035),(.035,-.035),(.035,.035),(-.035,.035)]])
  b.add(G.loft('Unibody rail '+str(s),rows,b.m['frame']),category='underbody')
 for end,y in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
  for dy in [-.22,.22]:box(b,'Subframe crossmember '+end+str(dy),(0,y+dy,.31),(.94,.055,.060),b.m['frame'],'underbody',radius=.008)
  for s in [-1,1]:
   tube(b,'Subframe side '+end+str(s),[(s*.44,y-.25,.33),(s*.47,y,.32),(s*.44,y+.25,.33)],.032,b.m['frame'],'underbody',sides=6)
   tube(b,'Control arm '+end+str(s),[(s*.48,y-.20,.32),(s*.68,y,.32),(s*.48,y+.20,.32)],.023,b.m['frame'],'underbody',sides=6)
   tube(b,'Halfshaft '+end+str(s),[(s*.12,y,S.HUB_HEIGHT),(s*.69,y,S.HUB_HEIGHT)],.018,b.m['caliper'],'underbody',sides=6)
   tube(b,'Strut '+end+str(s),[(s*.56,y,.76),(s*.65,y,.38)],.029,b.m['frame'],'underbody',sides=8)
   parent=bpy.data.objects['Steer_F'+('L' if s<0 else 'R')] if end=='F' else b.root
   tube(b,'Hub spindle '+end+str(s),[(s*.68,y,S.HUB_HEIGHT),(s*.81,y,S.HUB_HEIGHT)],.027,b.m['caliper'],'underbody',parent,sides=6)
 diff=G.lathe('AWD rear differential',[(-.13,0),(-.13,.08),(-.07,.145),(.07,.145),(.13,.08),(.13,0)],b.m['caliper'],16,axis='X',center=(S.REAR_AXLE,.35));b.add(diff,category='underbody')
 tube(b,'AWD propshaft',[(0,-1.08,.32),(0,.03,.30),(0,1.20,.35)],.027,b.m['frame'],'underbody',sides=8)
 box(b,'Transverse engine',(0,-1.47,.69),(.63,.52,.37),b.m['caliper'],'underbody',radius=.045)
 box(b,'Engine cover',(0,-1.46,.885),(.56,.46,.045),b.m['plastic'],'underbody',radius=.025)
 box(b,'Transaxle',(-.35,-1.34,.53),(.30,.40,.25),b.m['caliper'],'underbody',radius=.040)
 box(b,'Front sump',(0,-1.48,.43),(.40,.35,.08),b.m['frame'],'underbody',radius=.016)
 box(b,'Radiator',(0,-1.99,.66),(1.02,.06,.40),b.m['frame'],'underbody',radius=.01)
 box(b,'Fuel tank',(-.25,.53,.36),(.54,.63,.16),b.m['plastic'],'underbody',radius=.035)
 for y in [.30,.76]:box(b,'Tank strap '+str(y),(-.25,y,.275),(.55,.03,.009),b.m['frame'],'underbody',radius=0)
 tube(b,'Exhaust',[(.20,-1.57,.53),(.25,-1.06,.28),(.29,.52,.27),(.32,1.25,.45),(.47,1.75,.37),(.62,2.20,.38)],.025,b.m['brake'],'underbody',sides=8)
 box(b,'Muffler',(.40,1.80,.37),(.38,.37,.16),b.m['brake'],'underbody',radius=.035)
 for y in [-.77,.55,1.68]:tube(b,'Exhaust hanger '+str(y),[(.29,y,.29),(.40,y,.38)],.006,b.m['frame'],'underbody',sides=5)
 ob=G.lathe('Exhaust rolled tip',[(2.12,.037),(2.22,.037),(2.22,.034),(2.12,.034)],b.m['dark_chrome'],16,axis='Y',center=(.62,.38),closed=True);b.add(ob,category='underbody')
 box(b,'Front crash beam',(0,-2.13,.63),(1.36,.07,.10),b.m['frame'],'underbody',radius=.008)
 box(b,'Rear crash beam',(0,2.11,.61),(1.35,.06,.09),b.m['frame'],'underbody',radius=.008)
