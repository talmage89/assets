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
    (-3.0,.10,2.8),(0,.13,-.025),650,[
        L((-15.1,205,48),(250,113),2),L((-15.4,65,29),(664,167),2),
        L((-15.75,185,5),(309,204)),L((-15.75,70,3.8),(649,227)),
        L((-10.6,200,56),(268,76)),L((-10.6,72,56),(648,93)),
    ]),
 'trigger_right':match('receiver',(390,180,740,445),'Trigger left side: concavity toward photographed muzzle',
    (-.24,.08,.03),(0,.08,-.015),90,[
        L((-15.4,65,0),(663,225)),L((-15.75,140,0),(448,213)),
        L((-15.75,185,5),(309,204)),L((-15.75,74,15),(646,181)),
    ]),
 'trigger_quarter':match('open',(420,250,1010,520),'Trigger oblique: broad blade, angle/scale estimated',
    (-1.4,-.3,.55),(0,.08,.02),150,[
        L((-15.4,65,4),(448,323)),L((-15.75,70,56),(424,193)),
        L((-10.6,72,56),(414,158)),L((-10.6,195,56),(5,143)),
        L((-15.75,156,-.5),(174,320)),
    ]),
}

# The previous oblique fit mislabeled wood points as receiver corners. These
# native corners belong to the action. Use one action fit for both close-ups.
MATCHES['trigger_quarter']['crop']=(300,275,785,490)
MATCHES['trigger_quarter']['lens_bounds_mm']=(45,400)
MATCHES['hammer_photo']=dict(MATCHES['trigger_quarter'],crop=(350,115,630,280),
    title='Hammer: curved body, returning spur and fine thumb checkering')
MATCHES['hammer_photo'].update(lens=380,lens_bounds_mm=(80,900),target=(0,.052,.05))
MATCHES['lever_rest_photo']=dict(MATCHES['trigger_quarter'],crop=(290,300,790,495),
    title='Lever at rest: continuous forging and long finger opening')
MATCHES['open_photo']['lens_bounds_mm']=(80,1400)
MATCHES['used_photo']=match('open2',(0,110,1024,400),'Used right action: brown-plum oxide, gray edge rubs and handled walnut',
    (1.1,-.13,.40),(0,.14,.02),110,[
        L((15.75,70,56),(374,190),2),L((15.75,190,56),(704,193),2),
        L((15.75,74,15),(368,275),2),L((15.75,185,16),(685,258),2),
        L((0,72,56),(371,150)),L((0,200,56),(700,155)),
        L((0,-15,25),(82,244)),L((15.7,147.7,20),(566,250)),
    ])
MATCHES['sight_photo']=match('rear-blade',(100,94,320,224),'Semi-buckhorn blade: ruler photograph, different two-screw mounting',
    (0,-.1,.065),(0,.283,.065),140,[
        L((-9.75,283,68.7),(152,110)),L((9.75,283,68.7),(275,115)),
        L((-1.01,283,66.5),(201,124)),L((1.01,283,66.5),(221,124)),
        L((-9,283,59.7),(139,208)),L((9,283,59.7),(279,210)),
    ])
MATCHES['sight_photo']['lens_bounds_mm']=(45,900)
# Coplanar receiver landmarks cannot recover perspective distance. A distant
# camera is the weak-perspective comparison assumption; it avoids inventing
# extreme near-camera shortening of the loop below the calibration landmarks.
# Neither this assumption nor the fitted focal length is recovered EXIF.
