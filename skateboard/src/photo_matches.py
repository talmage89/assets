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
    presentation=dict(light='flash',exposure=.2),neutral=(650,680,850,730),
    landmarks=[a(p(0,s.nose_end,height(s,0,s.nose_end)+s.thickness+.00055),(78,449)),
               a(p(0,s.tail_end,height(s,0,s.tail_end)+s.thickness+.00055),(1287,421)),
               a(p(L,-s.axle_y,s.axle_z),(326,615)),a(p(L,s.axle_y,s.axle_z),(1008,618)),
               a(p(-.100,0,.097),(685,408)),a(p(.100,0,.097),(688,546))]),
 'period_used':dict(title='2010 used complete / underside assembly and wheel profile',photo='refs/period-side.jpg',crop=(0,320,3072,1900),location=(-.55,-.8,.6),target=(0,0,.09),lens=36,
    presentation=dict(invert=True,sun_direction=(.45,.25,-.80),sun_energy=2.4,sky_strength=.035,exposure=.85),neutral=(1550,1600,1800,1750),
    landmarks=[a(p(-s.axle_width/2,-s.axle_y,s.axle_z,True),(90,774)),a(p(s.axle_width/2,-s.axle_y,s.axle_z,True),(609,547)),
               a(p(-s.axle_width/2,s.axle_y,s.axle_z,True),(1766,1164)),a(p(s.axle_width/2,s.axle_y,s.axle_z,True),(2198,764))]),
 'period_truck':dict(title='2005 full-size loose street truck / web, seat and cup washers',photo='refs/period-truck.jpg',crop=(0,0,600,420),location=(-.22,-.05,.23),target=(0,-s.plate_y,.046),lens=60,
    presentation=dict(light='window',invert=True,isolate_truck=True,hide_wheels=True,sun_direction=(-.4,.4,-.8),sun_energy=2.2,sky_strength=.12,exposure=-.7),neutral=(350,144,380,151),
    landmarks=[a(p(-s.axle_width/2,-s.axle_y,s.axle_z,True),(25,279)),a(p(s.axle_width/2,-s.axle_y,s.axle_z,True),(551,41)),
               a(p(0,-.201545,.024783,True),(366,136)),
               a(p(-s.pitch_x/2,-s.plate_y-s.pitch_y/2,s.underside-.005,True),(243,261)),
               a(p(s.pitch_x/2,-s.plate_y-s.pitch_y/2,s.underside-.005,True),(350,228))]),
}
