"""Downtown pavement and parking. Ground's 152.4 mm curb datum is retained."""
import math
from geometry import Batch,pivot

def build_street(p,mats):
 root=pivot('DowntownStreet_'+p['region'],(0,0,0),street=True,static_root=True)
 b=Batch(root.name,root,mats);W=p['width'];walk=p['walk'];road=p['road_width'];a=-W/2-walk;c=W/2+walk
 curb=-walk;far=curb-road
 b.box((0,(curb+far)/2,-.20),(W+24,road,.095),'Roof',(.065,.067,.065))
 pits=[-W/2+6+i*13 for i in range(max(1,round((W-8)/13)))];pit=1.35;py=curb+1.05
 cuts=sorted({a,c,*[x+s*pit/2 for x in pits for s in (-1,1)]})
 for x0,x1 in zip(cuts,cuts[1:]):
  n=max(1,math.ceil((x1-x0)/1.524));dx=(x1-x0)/n
  for j in range(n):
   xx=x0+(j+.5)*dx;is_pit=any(abs(xx-x)<pit/2 for x in pits)
   spans=[(curb,py-pit/2),(py+pit/2,0)] if is_pit else [(curb,0)]
   for ya,yc in spans:
    nn=max(1,math.ceil((yc-ya)/1.524));dy=(yc-ya)/nn
    for k in range(nn):b.box((xx,ya+(k+.5)*dy,-.065),(dx-.005,dy-.005,.13),'Mineral',(.43,.43,.41))
 for xx in pits:
  b.box((xx,py,-.078),(pit,pit,.055),'Finish',(.075,.057,.033));pivot('Socket_TreePit_'+str(round(xx,3)),(xx,py,0),root,socket_kind='tree_pit')
  for side in (-1,1):
   for j in range(7):b.box((xx+side*(.26+j*.057),py,-.015),(.022,pit-.06,.025),'Finish',(.055,.055,.044))
  for yy in (py-pit/2,py+pit/2):b.box((xx,yy,-.014),(pit,.03,.028),'Finish',(.055,.055,.044))
 b.box((0,far-walk/2,-.075),(W+24,walk,.15),'Mineral',(.43,.43,.41))
 for y in (curb,far):
  for i in range(math.ceil((c-a)/1.524)):
   b.box((a+(i+.5)*1.524,y-.08 if y==curb else y+.08,-.0762),(1.52,.16,.1524),'Mineral',(.40,.40,.38))
 # Corner returns and the cut-off corner's triangular pedestrian apron.
 D=max(l['depth'] for l in p['lots'])
 for side,lot in ((-1,p['lots'][0]),(1,p['lots'][-1])):
  edge=side*W/2;xx=edge+side*walk/2;n=math.ceil((D+1)/1.524);dy=(D+1)/n
  for j in range(n):b.box((xx,(j+.5)*dy,-.065),(walk-.005,dy-.005,.13),'Mineral',(.43,.43,.41))
  ch=lot['chamfer'];b.prism([(edge,0,0),(edge-side*ch,0,0),(edge,ch,0)],(0,0,-.13),'Mineral',(.43,.43,.41))
  outer=edge+side*walk
  for j in range(math.ceil((D+1-curb)/1.524)):
   b.box((outer,curb+(j+.5)*1.524,-.0762),(.16,1.52,.1524),'Mineral',(.40,.40,.38))
  b.box((outer+side*3.5,(curb+D+8)/2,-.20),(7.0,D+8-curb,.095),'Roof',(.065,.067,.065))
 marks=[]
 if p['parking']=='parallel':
  for x in [a+3+i*6.40 for i in range(int((c-a-6)/6.40))]:
   for dx in (-2.9,2.9):b.box((x+dx,curb-1.20,-.1508),(.09,2.40,.0015),'Finish',(.61,.58,.46))
   marks.append(dict(x=x,y=curb-1.33,yaw=90))
 else:
  for x in [a+3+i*3.35 for i in range(int((c-a-7)/3.35))]:
   b.beam((x,curb-.22,-.1508),(x+2.65,curb-4.81,-.1508),.085,.0015,color=(.61,.58,.46));marks.append(dict(x=x+2.60,y=curb-2.55,yaw=30))
 for x in range(math.floor(a),math.ceil(c),5):b.box((x,(curb+far)/2,-.1508),(2.1,.085,.0015),'Finish',(.55,.39,.045))
 D=max(l['depth'] for l in p['lots']);b.box((0,D+4,-.08),(W+14,7.0,.16),'Roof',(.083,.080,.071))
 for lot in p['lots']:
  gap=D+1-lot['depth']
  if gap>0:b.box((lot['x'],lot['depth']+gap/2,-.065),(lot['width'],gap,.13),'Mineral',(.25,.24,.20))
 ob=b.finish();ob.data.calc_loop_triangles()
 return root,dict(triangles=len(ob.data.loop_triangles),pits=[(x,py,0) for x in pits],parking=marks,curb=curb,opposite=far-walk*.55)
