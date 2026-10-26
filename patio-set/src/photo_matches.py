"""Measured source-photo landmarks; camera estimation never changes our geometry.

The 252×268 manufacturer chair photograph is embedded in foxhill.pdf (p2).
Inspection follows the original photograph, not an inferred outline mesh.
"""
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def m(name,p,uv,w=1):return dict(name=name,world=(p[0]-1.45,p[1],p[2]),pixel=uv,weight=w)
MATCHES={'sling_chair':dict(photo=str(P/'refs/foxhill-photo-000.jpg'),crop=(0,0,252,268),
 title='Sling chair / bent frame, seat tension and fabric',
 location=(-3.2,-2.7,1.6),target=(-1.45,0,.48),lens=65,
 hide_assemblies=['Table','Chaise','Umbrella_Open','Umbrella_Closed'],background='alpha',exposure=-.25,
 landmarks=[
 m('Near crown',(-.277,.325,.945),(7,24),2),m('Far crown',(.277,.325,.945),(105,10),2),
 m('Near front foot',(-.309,-.334,.008),(149,262),2),m('Near rear foot',(-.309,.345,.008),(32,234),2),
 m('Far front foot',(.309,-.334,.008),(246,211),2),m('Far rear foot',(.309,.345,.008),(125,193)),
 m('Near arm bend',(-.309,-.292,.607),(139,113)),m('Far arm bend',(.309,-.292,.607),(241,88)),
 m('Near arm return',(-.309,.235,.613),(9,78)),m('Far arm return',(.309,.235,.613),(121,54))])}

# Installed, visibly used cafe set: table mineral spotting/leg scuffs and canopy
# seam/valance contrast. Age and exact size are unknown; dimensions here are our
# original design, so the residual explicitly includes design differences.
import runpy
D=runpy.run_path(str(Path(__file__).with_name('config.py')))['DINING']
S=1600/1280
MATCHES['used_set']=dict(photo=str(P/'refs/installed-used.jpg'),crop=(0,0,1600,2000),
 title='Installed used set / fading and outdoor deposits',
 location=(.3,-4,1.7),target=(0,0,1.2),lens=50,background='alpha',exposure=-.35,
 parts={**D['parts'],'Umbrella_Open':dict(translation=(.85,.35,0))},instances=D['instances'],
 hide_assemblies=['Chaise','Umbrella_Closed'],
 landmarks=[dict(name=name,world=p,pixel=(u*S,v*S),weight=w) for name,p,u,v,w in [
 ('Near left table corner',(-.762,-.4826,.762),83,1188,2),
 ('Near right table corner',(.762,-.4826,.762),731,1201,2),
 ('Near left table foot',(-.694,-.406,.013),109,1522,2),
 ('Near right table foot',(.694,-.406,.013),704,1522,2)]])
