"""Wider in-season course comparisons, calibrated on actual placed fixtures.

Homologous landmarks compare original designs, never manufacture a replica.
Native residuals remain visible. Crop transforms are handled by the kit.
"""
from pathlib import Path
import json,math
from plan import local,center,level,halfwidth
rows=json.loads(Path('build/manifest.json').read_text())
P={r['seed']:r['plan'] for r in rows}
def fixture_point(seed,kind,q):
 h=next(h for h in P[seed]['holes'] if h['fixture']==kind);cx,cy=center(h,.49);z=level(h,cx,.49)+.005
 return local(h,cx+q[0],cy+q[1],z+q[2])
def anchor(seed,kind,q,p,weight=1):return dict(world=fixture_point(seed,kind,q),pixel=p,weight=weight)
h=P[71]['holes'][0];L=h['length'];front=halfwidth(h,0)+.08;back=halfwidth(h,1)+.08
MATCHES={
 'period_lighthouse':dict(title='2007 course crop / upper crossing and water',photo='build/balanced-sunnyvale-2007.png',crop=(950,650,1750,1900),location=(-4,3.5,3.32),target=(0,24,3.3),lens=42,lens_bounds_mm=(42,42),camera_height_m=(3.32,.04),landmarks=[
 anchor(92,'lighthouse',(0,0,4.73),(1351,810)),anchor(92,'lighthouse',(.52*math.cos(7*math.pi/16),.52*math.sin(7*math.pi/16),3.22),(1318,886)),anchor(92,'lighthouse',(-.52*math.cos(7*math.pi/16),-.52*math.sin(7*math.pi/16),3.22),(1377,886)),anchor(92,'lighthouse',((.85-.35*.01/2.59)*math.cos(7*math.pi/16),(.85-.35*.01/2.59)*math.sin(7*math.pi/16),.65),(1299,1015)),anchor(92,'lighthouse',(-(.85-.35*.01/2.59)*math.cos(7*math.pi/16),-(.85-.35*.01/2.59)*math.sin(7*math.pi/16),.65),(1396,1015))]),
 'period_classic_green':dict(title='2011 in-season classic course / shared walks and aged greens',photo='build/balanced-michigan-2011.png',crop=(180,760,3072,2048),location=(-12,-18,1.65),target=(-16,-5,.13),lens=40,lens_bounds_mm=(32,50),camera_height_m=(1.65,.25),landmarks=[
 dict(world=local(h,-front,-L/2,.2774),pixel=(1944,1300)),dict(world=local(h,front,-L/2,.2774),pixel=(2645,1340)),dict(world=local(h,back,L/2,.2774),pixel=(2778,1262)),dict(world=local(h,-back,L/2,.2774),pixel=(2209,1249))]),
 'period_castle':dict(title='2011 landscaped castle course / original six-metre gatehouse',photo='build/balanced-castro-2011.png',crop=(0,900,4000,3000),location=(-34.43,37.36,1.8),target=(-10.81,4.68,2.8),lens=60,lens_bounds_mm=(50,70),camera_height_m=(1.8,.4),landmarks=[
 # Visible front-gate roof tips and eave centers. The old inferred ground
 # anchors were hidden by the fence, and the left roof tip was misplaced.
 anchor(71,'castle',(-1.2,0,4.2),(2014,1680)),anchor(71,'castle',(1.2,0,4.2),(2330,1620)),anchor(71,'castle',(-1.2,0,3.03),(2023,1920)),anchor(71,'castle',(1.2,0,3.03),(2338,1876))]),
}
SELECTION={'period_lighthouse':(92,'lighthouse'),'period_classic_green':(71,'hole'),'period_castle':(71,'castle')}
LIGHTING={
 'period_lighthouse':dict(sun=(.65,-.65,.9),sun_energy=6.5,sky_strength=.08,exposure=-.25),
 'period_classic_green':dict(sun=(.8,.7,.75),sun_energy=8.0,sky_strength=.08,exposure=-.40),
 'period_castle':dict(sun=(-.9,-.7,1.25),sun_energy=7.4,sky_strength=.075,exposure=-.20),
}
