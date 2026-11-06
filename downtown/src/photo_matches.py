"""Measured photographic landmarks for three original-family comparisons.

These are matching bays and street planes, not copied/traced facades. Dimensions
belong to our authored plans. Residuals disclose different proportions. Photos
are low-resolution public-domain HABS service images; estimated lenses only.
"""
from plan import generate


def bounds(region,index):
 p=generate({'midwest':411,'northeast':613}[region],region);b=p['lots'][index]
 return b,b['x']-b['width']/2,b['x']+b['width']/2

b,l,r=bounds('northeast',3);h=b['height'];f=b['floor_first'];u=b['upper']
# Left commercial frontage of the Foster facade (four upper sashes). Single
# frontage compared, rather than pretending our original row duplicates HABS.
MATCHES={
 'foster':dict(region='northeast',photo='refs/foster.jpg',crop=(85,20,365,422),title='Three-story cast-front proportions / HABS IN-86',
   location=((l+r)/2,-22,5.2),target=((l+r)/2,0,5.6),lens=43,lens_bounds_mm=(25,100),
   landmarks=[dict(world=(l,0,0),pixel=(124,397)),dict(world=(r,0,0),pixel=(346,396)),
     dict(world=(l,0,h),pixel=(116,42)),dict(world=(r,0,h),pixel=(344,42)),
     dict(world=(l,0,f),pixel=(123,279)),dict(world=(r,0,f),pixel=(346,279)),
     dict(world=(l,0,f+u),pixel=(120,184)),dict(world=(r,0,f+u),pixel=(345,184))]),
}
b,l,r=bounds('northeast',0);h=b['height'];dep=b['depth'];ch=b['chamfer'];
# Three-quarter row: first corner height, front width and receding street line.
MATCHES['mulberry']=dict(region='northeast',photo='refs/mulberry.jpg',crop=(13,22,625,438),title='Row height and street wall / HABS IN-11',
 location=(-55,-32,3.4),target=(-5,0,5),lens=40,lens_bounds_mm=(24,85),
 landmarks=[dict(world=(l+ch,0,0),pixel=(137,409)),dict(world=(r,0,0),pixel=(261,392)),
  dict(world=(l+ch,0,h),pixel=(135,148)),dict(world=(r,0,h),pixel=(266,191)),
  dict(world=(l+ch,0,b['floor_first']),pixel=(139,315)),dict(world=(r,0,b['floor_first']),pixel=(264,310)),
  dict(world=(r+18,0,0),pixel=(438,366)),dict(world=(r+18,0,h-.6),pixel=(440,243))])
b,l,r=bounds('midwest',2)
n=max(2,round((b['width']-.6)/1.95));x=l+b['width']/n/2;lo=b['floor_first']+.65;hi=lo+b['window_height']
MATCHES['madison']=dict(region='midwest',photo='refs/madison.jpg',crop=(82,150,171,376),title='Window reveal and sash / HABS IN-231 detail',
 location=(x-4,-5,6.2),target=(x,0,(lo+hi)/2),lens=50,lens_bounds_mm=(25,100),
 landmarks=[dict(world=(x-.51,0,lo),pixel=(105,329)),dict(world=(x+.51,0,lo),pixel=(137,350)),
  dict(world=(x-.51,0,hi),pixel=(105,194)),dict(world=(x+.51,0,hi),pixel=(137,222)),
  dict(world=(x-.51,0,(lo+hi)/2),pixel=(105,261)),dict(world=(x+.51,0,(lo+hi)/2),pixel=(137,286))])

# Color references are separate from the monochrome HABS form checks.
# Landmark coordinates refer to the original pixels, never texture projection.
b,l,r=bounds('midwest',0);h=b['height'];ch=b['chamfer']
MATCHES['auburn_block']=dict(region='midwest',photo='refs/auburn-color.jpg',crop=(0,520,3430,2240),title='Used Main Street / Auburn 2012 / original row comparison',
 location=(-52,-26,1.7),target=(-5,0,4),lens=38,lens_bounds_mm=(24,70),camera_height_m=(1.7,.5),
 neutral=(180,2075,250,2095),sun_direction=(.72,.52,-.62),sun_elevation=36,exposure=-.20,context=True,
 landmarks=[dict(world=(l+ch,0,0),pixel=(300,2050)),dict(world=(r,0,0),pixel=(995,1980)),
 dict(world=(l+ch,0,h),pixel=(300,625)),dict(world=(r,0,h),pixel=(995,865)),
 dict(world=(r+16,0,0),pixel=(2220,1810)),dict(world=(r+16,0,h-.3),pixel=(2220,1355))])
# Supersedes two rejected fits: the Auburn display crop had an implausible
# elevated camera; Galena's tiny landmarks touched a sign rather than the sash.
# Keep those earlier evidence files in ignored history, not active calibration.
b,l,r=bounds('northeast',3);base=b['floor_first']+b['upper'];x=l+b['width']/8;lo=base+.65;hi=lo+b['window_height']
MATCHES['louisiana_upper']=dict(region='northeast',photo='refs/louisiana-color.jpg',crop=(600,650,1520,2200),title='Used painted brick, hood and pressed cornice / Louisiana 2015',
 location=(x-6,-9,1.65),target=(x,0,lo+1),lens=45,lens_bounds_mm=(24,240),
 neutral=(836,1222,849,1233),sun_energy=0.,sky_strength=.30,exposure=-.15,
 landmarks=[dict(world=(x-.37,.125,hi-.1),pixel=(756,1355)),dict(world=(x+.37,.125,hi-.1),pixel=(941,1369)),
 dict(world=(x-.37,.125,lo+.1),pixel=(734,1978)),dict(world=(x+.37,.125,lo+.1),pixel=(915,1990))])
