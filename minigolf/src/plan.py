"""Original roadside-course grammar; pure Python, meters, deterministic seeds.

Cells reserve construction envelopes. Sinuous greens, obstacle sequence and
routing are authored here, never sampled from a published course plan.
"""
import math, random
KINDS=('classic','adventure')
FEATURES=('bank','bump','ramp','tunnel','dogleg','split','drop','loop','plain')

def center(h,t):
    bend=h['bend']; return (bend*math.sin(math.pi*t)**2, (t-.5)*h['length'])

def halfwidth(h,t):
    # Wider landing/cup head, narrowed fairway; tee receives a full putter stance.
    
    profile=(.65+.35*math.exp(-((t-.82)/.20)**2)+.13*math.exp(-((t-.10)/.13)**2)) if h.get('organic') else (.78+.22*math.exp(-((t-.87)/.16)**2))
    rounded=min(1,math.sqrt(max(.05,1-((t-.08)/.09)**2)) if t<.08 else 1,math.sqrt(max(.05,1-((t-.92)/.09)**2)) if t>.92 else 1) if h.get('organic') else 1
    return h['width']/2*profile*rounded

def level(h,x,t):
    yworld=h['origin'][1]+math.sin(math.radians(h['yaw']))*x+math.cos(math.radians(h['yaw']))*((t-.5)*h['length'])
    z=.125+h['rise']*t+h.get('base_z',0)
    if h.get('organic') and not h.get('crossing'):z+=.065*(max(0,yworld+7)-max(0,h['origin'][1]+7))
    f=h['feature']
    if f=='bump':z+=.26*math.exp(-((t-.50)/.13)**2)*(1-.2*(x/2)**2)
    if f=='bank':z+=.16*math.sin(math.pi*t)**2*(x/h['width']+.5)
    if f=='ramp':z+=.48*max(0,1-abs(t-.53)/.22)
    if f=='drop':z+=.26*(1-math.tanh((t-.57)*34))/2
    return z

def local(h,x,y,z=0):
    a=math.radians(h['yaw']);return (h['origin'][0]+x*math.cos(a)-y*math.sin(a),h['origin'][1]+x*math.sin(a)+y*math.cos(a),z)

def generate(seed=71,kind=None):
    rng=random.Random(seed);kind=kind or KINDS[seed%2];assert kind in KINDS
    adv=kind=='adventure';W,D=(64,65) if adv else (49,56)
    # Six columns with a wider central water/landscape spine in the adventure.
    xs=(-18,-12.5,-7.0,7.0,12.5,18) if adv else (-16,-10.8,-5.6,3.3,8.5,13.7)
    ys=(-5.5,4.6,14.8) if adv else (-5,4.3,13.6)
    cells=[(c,r) for c in range(6) for r in (range(3) if c%2==0 else reversed(range(3)))]
    features=list(FEATURES)*2;rng.shuffle(features)
    # Each course always shows its signature fixture and all reusable types.
    fixtures={1:'windmill',4:'castle',7:'covered_bridge',11:'lighthouse'}
    if adv:fixtures={1:'castle',4:'covered_bridge',6:'lighthouse',10:'windmill',16:'shipwreck'}
    elif seed%3==0:fixtures[16]='shipwreck'
    holes=[]
    for i,(c,r) in enumerate(cells):
        length=rng.uniform(7.0,8.6) if adv else rng.uniform(6.3,7.9)
        width=rng.uniform(2.45,3.25) if adv else rng.uniform(2.0,2.8)
        if not adv and i==0:length,width=5.2,3.6576
        fixture=fixtures.get(i)
        feature='plain' if fixture else features[i]
        # The drop remains a playable steep carpet break; no unsupported sheet.
        rise=rng.choice((.12,-.18,.35,-.45)) if adv else rng.choice((0,0,.035))
        yaw=(7*math.sin(r*1.7+c)+(-6 if c<3 else 6))+(180 if c%2 else 0) if adv else 5*math.sin(c+r)+(180 if c%2 else 0)
        h=dict(number=i+1,par=3 if fixture or feature in ('loop','drop','ramp') else 2,
               origin=(xs[c]+rng.uniform(-.10,.10),ys[r]+(.55*math.sin(c*1.6) if adv else .35*math.sin(c))),yaw=yaw,length=length,width=width,organic=adv,terrain_slope=.025 if adv else 0,
               base_z=(.07*max(0,ys[r]+6)+(.35 if c in (2,3) else 0)) if adv else 0,age=.42 if adv else .9,bend=rng.uniform(-.30,.30),rise=rise,feature=feature,fixture=fixture,
               border=('rock' if i%3 else 'brick') if adv else ('timber' if i in (6,7,8) else 'concrete'),
               carpet=i%3 if adv else i%2)
        if adv:
            if i<12:
                angle=math.radians(-90+i*30)
                h['origin']=(19.6*math.cos(angle),7+17.2*math.sin(angle))
                h['yaw']=math.degrees(math.atan2(19.6*math.sin(angle),17.2*math.cos(angle)))
            else:
                placement={12:((-7.8,13.9),180),13:((-7.8,3.8),180),14:((0,-4.5),-90),15:((7.8,2.7),0),16:((7.8,13.0),0),17:((0,6.1),90)}
                h['origin'],h['yaw']=placement[i]
                if i in (14,17):h.update(crossing=True,base_z=.58 if i==14 else 1.42,rise=-.16,feature='bank' if i==17 else 'plain')
            if not h.get('crossing'):h['base_z']=.065*max(0,h['origin'][1]+7)
        h['base_z']+=max(0,-h['rise'])
        tx,ty=center(h,.08);cx,cy=center(h,.88)
        h['tee']=local(h,tx,ty,level(h,tx,.08)+.0048)
        h['cup']=local(h,cx,cy,level(h,cx,.88)+.0048)
        # Reserve the cell, including sign and walking stance outside the edging.
        h['footprint']=[local(h,x,y)[:2] for x,y in ((-2.8,-length/2-1),(2.8,-length/2-1),(2.8,length/2+1),(-2.8,length/2+1))]
        holes.append(h)
    return dict(seed=seed,kind=kind,name='Cairn Creek' if adv else 'Bramble Putt',lot=(W,D),
                holes=holes,pond=(0,4.5),clubhouse=(0,-D/2+10),parking_y=-D/2+3.6,
                play_bounds=(-23,23,-13,27) if adv else (-20,18,-11,20),walk_width=1.524,driveways=(-W/2+12,W/2-4.5),parking_aisle=7.3152,parking_stall=(2.7432,5.4864),water=adv,style='harbor and quarry' if adv else 'painted Americana')
