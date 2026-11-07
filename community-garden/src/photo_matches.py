"""Measured review landmarks. Unsurveyed gardens: along-edge phases are inferred.

Pixel coordinates refer to prepared 1024px wide copies, avoiding false subpixel
precision from oversized originals. The source photographs remain untouched.
"""
from pathlib import Path
P=Path('build/photo-references')
MATCHES={
    'wise_bed':dict(title='Mature raised bed / July 2010',photo=str(P/'wise.jpg'),crop=(0,0,1024,768),
        location=(-2.3,-4.2,1.65),target=(0,0,.55),lens=38,lens_bounds_mm=(28,65),camera_height_m=(1.65,.30),
        landmarks=[
            dict(world=[-.6096,-1.2192,.23495],pixel=[153,561],weight=1),
            dict(world=[.6096,-1.2192,.23495],pixel=[420,607],weight=1),
            dict(world=[.6096,1.2192,.23495],pixel=[690,466],weight=1),
            dict(world=[-.6096,1.2192,.23495],pixel=[493,410],weight=.25)],
        exposure=-.35),
    'oliver_construction':dict(title='Bed construction / August installation',photo=str(P/'oliver.jpg'),crop=(0,0,1024,768),
        location=(.30,-2.5,1.75),target=(0,0,.22),lens=40,lens_bounds_mm=(28,65),camera_height_m=(1.75,.25),
        landmarks=[
            dict(world=[-.55,1.20,.23495],pixel=[486,248],weight=.6),
            dict(world=[.55,1.20,.23495],pixel=[754,232],weight=.6),
            dict(world=[.57,.8,.23495],pixel=[807,314],weight=.35),
            dict(world=[.57,-1.2,.23495],pixel=[923,750],weight=.35),
            dict(world=[.6096,-.8,.23495],pixel=[932,646],weight=.3),
            dict(world=[.6096,-.8,.16],pixel=[944,659],weight=.3)],
        exposure=-.35),
    'martin_place':dict(title='Neighborhood entrance / July 2009',photo=str(P/'martin.jpg'),crop=(0,0,1024,768),
        location=(3.2,-20,1.65),target=(3.4,-10,1.3),lens=40,lens_bounds_mm=(30,60),camera_height_m=(1.65,.15),
        landmarks=[
            dict(world=[3.4-.525,-12.192+.218,1.45+.33],pixel=[486,369]),
            dict(world=[3.4+.525,-12.192+.218,1.45+.33],pixel=[639,370]),
            dict(world=[3.4+.525,-12.192+.218,1.45-.33],pixel=[632,467]),
            dict(world=[3.4-.525,-12.192+.218,1.45-.33],pixel=[486,467]),
            dict(world=[3.4-.441,-12.192+.25,.05],pixel=[500,659],weight=.5),
            dict(world=[3.4+.441,-12.192+.25,1.90],pixel=[619,346],weight=.5)],
        exposure=-.35)
}
