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
h=P[71]['holes'][0];L=h['length'];front=halfwidth(h,0);back=halfwidth(h,1)
MATCHES={
 'period_lighthouse':dict(title='2007 in-season adventure course / original quarry course',photo='build/balanced-sunnyvale-2007.png',crop=(0,550,2816,2112),location=(-15,-70,1.8),target=(-7,-5,2.5),lens=42,lens_bounds_mm=(35,55),camera_height_m=(1.8,.6),landmarks=[
 anchor(92,'lighthouse',(0,0,4.73),(1351,810)),anchor(92,'lighthouse',(-.50,-.05,3.58),(1318,886)),anchor(92,'lighthouse',(.50,-.05,3.58),(1377,886)),anchor(92,'lighthouse',(-.80,-.05,.59),(1299,1015)),anchor(92,'lighthouse',(.80,-.05,.59),(1396,1015))]),
 'period_classic_green':dict(title='2011 in-season classic course / shared walks and aged greens',photo='build/balanced-michigan-2011.png',crop=(180,760,3072,2048),location=(-12,-18,1.65),target=(-16,-5,.13),lens=40,lens_bounds_mm=(32,50),camera_height_m=(1.65,.25),landmarks=[
 dict(world=local(h,-front,-L/2,.1298),pixel=(1944,1300)),dict(world=local(h,front,-L/2,.1298),pixel=(2645,1340)),dict(world=local(h,back,L/2,.1298),pixel=(2778,1262)),dict(world=local(h,-back,L/2,.1298),pixel=(2209,1249))]),
 'period_castle':dict(title='2011 landscaped castle course / original six-metre gatehouse',photo='build/balanced-castro-2011.png',crop=(0,900,4000,3000),location=(-22,-30,1.8),target=(-18,-5,3.2),lens=60,lens_bounds_mm=(50,70),camera_height_m=(1.8,.4),landmarks=[
 anchor(92,'castle',(-1.2,0,4.2),(2014,1753)),anchor(92,'castle',(1.2,0,4.2),(2330,1638)),anchor(92,'castle',(-1.2,-.45,0),(2040,2377)),anchor(92,'castle',(1.2,-.45,0),(2343,2307)),anchor(92,'castle',(0,-.915,1.38),(2185,2138),.35)]),
}
SELECTION={'period_lighthouse':(92,'lighthouse'),'period_classic_green':(71,'hole'),'period_castle':(92,'castle')}
LIGHTING={
 'period_lighthouse':dict(sun=(.65,-.65,.9),sun_energy=3.5,sky_strength=.14,exposure=-.25),
 'period_classic_green':dict(sun=(-.8,-.7,.75),sun_energy=3.7,sky_strength=.10,exposure=-.40),
 'period_castle':dict(sun=(-.9,-.7,1.25),sun_energy=4.0,sky_strength=.13,exposure=-.20),
}
