"""Placement-owned maintenance history. Masks follow building construction."""
import math,random
import geometry as G


def color(point,role,col,props):
    x,y,z=point;name=props.get('name','');p=G.PLAN
    if not p:return col
    wear=p['wear'];w=p['width'];l=p['length'];floor=p['floor']
    if role=='brick':
        # Splash follows variable grade wetting and corners, never a level band.
        reach=.65+.25*(.5+.5*math.sin(x*1.7+y*.81))**2
        damp=max(0,1-max(0,z-floor*.35)/reach)
        salt=max(0,math.sin(x*3.4+y*2.8)+.5*math.sin(x*8.3-y*5.7)-.45)
        salt*=math.exp(-((z-.48-.15*math.sin(x*1.9+y))/.32)**2)*.22
        nx,ny,_=props.get('normal_world',(0,-1,0))
        wall=.88+.055*nx-.035*ny+.045*math.sin(x*.24+y*.19+1)
        col=tuple(c*wall*(1-wear*damp*.62)+salt*a for c,a in zip(col,(.14,.12,.09)))
        # Copper outlet/sill paths use world stations, not repeated bay marks.
        station=min(abs(y+l/2-.4),abs(y-l/2+.4))
        runoff=math.exp(-(station/.20)**2)*math.exp(-max(0,z-.25)/3.4)
        col=tuple(c*(1-runoff*.16)*a for c,a in zip(col,(1-runoff*.10,1,1-runoff*.04)))
        if p['style']!='aframe':
            tx,ty=p['tower_xy'];wet=0
            if abs(y-(ty-2.285))<.49:
                for head,stations in ((4.87,(-1.42,.57,1.88)),(12.72,(-.73,.96)),(17.22,(-.15,1.63))):
                    drop=head-z
                    if 0<drop<2.1:
                        wet+=sum(math.exp(-((x-tx-s)/.27)**2) for s in stations)*(.42*(1-drop/2.1))
            if abs(y+l/2)<.48 and 5.8<z<7.2:
                wet+=sum(math.exp(-((x-s)/.22)**2) for s in (-.82,.63))*.26*(z-5.8)/1.4
            col=tuple(c*(1-wet) for c in col)
    if role=='stone':
        under=.42 if props.get('normal_z',0)<-.4 else 0
        joint=min(abs((x+.2)%1.22),abs((y+.17)%1.22))
        groove=math.exp(-(joint/.055)**2)
        dirt=(under+.34*groove+.08*(.5+.5*math.sin(x*.8+y*.6)))*wear
        col=tuple(c*(1-dirt) for c in col)
    if role=='timber' and ('Laminated bent' in name or 'rake edges' in name):
        # End grain and exposed front rake weather gray; sheltered spans stay warm.
        end=math.exp(-max(0,z-.45)/.78)
        exposed=math.exp(-((abs(y)-l/2-.55)/.45)**2)*.25
        amount=min(.94,(end*1.35+exposed)*wear)
        # Vertex tint counteracts the warm manufacture strip: these gains
        # produce neutral gray wood, rather than multiplying brown by gray.
        gray=(.35,.70,1.70)
        col=tuple(c*(1-amount)+g*amount for c,g in zip(col,gray))
    if role in ('slate','shingle'):
        # Site north is -X. Moss persists below overlapping north eave/slates.
        north=max(0,min(1,-x/(w/2)))
        tuft=max(0,math.sin(y*2.7+x*.6)+.46*math.sin(y*6.4-x*2.3)-.6)
        moss=north*tuft*.48*wear
        col=tuple(c*a for c,a in zip(col,(1-moss*.16,1+moss*1.5,1-moss*.45)))
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
    from surfaces import age_material
    age_material();m=G.Mesh('Rail-foot rust and step moss',parent,sheet=True)
    if p['style']!='aframe':
        y=-p['length']/2
        for side in (-1,1):
            x=side*1.98
            for j in (0,3):
                yy=y-2.34-j*.3302;z=p['floor']-j*.1524+.001
                m.geom([(x-.12,yy,z),(x+.11,yy,z),(x+.15,yy-.29,z),(x-.09,yy-.27,z)],[(0,1,2,3)],'age',color=(.83,.35,.13),uv=[[(.005,.755),(.495,.755),(.495,.995),(.005,.995)]])
        for j in (1,2,3):
            yy=y-2.34-j*.3302;z=p['floor']-j*.1524+.0013
            reach=(.57,.89,.68)[j-1]
            m.geom([(-2.13,yy,z),(-2.13+reach,yy,z),(-2.20+reach,yy-.26,z),(-2.13,yy-.28,z)],[(0,3,2,1)],'age',color=(.30,.78,.19),uv=[[(.005,.505),(.495,.505),(.495,.745),(.005,.745)]])
    if m.v:m.finish()
    roof_growth(parent,p)
    if p['style']=='aframe':fascia(parent,p)


def roof_growth(parent,p):
    """Interrupted moss below joints on the damp north pitch, not all roofs."""
    rng=random.Random(p['seed']+349);m=G.Mesh('North-pitch sheltered moss',parent,sheet=True)
    slope=math.tan(math.radians(p['pitch']));half=p['width']/2
    for j in range(8):
        # Colonies bridge damp courses at the eave and shaded tree stations.
        x=-half+rng.uniform(-.05,.40 if j<5 else half*.50)
        yy=-p['length']/2+j*p['length']/8+rng.uniform(-.5,.5)
        length=rng.uniform(.7,1.65);width=rng.uniform(2.8,5.3)
        width=min(width,p['length']/2-.2-yy)
        poly=[(x,yy),(x+length,yy+.035),(x+length*.86,yy+width),(x-.03,yy+width*.92)]
        points=[(xx,y,p['ridge']+xx*slope+.007) for xx,y in poly]
        m.geom(points,[(0,1,2,3)],'age',color=(.30,.78,.19),uv=[[(.005,.505),(.005,.745),(.495,.745),(.495,.505)]])
    m.finish()
    m=G.Mesh('Roof replacement packets and algae drainage',parent,sheet=True)
    for j in range(4):
        side=-1 if j<3 else 1;x=side*rng.uniform(half*.20,half*.78)
        yy=rng.uniform(-p['length']/2+1,p['length']/2-3)
        xa=x+side*rng.uniform(.6,1.2);yb=yy+rng.uniform(1.5,2.9)
        poly=[(xx,y,p['ridge']-abs(xx)*slope+.009) for xx,y in ((x,yy),(xa,yy),(xa,yb),(x,yb))]
        m.geom(poly,[(0,1,2,3)],'shingle' if p['style']=='aframe' else 'slate',color=(1.42,1.40,1.32))
    if p['style']=='aframe':
        for j in range(4):
            yy=rng.uniform(-p['length']/2+.5,p['length']/2-3);x=-.035;end=-half+.15
            width=rng.uniform(1.3,2.9)
            poly=[(xx,y,p['ridge']+xx*slope+.011) for xx,y in ((end,yy),(end,yy+width),(x,yy+width),(x,yy))]
            m.geom(poly,[(0,1,2,3)],'age',color=(.70,.73,.68),uv=[[(.005,.755),(.495,.755),(.495,.995),(.005,.995)]])
    if m.v:m.finish()


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
