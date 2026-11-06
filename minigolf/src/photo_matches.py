"""Period photographic framing for different original fixtures and lanes.

Landmarks are approximate homologous silhouette points, not a survey of the
photographed course. Residuals are retained; original scales are never changed.
"""
from pathlib import Path
from plan import center,halfwidth
import json
rows=json.loads(Path('build/manifest.json').read_text());classic=next(r for r in rows if r['kind']=='classic');h=classic['plan']['holes'][0];w=h['width'];L=h['length'];front=halfwidth(h,0);back=halfwidth(h,1)
MATCHES={
 'period_lighthouse':dict(title='2007 lighthouse / original functional ball tunnel',photo='build/balanced-sunnyvale-2007.png',crop=(1200,720,1480,1160),location=(1.3,-8,2),target=(0,0,2),lens=55,lens_bounds_mm=(35,100),camera_height_m=(1.65,.25),landmarks=[
  dict(world=(0,0,4.73),pixel=(1351,810)),dict(world=(-.50,-.05,3.58),pixel=(1318,886)),dict(world=(.50,-.05,3.58),pixel=(1377,886)),dict(world=(-.80,-.05,.59),pixel=(1299,1015)),dict(world=(.80,-.05,.59),pixel=(1396,1015))]),
 'period_classic_green':dict(title='2011 timber-edged green / original concrete-border hole',photo='build/balanced-michigan-2011.png',crop=(1800,1100,2920,1500),location=(3,-9,1.65),target=(0,0,.13),lens=45,lens_bounds_mm=(35,100),camera_height_m=(1.65,.25),landmarks=[
  dict(world=(-front,-L/2,.1298),pixel=(1944,1300)),dict(world=(front,-L/2,.1298),pixel=(2645,1340)),dict(world=(back,L/2,.1298),pixel=(2778,1262)),dict(world=(-back,L/2,.1298),pixel=(2209,1249))]),
 'period_castle':dict(title='2011 themed turrets / original small castle ball gateway',photo='build/balanced-castro-2011.png',crop=(1500,1400,2700,2600),location=(4,-8,1.65),target=(0,0,1.3),lens=50,lens_bounds_mm=(35,100),camera_height_m=(1.65,.25),landmarks=[
  dict(world=(-.8,0,2.80),pixel=(2014,1753)),dict(world=(.8,0,2.80),pixel=(2330,1638)),dict(world=(-.8,-.30,0),pixel=(2040,2377)),dict(world=(.8,-.30,0),pixel=(2343,2307)),dict(world=(0,-.61,.92),pixel=(2185,2138),weight=.35)]),
}
SELECTION={'period_lighthouse':(92,'lighthouse'),'period_classic_green':(71,'hole'),'period_castle':(92,'castle')}
LIGHTING={
 'period_lighthouse':dict(sun=(.65,-.65,.9),sun_energy=3.5,sky_strength=.14,exposure=-.25),
 'period_classic_green':dict(sun=(-.8,-.7,.75),sun_energy=3.7,sky_strength=.10,exposure=-.40),
 'period_castle':dict(sun=(-.9,-.7,1.25),sun_energy=4.0,sky_strength=.13,exposure=-.20),
}
