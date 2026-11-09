"""Placement-owned maintenance history. Masks follow building construction."""
import math,random
import geometry as G


def color(point,role,col,props):
    x,y,z=point;name=props.get('name','');p=G.PLAN
    if not p:return col
    wear=p['wear'];w=p['width'];l=p['length'];floor=p['floor']
    if role=='brick':
        # Splash follows variable grade wetting and corners, never a level band.
        reach=.32+.24*(.5+.5*math.sin(x*1.7+y*.81))**2
        damp=max(0,1-max(0,z-floor*.35)/reach)
        salt=max(0,math.sin(x*3.4+y*2.8)+.5*math.sin(x*8.3-y*5.7)-.45)
        salt*=math.exp(-((z-.48-.15*math.sin(x*1.9+y))/.32)**2)*.22
        col=tuple(c*(1-wear*damp*.36)+salt*a for c,a in zip(col,(.20,.18,.13)))
        # Copper outlet/sill paths use world stations, not repeated bay marks.
        station=min(abs(y+l/2-.4),abs(y-l/2+.4))
        runoff=math.exp(-(station/.20)**2)*math.exp(-max(0,z-.25)/3.4)
        col=tuple(c*(1-runoff*.16)*a for c,a in zip(col,(1-runoff*.10,1,1-runoff*.04)))
    if role=='stone':
        under=.27 if props.get('normal_z',0)<-.4 else 0
        groove=(.5+.5*math.sin(x*6.3+y*4.8))**10
        dirt=(under+.21*groove)*wear
        col=tuple(c*(1-dirt) for c in col)
    if role=='timber' and ('Laminated bent' in name or 'rake edges' in name):
        # End grain and exposed front rake weather gray; sheltered spans stay warm.
        end=math.exp(-max(0,z-.45)/.78)
        exposed=math.exp(-((abs(y)-l/2-.55)/.45)**2)*.25
        amount=min(.72,(end*.65+exposed)*wear)
        gray=(.21,.205,.175)
        col=tuple(c*(1-amount)+g*amount for c,g in zip(col,gray))
    if role in ('slate','shingle'):
        # Site north is -X. Moss persists below overlapping north eave/slates.
        north=max(0,min(1,-x/(w/2)))
        tuft=max(0,math.sin(y*2.7+x*.6)+.46*math.sin(y*6.4-x*2.3)-.6)
        moss=north*tuft*.28*wear
        col=tuple(c*a for c,a in zip(col,(1+moss*.18,1+moss*.75,1-moss*.24)))
    return col


def repairs(parent,p):
    """Small irregular repairs share exactly the wall's existing brick charts.

    Stair-stepped maintenance boundaries are assembled in source-local meters;
    they do not repeat on instanced bays. Additional geometry is only the broad
    repair area, with the fine mortar/brick relief still in the native normal.
    """
    rng=random.Random(p['seed']+491)
    for ob in list(parent.children_recursive):
        if not (ob.name.startswith('Nave bay') or ob.name.startswith('Low brick sidewall')):continue
        if ob.name.startswith('Nave bay'):
            idx=int(ob.name.rsplit('_',1)[1].split('.')[0]);side=int(ob.name.split()[2].split('_')[0])
            if (idx+side)%3:continue
            rr=G.root('Localized masonry repair',parent=ob)
            m=G.Mesh('Repointed lower masonry',rr,repair=True,sheet=True)
            for row in range(5):
                left=-1.75+rng.choice((0,.23,.46));right=-.82+rng.choice((0,.23,.46))
                z=.24+row*.1524
                m.geom([(left,-p['wall']/2-.0015,z),(right,-p['wall']/2-.0015,z),(right,-p['wall']/2-.0015,z+.1524),(left,-p['wall']/2-.0015,z+.1524)],[(0,1,2,3)],'brick',color=(1.16,1.17,1.08))
            m.finish()
    # Green copper at the exposed roof/wall transitions, on existing metal.
    # Rust stains originate at actual railing feet and are short gravity tracks.
    from surfaces import paint_material
    paint_material();m=G.Mesh('Rail-foot rust and step moss',parent,sheet=True)
    if p['style']!='aframe':
        y=-p['length']/2
        for side in (-1,1):
            x=side*1.98
            for j in range(3):
                yy=y-2.34-j*.3302;z=p['floor']-j*.1524+.001
                m.geom([(x-.08,yy,z),(x+.07,yy,z),(x+.10,yy-.29,z),(x-.06,yy-.27,z)],[(0,1,2,3)],'paint',color=(.65,.32,.13),uv=[[(.755,.505),(.995,.505),(.995,.745),(.755,.745)]])
    if m.v:m.finish()
    if p['style']=='aframe':fascia(parent,p)


def fascia(parent,p):
    from mathutils import Vector
    rng=random.Random(p['seed']+908);m=G.Mesh('Surviving paint on exposed rake fascia',parent,sheet=True)
    for s in (-1,1):
        a=Vector((s*(p['width']/2+.61),-p['length']/2-.721,p['eave']-.61*math.tan(math.radians(p['pitch']))))
        b=Vector((0,a.y,p['ridge']));delta=b-a;u=Vector((delta.z,0,-delta.x)).normalized()
        for j in range(32):
            if rng.random()<(.70 if j<5 else .20):continue
            t0=(j+rng.uniform(.03,.22))/32;t1=(j+rng.uniform(.65,.98))/32
            left=rng.uniform(-.070,-.035);right=rng.uniform(.025,.070)
            poly=[a+delta*t0+u*left,a+delta*t1+u*(left+.015),a+delta*t1+u*right,a+delta*((t0+t1)/2)+u*(right-.012),a+delta*t0+u*right]
            m.geom(poly,[tuple(range(5))],'stone',color=(1.35,1.33,1.22))
    m.finish()
