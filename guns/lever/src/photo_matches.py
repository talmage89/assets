"""Manually observed landmarks for comparison cameras, never model input."""
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]


def L(world,pixel,weight=1):return dict(world=[v*.001 for v in world],pixel=pixel,weight=weight)
def match(photo,crop,title,location,target,lens,landmarks):
    return dict(photo=str(BASE/'build/white-balanced'/(photo+'.png')),crop=crop,title=title,
        location=location,target=target,lens=lens,landmarks=landmarks,
        background='transparent',exposure=-.6,lens_bounds_mm=(45,150),
        camera_height_m=(location[2],.01))


MATCHES={
 'right_photo':match('right',(250,248,1950,590),'Right: original uncheckered .30-30 carbine',
    (1.4,.22,.17),(0,.22,.01),70,[
        L((0,708,48),(1908,278),3),L((0,200,48),(1072,281),3),
        L((15.4,65,29),(849,309),2),L((0,-257.2,8),(273,358),2),
        L((0,-257.2,-108),(280,553),2),L((0,282,66),(1180,267)),
        L((0,690,66),(1867,267)),L((18,447,21),(1478,319)),
    ]),
 'left_photo':match('profile',(30,63,1265,307),'Left: class comparison, .375 stock/finish differs',
    (-1.45,.23,.30),(0,.23,.015),70,[
        L((0,708,48),(58,126),3),L((0,200,48),(653,119),3),
        L((-15.4,65,29),(823,138),2),L((0,-257.2,8),(1235,145),2),
        L((0,-257.2,-108),(1231,280),2),L((0,282,66),(595,92)),
        L((0,690,66),(86,97)),L((-18,447,21),(424,134)),
    ]),
 'open_photo':match('receiver',(225,45,880,744),'Open action: lower link, carrier and lever',
    (-.30,.10,.22),(0,.13,-.025),70,[
        L((-15.1,205,48),(250,113),2),L((-15.4,65,29),(664,167),2),
        L((-15.75,185,5),(309,204)),L((-15.75,70,0),(649,227)),
        L((-10.6,200,56),(268,76)),L((-10.6,72,56),(648,93)),
    ]),
 'trigger_right':match('receiver',(390,180,740,445),'Trigger left side: concavity toward photographed muzzle',
    (-.24,.08,.03),(0,.08,-.015),90,[
        L((-15.4,65,0),(663,225)),L((-15.75,140,0),(448,213)),
        L((-15.75,185,5),(309,204)),L((-15.75,74,15),(646,181)),
    ]),
 'trigger_quarter':match('open',(420,250,1010,520),'Trigger oblique: broad blade, angle/scale estimated',
    (-.27,-.06,.15),(0,.08,-.01),90,[
        L((-15.4,65,0),(680,325)),L((-15.75,140,0),(485,287)),
        L((-15.75,185,5),(365,257)),L((-15.75,74,15),(648,281)),
    ]),
}
