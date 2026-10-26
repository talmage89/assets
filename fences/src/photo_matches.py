"""Manually inspected construction landmarks; no image-to-geometry tracing.

The photo is cedar, used for rail spacing/joinery and lens fit. Its bay length
is inferred as 8 ft: no survey or EXIF is available. The measured fit residual
includes different rail placement and partial foreground occlusion.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def a(world,pixel,weight=1):
    # A rail-side camera mirrors the fence X direction on the image.
    world=(-2.4384-world[0],world[1],world[2])
    return dict(world=world,pixel=pixel,weight=weight)
MATCHES={'match_rails':dict(title='Three-rail construction / aged pine versus cedar reference',
 photo=str(ROOT/'refs/cedar_fence_rails_pickets_denver.jpg'),crop=(235,150,710,570),
 location=(1.3,6.8,1.65),target=(-1.15,0,1.0),lens=55,
 studio_yaw=180,hide_assemblies=['Section_B','Post_Corner','Gate_Bay'],exposure=-1.15,
 landmarks=[
 a((-2.4384,.01905,1.73355),(270,210)),a((0,.01905,1.73355),(663,214)),
 a((-2.4384,.01905,.9652),(270,364)),a((0,.01905,.9652),(663,336)),
 a((-2.4384,.01905,.19685),(270,532),.7),a((-.35,.01905,.19685),(616,466),.5),
 a((-2.4384,0,1.84),(270,175),.5),a((0,0,1.84),(663,190),.5)])}
