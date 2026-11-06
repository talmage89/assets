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
    z=.125+h['rise']*t+h.get('terrain_slope',0)*max(0,yworld+9)
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
    xs=(-23,-16,-9,9,16,23) if adv else (-18,-11,-4,4,11,18)
    ys=(-6,5,16) if adv else (-5,5,15)
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
        fixture=fixtures.get(i)
        feature='plain' if fixture else features[i]
        # The drop remains a playable steep carpet break; no unsupported sheet.
        rise=rng.choice((0,.06,.12,.24)) if adv else rng.choice((0,0,.035))
        yaw=rng.uniform(-16,16)+(180 if c%2 else 0) if adv else rng.uniform(-8,8)+(180 if c%2 else 0)
        h=dict(number=i+1,par=3 if fixture or feature in ('loop','drop','ramp') else 2,
               origin=(xs[c]+rng.uniform(-.42,.42),ys[r]+(rng.uniform(-.65,.65) if adv else 0)),yaw=yaw,length=length,width=width,organic=adv,terrain_slope=.025 if adv else 0,
               bend=rng.uniform(-.40,.40),rise=rise,feature=feature,fixture=fixture,
               border=('rock' if i%3 else 'brick') if adv else ('timber' if i in (6,7,8) else 'concrete'),
               carpet=i%3 if adv else i%2)
        tx,ty=center(h,.08);cx,cy=center(h,.88)
        h['tee']=local(h,tx,ty,level(h,tx,.08)+.0048)
        h['cup']=local(h,cx,cy,level(h,cx,.88)+.0048)
        # Reserve the cell, including sign and walking stance outside the edging.
        h['footprint']=[local(h,x,y)[:2] for x,y in ((-2.8,-length/2-1),(2.8,-length/2-1),(2.8,length/2+1),(-2.8,length/2+1))]
        holes.append(h)
    return dict(seed=seed,kind=kind,name='Cairn Creek' if adv else 'Bramble Putt',lot=(W,D),
                holes=holes,pond=(0,4.5),clubhouse=(0,-D/2+10),parking_y=-D/2+3.6,
                walk_width=1.524,driveways=(-W/2+12,W/2-4.5),parking_aisle=7.3152,parking_stall=(2.7432,5.4864),water=adv,style='harbor and quarry' if adv else 'painted Americana')
