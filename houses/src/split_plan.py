"""Bounded 1955–75 side-split / split-entry grammar, in meters.

Floor datums, clear ceilings, structural zones and reserved stair runs are
explicit. This is an exterior shell, not a reproduced or engineered plan.
"""
from dataclasses import asdict
import copy
import math
import random
from plan import FT, merge, roof_faces, roof_junctions
from cape_plan import CapeBlock


class SplitBlock(CapeBlock):
    def occlusion_constraints(self):
        # Roofing continues under the neighboring high eave up to its wall.
        # Cutting at the roof's projecting skirt would expose an open wedge.
        return [(1,0,-self.x0),(-1,0,self.x1),(0,1,-self.y0),(0,-1,self.y1)]

PROOF_SEEDS = (51, 52, 53, 54, 55, 56)
PALETTES = (
    dict(name='oyster / red brown / olive', siding=(.53,.51,.45), trim=(.59,.58,.53), shutter=(.055,.065,.039), door=(.13,.17,.07)),
    dict(name='sage / red / walnut', siding=(.235,.28,.205), trim=(.55,.54,.47), shutter=(.045,.053,.033), door=(.115,.054,.025)),
    dict(name='muted blue / brown brick', siding=(.18,.245,.28), trim=(.59,.58,.54), shutter=(.027,.038,.045), door=(.23,.06,.035)),
    dict(name='fired red / warm gray', siding=(.28,.275,.25), trim=(.53,.51,.46), shutter=(.040,.044,.034), door=(.12,.16,.075)),
    dict(name='putty / buff brick', siding=(.38,.345,.27), trim=(.59,.57,.51), shutter=(.07,.063,.042), door=(.12,.055,.025)),
    dict(name='ochre / red brown', siding=(.48,.415,.255), trim=(.57,.55,.48), shutter=(.055,.065,.036), door=(.055,.10,.063)),
)


def roof_parts(plan):
    return plan['blocks'] + ([plan['porch']] if plan['porch'] else [])


def generate(seed, overrides=None):
    r = random.Random(seed); i = (seed-51) % 6
    spec = dict(type='split', kind='foyer' if i==4 else 'side',
        main=dict(width=r.choice((26,28,30,32))*FT, depth=r.choice((26,28,30))*FT,
                  roof=r.choice(('gable','hip')), pitch=r.choice((4,5,6))/12,
                  overhang=r.choice((16,18,22,24))*.0254, rake=r.choice((8,12,16))*.0254),
        wing=dict(width=r.choice((22,24,26))*FT, depth=r.choice((26,28,30))*FT,
                  side='left' if i in (1,3) else 'right', axis='Y' if i in (0,3,5) else 'X',
                  roof='hip' if i==1 else 'gable', projection=r.choice((0,2))*FT,
                  overhang=(0,8,6,0,8,10)[i]*.0254),
        floor=r.choice((18,24,30))*.0254, half_rise=r.choice((52,53,54))*.0254,
        ceiling=8*FT, floor_zone=10*.0254,
        garage=dict(kind=('integral','carport','attached','integral','attached','none')[i],
                    side='left' if i==1 else 'right', cars=1 if i in (2,3,4) else 2),
        wall_mix=('living_brick','lower_brick','front_brick','all_brick','lower_brick','living_brick')[i],
        brick_color=('red_brown','red','red_brown','red','buff','tan')[i],
        siding=('wood','battens','aluminum','wood','vinyl','battens')[i],
        window_update=('wood_storm','aluminum','vinyl','bronze','vinyl','wood_storm')[i],
        shutters=i in (2,3,4), picture='bay' if i==5 else 'picture',
        chimney=('ridge','gable',None,'ridge','gable','gable')[i],
        roof_age='newer' if i in (2,4) else 'tired',
        shingle_color=('warm_charcoal','dark_brown','weathered_wood','warm_charcoal','warm_charcoal','dark_brown')[i],
        rail=i in (0,2,3,4), hood='gable' if i==4 else 'overhang',
        rear_landing='stoop', returns=False, aerial=None,
        colors=copy.deepcopy(PALETTES[i]))
    if spec['kind']=='foyer':
        spec['main'].update(width=r.choice((42,44,46))*FT, depth=28*FT,roof='gable',pitch=4/12)
        spec['floor']=.1524
    if overrides: merge(spec,copy.deepcopy(overrides))
    if overrides and 'floor_zone' in overrides:
        if 'half_rise' in overrides:
            assert abs(2*spec['half_rise']-spec['ceiling']-spec['floor_zone'])<1e-8, 'Conflicting half rise and floor zone'
        else:spec['half_rise']=(spec['ceiling']+spec['floor_zone'])/2
    else:
        spec['floor_zone']=2*spec['half_rise']-spec['ceiling']
    s=spec; m=s['main']; w=s['wing']; g=s['garage']
    assert s['type']=='split' and s['kind'] in ('side','foyer')
    assert (24*FT<=m['width']<=32*FT) if s['kind']=='side' else (40*FT<=m['width']<=48*FT)
    assert 24*FT<=m['depth']<=32*FT and 20*FT<=w['width']<=26*FT and 24*FT<=w['depth']<=32*FT
    assert all(v in ('hip','gable') for v in (m['roof'],w['roof'])) and 4/12<=m['pitch']<=6/12
    assert .3048<=m['overhang']<=.6096 and .1524<=m['rake']<=.4572
    assert w['side'] in ('left','right') and w['axis'] in ('X','Y') and 0<=w['projection']<=2*FT
    assert 0<=w['overhang']<=.3048 and 48*.0254<=s['half_rise']<=60*.0254
    assert abs(s['ceiling']+s['floor_zone']-2*s['half_rise'])<1e-8, 'Incompatible half flights and ceiling'
    assert abs(s['ceiling']-8*FT)<1e-8 and .2032-1e-8<=s['floor_zone']<=.3048+1e-8
    assert (.3048<=s['floor']<=.9144) if s['kind']=='side' else (.05<=s['floor']<=.3048)
    assert g['kind'] in ('integral','attached','carport','none') and g['side'] in ('left','right') and g['cars'] in (1,2)
    assert s['kind']!='foyer' or g['kind'] in ('none','attached','carport'), 'Foyer lower floor too deep for integral garage'
    assert s['wall_mix'] in ('living_brick','lower_brick','front_brick','all_brick')
    assert s['brick_color'] in ('red','red_brown','buff','tan') and s['siding'] in ('wood','vinyl','aluminum','battens')
    assert s['window_update'] in ('wood_storm','bronze','aluminum','vinyl') and s['picture'] in ('picture','bay')
    assert s['roof_age'] in ('tired','newer') and s['chimney'] in (None,'ridge','gable')
    assert all(isinstance(s[k],bool) for k in ('shutters','rail'))
    assert s['hood'] in ('overhang','gable','flat')
    assert all(len(s['colors'][k])==3 and all(math.isfinite(v) and 0<=v<=.7 for v in s['colors'][k]) for k in ('siding','trim','shutter','door'))
    middle=s['floor']; half=(s['ceiling']+s['floor_zone'])/2
    # Quantities are derived together: no fake low basement with a seven-foot
    # story, and no claimed half-flight incompatible with the actual floor.
    lower=middle-half; upper=middle+half
    if s['kind']=='foyer': lower=middle-1.524; upper=lower+s['ceiling']+s['floor_zone']
    s['half_rise']=half
    plate=(upper if s['kind']=='foyer' else middle)+s['ceiling']
    main=SplitBlock('Main',-m['width']/2,m['width']/2,-m['depth']/2,m['depth']/2,
                   lower-.18 if s['kind']=='foyer' else -.3,lower if s['kind']=='foyer' else middle,
                   plate,plate+.254,m['roof'],m['pitch'],'X',m['overhang'],
                   2 if s['kind']=='foyer' else 1,upper,upper-s['floor_zone'],m['rake'])
    blocks=[main]
    if s['kind']=='side':
        x0=main.x1 if w['side']=='right' else main.x0-w['width']
        wing=SplitBlock('Wing',x0,x0+w['width'],main.y0-w['projection'],main.y0-w['projection']+w['depth'],
                      lower-.18,lower,upper+s['ceiling'],upper+s['ceiling']+.254,w['roof'],m['pitch'],w['axis'],m['overhang'],2,upper,upper-s['floor_zone'],m['rake'])
        blocks.append(wing)
        door_x=main.x0+main.width*(.82 if w['side']=='right' else .18)
    else: wing=main; door_x=main.cx-.20
    if g['kind'] in ('attached','carport'):
        width=(12 if g['cars']==1 else 22)*FT;side=g['side']
        anchor=max(b.x1 for b in blocks) if side=='right' else min(b.x0 for b in blocks)
        x0=anchor if side=='right' else anchor-width
        garage=SplitBlock('Garage',x0,x0+width,main.y0+1*FT,main.y0+1*FT+22*FT,0,.1016,2.54,2.794,'gable',4/12,'Y',.4064,1,0,2.54,.2032)
        blocks.append(garage)
    # Permanent wall footprint + entry steps, excluding replaceable driveway.
    count=math.ceil((middle-.010)/.19);front=min(main.y0-1.02-(count-1)*.28,min(b.y0 for b in blocks))
    cx=(min(b.x0 for b in blocks)+max(b.x1 for b in blocks))/2
    cy=(front+max(b.y1 for b in blocks))/2
    for b in blocks: b.x0-=cx;b.x1-=cx;b.y0-=cy;b.y1-=cy
    door_x-=cx
    porch=None
    if s['hood'] in ('gable','flat'):
        porch=SplitBlock('Porch',door_x-.82,door_x+.82,main.y0-.76,main.y0+.10,0,middle-.010,middle+2.20,middle+2.38,
                       'gable' if s['hood']=='gable' else 'shed',4/12 if s['hood']=='gable' else 1/12,'Y',.1016,1,0,middle+2.2,.0762)
    s['cladding']={b.name:{f:('veneer' if b.stories==2 or s['wall_mix']=='all_brick' or (f=='front' and s['wall_mix'] in ('living_brick','front_brick')) else 'siding') for f in ('front','back','left','right')} for b in blocks}
    parking=wing if g['kind']=='integral' else (garage if g['kind'] in ('attached','carport') else None)
    drive_x=parking.cx if parking else main.x0-1.9 if w['side']=='right' else main.x1+1.9
    drive_top=lower if g['kind']=='integral' else .1016 if parking else .025
    drive_back=(parking.y0+(w['overhang'] if g['kind']=='integral' else 0)) if parking else main.y0
    driveway=dict(x=drive_x,width=(16 if g['cars']==2 else 10)*FT+.4 if parking else 3.1,
                  back=drive_back,front=min(b.y0 for b in blocks)-10.0,back_z=drive_top,front_z=.025)
    sockets=dict(FrontThreshold=(door_x,main.y0-.10,middle),Walk=(door_x,front-cy,0),Driveway=(drive_x,driveway['front'],.025))
    if parking: sockets['GarageApron']=(drive_x,drive_back-.13,drive_top)
    stairs=[]
    for name,a,b in [('up',middle,upper),('down',lower,middle)]:
        rise=b-a;nr=math.ceil(rise/.19685);stairs.append(dict(name=name,from_z=a,to_z=b,risers=nr,riser_m=rise/nr,tread_m=.254,run_m=(nr-1)*.254,width_m=.9144,landing_m=.9144))
    return dict(seed=seed,spec=s,blocks=blocks,porch=porch,door_x=door_x,sockets=sockets,
                levels=dict(lower=lower,living=middle,upper=upper),stairs=stairs,driveway=driveway,
                floor_levels={b.name:([lower,upper] if b.stories==2 else [b.floor]) for b in blocks})


def openings(plan):
    s=plan['spec'];m=plan['blocks'][0];wing=next((b for b in plan['blocks'] if b.name=='Wing'),m)
    lv=plan['levels'];right=s['wing']['side']=='right';result=[]
    def add(b,face,u,z,w,h,kind='window',role='bedroom',style='hung',shutters=False,**kw):
        result.append(dict(id=f'{b.name}_{face}_{len(result):02}',block=b.name,face=face,u=u,z=z,w=w,h=h,kind=kind,role=role,style=style,shutters=shutters,system=s['window_update'],**kw))
    if s['kind']=='side':
        add(m,'front',m.width*(.34 if right else .66),lv['living']+.66,2.7432,1.3716,role='living picture',style=s['picture'])
        add(m,'front',plan['door_x']-m.x0,lv['living'],.9144,2.032,'door','entry')
        for frac in (.26,.74):
            add(wing,'front',wing.width*frac,lv['upper']+1.00,1.2192,1.016,style='slider' if not s['shutters'] else 'hung',shutters=s['shutters'])
        if s['garage']['kind']=='integral':
            add(wing,'front',wing.width/2,lv['lower'],4.8768 if s['garage']['cars']==2 else 2.7432,2.1336,'garage','lower garage',recess=s['wing']['overhang'])
        else:
            for frac in (.26,.74):add(wing,'front',wing.width*frac,.20,1.3716,.6096,role='lower family room',style='slider',recess=s['wing']['overhang'])
    else:
        add(m,'front',m.width*.19,lv['upper']+.66,2.7432,1.3716,role='living picture',style='picture')
        for frac in (.68,.87):add(m,'front',m.width*frac,lv['upper']+.86,.8128,1.2192,shutters=s['shutters'])
        add(m,'front',plan['door_x']-m.x0,lv['living'],.9144,2.032,'door','split foyer landing')
        for frac in (.19,.73):add(m,'front',m.width*frac,.08,1.524,.6096,role='lower family room',style='slider')
    # Back of the quiet wing: kitchen, door/stoop, dining. A foil to the
    # two levels of bedroom/recreation glazing on the adjacent wing.
    mf=lv['upper'] if s['kind']=='foyer' else lv['living']
    for frac,w,h,z,role in ((.15,1.2192,.9144,mf+1.10,'kitchen'),(.82,1.524,1.2192,mf+.80,'dining')):
        add(m,'back',m.width*frac,z,w,h,role=role,style='slider')
    add(m,'back',m.width*.46,mf,.8636,2.032,'service','kitchen rear entry')
    outer='left' if right else 'right'
    if not any(b.name=='Garage' and ((b.cx<m.cx)==(outer=='left')) for b in plan['blocks']):
        for f in (.24,.78):add(m,outer,m.depth*f,mf+.90,1.2192,1.016,role='dining / kitchen',style='slider')
    if s['kind']=='side':
        for face in ('back','right' if right else 'left'):
            if face!='back' and any(b.name=='Garage' and ((b.cx>wing.cx)==right) for b in plan['blocks']):continue
            length=wing.width if face=='back' else wing.depth
            for f in (.23,.76):
                add(wing,face,length*f,lv['upper']+1.00,1.2192,1.016,style='slider')
                add(wing,face,length*f,-.08,1.2192,.7112,role='lower recreation',style='slider',recess=s['wing']['overhang'] if face=='front' else 0,well=True)
    else:
        for f in (.16,.82):add(m,'back',m.width*f,-.08,1.2192,.7112,role='lower recreation',style='slider',well=True)
        # Daylight recreation rooms also face the free gable. The two-story
        # box needs a real lower room, rather than front-only cellar glazing.
        free='left' if s['garage']['side']=='right' else 'right'
        for f in (.25,.78):add(m,free,m.depth*f,-.08,1.2192,.7112,role='lower recreation',style='slider',well=True)
    for b in plan['blocks']:
        if b.name=='Garage' and s['garage']['kind']=='attached':
            add(b,'front',b.width/2,b.floor,2.7432 if s['garage']['cars']==1 else 4.8768,2.1336,'garage','attached garage')
            add(b,'back',b.width/2,1.32,.9144,.6096,role='workshop',style='slider')
    return result


def serialize(plan):
    return {**plan,'blocks':[asdict(b) for b in plan['blocks']],
            'porch':asdict(plan['porch']) if plan['porch'] else None,
            'openings':openings(plan),'roof_faces':roof_faces(roof_parts(plan)),
            'roof_junctions':roof_junctions(roof_parts(plan))}
