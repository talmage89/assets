"""Bounded, seeded American joint-use distribution construction grammar."""
import random
FT=.3048
IN=.0254
SEEDS=(101,102,103,104)
PROFILES={
 101:dict(town='Older northern grid',length_ft=40,phases=3,framing='crossarm',arm_ft=8,comm=True,spacing_ft=140,house_types=['cape','ranch','split']),
 102:dict(town='Low postwar feeder',length_ft=35,phases=1,framing='armless',arm_ft=8,comm=True,spacing_ft=110,house_types=['ranch','cape']),
 103:dict(town='Small commercial edge',length_ft=45,phases=3,framing='crossarm',arm_ft=10,comm=False,spacing_ft=185,house_types=['builder_colonial','split']),
 104:dict(town='Later suburban rebuild',length_ft=40,phases=3,framing='armless',arm_ft=8,comm=True,spacing_ft=160,house_types=['split','builder_colonial','ranch']),
}


def pole_spec(length_ft=40,phases=3,framing='crossarm',arm_ft=8,comm=True,kind='tangent',seed=1):
    if length_ft not in (35,40,45):raise ValueError('Supported ANSI class 4 lengths: 35/40/45 ft')
    if phases not in (1,3) or framing not in ('crossarm','armless'):raise ValueError('Invalid framing')
    embed_ft=6.5 if length_ft==45 else 6
    height=(length_ft-embed_ft)*FT
    neutral={35:7.48,40:7.94,45:8.55}[length_ft]
    return dict(length_ft=length_ft,embed_ft=embed_ft,height=height,pole_class=4,
       circumference_6ft_in={35:31.5,40:33.5,45:35}[length_ft],top_circumference_in=21,
       phases=phases,framing=framing,arm_ft=arm_ft,comm=comm,kind=kind,seed=seed,
       primary=height-.22,neutral=neutral,communication=neutral-1.32)


def street(seed):
    profile=dict(PROFILES.get(seed,PROFILES[SEEDS[seed%4]]));rng=random.Random(seed)
    poles=[];y=0
    for i,kind in enumerate(('deadend','transformer','angle','transformer','riser')):
        if i:y+=profile['spacing_ft']*FT*rng.uniform(.96,1.04)
        # A small line jog stays inside the existing planting strip; a road
        # corner would require a matching ground/street layout, not poles
        # drifting across this straight roadway.
        x=-5.05+(max(0,i-2)*.15 if seed==104 else 0)
        spec=pole_spec(**{k:profile[k] for k in ('length_ft','phases','framing','arm_ft','comm')},kind=kind,seed=seed*10+i)
        spec.update(name=f'P{i}',location=(x,y,.16764),light=(i==1 or i==3) and seed!=103,bank=3 if seed==103 and i==3 else 1)
        poles.append(spec)
    # Place two rows of six houses; each transformer serves its nearest lots.
    houses=[]
    for side in (-1,1):
        for i in range(6):
            yy=(i+.4)*y/6
            houses.append(dict(name=f'House_{side}_{i}',type=profile['house_types'][(i+(side==1))%len(profile['house_types'])],
                seed={'ranch':12,'cape':31,'split':51,'builder_colonial':27}[profile['house_types'][(i+(side==1))%len(profile['house_types'])]],
                location=(side*20.5,yy,.16764),yaw=-90 if side==1 else 90))
    return dict(seed=seed,profile=profile,poles=poles,houses=houses,length=y)
