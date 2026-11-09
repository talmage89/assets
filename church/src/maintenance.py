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
