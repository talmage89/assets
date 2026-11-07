"""Seeded installer layouts; discrete connected topology, not scattered obstacles.

Zones are construction review geometry, not an engineering certification.
Coordinates in Blender meters. Swings are always independent of the composite.
"""
import random,math
from dimensions import *
SEEDS=(101,202,303)

def site(seed):
    rng=random.Random(seed)
    if not 1<=seed<2**31:raise ValueError('Seed must be a positive 31-bit integer')
    era=(1996,2005,2013)[(seed//100-1)%3];inclusive=era==2013
    if era==1996:
        decks=[(0,0,1.2192),(GRID,0,1.2192),(GRID,GRID,1.8288)]
        events=[('SlideStraight48',(0,-HALF,0),0),('SlideWave72',(GRID+HALF,GRID,0),90),('Stairs48',(-HALF,0,0),-90),('Arch48',(GRID+HALF,0,0),90),('Ladder72',(GRID,GRID+HALF,0),180),('OverheadLadder',(-HALF,GRID,0),-90)]
        swing=(13.8,1.1,0);rider=(-7.5,-4.6,0);spin=(3.1,6.85,0);surf=(-10.1,-7.6,19.5,10.0)
    elif era==2005:
        decks=[(0,0,.6096),(0,GRID,1.2192),(GRID,GRID,1.2192),(2*GRID,GRID,1.8288)]
        events=[('Transfer24',(0,-HALF,0),0),('SlideWave48',(-HALF,GRID,0),-90),('SlideSpiral72',(2*GRID+HALF,GRID,0),90),('FirePole',(GRID,GRID+HALF,0),180),('ChainNet48',(GRID,GRID-HALF,0),0),('RockWall48',(0,GRID+HALF,0),180),('OverheadRings',(-HALF,0,0),-90)]
        swing=(-11.1,1.0,0);rider=(9.3,-3.1,0);spin=(9.3,4.8,0);surf=(-16.8,-6.0,12.35,8.0)
    else:
        # Low broad accessible deck spine and separate older-child upper tower.
        decks=[(0,0,.6096),(GRID,0,.6096),(2*GRID,0,.6096),(2*GRID,GRID,1.2192),(3*GRID,GRID,1.2192)]
        events=[('RampStart',(0,-HALF-1.8288,0),0),('Transfer24',(-HALF,0,0),-90),('SlideStraight24',(GRID,-HALF,0),0),('SlideTube48',(3*GRID+HALF,GRID,0),90),('RockWall48',(2*GRID,GRID+HALF,0),180),('Arch48',(3*GRID,GRID+HALF,0),180),('VerticalLadder48',(3*GRID,GRID-HALF,0),0)]
        swing=(14.85,-1.7,0);rider=(-6.1,-3.2,0);spin=(-6.6,4.5,0);surf=(-9.6,-13.4,20.55,8.8)
    # The three review seeds pin the authored period examples. Other positive
    # seeds select compatible events on those connected installation scaffolds.
    # None of these substitutions increases the reserved use-zone envelope.
    if seed not in SEEDS:
        variants=[]
        for kind,pos,yaw in events:
            if kind=='Arch48':kind=rng.choice(('Arch48','ChainNet48','RockWall48'))
            elif kind in ('SlideStraight48','SlideWave48'):kind=rng.choice(('SlideStraight48','SlideWave48'))
            elif kind in ('OverheadLadder','OverheadRings'):kind=rng.choice(('OverheadLadder','OverheadRings'))
            variants.append((kind,pos,yaw))
        events=variants
    modules=[]
    def add(kind,pos,yaw=0,group='composite'):modules.append(dict(kind=kind,pos=list(pos),yaw=yaw,group=group))
    if inclusive:
        # A six-foot turning bay gives 1.70 m clear between the corner posts.
        add('Deck72',(0,-HALF-.9144,.6096))
        add('RampHeadBridge',(0,-HALF-1.8288,.6096))
        for x in (-.9144,.9144):
            add('Barrier72',(x,-HALF-.9144,.6096),90)
            for y in (-HALF,-HALF-1.8288):add('Post1730',(x,y,0))
        for y in (-HALF,-HALF-1.8288):
            for x in (-.77,.77):add('NeckGuard',(x,y,.6096))
    # Deck interfaces: every external side gets a barrier unless an event owns it.
    open_edges=set()
    for kind,pos,yaw in events:
        if kind=='RampStart':
            for j in range(6):add('RampSegment',(pos[0],pos[1]-j*1.2192,.6096-j*.1016),0)
            add('RampLanding',(pos[0],pos[1]-7.3152-.762,0))
        else:add(kind,pos,yaw)
        open_edges.add((round(pos[0],4),round(pos[1],4)))
    posts={}
    for i,(x,y,h) in enumerate(decks):
        add('Deck',(x,y,h));
        for sx in (-1,1):
            for sy in (-1,1):
                k=(round(x+sx*HALF,4),round(y+sy*HALF,4));posts[k]=max(posts.get(k,0),h+1.12)
        for dx,dy,angle in [(0,-HALF,0),(HALF,0,90),(0,HALF,180),(-HALF,0,-90)]:
            mid=(round(x+dx,4),round(y+dy,4))
            neighbor=next((d for d in decks if abs(d[0]-(x+2*dx))<1e-4 and abs(d[1]-(y+2*dy))<1e-4),None)
            if neighbor:
                if neighbor[2]>h+.01:
                    # One 24in rise becomes three 8in closed intermediate steps.
                    add('InterdeckSteps',(x+dx,y+dy,h),angle)
                continue
            if mid in open_edges:continue
            kind='Barrier'
            if i==0 and dx==HALF:kind='PanelWheel'
            if i==len(decks)-1 and dy==HALF:kind='PanelTic'
            if inclusive and i==1 and dy==HALF:kind='PanelPeriscope'
            add(kind,(x+dx,y+dy,h),angle)
    for (x,y),h in posts.items():
        kind='Post'+str(round(h*1000));add(kind,(x,y,0))
    roof_deck=decks[-1]
    roof='Shade' if inclusive else 'HipRoof'
    if seed not in SEEDS and era==2005:roof=rng.choice(('HipRoof','Shade'))
    add(roof,(roof_deck[0],roof_deck[1],roof_deck[2]+1.32))
    # Extend four supporting post ends up into the roof sockets.
    for sx in (-1,1):
        for sy in (-1,1):
            add('RoofRiser',(roof_deck[0]+sx*HALF,roof_deck[1]+sy*HALF,roof_deck[2]+1.12))
    add('SwingFrame',swing,0,'swing')
    for i,x in enumerate((-SWING_BAY/2-SWING_SEAT_OFFSET,-SWING_BAY/2+SWING_SEAT_OFFSET,SWING_BAY/2-SWING_SEAT_OFFSET,SWING_BAY/2+SWING_SEAT_OFFSET)):
        add('SwingBucket' if i>=2 else 'SwingBelt',(swing[0]+x,swing[1],SWING_H),0,'swing')
    add('SpringRider',rider,0,'rider');add('Roundabout',spin,0,'spinner')
    # Compact but explicit operational separation. Composite zone is generated
    # from actual placed geometry by build.py; separate swing/rider/spinner here.
    zones=[dict(name='Swing front/back 2H',group='swing',rect=[swing[0]-SWING_BAY-SWING_OVERHANG-USE,swing[1]-2*SWING_H,swing[0]+SWING_BAY+SWING_OVERHANG+USE,swing[1]+2*SWING_H],rule='CPSC 5.3.8.3.3'),dict(name='Spring rider 6ft',group='rider',rect=[rider[0]-.5-USE,rider[1]-.5-USE,rider[0]+.5+USE,rider[1]+.5+USE],rule='CPSC 5.3.7'),dict(name='Roundabout 6ft',group='spinner',rect=[spin[0]-.94-USE,spin[1]-.94-USE,spin[0]+.94+USE,spin[1]+.94+USE],rule='CPSC 5.3.4')]
    return dict(seed=seed,year=era,age='sun faded / maintenance repaint' if era==1996 else 'middle years' if era==2005 else 'newer inclusive',modules=modules,decks=decks,zones=zones,surface=list(surf),walk_y=surf[1]-1.65,inclusive=inclusive,selection_policy='Period scaffold plus seeded compatible events; review seeds pin canonical choices')
