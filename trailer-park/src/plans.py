"""Bounded manufactured-home and community grammar; meters, no Blender.

Long home axis is X, entry face -Y. Lot frontage runs along the street.
Transport nominal sizes are distinct from the authored wall-line body sizes.
"""
import random,math

FT = .3048
PALETTES = ((.46,.43,.32),(.25,.36,.34),(.47,.46,.39),(.33,.39,.43),(.50,.40,.26),(.38,.42,.28))


def home(seed, era=None, width_ft=None, length_ft=None):
    r=random.Random(seed)
    era=era or r.choice(('1972','1984','1996'))
    if era not in ('1972','1984','1996'):raise ValueError('era: 1972, 1984, 1996')
    double=era=='1996'
    w=width_ft or r.choice((24,28,32) if double else (12,14) if era=='1972' else (14,16))
    l=length_ft or r.choice((52,56,60,64) if double else (52,60,64,70,76,80))
    if w not in ((24,28,32) if double else (12,14,16)) or l not in (52,56,60,64,70,76,80):raise ValueError('unsupported transport size')
    return dict(seed=seed,era=era,double=double,nominal_ft=[w,l],width=w*FT,length=l*FT,
                floor=.91,eave=3.12 if era=='1972' else 3.35,pitch=.25 if double else .1667 if era=='1984' else 0,
                siding='vinyl' if double else r.choice(('ribbed','lap')),roof='shingle' if double or era=='1984' and seed%3==0 else 'rolled',
                color=PALETTES[seed%len(PALETTES)],trim=(.62,.61,.54),accent=(.07,.14,.13) if seed%2 else (.18,.13,.075),
                missing_skirt=era=='1972' and seed%3==0,deck_width=r.choice((3.048,3.6576,4.2672)),
                carport=seed%4!=1,room=era=='1972' and seed%3==1,awning_sag=.09 if era=='1972' and seed%4==0 else 0,
                tarp=era=='1972' and seed%5==0,propane=seed%3!=1,ac='window' if era=='1972' else 'condenser',
                dish=seed%3!=0,upkeep=('patched','kept','faded')[seed%3])


def park(seed=101, kind=None, rows=5):
    kind=kind or ('old' if seed%2 else 'new')
    if kind not in ('old','new') or rows not in (4,5,6):raise ValueError('kind old/new; rows 4..6')
    r=random.Random(seed);old=kind=='old';pitch=(40 if old else 64)*FT;depth=(110 if old else 120)*FT
    street=(20 if old else 24)*FT
    span=rows*pitch
    # Different road graphs: a through lane vs a closed loop with a south entry.
    loop_x=18.5
    lots=[]
    for side in (-1,1):
        for j in range(rows):
            hs=seed*100+len(lots)+1
            era=('1972' if j%3!=2 else '1984') if old else ('1984' if j==rows-1 else '1996')
            spec=home(hs,era,length_ft=r.choice((52,60,64,70)) if old else r.choice((56,60,64)) if era=='1996' else 76)
            yy=(j-(rows-1)/2)*pitch
            # Both street-facing end walls have a 6 m drive approach. Side
            # entries, decks and carports stay inside the lot's own frontage.
            edge=street/2 if old else loop_x+street/2
            xx=side*(edge+6.096+spec['length']/2)
            spec['lot_number']=len(lots)+1
            lots.append(dict(number=len(lots)+1,home=spec,origin=[xx,yy+1.15,0],yaw=0 if side<0 else 180,
                             lot=[side*(edge+depth/2),yy,depth,pitch],side=side))
    if not old:
        # Two shorter infill lots use the loop's middle block. Amenities keep
        # their own connected reservations rather than filling a vacant island.
        inner=2*loop_x-street
        for yy in (-5.8,24.5):
            hs=seed*100+len(lots)+1;spec=home(hs,'1996',24,52);spec['lot_number']=len(lots)+1
            xx=loop_x-street/2-6.096-spec['length']/2
            lots.append(dict(number=len(lots)+1,home=spec,origin=[xx,yy,0],yaw=0,
                             lot=[0,yy,inner,pitch],side=0,central=True))
    roads=[[[0,-span/2-21,0],[0,span/2+21,0]]]
    if not old:
        top=span/2+9;radius=7.0;loop=[]
        for cx,cy,start in ((loop_x-radius,-top+radius,270),(loop_x-radius,top-radius,0),(-loop_x+radius,top-radius,90),(-loop_x+radius,-top+radius,180)):
            loop.extend([[cx+radius*math.cos(math.radians(start+i*90/12)),cy+radius*math.sin(math.radians(start+i*90/12)),0] for i in range(13)])
        loop.append(loop[0]);roads=[loop,[[0,-span/2-21,0],[0,-span/2-9,0]]]
    return dict(seed=seed,kind=kind,name='Alder Court' if old else 'Meadow Bend',year=1968 if old else 1994,
                street_width=street,lot_frontage=pitch,lot_depth=depth,span=span,loop_x=loop_x,
                size=[2*(street/2+depth+3+(0 if old else loop_x)),span+42],lots=lots,
                roads=roads)
