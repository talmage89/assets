"""Seeded builder-colonial grammar and exact planar roof envelope, meters.

No Blender or reference-image dependency. Rectangular blocks overlap at a
framed connection. Roofs are lower envelopes of planes; their union retains
the higher roof in the overlap. This creates real intersections, not stacked
roof boxes. Unsupported plans fail rather than produce arbitrary architecture.
"""
from dataclasses import dataclass, asdict
import copy
import json
import math
import random

EPS = 1e-8
FT = .3048
PROOF_SEEDS=(27,2,3,6,8,14)


def clip(poly, a, b, c):
    """Convex polygon intersected with a*x+b*y+c >= 0."""
    out = []
    if not poly:
        return out
    for p, q in zip(poly, poly[1:] + poly[:1]):
        dp, dq = a*p[0]+b*p[1]+c, a*q[0]+b*q[1]+c
        if dp >= -EPS:
            out.append(p)
        if (dp > EPS and dq < -EPS) or (dp < -EPS and dq > EPS):
            t = dp/(dp-dq)
            out.append((p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])))
    clean = []
    for p in out:
        if not clean or math.dist(clean[-1], p) > EPS:
            clean.append(p)
    if len(clean)>1 and math.dist(clean[0], clean[-1])<EPS:
        clean.pop()
    return clean if len(clean)>=3 and abs(area(clean))>EPS else []


def area(poly):
    return .5*sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1]))


def subtract(poly, constraints):
    """Disjoint convex pieces outside a convex region; no raster sampling."""
    parts = []
    for a,b,c in constraints:
        outside = clip(poly,-a,-b,-c)
        if outside:
            parts.append(outside)
        poly = clip(poly,a,b,c)
        if not poly:
            break
    return parts


@dataclass
class Block:
    name: str
    x0: float
    x1: float
    y0: float
    y1: float
    base: float
    floor: float
    plate: float
    eave: float
    roof: str
    pitch: float
    ridge_axis: str
    overhang: float = .3048
    stories: int = 2
    upper_floor: float = 3.556
    first_plate: float = 3.2512

    @property
    def cx(self): return (self.x0+self.x1)/2
    @property
    def cy(self): return (self.y0+self.y1)/2
    @property
    def width(self): return self.x1-self.x0
    @property
    def depth(self): return self.y1-self.y0

    def contains(self,x,y,margin=0):
        return self.x0-margin<=x<=self.x1+margin and self.y0-margin<=y<=self.y1+margin

    def domain(self):
        o=self.overhang
        return [(self.x0-o,self.y0-o),(self.x1+o,self.y0-o),
                (self.x1+o,self.y1+o),(self.x0-o,self.y1+o)]

    def planes(self):
        p=self.pitch; ex=self.eave+p*self.width/2; ey=self.eave+p*self.depth/2
        if self.roof=='cricket':
            top=self.eave+.04*self.depth/2
            return [(a,b,top-a*self.cx-b*self.cy) for a in (-p,p) for b in (-.04,.04)]
        xp=[(p,0,ex-p*self.cx),(-p,0,ex+p*self.cx)]
        yp=[(0,p,ey-p*self.cy),(0,-p,ey+p*self.cy)]
        return xp+yp if self.roof=='hip' else (yp if self.ridge_axis=='X' else xp)

    def height(self,x,y):
        return min(a*x+b*y+c for a,b,c in self.planes())

    def faces(self):
        out=[]
        for i,p in enumerate(self.planes()):
            poly=self.domain()
            for q in self.planes():
                poly=clip(poly,q[0]-p[0],q[1]-p[1],q[2]-p[2])
            if poly:
                out.append((i,p,poly))
        return out


def roof_faces(blocks):
    """Visible roof top polygons with analytic clipping against every neighbor."""
    result=[]
    for block in blocks:
        for index,plane,poly in block.faces():
            parts=[poly]
            for other in blocks:
                if other is block: continue
                o=other.overhang
                cuts=[(1,0,-other.x0+o),(-1,0,other.x1+o),
                      (0,1,-other.y0+o),(0,-1,other.y1+o)]
                cuts += [(p[0]-plane[0],p[1]-plane[1],p[2]-plane[2]) for p in other.planes()]
                parts=[part for v in parts for part in subtract(v,cuts)]
            result += [dict(block=block.name,index=index,plane=plane,polygon=v) for v in parts]
    return result


def line_segment(p,q,constraints):
    """Intersect two z=ax+by+c planes, clipped by XY half spaces."""
    a,b,c=p[0]-q[0],p[1]-q[1],p[2]-q[2]
    length=math.hypot(a,b)
    if length<EPS: return None
    origin=(-a*c/(length*length),-b*c/(length*length))
    direction=(-b/length,a/length);lo,hi=-1000.,1000.
    for u,v,w in constraints:
        d=u*direction[0]+v*direction[1]; k=u*origin[0]+v*origin[1]+w
        if abs(d)<EPS:
            if k < -EPS:return None
        elif d>0:lo=max(lo,-k/d)
        else:hi=min(hi,-k/d)
    if hi-lo<.005:return None
    pts=[(origin[0]+t*direction[0],origin[1]+t*direction[1]) for t in (lo,hi)]
    return [(*v,p[0]*v[0]+p[1]*v[1]+p[2]) for v in pts]


def roof_junctions(blocks, visible=True):
    result=[]
    for bi,b in enumerate(blocks):
        for bj,c in enumerate(blocks[bi:],bi):
            for i,p in enumerate(b.planes()):
                for j,q in enumerate(c.planes()):
                    if bi==bj and j<=i:continue
                    constraints=[]
                    for block,plane in ((b,p),(c,q)):
                        o=block.overhang
                        constraints += [(1,0,-block.x0+o),(-1,0,block.x1+o),
                                        (0,1,-block.y0+o),(0,-1,block.y1+o)]
                        constraints += [(r[0]-plane[0],r[1]-plane[1],r[2]-plane[2]) for r in block.planes()]
                    segment=line_segment(p,q,constraints)
                    if segment:
                        parts=[segment]
                        if visible:
                            parts=visible_line(segment,blocks,[b,c])
                        for part in parts:
                            result.append(dict(kind='ridge' if bi==bj else 'valley',blocks=[b.name,c.name],points=part))
    return result


def visible_line(segment,blocks,owners):
    a,c=segment;t=[c[k]-a[k] for k in range(3)];cuts={0.,1.}
    for other in blocks:
        if other in owners:continue
        o=other.overhang
        for axis,lo,hi in ((0,other.x0-o,other.x1+o),(1,other.y0-o,other.y1+o)):
            if abs(t[axis])>EPS:cuts.update([(lo-a[axis])/t[axis],(hi-a[axis])/t[axis]])
        for p in other.planes():
            d=p[0]*t[0]+p[1]*t[1]-t[2]
            if abs(d)>EPS:cuts.add(-(p[0]*a[0]+p[1]*a[1]+p[2]-a[2])/d)
    cuts=sorted(k for k in cuts if 0<=k<=1);result=[]
    for lo,hi in zip(cuts,cuts[1:]):
        if hi-lo<EPS:continue
        mid=[a[k]+t[k]*(lo+hi)/2 for k in range(3)]
        hidden=any(other not in owners and other.contains(*mid[:2],other.overhang) and other.height(*mid[:2])>mid[2]+1e-6 for other in blocks)
        if not hidden:result.append([[a[k]+t[k]*v for k in range(3)] for v in (lo,hi)])
    return result


def roof_blocks(blocks):
    """Tapered saddles drain both ends of a hip/garage dead-valley condition.

    Two narrow cricket side valleys fall at 2%, rather than leaving a level
    concealed trough. Their 4% crown is real geometry, not a check exemption.
    """
    out=list(blocks)
    for row in roof_junctions(blocks):
        a,c=row['points']
        if row['kind']=='valley' and abs(a[2]-c[2])<1e-5 and math.dist(a,c)>.1:
            assert abs(a[0]-c[0])<1e-5, 'Unsupported flat valley direction'
            out.append(Block('Cricket',a[0]-.35,a[0]+.35,min(a[1],c[1]),max(a[1],c[1]),
                             0,0,0,a[2],'cricket',blocks[0].pitch,'Y',0,0))
    return out


PALETTES = [
    dict(name='sage / charcoal / oxblood',siding=(.35,.39,.31),trim=(.68,.66,.59),shutter=(.045,.061,.050),door=(.22,.036,.027)),
    dict(name='warm gray / navy',siding=(.36,.35,.32),trim=(.69,.68,.62),shutter=(.024,.045,.063),door=(.035,.065,.105)),
    dict(name='muted blue / ink',siding=(.24,.32,.36),trim=(.68,.68,.63),shutter=(.026,.034,.035),door=(.16,.048,.031)),
    dict(name='sand / forest',siding=(.46,.40,.30),trim=(.68,.65,.57),shutter=(.033,.072,.047),door=(.12,.031,.022)),
    dict(name='warm white / charcoal',siding=(.70,.69,.65),trim=(.70,.69,.65),shutter=(.030,.033,.031),door=(.20,.035,.022)),
    dict(name='clay / blue gray',siding=(.39,.32,.25),trim=(.68,.65,.58),shutter=(.055,.082,.094),door=(.038,.062,.071)),
]


def merge(base, override):
    for k,v in override.items():
        if isinstance(v,dict) and isinstance(base.get(k),dict):merge(base[k],v)
        else:base[k]=v
    return base


def generate(seed=27, overrides=None):
    r=random.Random(seed)
    spec=dict(type='builder_colonial',
        main=dict(width=r.choice([38,40,42])*FT,depth=r.choice([26,28,29])*FT,stories=2,
                  roof=r.choice(['gable','hip']),pitch=r.choice([6,7,8])/12),
        garage=dict(width=r.choice([22,23,24])*FT,depth=r.choice([22,23,24])*FT,
                    projection=r.choice([4,5,6])*FT,overlap=4*FT,
                    side=r.choice(['left','right']),stories=2,roof='gable'),
        bays=r.choice([4,5]),porch=r.choice(['gable','hip']),veneer=r.choice([True,True,False]),
        colors=copy.deepcopy(PALETTES[r.randrange(len(PALETTES))]))
    spec['cladding']={name:{face:('veneer' if face=='front' and spec['veneer'] and (name=='Main' or seed%4!=2) else 'siding')
                    for face in ('front','back','left','right')} for name in ('Main','Garage')}
    spec.update(rear_landing='patio' if seed%2 else 'deck',fireplace=(seed%3==0),
                shingle_color=('warm_charcoal','weathered_wood','dark_brown')[seed%3])
    if overrides:
        merge(spec,copy.deepcopy(overrides))
        if 'veneer' in overrides and 'cladding' not in overrides:
            for name in ('Main','Garage'):spec['cladding'][name]['front']='veneer' if spec['veneer'] else 'siding'
    m,g=spec['main'],spec['garage']
    assert spec['type']=='builder_colonial'
    assert m['stories']==g['stories']==2, 'This grammar implements a room-over-garage type'
    assert m['roof'] in ('gable','hip') and g['roof']=='gable'
    assert 11.58<=m['width']<=13.5 and 7.6<=m['depth']<=9.5
    assert 6.4<=g['width']<=7.5 and 6.4<=g['depth']<=7.5
    assert .9<=g['projection']<=1.9 and .9<=g['overlap']<=1.5
    assert .5<=m['pitch']<=2/3 and spec['bays'] in (4,5)
    assert g['side'] in ('left','right') and spec['porch'] in ('gable','hip')
    assert spec['rear_landing'] in ('patio','deck')
    assert spec['shingle_color'] in ('warm_charcoal','weathered_wood','dark_brown')
    assert all(value in ('siding','veneer') for faces in spec['cladding'].values() for value in faces.values())
    assert set(spec['cladding'])=={'Main','Garage'} and all(set(faces)=={'front','back','left','right'} for faces in spec['cladding'].values())
    assert all(len(spec['colors'][key])==3 and all(math.isfinite(v) and .0<=v<=.72 for v in spec['colors'][key]) for key in ('siding','trim','shutter','door'))
    main=Block('Main',-m['width']/2,m['width']/2,-m['depth']/2,m['depth']/2,
               .0,.508,5.9944,6.1468,m['roof'],m['pitch'],'X')
    x0=main.x1-g['overlap']; x1=x0+g['width']
    if g['side']=='left':x0,x1=-x1,-x0
    garage=Block('Garage',x0,x1,main.y0-g['projection'],main.y0-g['projection']+g['depth'],
                 0.,.1016,5.588,5.7404,'gable',m['pitch'],'Y')
    garage.upper_floor=3.15;garage.first_plate=2.8448
    cx=(min(main.x0,garage.x0)+max(main.x1,garage.x1))/2
    cy=(min(main.y0,garage.y0)+max(main.y1,garage.y1))/2
    for b in (main,garage):
        b.x0-=cx;b.x1-=cx;b.y0-=cy;b.y1-=cy
    blocks=[main,garage]
    # Entry is centered on the principal block; all bay positions are rhythmic.
    door_x=main.cx
    entry=Block('Porch',door_x-1.524,door_x+1.524,main.y0-1.6764,main.y0-.012,
                .0,.48,2.94,3.0924,spec['porch'],.5,'Y',.2032,1)
    # Center the permanent structural footprint, including the stoop/nosings.
    # Roof overhangs and movable splash blocks are outside that footprint.
    dy=(min(main.y0,garage.y0,entry.y0-.6257)+max(main.y1,garage.y1))/2
    for b in (main,garage,entry):b.y0-=dy;b.y1-=dy
    return dict(seed=seed,spec=spec,blocks=blocks,porch=entry,
                floor_levels=dict(Main=[main.floor,main.upper_floor],Garage=[garage.floor,garage.upper_floor]),door_x=door_x,
                sockets=dict(FrontThreshold=(door_x,main.y0-.10,.508),
                    Walk=(door_x,entry.y0-.6257,0),
                    GarageApron=(garage.cx,garage.y0-.13,.1016)))


def wall_frame(block,face):
    # local u runs right on front/back, toward back on left/right; v is outward.
    if face=='front':return (block.x0,block.y0),(1,0),(0,-1),block.width
    if face=='back':return (block.x0,block.y1),(1,0),(0,1),block.width
    if face=='left':return (block.x0,block.y0),(0,1),(-1,0),block.depth
    return (block.x1,block.y0),(0,1),(1,0),block.depth


def openings(plan):
    result=[];main,garage=plan['blocks'];n=plan['spec']['bays']
    def add(b,face,u,z,w,h,kind='window',role='bedroom',shutters=False):
        o,t,normal,length=wall_frame(b,face)
        # Keep casings + half-width shutters clear of real block intersections.
        for s in (-1,0,1):
            x=o[0]+t[0]*(u+s*w/2)+normal[0]*.01
            y=o[1]+t[1]*(u+s*w/2)+normal[1]*.01
            for other in plan['blocks']:
                if other is b:continue
                if other.contains(x,y) and other.height(x,y)>z-.06:
                    return
        result.append(dict(id=f'{b.name}_{face}_{len(result):02}',block=b.name,face=face,
            u=u,z=z,w=w,h=h,kind=kind,role=role,shutters=shutters))
    for b in plan['blocks']:
        if b is main:
            bay=[1.25+(b.width-2.5)*i/(n-1) for i in range(n)]
            # Four ground-floor bays leave the centered portico and columns clear.
            for f in (.10,.28,.72,.90):
                add(b,'front',b.width*f,1.27,.9144,1.524,shutters=True,role='living / dining')
            for u in bay:
                add(b,'front',u,4.2164,.9144,1.3716,shutters=True)
            add(b,'front',b.width/2,.508,.9144,2.032,'door','entry')
            # Kitchen and dining share a rear exit; upper room rhythm is quieter.
            for u,z,w,h,role in ((b.width*.20,1.70,1.524,1.016,'kitchen sink'),
                                    (b.width*.85,1.27,.9144,1.524,'family room')):
                add(b,'back',u,z,w,h,role=role)
            add(b,'back',b.width*.56,.508,1.8288,2.032,'patio','kitchen patio')
            for u in (b.width*.18,b.width*.48,b.width*.81):
                add(b,'back',u,4.2164,1.067,1.3716)
            for face in ('left','right'):
                outer=face==('left' if plan['spec']['garage']['side']=='right' else 'right')
                if outer:add(b,face,b.depth*.29,2.60,.686,1.4224,role='stairwell landing')
                for u in (b.depth*.64,b.depth*.85):
                    if not (outer and plan['spec']['fireplace'] and u<b.depth*.7):
                        add(b,face,u,1.27,.9144,1.524,role='living')
                    add(b,face,u,4.2164,.9144,1.3716)
        else:
            add(b,'front',b.width/2,.1016,4.8768,2.1336,'garage','closed sectional')
            for u in (b.width*.27,b.width*.73):
                add(b,'front',u,3.9624,.9144,1.2192,shutters=True,role='room over garage')
                add(b,'back',u,3.9624,.9144,1.2192,role='room over garage')
            face='right' if plan['spec']['garage']['side']=='right' else 'left'
            for u in (b.depth*.28,):
                add(b,face,u,1.25,.9144,1.067,role='garage')
            add(b,face,b.depth*.76,.1016,.8636,2.032,'service','garage service')
            for u in (b.depth*.25,b.depth*.69):add(b,face,u,3.9624,.9144,1.2192,role='room over garage')
    return result


def serialize(plan):
    return {**plan,'blocks':[asdict(b) for b in plan['blocks']],
            'porch':asdict(plan['porch']),'openings':openings(plan),
            'roof_faces':roof_faces(roof_blocks(plan['blocks'])),
            'roof_junctions':roof_junctions(roof_blocks(plan['blocks']))}


def load(seed,path=None):
    return generate(seed,json.loads(path.read_text()) if path else None)
