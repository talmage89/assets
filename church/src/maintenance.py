"""Nonrepeating repaired masonry and gravity marks at real water traps."""
import math,random
import geometry as G


def add(parent,p):
    rng=random.Random(p['seed']+7109);modern=p['style']=='aframe';w=p['width'];l=p['length']
    m=G.Mesh('Frontage masonry maintenance',parent,sheet=True,repair=True)
    patches=[(-w*.34,-w*.255,.18,.70)] if modern else [(w*.29,w*.44,.34,2.1),(-w*.44,-w*.33,.42,1.55)]
    if not modern and p['tower']=='corner':patches.append((p['tower_xy'][0]-.8,p['tower_xy'][0]+1.7,.48,2.8))
    for i,(a,b,lo,hi) in enumerate(patches):
        yy=p['tower_xy'][1]-2.285-.0016 if not modern and i==2 else -l/2-.0016-(.02 if modern else 0)
        for j in range(math.ceil((hi-lo)/.1524)):
            z=lo+j*.1524;za=min(z+.1524,hi)
            aa=a+rng.choice((0,.23,.46));bb=b-rng.choice((0,.23))
            m.geom([(aa,yy,z),(bb,yy,z),(bb,yy,za),(aa,yy,za)],[(0,1,2,3)],'brick',color=(1.24,1.28,1.24))
    m.finish()
    from surfaces import age_material
    age_material();m=G.Mesh('Runoff below projecting courses and sills',parent,sheet=True)
    def track(x,y,head,length,width,color):
        poly=[(x-width*.28,y,head-length),(x+width*.35,y,head-length),(x+width*.55,y,head),(x-width*.55,y,head)]
        m.geom(poly,[(0,1,2,3)],'age',color=color,uv=[[(.005,.755),(.495,.755),(.495,.995),(.005,.995)]])
    if not modern:
        tx,ty=p['tower_xy']
        for j in range(13 if p['tower'] in ('corner','center') else 0):
            head=rng.choice((4.87,12.72,17.22));x=tx+rng.uniform(-2.15,2.15)
            track(x,ty-2.287,head,rng.uniform(.35,1.6),rng.uniform(.06,.24),(.70,.71,.60))
        for x in (-.82,.63):track(x,-l/2-.002,p['eave']-1.03,rng.uniform(.52,1.1),.13,(.62,.73,.57))
        # Downpipe outlets stain irregularly below the copper offset, on the
        # neighboring masonry rather than floating in the air.
        for side in (-1,1):
            for end in (-1,1):
                rr=G.root('Copper outlet runoff',(side*(w/2+.002),end*(l/2-.4),0),parent)
                rr.rotation_euler.z=side*math.pi/2
                mm=G.Mesh('Localized copper and splash stain',rr,sheet=True)
                mm.geom([(-.15,0,.15),(.18,0,.15),(.07,0,1.5),(-.08,0,1.35)],[(0,1,2,3)],'age',color=(.42,.75,.53),uv=[[(.005,.755),(.495,.755),(.495,.995),(.005,.995)]]);mm.finish()
    if m.v:m.finish()
    ledge_runoff(parent,p)


def ledge_runoff(parent,p):
    """Place broad washes below actual sill/course stations in local frames."""
    rng=random.Random(p['seed']+911)
    from surfaces import age_material
    age_material()
    for root in [parent,*list(parent.children_recursive)]:
        kind=root.get('module_kind');rows=[]
        if kind=='Tower' and p['tower']!='freestanding':
            for side in range(4):
                for z in (4.88,12.73,17.23):rows.append((side*math.pi/2,0,-2.286,z,4.4))
        elif kind in ('WallBay','ExitBay'):
            rows=[(0,0,-p['wall']/2-.002,2.20,1.7)]
        elif kind=='ClassroomBay':rows=[(0,0,-.154,1.05,2.6),(0,0,-.154,2.60,2.6)]
        elif kind=='Buttress':rows=[(0,0,-1.152,2.26,.60),(0,0,-.882,5.36,.60)]
        for yaw,x,y,z,width in rows:
            rr=G.root('Sheltered sill and course wash',parent=root);rr.rotation_euler.z=yaw
            wash=G.Mesh('Broad interrupted water wash',rr,sheet=True)
            length=rng.uniform(.48,1.15)
            wash.geom([(x-width/2,y,z-length),(x+width/2,y,z-length),
                       (x+width/2,y,z),(x-width/2,y,z)],[(0,1,2,3)],
                      'age',color=(.72,.75,.66),
                      uv=[[(.005,.755),(.495,.755),(.495,.995),(.005,.995)]])
            wash.finish()
