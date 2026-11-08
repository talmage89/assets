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


def park(seed=101, kind=None, rows=9):
    kind=kind or ('old' if seed%2 else 'new')
    if kind not in ('old','new') or not 8<=rows<=10:raise ValueError('kind old/new; rows 8..10')
    r=random.Random(seed);old=kind=='old'
    pitch=(32 if old else 56)*FT;depth=(110 if old else 95)*FT
    street=(20 if old else 24)*FT
    span=rows*pitch
    # Four rows, two narrow lanes: old through streets / newer connected loop.
    # 3520 / 5320 sqft lots; gross density includes the two common end strips.
    loop_x=depth+street/2
    lots=[]
    for lane in (-loop_x,loop_x):
      for side in (-1,1):
        for j in range(rows):
            hs=seed*100+len(lots)+1;variant=(j*5+len(lots)//rows*3)%8
            era=('1972' if variant%3!=2 else '1984') if old else ('1984' if variant==7 else '1996')
            vs=seed*100+variant+1
            spec=home(vs,era,width_ft=(16 if era=='1984' else 12 if variant%4==3 else 14) if old else (16 if era=='1984' else (24,28,28,24)[variant%4]),
                      length_ft=(52,60,64,70)[variant%4] if old else (52,56,60,64)[variant%4])
            spec.update(variant_id=f'{kind}-{variant}',occupant_seed=hs)
            yy=(j-(rows-1)/2)*pitch
            # Both street-facing end walls have a 6 m drive approach. Side
            # entries, decks and carports stay inside the lot's own frontage.
            xx=lane+side*(street/2+6.096+spec['length']/2)
            lots.append(dict(number=len(lots)+1,home=spec,origin=[xx,yy+1.15,0],yaw=0 if side<0 else 180,
                             lot=[lane+side*(street/2+depth/2),yy,depth,pitch],side=side,lane=lane))
    if not old:
        # Three residential-size reservations for clubhouse, play and laundry.
        lots=[q for q in lots if not (q['lane']*q['side']<0 and
              (q['lot'][1]<-span/2+pitch or q['lot'][1]>span/2-pitch and q['lane']<0))]
    roads=[[[x,-span/2-10,0],[x,span/2+10,0]] for x in (-loop_x,loop_x)]
    if not old:
        top=span/2+5;radius=5.0;loop=[]
        for cx,cy,start in ((loop_x-radius,-top+radius,270),(loop_x-radius,top-radius,0),(-loop_x+radius,top-radius,90),(-loop_x+radius,-top+radius,180)):
            loop.extend([[cx+radius*math.cos(math.radians(start+i*90/12)),cy+radius*math.sin(math.radians(start+i*90/12)),0] for i in range(13)])
        loop.append(loop[0]);roads=[loop,[[0,-span/2-10,0],[0,-span/2-5,0]]]
    return dict(seed=seed,kind=kind,name='Alder Court' if old else 'Meadow Bend',year=1968 if old else 1994,
                street_width=street,lot_frontage=pitch,lot_depth=depth,span=span,loop_x=loop_x,
                size=[4*depth+2*street+3,span+20],lots=lots,roads=roads,
                lot_area_sqft=(3520 if old else 5320),template_count=8,
                density_note='Gross parcel includes two lanes and common end strips; modern code comparators, not historical approval.')
