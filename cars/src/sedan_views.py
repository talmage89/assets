"""S240 review framing, in Blender authoring axes; sedan-only."""
SHOTS={
 'front_three_quarter':dict(location=(6,-8,2.5),target=(0,-.1,.74),lens=58,aspect=1.65,studio_yaw=-35),
 'rear_three_quarter':dict(location=(-6,8,2.5),target=(0,.12,.74),lens=58,aspect=1.65,studio_yaw=145),
 'face':dict(location=(.8,-4.3,1.25),target=(0,-2.14,.56),lens=65,aspect=1.55,studio_yaw=-35,paint='Graphite'),
 'lamp_unlit':dict(location=(1.95,-3.6,1.10),target=(.72,-2.08,.78),lens=95,aspect=1.50,studio_yaw=-35,paint='Graphite'),
 'lamp_lit':dict(location=(1.95,-3.6,1.10),target=(.72,-2.08,.78),lens=95,aspect=1.50,studio_yaw=-35,paint='Graphite',lights=True),
 'wheel':dict(location=(2.20,-2.60,.68),target=(.80,-1.475,.34),lens=85,aspect=1.2,studio_yaw=-45),
 'plate_detail':dict(location=(.35,3.65,1.05),target=(0,2.38,.86),lens=90,aspect=1.55,studio_yaw=145,paint='Graphite'),
 'mirror':dict(location=(1.80,-2.20,1.25),target=(.97,-.85,1.00),lens=100,aspect=1.5,studio_yaw=-35,paint='Graphite'),
 'interior_glass':dict(location=(1.72,-.55,1.20),target=(0,-.23,.82),lens=43,aspect=1.5,studio_yaw=95,paint='Graphite',exposure=-1.3),
 'underbody':dict(location=(3.8,5.3,.15),target=(0,1.0,.25),lens=60,aspect=1.65,studio_yaw=145,exposure=-1.3),
 'underbody_layout':dict(location=(2.8,3.8,-2.2),target=(0,0,.25),lens=35,aspect=1.65,studio_yaw=145,exposure=-1.3,underside=True),
 'opened_front':dict(location=(6.8,-8,3.3),target=(0,-.10,.90),lens=55,aspect=1.65,studio_yaw=-35,
    parts={'Door_FL':((-.14,0,1),60),'Door_FR':((.14,0,1),-60),'Door_RL':((-.14,0,1),62),'Door_RR':((.14,0,1),-62),'Hood':('X',-62),'Trunk':('X',72),'Steer_FL':('Z',30),'Steer_FR':('Z',30)}),
 'opened_rear':dict(location=(-6.8,8,3.3),target=(0,.1,.90),lens=55,aspect=1.65,studio_yaw=145,
    parts={'Door_FL':((-.14,0,1),60),'Door_FR':((.14,0,1),-60),'Door_RL':((-.14,0,1),62),'Door_RR':((.14,0,1),-62),'Hood':('X',-62),'Trunk':('X',72)}),
 'side':dict(location=(10,0,.75),target=(0,0,.75),ortho=5.7,aspect=2,studio_yaw=-35),
 'front':dict(location=(0,-10,.78),target=(0,0,.78),ortho=2.55,aspect=1.25,studio_yaw=-35),
 'rear':dict(location=(0,10,.78),target=(0,0,.78),ortho=2.55,aspect=1.25,studio_yaw=145),
 'top':dict(location=(0,0,12),target=(0,0,0),ortho=5.7,aspect=1.25,studio_yaw=-35),
 'scale':dict(location=(6,-8,2.5),target=(.40,-.10,.80),lens=51,aspect=1.65,studio_yaw=-35,human=True),
}


def motion_shots():
    """Five visible poses for every mechanism group; collision reports are separate."""
    result={}
    for group,view in [('doors','front_three_quarter'),('hood','front_three_quarter'),('trunk','rear_three_quarter'),('steering','front_three_quarter'),('wheels','wheel')]:
        for index in range(5):
            t=index/4;shot=dict(SHOTS[view]);parts={}
            if group=='doors':parts={'Door_'+code:((-.14 if code.endswith('L') else .14,0,1),(60 if code.startswith('F') else 68)*t*(-1 if code.endswith('R') else 1)) for code in ['FL','FR','RL','RR']}
            if group=='hood':parts={'Hood':('X',-62*t)}
            if group=='trunk':parts={'Trunk':('X',72*t)}
            if group=='steering':parts={'Steer_'+code:('Z',-35+70*t) for code in ['FL','FR']}
            if group=='wheels':parts={'Wheel_'+code:('X',90*t) for code in ['FL','FR','RL','RR']}
            shot.update(parts=parts,motion_group=group)
            result[group+'_'+str(index)]=shot
    return result
