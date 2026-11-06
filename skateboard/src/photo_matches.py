"""Manually inspected photo landmarks, never image-derived meshes or textures.
Unknown complete-board sizes are normalized to our default class; residuals
include their real shape differences. No lens is claimed as recovered EXIF.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
from spec import spec,height
s=spec();L=s.axle_width/2-.0206
lift=height(s,0,s.nose_end)+s.thickness+.00055

def p(x,y,z,inv=False):return (x,-y,lift-z) if inv else (x,y,z)
def a(world,pixel):return dict(world=world,pixel=pixel)
MATCHES={
 'period_horizontal':dict(title='2006 street board / kick transition and stance concave',photo='refs/period-horizontal.jpg',crop=(35,350,1320,695),location=(1.1,-.08,.45),target=(0,0,.09),lens=55,
    presentation=dict(light='flash',exposure=-.6),neutral=(650,680,850,730),
    landmarks=[a(p(0,s.nose_end,height(s,0,s.nose_end)+s.thickness+.00055),(78,449)),
               a(p(0,s.tail_end,height(s,0,s.tail_end)+s.thickness+.00055),(1287,421)),
               a(p(L,-s.axle_y,s.axle_z),(326,615)),a(p(L,s.axle_y,s.axle_z),(1008,618)),
               a(p(-.100,0,.097),(685,408)),a(p(.100,0,.097),(688,546))]),
 'period_used':dict(title='2010 used complete / underside assembly and wheel profile',photo='refs/period-side.jpg',crop=(0,320,3072,1900),location=(-.55,-.8,.6),target=(0,0,.09),lens=36,
    presentation=dict(invert=True,sun_direction=(.45,.25,-.80),sun_energy=2.4,sky_strength=.035,exposure=.85),neutral=(1550,1600,1800,1750),
    landmarks=[a(p(-s.axle_width/2,-s.axle_y,s.axle_z,True),(90,774)),a(p(s.axle_width/2,-s.axle_y,s.axle_z,True),(609,547)),
               a(p(-s.axle_width/2,s.axle_y,s.axle_z,True),(1766,1164)),a(p(s.axle_width/2,s.axle_y,s.axle_z,True),(2198,764))]),
 'period_mini':dict(title='2008 complete / close truck construction (mini deck)',photo='refs/period-mini.jpg',crop=(350,80,2900,2100),location=(-.35,-.10,.48),target=(0,.22,.09),lens=65,
    presentation=dict(invert=True,sun_direction=(.3,-.5,-.76),sun_energy=2.6,sky_strength=.025,exposure=.85),neutral=(120,400,300,650),
    landmarks=[a(p(-.100,-s.axle_y,s.axle_z,True),(1629,1784)),a(p(.069,-s.axle_y,s.axle_z,True),(2425,610)),
               a(p(-s.pitch_x/2,-s.plate_y-s.pitch_y/2,s.underside-.006,True),(1769,1471)),
               a(p(s.pitch_x/2,-s.plate_y-s.pitch_y/2,s.underside-.006,True),(1919,1079)),
               a(p(-s.pitch_x/2,-s.plate_y+s.pitch_y/2,s.underside-.006,True),(2340,1682)),
               a(p(s.pitch_x/2,-s.plate_y+s.pitch_y/2,s.underside-.006,True),(2626,1331))]),
}
