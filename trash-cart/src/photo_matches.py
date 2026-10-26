"""Photo landmarks inspected on a 50 px grid; review camera fit only."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def anchor(p,pixel,w=1):return dict(world=(p[0],p[1]+.041075,p[2]),pixel=pixel,weight=w)
MATCHES={
 'match_front':dict(title='96-gallon cart / front construction',photo=str(ROOT/'refs/cart-004.webp'),crop=(0,0,800,800),location=(2,-3,1.85),target=(0,0,.55),lens=80,hide_assemblies=['AtlasBlueLid'],landmarks=[
  anchor((-.335,-.408,1.038),(156,174)),anchor((.335,-.408,1.038),(407,220)),anchor((.335,.326,1.038),(635,147)),
  anchor((.305,.27385,.127),(553,649)),
  anchor((-.105,-.336,.535),(276,447)),anchor((.105,-.336,.535),(355,474))]),
 'match_back':dict(title='96-gallon cart / rear hinge and axle',photo=str(ROOT/'refs/cart-006.webp'),crop=(0,0,1000,1000),location=(2.4,3.5,1.9),target=(0,0,.55),lens=85,hide_assemblies=['AtlasBlueLid'],landmarks=[
  anchor((.335,-.408,1.038),(182,131)),anchor((.335,.326,1.038),(536,190)),anchor((-.335,.326,1.038),(810,160)),
  anchor((.305,.27385,.127),(423,790)),anchor((-.305,.27385,.127),(685,726))])
}
