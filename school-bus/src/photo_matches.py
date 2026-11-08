"""Hand-measured landmarks on four service photographs, never traced.

Pixels below were read on a 1400px-wide comparison grid; expanded to originals.
They fit vehicle class and camera only. Different bodies/lengths remain visible.
"""
from pathlib import Path
from PIL import Image
import spec as S
BASE=Path(__file__).resolve().parents[1]
def match(photo,title,location,target,lens,world,pixels):
    path=BASE/'build/balanced'/photo;w,h=Image.open(path).size;scale=w/1400
    return dict(photo=str(path),title=title,crop=tuple(round(v) for v in (-w*.10,-h*.06,w*1.10,h*1.06)),location=location,target=target,lens=lens,
        lens_bounds_mm=(20,100),camera_height_m=(1.65,.8),background='transparent',
        exposure={'service-front.jpg':2.6,'used-long-side.jpg':2.7,'service-rear.jpg':2.2,'vision-service.jpg':2.4}[photo],
        landmarks=[dict(world=p,pixel=(u*scale,v*scale)) for p,(u,v) in zip(world,pixels)])
F,R,H=S.FRONT_AXLE,S.REAR_AXLE,S.HUB
MATCHES={
 'service_front':match('service-front.jpg','Period Type C / front in service',(8,-12,1.6),(0,-1,1.5),40,
    [(1.015,F,H),(1.057,R,H),(1.155,F,0),(1.196,R,0),(-1.138,-3.70,2.672),(1.138,-3.70,2.672)],
    [(763,719),(1259,622),(762,872),(1256,698),(402,191),(872,148)]),
 'service_side':match('used-long-side.jpg','Used 77-passenger Type C / long body',(14,-1,1.65),(0,0,1.5),50,
    [(1.015,F,H),(1.057,R,H),(1.155,F,0),(1.196,R,0),
     (1.219,-3.92,2.71),(1.219,6.006,2.71),(1.219,-3.92,.70),(1.219,6.006,.70)],
    [(110,615),(882,632),(109,671),(888,690),(185,396),(1384,397),(185,616),(1383,620)]),
 'service_rear':match('service-rear.jpg','2010 Type C / rear in later service',(-11,15,1.7),(0,1,1.6),45,
    [(-1.015,F,H),(-1.057,R,H),(-1.155,F,0),(-1.196,R,0),(-1.219,6.006,2.71),(1.219,6.006,2.71)],
    [(1314,390),(721,421),(1317,451),(719,510),(211,104),(18,123)]),
 'vision_front':match('vision-service.jpg','Second maker / compound hood and optics in service',(-8,-12,1.6),(0,-1,1.5),45,
    [(-1.015,F,H),(-1.057,R,H),(-1.155,F,0),(-1.196,R,0),(-1.138,-3.70,2.672),(1.138,-3.70,2.672)],
    [(772,698),(317,583),(794,799),(319,645),(704,292),(1024,324)]),
}
