"""Original 1940–55 Cape grammar, meters; no image/Blender dependency.

Anisotropic overhangs and the shed plane are opt-in Block specializations.
The shared exact half-space roof union resolves real dormer penetrations.
"""
from dataclasses import dataclass, asdict
import copy
import math
import random
from plan import Block, FT, merge, roof_faces, roof_junctions, wall_frame

PROOF_SEEDS=(31,32,33,34,35,36)
PALETTES=(
 dict(name='warm white / bottle green',siding=(.61,.60,.55),trim=(.64,.63,.58),shutter=(.032,.062,.039),door=(.16,.035,.022)),
 dict(name='weathered gray / ink',siding=(.27,.275,.26),trim=(.59,.58,.53),shutter=(.025,.031,.030),door=(.12,.048,.026)),
 dict(name='ochre cream / charcoal',siding=(.49,.42,.24),trim=(.60,.58,.51),shutter=(.035,.038,.032),door=(.16,.043,.029)),
 dict(name='sage / warm ivory',siding=(.25,.30,.21),trim=(.57,.55,.47),shutter=(.035,.051,.031),door=(.23,.066,.032)),
 dict(name='Cape blue / warm white',siding=(.16,.235,.28),trim=(.60,.59,.54),shutter=(.029,.036,.041),door=(.22,.043,.026)),
 dict(name='barn red / oyster',siding=(.235,.051,.034),trim=(.56,.53,.45),shutter=(.038,.042,.031),door=(.063,.080,.040)),
)

@dataclass
class CapeBlock(Block):
    rake: float=.0762
    def domain(self):
        ox,oy=(self.rake,self.overhang) if self.ridge_axis=='X' else (self.overhang,self.rake)
        return [(self.x0-ox,self.y0-oy),(self.x1+ox,self.y0-oy),(self.x1+ox,self.y1+oy),(self.x0-ox,self.y1+oy)]
    def constraints(self):
        p=self.domain();return [(1,0,-p[0][0]),(-1,0,p[1][0]),(0,1,-p[0][1]),(0,-1,p[2][1])]
    def occlusion_constraints(self):
        # A dormer removes the parent roof inside its framed walls. The
        # parent roofing continues beneath its projecting rake/eave skirts.
        if self.name.startswith('Dormer') or self.name=='RearShed':
            return [(1,0,-self.x0),(-1,0,self.x1),(0,1,-self.y0),(0,-1,self.y1)]
        return self.constraints()
    def covers(self,x,y,eps=0):
        return all(a*x+b*y+c>=-eps for a,b,c in self.constraints())
    def planes(self):
        if self.roof=='shed':return [(0,-self.pitch,self.eave+self.pitch*self.y1)]
        return super().planes()


def roof_parts(plan):
    return plan['blocks']+([plan['porch']] if plan['porch'] else [])


def generate(seed,overrides=None):
    r=random.Random(seed);i=seed%6
    spec=dict(type='cape',main=dict(width=r.choice((24,26,28,30,32,34))*FT,depth=r.choice((24,26,28,30,32))*FT,
        stories=1.5,roof='gable',pitch=r.choice((8,9,10,12))/12,overhang=r.choice((6,8,10))*.0254,rake=r.choice((0,3,4,6))*.0254),
        floor=r.choice((18,24,30))*.0254,foundation='crawlspace' if i==4 else 'basement',
        dormers=(2,2,3,0,2,3)[i],rear_shed=i in (0,3,5),wing=('none','none','porch','none','wing','none')[i],
        garage=dict(kind=('none','detached','breezeway','none','detached','breezeway')[i],side='left' if i%2 else 'right'),
        door_offset=i==3,hood=('hood','none','portico','hood','none','portico')[i],returns=bool(i%2),
        siding=('wood','vinyl','cedar','cement','aluminum','wood')[i],
        window_update=('six_over_six','one_over_one','eight_over_eight','six_over_six','one_over_one','six_over_six')[i],
        storms=i in (0,2,3),shutters=i!=3,chimney=('ridge','gable','gable','gable',None,'gable')[i],
        roof_age='newer' if i in (1,4) else 'tired',shingle_color=('warm_charcoal','weathered_wood','dark_brown')[i%3],
        colors=copy.deepcopy(PALETTES[i]),rear_landing='stoop')
    if spec['dormers']==3:spec['main']['width']=max(spec['main']['width'],30*FT)
    if spec['main']['pitch']*spec['main']['depth']/2<3.25 and (spec['dormers'] or spec['rear_shed']):spec['main']['pitch']=min(1,math.ceil(3.25/(spec['main']['depth']/2)*12)/12)
    if overrides:merge(spec,copy.deepcopy(overrides))
    s=spec;m=s['main'];g=s['garage']
    assert s['type']=='cape' and m['stories']==1.5 and m['roof']=='gable'
    assert 24*FT-1e-8<=m['width']<=34*FT+1e-8 and 24*FT-1e-8<=m['depth']<=32*FT+1e-8
    assert 8/12<=m['pitch']<=1 and .1016<=m['overhang']<=.3048 and 0<=m['rake']<=.1524
    assert .4572<=s['floor']<=.762 and s['foundation'] in ('basement','crawlspace')
    assert s['dormers'] in (0,2,3) and s['wing'] in ('none','wing','porch')
    assert s['siding'] in ('wood','cedar','vinyl','aluminum','cement')
    assert g['kind'] in ('none','detached','breezeway') and g['side'] in ('left','right')
    assert s['hood'] in ('none','hood','portico') and s['chimney'] in (None,'ridge','gable')
    assert s['window_update'] in ('six_over_six','eight_over_eight','one_over_one') and s['roof_age'] in ('newer','tired')
    assert all(isinstance(s[k],bool) for k in ('rear_shed','returns','door_offset','storms','shutters'))
    assert all(len(s['colors'][k])==3 and all(math.isfinite(v) and 0<=v<=.7 for v in s['colors'][k]) for k in ('siding','trim','shutter','door'))
    floor=s['floor'];plate=floor+8*FT
    # Low eave: roof bearing at 10–11 ft, despite half-story sleeping space.
    eave=plate+.2032
    main=CapeBlock('Main',-m['width']/2,m['width']/2,-m['depth']/2,m['depth']/2,0,floor,plate,eave,'gable',m['pitch'],'X',m['overhang'],1,floor+8*FT+.254,plate,m['rake'])
    blocks=[main];side=-1 if g['side']=='left' else 1
    wing=None
    if s['wing']!='none':
        width=(10 if s['wing']=='porch' else 12)*FT;depth=14*FT;x0=main.x1 if side==1 else main.x0-width
        wing=CapeBlock('Wing',x0,x0+width,main.y0+1.22,main.y0+1.22+depth,0,floor,plate-.20,eave-.20,'gable',5/12,'X',.2032,1,0,plate-.2,.0762)
        blocks.append(wing)
    if g['kind']!='none':
        # Wing and parking always occupy opposite sides, preventing intersecting additions.
        gs=-side if wing else side;gap=(8 if g['kind']=='breezeway' else 10)*FT
        gx=main.x1+gap if gs==1 else main.x0-gap-12*FT
        gy=main.y0+2*FT if g['kind']=='breezeway' else main.y1+2*FT
        garage=CapeBlock('Garage',gx,gx+12*FT,gy,gy+20*FT,0,.1016,2.54,2.68,'gable',6/12,'Y',.2032,1,0,2.54,.1016)
        if g['kind']=='breezeway':
            a,c=(main.x1,garage.x0) if gs==1 else (garage.x1,main.x0)
            bridge=CapeBlock('Breezeway',a,c,gy+.40,gy+.40+2.14,0,.1016,2.41,2.56,'gable',4/12,'X',.1524,1,0,2.41,.0254)
            blocks.append(bridge)
        blocks.append(garage)
    # Two dormers correspond to two side bays; three use a five-bay facade.
    centers=[main.x0+main.width*f for f in ((.25,.75) if s['dormers']==2 else (.21,.50,.79))] if s['dormers'] else []
    for j,x in enumerate(centers):
        width=4.5*FT;y0=main.y0+.50;dormer_eave=main.upper_floor+1.72
        # Back boundary is buried in the parent slope; exact union clips the surplus.
        ridge=dormer_eave+width/2*min(1,m['pitch']+.08)
        back=main.y0+(ridge-main.eave)/main.pitch+.20
        blocks.append(CapeBlock(f'Dormer{j+1}',x-width/2,x+width/2,y0,back,main.height(x,y0)-.14,main.upper_floor,main.upper_floor+1.80,dormer_eave,'gable',min(1,m['pitch']+.08),'Y',.0762,1,0,main.upper_floor+1.8,.0508))
    if s['rear_shed']:
        # Added rear shed starts below the ridge; front edge tucks into parent roof.
        y1=main.y1-.48;ev=main.upper_floor+2.05;pitch=2/12
        # Parent rear plane z=-p*y+ridge; solve equality with shed plane.
        intersection=(main.eave+main.pitch*(main.cy+main.depth/2)-ev-pitch*y1)/(main.pitch-pitch)
        assert intersection>main.cy+.15,'Shed dormer reaches ridge; depth/pitch cannot fit attic headroom'
        blocks.append(CapeBlock('RearShed',main.x0+.52,main.x1-.52,intersection-.12,y1,0,main.upper_floor,ev-.12,ev,'shed',pitch,'X',.0762,1,0,ev-.12,.0508))
    door_x=main.cx+(-main.width*.15 if s['door_offset'] else 0)
    porch=None
    if s['hood']!='none':
        width=(6 if s['hood']=='portico' else 4.8)*FT;dep=(4 if s['hood']=='portico' else 2.2)*FT
        porch=CapeBlock('Porch',door_x-width/2,door_x+width/2,main.y0-dep,main.y0+.10,0,floor-.028,floor+2.20,floor+2.34,'gable',8/12,'Y',.0762,1,0,floor+2.2,.0508)
    # Origin uses permanent ground footprint: house/additions/garage and entry steps.
    count=math.ceil((floor-.028)/.19);front=main.y0-1.02-(count-1)*.28
    ground=[b for b in blocks if not b.name.startswith('Dormer') and b.name!='RearShed']
    cx=(min(b.x0 for b in ground)+max(b.x1 for b in ground))/2;cy=(min(front,min(b.y0 for b in ground))+max(b.y1 for b in ground))/2
    for b in blocks+([porch] if porch else []):b.x0-=cx;b.x1-=cx;b.y0-=cy;b.y1-=cy
    door_x-=cx
    s['cladding']={b.name:{f:'siding' for f in ('front','back','left','right')} for b in blocks}
    sockets=dict(FrontThreshold=(door_x,main.y0-.10,floor),Walk=(door_x,front-cy,0),Driveway=(main.x1+1.65 if g['side']=='right' else main.x0-1.65,main.y0,0))
    if g['kind']!='none':
        sockets['GarageApron']=(garage.cx,garage.y0-.13,garage.floor)
        sockets['Driveway']=(garage.cx,main.y0,0)
    return dict(seed=seed,spec=s,blocks=blocks,porch=porch,door_x=door_x,sockets=sockets,floor_levels={b.name:[b.floor] for b in blocks},dormer_centers=[x-cx for x in centers])


def openings(plan):
    s=plan['spec'];m=plan['blocks'][0];result=[]
    def add(b,f,u,z,w,h,kind='window',role='bedroom',shutters=False,**kw):
        result.append(dict(id=f'{b.name}_{f}_{len(result):02}',block=b.name,face=f,u=u,z=z,w=w,h=h,kind=kind,role=role,shutters=shutters,**kw))
    if s['door_offset']:
        add(m,'front',m.width*.73,m.floor+.72,2.05,1.25,role='updated living picture',style='picture')
        add(m,'front',m.width*.14,m.floor+.7366,.762,1.3716,shutters=False)
    else:
        fs=(.25,.75) if s['dormers']!=3 else (.11,.31,.69,.89)
        for f in fs:add(m,'front',m.width*f,m.floor+.7366,.762,1.3716,shutters=s['shutters'])
    add(m,'front',plan['door_x']-m.x0,m.floor,.9144,2.032,'door','entry')
    add(m,'back',m.width*.17,m.floor+1.02,1.2192,1.016,role='kitchen')
    add(m,'back',m.width*.47,m.floor,.8636,2.032,'service','rear entry')
    add(m,'back',m.width*.82,m.floor+.7366,.9144,1.3716,role='bedroom')
    for f in ('left','right'):
        attached=any(b.name in ('Wing','Breezeway') and abs((b.x1 if f=='left' else b.x0)-(m.x0 if f=='left' else m.x1))<.01 for b in plan['blocks'])
        if not attached:
            occupied={('left' if v.cx<m.cx else 'right') for v in plan['blocks'] if v.name in ('Wing','Breezeway')}
            chimney_end='right' if 'left' in occupied else 'left'
            for frac in ((.20,.49) if s['chimney']=='gable' and f==chimney_end else (.20,.80)):add(m,f,m.depth*frac,m.floor+.7366,.762,1.3716)
        add(m,f,m.depth*.5,m.upper_floor+.65,.762,1.016,role='attic bedroom')
    for b in plan['blocks'][1:]:
        if b.name.startswith('Dormer'):add(b,'front',b.width/2,m.upper_floor+.55,.7112,1.016,role='dormer bedroom')
        elif b.name=='RearShed':
            for u in (.20,.5,.8):add(b,'back',b.width*u,m.upper_floor+.65,.762,1.016,role='shed bedroom')
        elif b.name=='Garage':
            add(b,'front',b.width/2,b.floor,2.7432,2.1336,'garage','closed sectional')
            add(b,'back',b.width*.5,1.18,.762,.762,role='workshop')
        elif b.name=='Wing':
            for f in ('front','back'):add(b,f,b.width*.5,b.floor+.80,.9144,1.2192,role='sunroom' if s['wing']=='porch' else 'wing bedroom')
            outer='right' if b.cx>m.cx else 'left'
            for u in (.25,.75):add(b,outer,b.depth*u,b.floor+.80,.9144,1.2192,role='sunroom')
    return result


def serialize(plan):
    roof=roof_parts(plan)
    return {**plan,'blocks':[asdict(b) for b in plan['blocks']], 'porch':asdict(plan['porch']) if plan['porch'] else None,
        'openings':openings(plan),'roof_faces':roof_faces(roof),'roof_junctions':roof_junctions(roof)}
